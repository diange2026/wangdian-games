"""
单位管理API
提供单位的CRUD操作和查询功能
"""
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from app import crud, schemas
from app.api import deps
from app.models.company import Company, CompanyCertificate
from app.schemas.company import (
    CompanyCreate, CompanyUpdate, CompanyResponse,
    CompanyQueryParams, CompanyStatsResponse
)

router = APIRouter()


@router.get("/", response_model=Dict[str, Any])
def get_companies(
    params: CompanyQueryParams = Depends(),
    db: Session = Depends(deps.get_db),
    current_user: Dict = Depends(deps.get_current_active_user)
) -> Any:
    """
    获取单位列表（带分页、排序和过滤）
    """
    # 构建查询条件
    query = db.query(Company)
    
    # 应用过滤条件
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
    
    # 获取总数
    total = query.count()
    
    # 应用排序
    sort_field = getattr(Company, params.sort_by, Company.created_at)
    if params.sort_order == "desc":
        query = query.order_by(sort_field.desc())
    else:
        query = query.order_by(sort_field.asc())
    
    # 应用分页
    offset = (params.page - 1) * params.page_size
    companies = query.offset(offset).limit(params.page_size).all()
    
    # 计算证照统计信息
    company_ids = [c.id for c in companies]
    certificate_stats = {}
    if company_ids:
        stats_query = db.query(
            CompanyCertificate.company_id,
            func.count(CompanyCertificate.id).label("total"),
            func.sum(func.case((CompanyCertificate.certificate_status == "valid", 1), else_=0)).label("valid"),
            func.sum(func.case((CompanyCertificate.certificate_status == "expiring_soon", 1), else_=0)).label("expiring_soon")
        ).filter(
            CompanyCertificate.company_id.in_(company_ids)
        ).group_by(
            CompanyCertificate.company_id
        ).all()
        
        for stat in stats_query:
            certificate_stats[stat.company_id] = {
                "total": stat.total or 0,
                "valid": stat.valid or 0,
                "expiring_soon": stat.expiring_soon or 0
            }
    
    # 构建响应数据
    company_responses = []
    for company in companies:
        stats = certificate_stats.get(company.id, {"total": 0, "valid": 0, "expiring_soon": 0})
        company_dict = {
            **company.__dict__,
            "certificate_count": stats["total"],
            "valid_certificate_count": stats["valid"],
            "expiring_certificate_count": stats["expiring_soon"]
        }
        company_responses.append(CompanyResponse(**company_dict))
    
    return {
        "total": total,
        "page": params.page,
        "page_size": params.page_size,
        "total_pages": (total + params.page_size - 1) // params.page_size,
        "data": company_responses
    }


@router.get("/stats", response_model=CompanyStatsResponse)
def get_company_stats(
    db: Session = Depends(deps.get_db),
    current_user: Dict = Depends(deps.get_current_active_user)
) -> Any:
    """
    获取单位统计信息
    """
    # 总数统计
    total_count = db.query(func.count(Company.id)).scalar() or 0
    
    # 状态统计
    active_count = db.query(func.count(Company.id)).filter(Company.status == "active").scalar() or 0
    suspended_count = db.query(func.count(Company.id)).filter(Company.status == "suspended").scalar() or 0
    blacklisted_count = db.query(func.count(Company.id)).filter(Company.status == "blacklisted").scalar() or 0
    
    # 风险等级统计
    low_risk_count = db.query(func.count(Company.id)).filter(Company.risk_level == "low").scalar() or 0
    medium_risk_count = db.query(func.count(Company.id)).filter(Company.risk_level == "medium").scalar() or 0
    high_risk_count = db.query(func.count(Company.id)).filter(Company.risk_level == "high").scalar() or 0
    
    # 按类型统计
    type_stats = {}
    for company_type in ["supplier", "contractor", "service_provider", "other"]:
        count = db.query(func.count(Company.id)).filter(Company.company_type == company_type).scalar() or 0
        type_stats[company_type] = count
    
    return CompanyStatsResponse(
        total_count=total_count,
        active_count=active_count,
        suspended_count=suspended_count,
        blacklisted_count=blacklisted_count,
        low_risk_count=low_risk_count,
        medium_risk_count=medium_risk_count,
        high_risk_count=high_risk_count,
        by_type=type_stats
    )


@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_company(
    company_in: CompanyCreate,
    db: Session = Depends(deps.get_db),
    current_user: Dict = Depends(deps.get_current_active_user)
) -> Any:
    """
    创建新单位
    """
    # 检查单位编码是否已存在
    existing_company = db.query(Company).filter(
        Company.company_code == company_in.company_code
    ).first()
    
    if existing_company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"单位编码 '{company_in.company_code}' 已存在"
        )
    
    # 创建单位
    company_data = company_in.model_dump()
    company_data["created_by"] = current_user["id"]
    company_data["updated_by"] = current_user["id"]
    
    company = Company(**company_data)
    db.add(company)
    db.commit()
    db.refresh(company)
    
    return CompanyResponse(
        **company.__dict__,
        certificate_count=0,
        valid_certificate_count=0,
        expiring_certificate_count=0
    )


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: int,
    db: Session = Depends(deps.get_db),
    current_user: Dict = Depends(deps.get_current_active_user)
) -> Any:
    """
    根据ID获取单位详情
    """
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="单位不存在"
        )
    
    # 计算证照统计
    certificate_count = db.query(func.count(CompanyCertificate.id)).filter(
        CompanyCertificate.company_id == company_id
    ).scalar() or 0
    
    valid_count = db.query(func.count(CompanyCertificate.id)).filter(
        CompanyCertificate.company_id == company_id,
        CompanyCertificate.certificate_status == "valid"
    ).scalar() or 0
    
    expiring_count = db.query(func.count(CompanyCertificate.id)).filter(
        CompanyCertificate.company_id == company_id,
        CompanyCertificate.certificate_status == "expiring_soon"
    ).scalar() or 0
    
    return CompanyResponse(
        **company.__dict__,
        certificate_count=certificate_count,
        valid_certificate_count=valid_count,
        expiring_certificate_count=expiring_count
    )


@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(
    company_id: int,
    company_in: CompanyUpdate,
    db: Session = Depends(deps.get_db),
    current_user: Dict = Depends(deps.get_current_active_user)
) -> Any:
    """
    更新单位信息
    """
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="单位不存在"
        )
    
    # 如果需要更新单位编码，检查是否冲突
    if company_in.company_code and company_in.company_code != company.company_code:
        existing = db.query(Company).filter(
            Company.company_code == company_in.company_code,
            Company.id != company_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"单位编码 '{company_in.company_code}' 已被其他单位使用"
            )
    
    # 更新字段
    update_data = company_in.model_dump(exclude_unset=True)
    update_data["updated_by"] = current_user["id"]
    
    for field, value in update_data.items():
        if value is not None:
            setattr(company, field, value)
    
    db.commit()
    db.refresh(company)
    
    # 重新计算统计信息
    certificate_count = db.query(func.count(CompanyCertificate.id)).filter(
        CompanyCertificate.company_id == company_id
    ).scalar() or 0
    
    valid_count = db.query(func.count(CompanyCertificate.id)).filter(
        CompanyCertificate.company_id == company_id,
        CompanyCertificate.certificate_status == "valid"
    ).scalar() or 0
    
    expiring_count = db.query(func.count(CompanyCertificate.id)).filter(
        CompanyCertificate.company_id == company_id,
        CompanyCertificate.certificate_status == "expiring_soon"
    ).scalar() or 0
    
    return CompanyResponse(
        **company.__dict__,
        certificate_count=certificate_count,
        valid_certificate_count=valid_count,
        expiring_certificate_count=expiring_count
    )


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(
    company_id: int,
    db: Session = Depends(deps.get_db),
    current_user: Dict = Depends(deps.get_current_active_user)
) -> None:
    """
    删除单位（软删除）
    """
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="单位不存在"
        )
    
    # 软删除：更新状态为已删除
    company.status = "suspended"
    company.updated_by = current_user["id"]
    db.commit()


@router.get("/{company_id}/certificates")
def get_company_certificates(
    company_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(deps.get_db),
    current_user: Dict = Depends(deps.get_current_active_user)
) -> Any:
    """
    获取单位的证照列表
    """
    # 检查单位是否存在
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="单位不存在"
        )
    
    # 获取证照列表
    query = db.query(CompanyCertificate).filter(
        CompanyCertificate.company_id == company_id
    )
    
    total = query.count()
    certificates = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": certificates
    }


@router.get("/search/by-name/{company_name}")
def search_companies_by_name(
    company_name: str,
    db: Session = Depends(deps.get_db),
    current_user: Dict = Depends(deps.get_current_active_user)
) -> Any:
    """
    根据名称搜索单位（模糊匹配）
    """
    companies = db.query(Company).filter(
        Company.company_name.ilike(f"%{company_name}%")
    ).limit(10).all()
    
    return {
        "count": len(companies),
        "data": companies
    }


@router.get("/search/by-code/{company_code}")
def search_companies_by_code(
    company_code: str,
    db: Session = Depends(deps.get_db),
    current_user: Dict = Depends(deps.get_current_active_user)
) -> Any:
    """
    根据编码搜索单位（精确匹配）
    """
    company = db.query(Company).filter(
        Company.company_code == company_code
    ).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="单位不存在"
        )
    
    return company