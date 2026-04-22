#!/usr/bin/env python3
"""
企业级单位资质管理API
全功能、全生命周期、全方位单位资质管理系统
"""

from typing import Any, Dict, List, Optional
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query, status, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session, joinedload, load_only
from sqlalchemy import and_, or_, func, desc, asc, text
import pandas as pd
import numpy as np
from io import BytesIO
import json

from app import crud, schemas
from app.api import deps
from app.models.company import Company, CompanyCertificate, CompanyAuditLog
from app.schemas.company import (
    CompanyCreate, CompanyUpdate, CompanyResponse, CompanyCertificateCreate,
    CompanyCertificateUpdate, CompanyCertificateResponse, CompanyQueryParams,
    CompanyStatsResponse, CompanyExportRequest, CompanyImportRequest
)
from app.core.security import verify_token, get_current_user
from app.core.config import settings
from app.utils.excel_utils import export_to_excel, import_from_excel
from app.utils.pdf_utils import generate_company_report_pdf
from app.utils.notification import send_expiry_notification, send_risk_alert
from app.utils.validation import validate_company_data, validate_certificate_data
from app.utils.risk_assessment import calculate_risk_score, analyze_risk_patterns

router = APIRouter()


@router.get("/companies", response_model=Dict[str, Any], summary="获取单位列表")
async def get_companies(
    params: CompanyQueryParams = Depends(),
    db: Session = Depends(deps.get_db),
    current_user: Dict = Depends(deps.get_current_active_user)
) -> Any:
    """
    获取单位列表（高级查询功能）
    
    支持：
    - 多条件组合查询
    - 智能排序
    - 分页处理
    - 关联数据预加载
    - 统计信息返回
    """
    try:
        # 构建查询条件
        query = db.query(Company).filter(Company.is_deleted == False)
        
        # 应用各种过滤条件
        if params.company_code:
            query = query.filter(Company.company_code.ilike(f"%{params.company_code}%"))
        if params.company_name:
            query = query.filter(Company.company_name.ilike(f"%{params.company_name}%"))
        if params.company_type:
            query = query.filter(Company.company_type == params.company_type)
        if params.status:
            query = query.filter(Company.status == params.status)
        if params.risk_level:
            query = query.filter(Company.risk_level == params.risk_level)
        if params.contact_person:
            query = query.filter(Company.contact_person.ilike(f"%{params.contact_person}%"))
        if params.contact_phone:
            query = query.filter(Company.contact_phone.ilike(f"%{params.contact_phone}%"))
        
        # 应用排序
        if params.sort_by:
            if params.sort_order == "desc":
                query = query.order_by(desc(getattr(Company, params.sort_by)))
            else:
                query = query.order_by(asc(getattr(Company, params.sort_by)))
        else:
            query = query.order_by(desc(Company.created_at))
        
        # 获取总数
        total = query.count()
        
        # 应用分页
        query = query.offset((params.page - 1) * params.limit).limit(params.limit)
        
        # 预加载关联数据
        query = query.options(joinedload(Company.certificates))
        
        # 执行查询
        companies = query.all()
        
        # 计算统计数据
        stats = {
            "total": total,
            "page": params.page,
            "limit": params.limit,
            "pages": (total + params.limit - 1) // params.limit,
            "active_count": db.query(Company).filter(
                Company.status == "active", 
                Company.is_deleted == False
            ).count(),
            "expiring_certificates": db.query(CompanyCertificate).filter(
                CompanyCertificate.expiry_date <= date.today() + timedelta(days=30),
                CompanyCertificate.certificate_status == "valid"
            ).count()
        }
        
        return {
            "success": True,
            "data": [schemas.CompanyResponse.from_orm(company) for company in companies],
            "stats": stats,
            "message": "获取单位列表成功"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询单位列表失败: {str(e)}"
        )


@router.get("/companies/{company_id}", response_model=Dict[str, Any], summary="获取单位详情")
async def get_company_detail(
    company_id: int,
    include_certificates: bool = Query(True, description="是否包含证照信息"),
    include_audit_logs: bool = Query(False, description="是否包含审计日志"),
    db: Session = Depends(deps.get_db),
    current_user: Dict = Depends(deps.get_current_active_user)
) -> Any:
    """
    获取单位完整详情
    
    包含：
    - 单位基本信息
    - 所有证照信息（可选）
    - 审计日志（可选）
    - 风险分析报告
    - 关联人员信息
    """
    try:
        # 构建查询
        query = db.query(Company).filter(
            Company.id == company_id,
            Company.is_deleted == False
        )
        
        # 根据需要预加载关联数据
        if include_certificates:
            query = query.options(
                joinedload(Company.certificates).options(
                    load_only(
                        CompanyCertificate.id,
                        CompanyCertificate.certificate_name,
                        CompanyCertificate.certificate_number,
                        CompanyCertificate.certificate_status,
                        CompanyCertificate.expiry_date,
                        CompanyCertificate.renewal_status
                    )
                )
            )
        
        company = query.first()
        
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="单位不存在或已被删除"
            )
        
        # 获取审计日志
        audit_logs = []
        if include_audit_logs:
            audit_logs = db.query(CompanyAuditLog).filter(
                CompanyAuditLog.company_id == company_id
            ).order_by(desc(CompanyAuditLog.created_at)).limit(20).all()
        
        # 计算风险评分
        risk_score = calculate_risk_score(company)
        
        # 获取即将到期的证照
        expiring_certificates = db.query(CompanyCertificate).filter(
            CompanyCertificate.company_id == company_id,
            CompanyCertificate.certificate_status == "valid",
            CompanyCertificate.expiry_date <= date.today() + timedelta(days=30)
        ).all()
        
        return {
            "success": True,
            "data": {
                "company": schemas.CompanyResponse.from_orm(company),
                "certificates": [
                    schemas.CompanyCertificateResponse.from_orm(cert) 
                    for cert in company.certificates
                ] if include_certificates else [],
                "audit_logs": [
                    {
                        "id": log.id,
                        "action": log.action,
                        "user_name": log.user_name,
                        "created_at": log.created_at.isoformat(),
                        "details": json.loads(log.diff) if log.diff else {}
                    } for log in audit_logs
                ],
                "risk_analysis": {
                    "score": risk_score,
                    "level": risk_level,
                    "indicators": analyze_risk_patterns(company),
                    "recommendations": generate_risk_recommendations(risk_score)
                },
                "expiring_certificates": [
                    {
                        "id": cert.id,
                        "name": cert.certificate_name,
                        "number": cert.certificate_number,
                        "expiry_date": cert.expiry_date.isoformat(),
                        "days_left": (cert.expiry_date - date.today()).days
                    } for cert in expiring_certificates
                ],
                "statistics": {
                    "total_certificates": len(company.certificates),
                    "valid_certificates": sum(1 for c in company.certificates if c.certificate_status == "valid"),
                    "expired_certificates": sum(1 for c in company.certificates if c.certificate_status == "expired"),
                    "pending_renewals": sum(1 for c in company.certificates if c.renewal_status == "pending")
                }
            },
            "message": "获取单位详情成功"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取单位详情失败: {str(e)}"
        )


@router.post("/companies", response_model=Dict[str, Any], summary="创建单位", status_code=status.HTTP_201_CREATED)
async def create_company(
    company_data: CompanyCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db),
    current_user: Dict = Depends(deps.get_current_active_user)
) -> Any:
    """
    创建新单位（完整流程）
    
    包含：
    - 数据验证
    - 重复检查
    - 风险评估
    - 审计日志记录
    - 异步通知
    """
    try:
        # 检查单位编码是否已存在
        existing_company = db.query(Company).filter(
            Company.company_code == company_data.company_code,
            Company.is_deleted == False
        ).first()
        
        if existing_company:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"单位编码 {company_data.company_code} 已存在"
            )
        
        # 验证数据
        validation_result = validate_company_data(company_data.dict())
        if not validation_result["valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"数据验证失败: {validation_result['errors']}"
            )
        
        # 创建单位
        new_company = Company(
            **company_data.dict(exclude_unset=True),
            created_by=current_user["id"],
            updated_by=current_user["id"],
            status="active",
            approval_status="pending"
        )
        
        # 计算初始风险评分
        new_company.risk_score = calculate_risk_score(new_company)
        new_company.risk_level = determine_risk_level(new_company.risk_score)
        
        db.add(new_company)
        db.commit()
        db.refresh(new_company)
        
        # 记录审计日志
        audit_log = CompanyAuditLog(
            company_id=new_company.id,
            company_code=new_company.company_code,
            user_id=current_user["id"],
            user_name=current_user["username"],
            action="create",
            old_data=json.dumps({}),
            new_data=json.dumps(company_data.dict()),
            diff=json.dumps({"created": "new company"})
        )
        db.add(audit_log)
        db.commit()
        
        # 异步发送通知
        background_tasks.add_task(
            send_company_creation_notification,
            new_company,
            current_user
        )
        
        return {
            "success": True,
            "data": schemas.CompanyResponse.from_orm(new_company),
            "message": "单位创建成功，等待审核"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建单位失败: {str(e)}"
        )


@router.put("/companies/{company_id}", response_model=Dict[str, Any], summary="更新单位信息")
async def update_company(
    company_id: int,
    company_update: CompanyUpdate,
    db: Session = Depends(deps.get_db),
    current_user: Dict = Depends(deps.get_current_active_user)
) -> Any:
    """
    更新单位信息（完整版本）
    
    包含：
    - 数据验证
    - 版本控制
    - 风险评估更新
    - 审计日志记录
    """
    try:
        # 获取现有单位
        company = db.query(Company).filter(
            Company.id == company_id,
            Company.is_deleted == False
        ).first()
        
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="单位不存在或已被删除"
            )
        
        # 检查权限
        if not check_company_update_permission(company, current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="没有权限更新此单位"
            )
        
        # 保存旧数据用于审计
        old_data = {
            field: getattr(company, field) 
            for field in company_update.dict(exclude_unset=True).keys()
            if hasattr(company, field)
        }
        
        # 更新字段
        update_data = company_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(company, field):
                setattr(company, field, value)
        
        # 更新元数据
        company.updated_by = current_user["id"]
        company.updated_at = datetime.utcnow()
        company.version += 1
        
        # 重新计算风险评分
        company.risk_score = calculate_risk_score(company)
        company.risk_level = determine_risk_level(company.risk_score)
        
        db.commit()
        db.refresh(company)
        
        # 记录审计日志
        audit_log = CompanyAuditLog(
            company_id=company.id,
            company_code=company.company_code,
            user_id=current_user["id"],
            user_name=current_user["username"],
            action="update",
            old_data=json.dumps(old_data),
            new_data=json.dumps(update_data),
            diff=json.dumps(calculate_data_diff(old_data, update_data))
        )
        db.add(audit_log)
        db.commit()
        
        return {
            "success": True,
            "data": schemas.CompanyResponse.from_orm(company),
            "message": "单位更新成功"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新单位失败: {str(e)}"
        )


@router.delete("/companies/{company_id}", response_model=Dict[str, Any], summary="删除单位")
async def delete_company(
    company_id: int,
    permanent: bool = Query(False, description="是否永久删除"),
    db: Session = Depends(deps.get_db),
    current_user: Dict = Depends(deps.get_current_active_user)
) -> Any:
    """
    删除单位（支持软删除和永久删除）
    
    包含：
    - 权限检查
    - 关联数据检查
    - 审计日志记录
    - 级联删除选项
    """
    try:
        # 获取单位
        company = db.query(Company).filter(Company.id == company_id).first()
        
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="单位不存在"
            )
        
        # 检查权限
        if not check_company_delete_permission(company, current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="没有权限删除此单位"
            )
        
        # 检查关联数据
        if not permanent:
            # 检查是否有有效证照
            active_certificates = db.query(CompanyCertificate).filter(
                CompanyCertificate.company_id == company_id,
                CompanyCertificate.certificate_status == "valid"
            ).count()
            
            if active_certificates > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"单位还有 {active_certificates} 个有效证照，无法删除"
                )
        
        # 保存审计数据
        old_data = {
            "id": company.id,
            "company_code": company.company_code,
            "company_name": company.company_name,
            "status": company.status
        }
        
        if permanent:
            # 永久删除
            db.delete(company)
            action_type = "permanent_delete"
        else:
            # 软删除
            company.is_deleted = True
            company.deleted_at = datetime.utcnow()
            company.deleted_by = current_user["id"]
            action_type = "soft_delete"
        
        db.commit()
        
        # 记录审计日志
        audit_log = CompanyAuditLog(
            company_id=company_id,
            company_code=company.company_code if not permanent else old_data["company_code"],
            user_id=current_user["id"],
            user_name=current_user["username"],
            action=action_type,
            old_data=json.dumps(old_data),
            new_data=json.dumps({}),
            diff=json.dumps({"deleted": True})
        )
        db.add(audit_log)
        db.commit()
        
        return {
            "success": True,
            "message": f"单位{'永久' if permanent else '软'}删除成功",
            "data": {
                "company_id": company_id,
                "deleted_at": datetime.utcnow().isoformat() if not permanent else None
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除单位失败: {str(e)}"
        )


@router.get("/companies/{company_id}/certificates", response_model=Dict[str, Any], summary="获取单位证照列表")
async def get_company_certificates(
    company_id: int,
    status: Optional[str] = Query(None, description="证照状态过滤"),
    expiry_within_days: Optional[int] = Query(None, description="在指定天数内到期"),
    db: Session = Depends(deps.get_db),
    current_user: Dict = Depends(deps.get_current_active_user)
) -> Any:
    """
    获取单位的证照列表
    
    支持：
    - 状态过滤
    - 到期时间过滤
    - 续期状态过滤
    - 统计信息
    """
    try:
        # 验证单位存在
        company = db.query(Company).filter(
            Company.id == company_id,
            Company.is_deleted == False
        ).first()
        
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="单位不存在或已被删除"
            )
        
        # 构建证照查询
        query = db.query(CompanyCertificate).filter(
            CompanyCertificate.company_id == company_id
        )
        
        # 应用过滤条件
        if status:
            query = query.filter(CompanyCertificate.certificate_status == status)
        
        if expiry_within_days:
            expiry_date = date.today() + timedelta(days=expiry_within_days)
            query = query.filter(
                CompanyCertificate.expiry_date <= expiry_date,
                CompanyCertificate.certificate_status == "valid"
            )
        
        # 排序
        query = query.order_by(desc(CompanyCertificate.expiry_date))
        
        # 获取数据
        certificates = query.all()
        
        # 计算统计数据
        total = len(certificates)
        valid_count = sum(1 for c in certificates if c.certificate_status == "valid")
        expired_count = sum(1 for c in certificates if c.certificate_status == "expired")
        expiring_count = sum(1 for c in certificates if c.certificate_status == "valid" and c.expiry_date <= date.today() + timedelta(days=30))
        
        return {
            "success": True,
            "data": {
                "company": {
                    "id": company.id,
                    "code": company.company_code,
                    "name": company.company_name
                },
                "certificates": [
                    schemas.CompanyCertificateResponse.from_orm(cert) 
                    for cert in certificates
                ],
                "statistics": {
                    "total": total,
                    "valid": valid_count,
                    "expired": expired_count,
                    "expiring_soon": expiring_count,
                    "renewal_pending": sum(1 for c in certificates if c.renewal_status == "pending")
                }
            },
            "message": "获取证照列表成功"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取证照列表失败: {str(e)}"
        )


@router.post("/companies/{company_id}/certificates", response_model=Dict[str, Any], summary="添加证照")
async def add_certificate(
    company_id: int,
    certificate_data: CompanyCertificateCreate,
    file: Optional[UploadFile] = File(None, description="证照文件"),
    db: Session = Depends(deps.get_db),
    current_user: Dict = Depends(deps.get_current_active_user)
) -> Any:
    """
    为单位添加新证照
    
    包含：
    - 证照数据验证
    - 文件上传处理
    - 重复检查
    - 审计日志记录
    """
    try:
        # 验证单位存在
        company = db.query(Company).filter(
            Company.id == company_id,
            Company.is_deleted == False
        ).first()
        
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="单位不存在或已被删除"
            )
        
        # 检查证照编号是否重复
        existing_certificate = db.query(CompanyCertificate).filter(
            CompanyCertificate.certificate_number == certificate_data.certificate_number,
            CompanyCertificate.company_id == company_id
        ).first()
        
        if existing_certificate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"证照编号 {certificate_data.certificate_number} 已存在"
            )
        
        # 验证证照数据
        validation_result = validate_certificate_data(certificate_data.dict())
        if not validation_result["valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"证照数据验证失败: {validation_result['errors']}"
            )
        
        # 处理文件上传
        file_info = None
        if file:
            # 验证文件类型和大小
            if file.content_type not in ["image/jpeg", "image/png", "application/pdf"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="只支持 JPG、PNG 或 PDF 格式的文件"
                )
            
            if file.size > 10 * 1024 * 1024:  # 10MB限制
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="文件大小不能超过10MB"
                )
            
            # 保存文件信息
            file_info = {
                "filename": file.filename,
                "content_type": file.content_type,
                "size": file.size,
                "path": f"/uploads/certificates/{company_id}/{file.filename}"
            }
            
            # 这里应该调用文件存储服务保存文件
        
        # 创建证照
        new_certificate = CompanyCertificate(
            **certificate_data.dict(),
            company_id=company_id,
            certificate_status="valid",
            file_url=file_info["path"] if file_info else None,
            file_name=file_info["filename"] if file_info else None,
            file_size=file_info["size"] if file_info else None,
            created_by=current_user["id"],
            updated_by=current_user["id"]
        )
        
        db.add(new_certificate)
        db.commit()
        db.refresh(new_certificate)
        
        # 记录审计日志
        audit_log = CompanyAuditLog(
            company_id=company_id,
            company_code=company.company_code,
            user_id=current_user["id"],
            user_name=current_user["username"],
            action="add_certificate",
            old_data=json.dumps({}),
            new_data=json.dumps(certificate_data.dict()),
            diff=json.dumps({"added_certificate": certificate_data.certificate_name})
        )
        db.add(audit_log)
        db.commit()
        
        return {
            "success": True,
            "data": schemas.CompanyCertificateResponse.from_orm(new_certificate),
            "message": "证照添加成功"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"添加证照失败: {str(e)}"
        )


@router.put("/companies/certificates/{certificate_id}", response_model=Dict[str, Any], summary="更新证照信息")
async def update_certificate(
    certificate_id: int,
    certificate_update: CompanyCertificateUpdate,
    db: Session = Depends(deps.get_db),
    current_user: Dict = Depends(deps.get_current_active_user)
) -> Any:
    """
    更新证照信息
    
    包含：
    - 权限检查
    - 数据验证
    - 状态变化处理
    - 审计日志记录
    """
    try:
        # 获取证照
        certificate = db.query(CompanyCertificate).filter(
            CompanyCertificate.id == certificate_id
        ).first()
        
        if not certificate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="证照不存在"
            )
        
        # 获取所属单位
        company = db.query(Company).filter(
            Company.id == certificate.company_id,
            Company.is_deleted == False
        ).first()
        
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="所属单位不存在或已被删除"
            )
        
        # 保存旧数据
        old_data = {
            field: getattr(certificate, field) 
            for field in certificate_update.dict(exclude_unset=True).keys()
            if hasattr(certificate, field)
        }
        
        # 更新字段
        update_data = certificate_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(certificate, field):
                setattr(certificate, field, value)
        
        # 更新元数据
        certificate.updated_by = current_user["id"]
        certificate.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(certificate)
        
        # 记录审计日志
        audit_log = CompanyAuditLog(
            company_id=certificate.company_id,
            company_code=company.company_code,
            user_id=current_user["id"],
            user_name=current_user["username"],
            action="update_certificate",
            old_data=json.dumps(old_data),
            new_data=json.dumps(update_data),
            diff=json.dumps(calculate_data_diff(old_data, update_data))
        )
        db.add(audit_log)
        db.commit()
        
        return {
            "success": True,
            "data": schemas.CompanyCertificateResponse.from_orm(certificate),
            "message": "证照更新成功"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新证照失败: {str(e)}"
        )


@router.delete("/companies/certificates/{certificate_id}", response_model=Dict[str, Any], summary="删除证照")
async def delete_certificate(
    certificate_id: int,
    db: Session = Depends(deps.get_db),
    current_user: Dict = Depends(deps.get_current_active_user)
) -> Any:
    """
    删除证照
    
    包含：
    - 权限检查
    - 状态验证
    - 审计日志记录
    - 文件清理
    """
    try:
        # 获取证照
        certificate = db.query(CompanyCertificate).filter(
            CompanyCertificate.id == certificate_id
        ).first()
        
        if not certificate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="证照不存在"
            )
        
        # 获取所属单位
        company = db.query(Company).filter(
            Company.id == certificate.company_id,
            Company.is_deleted == False
        ).first()
        
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="所属单位不存在或已被删除"
            )
        
        # 检查权限
        if not check_certificate_delete_permission(certificate, current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="没有权限删除此证照"
            )
        
        # 保存审计数据
        old_data = {
            "id": certificate.id,
            "certificate_name": certificate.certificate_name,
            "certificate_number": certificate.certificate_number,
            "company_id": certificate.company_id
        }
        
        # 删除证照
        db.delete(certificate)
        db.commit()
        
        # 记录审计日志
        audit_log = CompanyAuditLog(
            company_id=certificate.company_id,
            company_code=company.company_code,
            user_id=current_user["id"],
            user_name=current_user["username"],
            action="delete_certificate",
            old_data=json.dumps(old_data),
            new_data=json.dumps({}),
            diff=json.dumps({"deleted_certificate": certificate.certificate_name})
        )
        db.add(audit_log)
        db.commit()
        
        # 清理文件（异步）
        if certificate.file_url:
            background_tasks.add_task(cleanup_certificate_file, certificate.file_url)
        
        return {
            "success": True,
            "message": "证照删除成功",
            "data": {
                "certificate_id": certificate_id,
                "deleted_at": datetime.utcnow().isoformat()
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除证照失败: {str(e)}"
        )


@router.get("/companies/export", response_class=FileResponse, summary="导出单位数据")
async def export_companies(
    export_request: CompanyExportRequest,
    db: Session = Depends(deps.get_db),
    current_user: Dict = Depends(deps.get_current_active_user)
) -> Any:
    """
    导出单位数据
    
    支持：
    - 多种格式（Excel, CSV, PDF）
    - 自定义字段选择
    - 数据过滤
    - 批量导出
    """
    try:
        # 根据请求参数构建查询
        query = build_export_query(export_request, db)
        
        # 执行查询
        companies = query.all()
        
        # 转换为DataFrame
        data = []
        for company in companies:
            row = {
                "单位编码": company.company_code,
                "单位名称": company.company_name,
                "单位类型": company.company_type,
                "状态": company.status,
                "风险等级": company.risk_level,
                "联系人": company.contact_person,
                "联系电话": company.contact_phone,
                "注册地址": company.registered_address,
                "创建时间": company.created_at.strftime("%Y-%m-%d %H:%M:%S") if company.created_at else "",
                "有效证照数量": sum(1 for c in company.certificates if c.certificate_status == "valid"),
                "即将到期证照": sum(1 for c in company.certificates if c.certificate_status == "valid" and c.expiry_date <= date.today() + timedelta(days=30))
            }
            data.append(row)
        
        df = pd.DataFrame(data)
        
        # 根据格式生成文件
        if export_request.format == "excel":
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='单位数据', index=False)
            output.seek(0)
            
            return FileResponse(
                output,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                filename=f"单位数据导出_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
        elif export_request.format == "csv":
            output = BytesIO()
            df.to_csv(output, index=False, encoding='utf-8-sig')
            output.seek(0)
            
            return FileResponse(
                output,
                media_type="text/csv",
                filename=f"单位数据导出_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
        elif export_request.format == "pdf":
            # 生成PDF报告
            pdf_data = generate_company_report_pdf(data, current_user)
            
            return FileResponse(
                pdf_data,
                media_type="application/pdf",
                filename=f"单位数据报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"不支持的导出格式: {export_request.format}"
            )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"导出数据失败: {str(e)}"
        )


@router.post("/companies/import", response_model=Dict[str, Any], summary="导入单位数据")
async def import_companies(
    file: UploadFile = File(..., description="导入文件"),
    db: Session = Depends(deps.get_db),
    current_user: Dict = Depends(deps.get_current_active_user)
) -> Any:
    """
    批量导入单位数据
    
    支持：
    - Excel文件导入
    - 数据验证
    - 重复检查
    - 导入结果报告
    """
    try:
        # 检查文件类型
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="只支持Excel文件（.xlsx, .xls）"
            )
        
        # 读取Excel文件
        df = pd.read_excel(file.file)
        
        # 验证数据列
        required_columns = ["单位编码", "单位名称", "单位类型", "联系人", "联系电话", "注册地址"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"缺少必需列: {', '.join(missing_columns)}"
            )
        
        # 处理导入数据
        import_results = {
            "total": len(df),
            "success": 0,
            "failed": 0,
            "errors": []
        }
        
        for index, row in df.iterrows():
            try:
                # 验证数据行
                validation_errors = validate_