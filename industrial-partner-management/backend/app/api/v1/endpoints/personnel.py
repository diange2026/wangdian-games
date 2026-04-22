from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_

from app.api.deps import get_db
from app.models.personnel import (
    Personnel, PersonnelCertificate, PersonnelTrainingRecord,
    PersonnelCertificateAlert, PersonnelCertificateAlertLog,
    GenderEnum, EmploymentStatusEnum, PersonnelStatusEnum,
    CertificateStatusEnum, ApprovalStatusEnum
)
from app.schemas.personnel import (
    PersonnelCreate, PersonnelUpdate, PersonnelInDB, PersonnelSimple,
    PersonnelCertificateCreate, PersonnelCertificateUpdate, PersonnelCertificateInDB,
    PersonnelTrainingRecordCreate, PersonnelTrainingRecordUpdate, PersonnelTrainingRecordInDB,
    PersonnelCertificateAlertCreate, PersonnelCertificateAlertUpdate, PersonnelCertificateAlertInDB,
    PersonnelCertificateAlertLogCreate, PersonnelCertificateAlertLogInDB,
    PersonnelQueryParams, PersonnelCertificateQueryParams, PersonnelTrainingRecordQueryParams,
    PersonnelPaginatedResponse, PersonnelCertificatePaginatedResponse, PersonnelTrainingRecordPaginatedResponse,
    PersonnelStats, CertificateStats, TrainingStats, AlertStats,
    BulkPersonnelCreate, BulkPersonnelCertificateCreate, BulkPersonnelTrainingRecordCreate,
    BulkUpdateStatus, BulkUpdateCertificateStatus
)

router = APIRouter()


# ============================================
# 人员管理端点
# ============================================

@router.get("/", response_model=PersonnelPaginatedResponse)
def get_personnel_list(
    db: Session = Depends(get_db),
    company_id: Optional[int] = Query(None, description="单位ID"),
    name: Optional[str] = Query(None, description="姓名"),
    personnel_code: Optional[str] = Query(None, description="人员编号"),
    id_card: Optional[str] = Query(None, description="身份证号"),
    employment_status: Optional[EmploymentStatusEnum] = Query(None, description="在职状态"),
    status: Optional[PersonnelStatusEnum] = Query(None, description="审核状态"),
    work_type: Optional[str] = Query(None, description="工种"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页大小")
):
    """获取人员列表（分页）"""
    # 构建查询条件
    filters = [Personnel.deleted_at.is_(None)]
    
    if company_id:
        filters.append(Personnel.company_id == company_id)
    if name:
        filters.append(Personnel.name.ilike(f"%{name}%"))
    if personnel_code:
        filters.append(Personnel.personnel_code.ilike(f"%{personnel_code}%"))
    if id_card:
        filters.append(Personnel.id_card == id_card)
    if employment_status:
        filters.append(Personnel.employment_status == employment_status)
    if status:
        filters.append(Personnel.status == status)
    if work_type:
        filters.append(Personnel.work_type == work_type)
    
    # 计算总数
    total = db.query(func.count(Personnel.id)).filter(*filters).scalar()
    
    # 分页查询
    offset = (page - 1) * page_size
    personnel_list = (
        db.query(Personnel)
        .filter(*filters)
        .order_by(Personnel.created_at.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )
    
    # 转换为简单模型（包含单位名称）
    items = []
    for person in personnel_list:
        person_dict = PersonnelSimple.from_orm(person)
        if person.company:
            person_dict.company_name = person.company.name
        items.append(person_dict)
    
    total_pages = (total + page_size - 1) // page_size
    
    return PersonnelPaginatedResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        items=items
    )


@router.post("/", response_model=PersonnelInDB, status_code=status.HTTP_201_CREATED)
def create_personnel(
    personnel_data: PersonnelCreate,
    db: Session = Depends(get_db)
):
    """创建新人员"""
    # 检查人员编号是否已存在
    existing_personnel = db.query(Personnel).filter(
        Personnel.personnel_code == personnel_data.personnel_code,
        Personnel.deleted_at.is_(None)
    ).first()
    if existing_personnel:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"人员编号 {personnel_data.personnel_code} 已存在"
        )
    
    # 检查身份证号是否已存在
    existing_id_card = db.query(Personnel).filter(
        Personnel.id_card == personnel_data.id_card,
        Personnel.deleted_at.is_(None)
    ).first()
    if existing_id_card:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"身份证号 {personnel_data.id_card} 已存在"
        )
    
    # 检查单位是否存在
    from app.models.company import Company
    company = db.query(Company).filter(
        Company.id == personnel_data.company_id,
        Company.deleted_at.is_(None)
    ).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"单位 ID {personnel_data.company_id} 不存在"
        )
    
    # 创建人员
    personnel_dict = personnel_data.dict(exclude_unset=True)
    personnel = Personnel(**personnel_dict)
    db.add(personnel)
    db.commit()
    db.refresh(personnel)
    
    return personnel


@router.get("/{personnel_id}", response_model=PersonnelInDB)
def get_personnel(
    personnel_id: int,
    db: Session = Depends(get_db)
):
    """获取人员详情"""
    personnel = db.query(Personnel).filter(
        Personnel.id == personnel_id,
        Personnel.deleted_at.is_(None)
    ).first()
    
    if not personnel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"人员 ID {personnel_id} 不存在"
        )
    
    return personnel


@router.put("/{personnel_id}", response_model=PersonnelInDB)
def update_personnel(
    personnel_id: int,
    personnel_data: PersonnelUpdate,
    db: Session = Depends(get_db)
):
    """更新人员信息"""
    personnel = db.query(Personnel).filter(
        Personnel.id == personnel_id,
        Personnel.deleted_at.is_(None)
    ).first()
    
    if not personnel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"人员 ID {personnel_id} 不存在"
        )
    
    # 更新字段
    update_data = personnel_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(personnel, field, value)
    
    db.commit()
    db.refresh(personnel)
    
    return personnel


@router.delete("/{personnel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_personnel(
    personnel_id: int,
    db: Session = Depends(get_db)
):
    """软删除人员"""
    personnel = db.query(Personnel).filter(
        Personnel.id == personnel_id,
        Personnel.deleted_at.is_(None)
    ).first()
    
    if not personnel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"人员 ID {personnel_id} 不存在"
        )
    
    # 软删除
    from datetime import datetime
    personnel.deleted_at = datetime.now()
    db.commit()


@router.post("/bulk", response_model=List[PersonnelInDB], status_code=status.HTTP_201_CREATED)
def bulk_create_personnel(
    bulk_data: BulkPersonnelCreate,
    db: Session = Depends(get_db)
):
    """批量创建人员"""
    results = []
    errors = []
    
    for item in bulk_data.items:
        try:
            # 检查人员编号是否已存在
            existing_personnel = db.query(Personnel).filter(
                Personnel.personnel_code == item.personnel_code,
                Personnel.deleted_at.is_(None)
            ).first()
            if existing_personnel:
                errors.append(f"人员编号 {item.personnel_code} 已存在")
                continue
            
            # 检查身份证号是否已存在
            existing_id_card = db.query(Personnel).filter(
                Personnel.id_card == item.id_card,
                Personnel.deleted_at.is_(None)
            ).first()
            if existing_id_card:
                errors.append(f"身份证号 {item.id_card} 已存在")
                continue
            
            # 创建人员
            personnel_dict = item.dict(exclude_unset=True)
            personnel = Personnel(**personnel_dict)
            db.add(personnel)
            results.append(personnel)
        
        except Exception as e:
            errors.append(f"创建人员 {item.personnel_code} 失败: {str(e)}")
    
    if errors:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors": errors, "success_count": len(results)}
        )
    
    db.commit()
    for personnel in results:
        db.refresh(personnel)
    
    return results


@router.put("/bulk/status", status_code=status.HTTP_200_OK)
def bulk_update_personnel_status(
    bulk_data: BulkUpdateStatus,
    db: Session = Depends(get_db)
):
    """批量更新人员状态"""
    updated_count = 0
    
    for personnel_id in bulk_data.ids:
        personnel = db.query(Personnel).filter(
            Personnel.id == personnel_id,
            Personnel.deleted_at.is_(None)
        ).first()
        
        if personnel:
            personnel.status = bulk_data.status
            if bulk_data.updated_by:
                personnel.updated_by = bulk_data.updated_by
            updated_count += 1
    
    db.commit()
    
    return {
        "message": f"成功更新 {updated_count} 个人员状态",
        "updated_count": updated_count,
        "total_count": len(bulk_data.ids)
    }


# ============================================
# 人员证书管理端点
# ============================================

@router.get("/{personnel_id}/certificates", response_model=PersonnelCertificatePaginatedResponse)
def get_personnel_certificates(
    personnel_id: int,
    db: Session = Depends(get_db),
    certificate_type: Optional[str] = Query(None, description="证书类型"),
    certificate_status: Optional[CertificateStatusEnum] = Query(None, description="证书状态"),
    approval_status: Optional[ApprovalStatusEnum] = Query(None, description="审核状态"),
    expiry_start_date: Optional[str] = Query(None, description="到期开始日期"),
    expiry_end_date: Optional[str] = Query(None, description="到期结束日期"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页大小")
):
    """获取人员证书列表"""
    # 验证人员是否存在
    personnel = db.query(Personnel).filter(
        Personnel.id == personnel_id,
        Personnel.deleted_at.is_(None)
    ).first()
    
    if not personnel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"人员 ID {personnel_id} 不存在"
        )
    
    # 构建查询条件
    filters = [
        PersonnelCertificate.personnel_id == personnel_id,
        PersonnelCertificate.deleted_at.is_(None)
    ]
    
    if certificate_type:
        filters.append(PersonnelCertificate.certificate_type == certificate_type)
    if certificate_status:
        filters.append(PersonnelCertificate.certificate_status == certificate_status)
    if approval_status:
        filters.append(PersonnelCertificate.approval_status == approval_status)
    if expiry_start_date:
        filters.append(PersonnelCertificate.expiry_date >= expiry_start_date)
    if expiry_end_date:
        filters.append(PersonnelCertificate.expiry_date <= expiry_end_date)
    
    # 计算总数
    total = db.query(func.count(PersonnelCertificate.id)).filter(*filters).scalar()
    
    # 分页查询
    offset = (page - 1) * page_size
    certificates = (
        db.query(PersonnelCertificate)
        .filter(*filters)
        .order_by(PersonnelCertificate.expiry_date.asc())
        .offset(offset)
        .limit(page_size)
        .all()
    )
    
    # 转换为响应模型
    items = []
    for cert in certificates:
        cert_dict = PersonnelCertificateInDB.from_orm(cert)
        cert_dict.personnel_name = personnel.name
        cert_dict.personnel_code = personnel.personnel_code
        items.append(cert_dict)
    
    total_pages = (total + page_size - 1) // page_size
    
    return PersonnelCertificatePaginatedResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        items=items
    )


@router.post("/{personnel_id}/certificates", response_model=PersonnelCertificateInDB, status_code=status.HTTP_201_CREATED)
def create_personnel_certificate(
    personnel_id: int,
    certificate_data: PersonnelCertificateCreate,
    db: Session = Depends(get_db)
):
    """为人员创建证书"""
    # 验证人员是否存在
    personnel = db.query(Personnel).filter(
        Personnel.id == personnel_id,
        Personnel.deleted_at.is_(None)
    ).first()
    
    if not personnel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"人员 ID {personnel_id} 不存在"
        )
    
    # 检查证书编号是否已存在
    existing_certificate = db.query(PersonnelCertificate).filter(
        PersonnelCertificate.certificate_number == certificate_data.certificate_number,
        PersonnelCertificate.deleted_at.is_(None)
    ).first()
    if existing_certificate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"证书编号 {certificate_data.certificate_number} 已存在"
        )
    
    # 创建证书
    certificate_dict = certificate_data.dict(exclude_unset=True)
    certificate_dict["personnel_id"] = personnel_id
    certificate = PersonnelCertificate(**certificate_dict)
    db.add(certificate)
    db.commit()
    db.refresh(certificate)
    
    return certificate


@router.get("/certificates/{certificate_id}", response_model=PersonnelCertificateInDB)
def get_personnel_certificate(
    certificate_id: int,
    db: Session = Depends(get_db)
):
    """获取证书详情"""
    certificate = db.query(PersonnelCertificate).filter(
        PersonnelCertificate.id == certificate_id,
        PersonnelCertificate.deleted_at.is_(None)
    ).first()
    
    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"证书 ID {certificate_id} 不存在"
        )
    
    return certificate


@router.put("/certificates/{certificate_id}", response_model=PersonnelCertificateInDB)
def update_personnel_certificate(
    certificate_id: int,
    certificate_data: PersonnelCertificateUpdate,
    db: Session = Depends(get_db)
):
    """更新证书信息"""
    certificate = db.query(PersonnelCertificate).filter(
        PersonnelCertificate.id == certificate_id,
        PersonnelCertificate.deleted_at.is_(None)
    ).first()
    
    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"证书 ID {certificate_id} 不存在"
        )
    
    # 更新字段
    update_data = certificate_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(certificate, field, value)
    
    db.commit()
    db.refresh(certificate)
    
    return certificate


@router.delete("/certificates/{certificate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_personnel_certificate(
    certificate_id: int,
    db: Session = Depends(get_db)
):
    """软删除证书"""
    certificate = db.query(PersonnelCertificate).filter(
        PersonnelCertificate.id == certificate_id,
        PersonnelCertificate.deleted_at.is_(None)
    ).first()
    
    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"证书 ID {certificate_id} 不存在"
        )
    
    # 软删除
    from datetime import datetime
    certificate.deleted_at = datetime.now()
    db.commit()


@router.post("/certificates/bulk", response_model=List[PersonnelCertificateInDB], status_code=status.HTTP_201_CREATED)
def bulk_create_personnel_certificates(
    bulk_data: BulkPersonnelCertificateCreate,
    db: Session = Depends(get_db)
):
    """批量创建人员证书"""
    results = []
    errors = []
    
    for item in bulk_data.items:
        try:
            # 检查人员是否存在
            personnel = db.query(Personnel).filter(
                Personnel.id == item.personnel_id,
                Personnel.deleted_at.is_(None)
            ).first()
            if not personnel:
                errors.append(f"人员 ID {item.personnel_id} 不存在")
                continue
            
            # 检查证书编号是否已存在
            existing_certificate = db.query(PersonnelCertificate).filter(
                PersonnelCertificate.certificate_number == item.certificate_number,
                PersonnelCertificate.deleted_at.is_(None)
            ).first()
            if existing_certificate:
                errors.append(f"证书编号 {item.certificate_number} 已存在")
                continue
            
            # 创建证书
            certificate_dict = item.dict(exclude_unset=True)
            certificate = PersonnelCertificate(**certificate_dict)
            db.add(certificate)
            results.append(certificate)
        
        except Exception as e:
            errors.append(f"创建证书 {item.certificate_number} 失败: {str(e)}")
    
    if errors:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors": errors, "success_count": len(results)}
        )
    
    db.commit()
    for certificate in results:
        db.refresh(certificate)
    
    return results


@router.put("/certificates/bulk/status", status_code=status.HTTP_200_OK)
def bulk_update_certificate_status(
    bulk_data: BulkUpdateCertificateStatus,
    db: Session = Depends(get_db)
):
    """批量更新证书状态"""
    updated_count = 0
    
    for certificate_id in bulk_data.ids:
        certificate = db.query(PersonnelCertificate).filter(
            PersonnelCertificate.id == certificate_id,
            PersonnelCertificate.deleted_at.is_(None)
        ).first()
        
        if certificate:
            if bulk_data.certificate_status:
                certificate.certificate_status = bulk_data.certificate_status
            if bulk_data.approval_status:
                certificate.approval_status = bulk_data.approval_status
            if bulk_data.review_notes:
                certificate.review_notes = bulk_data.review_notes
            if bulk_data.reviewed_by:
                certificate.reviewed_by = bulk_data.reviewed_by
                certificate.reviewed_at = func.now()
            updated_count += 1
    
    db.commit()
    
    return {
        "message": f"成功更新 {updated_count} 个证书状态",
        "updated_count": updated_count,
        "total_count": len(bulk_data.ids)
    }


# ============================================
# 人员培训记录端点
# ============================================

@router.get("/{personnel_id}/trainings", response_model=PersonnelTrainingRecordPaginatedResponse)
def get_personnel_trainings(
    personnel_id: int,
    db: Session = Depends(get_db),
    training_type: Optional[str] = Query(None, description="培训类型"),
    training_start_date: Optional[str] = Query(None, description="培训开始日期"),
    training_end_date: Optional[str] = Query(None, description="培训结束日期"),
    is_passed: Optional[bool] = Query(None, description="是否通过"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页大小")
):
    """获取人员培训记录"""
    # 验证人员是否存在
    personnel = db.query(Personnel).filter(
        Personnel.id == personnel_id,
        Personnel.deleted_at.is_(None)
    ).first()
    
    if not personnel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"人员 ID {personnel_id} 不存在"
        )
    
    # 构建查询条件
    filters = [
        PersonnelTrainingRecord.personnel_id == personnel_id,
        PersonnelTrainingRecord.deleted_at.is_(None)
    ]
    
    if training_type:
        filters.append(PersonnelTrainingRecord.training_type == training_type)
    if training_start_date:
        filters.append(PersonnelTrainingRecord.training_date >= training_start_date)
    if training_end_date:
        filters.append(PersonnelTrainingRecord.training_date <= training_end_date)
    if is_passed is not None:
        filters.append(PersonnelTrainingRecord.is_passed == is_passed)
    
    # 计算总数
    total = db.query(func.count(PersonnelTrainingRecord.id)).filter(*filters).scalar()
    
    # 分页查询
    offset = (page - 1) * page_size
    trainings = (
        db.query(PersonnelTrainingRecord)
        .filter(*filters)
        .order_by(PersonnelTrainingRecord.training_date.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )
    
    total_pages = (total + page_size - 1) // page_size
    
    return PersonnelTrainingRecordPaginatedResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        items=trainings
    )


@router.post("/{personnel_id}/trainings", response_model=PersonnelTrainingRecordInDB, status_code=status.HTTP_201_CREATED)
def create_personnel_training(
    personnel_id: int,
    training_data: PersonnelTrainingRecordCreate,
    db: Session = Depends(get_db)
):
    """为人员创建培训记录"""
    # 验证人员是否存在
    personnel = db.query(Personnel).filter(
        Personnel.id == personnel_id,
        Personnel.deleted_at.is_(None)
    ).first()
    
    if not personnel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"人员 ID {personnel_id} 不存在"
        )
    
    # 创建培训记录
    training_dict = training_data.dict(exclude_unset=True)
    training_dict["personnel_id"] = personnel_id
    training = PersonnelTrainingRecord(**training_dict)
    db.add(training)
    db.commit()
    db.refresh(training)
    
    return training


# ============================================
# 统计分析端点
# ============================================

@router.get("/stats/personnel", response_model=PersonnelStats)
def get_personnel_stats(
    company_id: Optional[int] = Query(None, description="单位ID"),
    db: Session = Depends(get_db)
):
    """获取人员统计信息"""
    # 构建基础查询条件
    base_filters = [Personnel.deleted_at.is_(None)]
    if company_id:
        base_filters.append(Personnel.company_id == company_id)
    
    # 总人员数
    total_personnel = db.query(func.count(Personnel.id)).filter(*base_filters).scalar()
    
    # 在职人员数
    active_filters = base_filters + [Personnel.employment_status == EmploymentStatusEnum.ACTIVE]
    active_personnel = db.query(func.count(Personnel.id)).filter(*active_filters).scalar()
    
    # 待审核人员数
    pending_filters = base_filters + [Personnel.status == PersonnelStatusEnum.PENDING_REVIEW]
    pending_review_personnel = db.query(func.count(Personnel.id)).filter(*pending_filters).scalar()
    
    # 过期证书数
    from datetime import date
    expired_cert_filters = [
        PersonnelCertificate.certificate_status == CertificateStatusEnum.EXPIRED,
        PersonnelCertificate.deleted_at.is_(None)
    ]
    if company_id:
        expired_cert_filters.append(Personnel.company_id == company_id)
    
    expired_certificates = (
        db.query(func.count(PersonnelCertificate.id))
        .join(Personnel)
        .filter(*expired_cert_filters)
        .scalar()
    )
    
    # 即将过期证书数（30天内）
    today = date.today()
    soon_expiry_filters = [
        PersonnelCertificate.certificate_status == CertificateStatusEnum.VALID,
        PersonnelCertificate.approval_status == ApprovalStatusEnum.APPROVED,
        PersonnelCertificate.expiry_date.between(today, today.replace(day=today.day + 30)),
        PersonnelCertificate.deleted_at.is_(None)
    ]
    if company_id:
        soon_expiry_filters.append(Personnel.company_id == company_id)
    
    expiring_soon_certificates = (
        db.query(func.count(PersonnelCertificate.id))
        .join(Personnel)
        .filter(*soon_expiry_filters)
        .scalar()
    )
    
    return PersonnelStats(
        total_personnel=total_personnel or 0,
        active_personnel=active_personnel or 0,
        pending_review_personnel=pending_review_personnel or 0,
        expired_certificates=expired_certificates or 0,
        expiring_soon_certificates=expiring_soon_certificates or 0
    )


@router.get("/stats/certificates", response_model=CertificateStats)
def get_certificate_stats(
    company_id: Optional[int] = Query(None, description="单位ID"),
    db: Session = Depends(get_db)
):
    """获取证书统计信息"""
    # 构建基础查询条件
    base_filters = [PersonnelCertificate.deleted_at.is_(None)]
    if company_id:
        base_filters.append(Personnel.company_id == company_id)
        base_query = db.query(PersonnelCertificate).join(Personnel).filter(*base_filters)
    else:
        base_query = db.query(PersonnelCertificate).filter(*base_filters)
    
    # 总证书数
    total_certificates = base_query.count()
    
    # 有效证书数
    valid_certificates = base_query.filter(
        PersonnelCertificate.certificate_status == CertificateStatusEnum.VALID
    ).count()
    
    # 过期证书数
    expired_certificates = base_query.filter(
        PersonnelCertificate.certificate_status == CertificateStatusEnum.EXPIRED
    ).count()
    
    # 待审核证书数
    pending_review_certificates = base_query.filter(
        PersonnelCertificate.approval_status == ApprovalStatusEnum.PENDING_REVIEW
    ).count()
    
    # 按类型统计
    type_stats = {}
    type_query = (
        base_query
        .with_entities(
            PersonnelCertificate.certificate_type,
            func.count(PersonnelCertificate.id).label("count")
        )
        .group_by(PersonnelCertificate.certificate_type)
        .all()
    )
    
    for cert_type, count in type_query:
        type_stats[cert_type] = count
    
    return CertificateStats(
        total_certificates=total_certificates,
        valid_certificates=valid_certificates,
        expired_certificates=expired_certificates,
        pending_review_certificates=pending_review_certificates,
        by_type=type_stats
    )


# ============================================
# 预警管理端点
# ============================================

@router.get("/alerts/config", response_model=List[PersonnelCertificateAlertInDB])
def get_alert_configs(
    certificate_type: Optional[str] = Query(None, description="证书类型"),
    is_enabled: Optional[bool] = Query(None, description="是否启用"),
    db: Session = Depends(get_db)
):
    """获取预警配置列表"""
    filters = []
    
    if certificate_type:
        filters.append(PersonnelCertificateAlert.certificate_type == certificate_type)
    if is_enabled is not None:
        filters.append(PersonnelCertificateAlert.is_enabled == is_enabled)
    
    configs = (
        db.query(PersonnelCertificateAlert)
        .filter(*filters)
        .order_by(PersonnelCertificateAlert.certificate_type, PersonnelCertificateAlert.days_before)
        .all()
    )
    
    return configs


@router.post("/alerts/config", response_model=PersonnelCertificateAlertInDB, status_code=status.HTTP_201_CREATED)
def create_alert_config(
    config_data: PersonnelCertificateAlertCreate,
    db: Session = Depends(get_db)
):
    """创建预警配置"""
    # 检查是否已存在相同配置
    existing_config = db.query(PersonnelCertificateAlert).filter(
        PersonnelCertificateAlert.certificate_type == config_data.certificate_type,
        PersonnelCertificateAlert.alert_type == config_data.alert_type
    ).first()
    
    if existing_config:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"该证书类型和预警类型的配置已存在"
        )
    
    # 创建配置
    config_dict = config_data.dict(exclude_unset=True)
    config = PersonnelCertificateAlert(**config_dict)
    db.add(config)
    db.commit()
    db.refresh(config)
    
    return config


@router.put("/alerts/config/{config_id}", response_model=PersonnelCertificateAlertInDB)
def update_alert_config(
    config_id: int,
    config_data: PersonnelCertificateAlertUpdate,
    db: Session = Depends(get_db)
):
    """更新预警配置"""
    config = db.query(PersonnelCertificateAlert).filter(
        PersonnelCertificateAlert.id == config_id
    ).first()
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"预警配置 ID {config_id} 不存在"
        )
    
    # 更新字段
    update_data = config_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(config, field, value)
    
    db.commit()
    db.refresh(config)
    
    return config