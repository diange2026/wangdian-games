from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, Field, validator, ConfigDict
from app.models.company import (
    CompanyType, CompanyStatus, RiskLevel,
    CertificateType, CertificateStatus, ReviewStatus
)


# ==================== 基础分页和排序 ====================
class PaginationParams(BaseModel):
    """分页参数"""
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=20, ge=1, le=100, description="每页数量")
    

class SortParams(BaseModel):
    """排序参数"""
    sort_by: str = Field(default="created_at", description="排序字段")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$", description="排序方向")


# ==================== 单位相关Schema ====================
class CompanyBase(BaseModel):
    """单位基础信息"""
    company_code: str = Field(..., min_length=1, max_length=50, description="单位编码")
    company_name: str = Field(..., min_length=1, max_length=200, description="单位名称")
    company_type: CompanyType = Field(..., description="单位类型")
    legal_person: Optional[str] = Field(None, max_length=100, description="法人代表")
    contact_person: str = Field(..., min_length=1, max_length=100, description="联系人")
    contact_phone: str = Field(..., min_length=1, max_length=20, description="联系电话")
    contact_email: Optional[str] = Field(None, max_length=100, description="联系邮箱")
    registered_address: Optional[str] = Field(None, max_length=500, description="注册地址")
    business_address: Optional[str] = Field(None, max_length=500, description="经营地址")
    business_scope: Optional[str] = Field(None, description="经营范围")
    cooperation_start_date: Optional[date] = Field(None, description="合作开始日期")
    cooperation_end_date: Optional[date] = Field(None, description="合作结束日期")
    risk_level: RiskLevel = Field(default=RiskLevel.MEDIUM, description="风险等级")
    remarks: Optional[str] = Field(None, description="备注")


class CompanyCreate(CompanyBase):
    """创建单位"""
    pass


class CompanyUpdate(BaseModel):
    """更新单位信息"""
    company_name: Optional[str] = Field(None, min_length=1, max_length=200, description="单位名称")
    company_type: Optional[CompanyType] = Field(None, description="单位类型")
    legal_person: Optional[str] = Field(None, max_length=100, description="法人代表")
    contact_person: Optional[str] = Field(None, min_length=1, max_length=100, description="联系人")
    contact_phone: Optional[str] = Field(None, min_length=1, max_length=20, description="联系电话")
    contact_email: Optional[str] = Field(None, max_length=100, description="联系邮箱")
    registered_address: Optional[str] = Field(None, max_length=500, description="注册地址")
    business_address: Optional[str] = Field(None, max_length=500, description="经营地址")
    business_scope: Optional[str] = Field(None, description="经营范围")
    status: Optional[CompanyStatus] = Field(None, description="状态")
    cooperation_start_date: Optional[date] = Field(None, description="合作开始日期")
    cooperation_end_date: Optional[date] = Field(None, description="合作结束日期")
    risk_level: Optional[RiskLevel] = Field(None, description="风险等级")
    audit_score: Optional[float] = Field(None, ge=0, le=100, description="审核评分")
    remarks: Optional[str] = Field(None, description="备注")


class CompanyInDB(CompanyBase):
    """数据库中的单位信息"""
    id: int = Field(..., description="单位ID")
    status: CompanyStatus = Field(..., description="状态")
    audit_score: float = Field(..., ge=0, le=100, description="审核评分")
    created_by: Optional[int] = Field(None, description="创建人")
    updated_by: Optional[int] = Field(None, description="更新人")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    model_config = ConfigDict(from_attributes=True)


class CompanyResponse(CompanyInDB):
    """API响应中的单位信息"""
    certificate_count: int = Field(default=0, description="证照数量")
    valid_certificate_count: int = Field(default=0, description="有效证照数量")
    expiring_certificate_count: int = Field(default=0, description="即将到期证照数量")


# ==================== 单位证照相关Schema ====================
class CompanyCertificateBase(BaseModel):
    """单位证照基础信息"""
    certificate_type: CertificateType = Field(..., description="证照类型")
    certificate_name: str = Field(..., min_length=1, max_length=200, description="证照名称")
    certificate_number: str = Field(..., min_length=1, max_length=100, description="证照编号")
    issuing_authority: Optional[str] = Field(None, max_length=200, description="发证机关")
    issue_date: Optional[date] = Field(None, description="发证日期")
    expiry_date: date = Field(..., description="有效期至")
    is_long_term: bool = Field(default=False, description="是否长期有效")
    review_notes: Optional[str] = Field(None, description="审核意见")


class CompanyCertificateCreate(CompanyCertificateBase):
    """创建单位证照"""
    company_id: int = Field(..., gt=0, description="单位ID")


class CompanyCertificateUpdate(BaseModel):
    """更新单位证照"""
    certificate_type: Optional[CertificateType] = Field(None, description="证照类型")
    certificate_name: Optional[str] = Field(None, min_length=1, max_length=200, description="证照名称")
    certificate_number: Optional[str] = Field(None, min_length=1, max_length=100, description="证照编号")
    issuing_authority: Optional[str] = Field(None, max_length=200, description="发证机关")
    issue_date: Optional[date] = Field(None, description="发证日期")
    expiry_date: Optional[date] = Field(None, description="有效期至")
    is_long_term: Optional[bool] = Field(None, description="是否长期有效")
    certificate_status: Optional[CertificateStatus] = Field(None, description="证照状态")
    review_status: Optional[ReviewStatus] = Field(None, description="审核状态")
    review_notes: Optional[str] = Field(None, description="审核意见")
    reviewed_by: Optional[int] = Field(None, description="审核人")


class CompanyCertificateInDB(CompanyCertificateBase):
    """数据库中的单位证照信息"""
    id: int = Field(..., description="证照ID")
    company_id: int = Field(..., gt=0, description="单位ID")
    certificate_status: CertificateStatus = Field(..., description="证照状态")
    review_status: ReviewStatus = Field(..., description="审核状态")
    storage_path: Optional[str] = Field(None, description="证照文件存储路径")
    file_name: Optional[str] = Field(None, description="文件名")
    file_size: Optional[int] = Field(None, ge=0, description="文件大小(字节)")
    file_md5: Optional[str] = Field(None, description="文件MD5")
    reviewed_by: Optional[int] = Field(None, description="审核人")
    reviewed_at: Optional[datetime] = Field(None, description="审核时间")
    created_by: Optional[int] = Field(None, description="创建人")
    updated_by: Optional[int] = Field(None, description="更新人")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    model_config = ConfigDict(from_attributes=True)


class CompanyCertificateResponse(CompanyCertificateInDB):
    """API响应中的单位证照信息"""
    company_name: Optional[str] = Field(None, description="单位名称")
    days_remaining: Optional[int] = Field(None, description="剩余天数")
    is_expiring_soon: bool = Field(default=False, description="是否即将到期")
    is_expired: bool = Field(default=False, description="是否已过期")


# ==================== 查询参数 ====================
class CompanyQueryParams(PaginationParams, SortParams):
    """单位查询参数"""
    company_code: Optional[str] = Field(None, description="单位编码")
    company_name: Optional[str] = Field(None, description="单位名称")
    company_type: Optional[CompanyType] = Field(None, description="单位类型")
    status: Optional[CompanyStatus] = Field(None, description="状态")
    risk_level: Optional[RiskLevel] = Field(None, description="风险等级")
    contact_person: Optional[str] = Field(None, description="联系人")
    contact_phone: Optional[str] = Field(None, description="联系电话")


class CertificateQueryParams(PaginationParams, SortParams):
    """证照查询参数"""
    company_id: Optional[int] = Field(None, description="单位ID")
    company_name: Optional[str] = Field(None, description="单位名称")
    certificate_type: Optional[CertificateType] = Field(None, description="证照类型")
    certificate_status: Optional[CertificateStatus] = Field(None, description="证照状态")
    review_status: Optional[ReviewStatus] = Field(None, description="审核状态")
    certificate_number: Optional[str] = Field(None, description="证照编号")
    expiry_date_start: Optional[date] = Field(None, description="有效期开始")
    expiry_date_end: Optional[date] = Field(None, description="有效期结束")
    is_expiring_soon: Optional[bool] = Field(None, description="是否即将到期")
    is_expired: Optional[bool] = Field(None, description="是否已过期")


# ==================== 批量操作 ====================
class BulkCreateCertificates(BaseModel):
    """批量创建证照"""
    certificates: List[CompanyCertificateCreate] = Field(..., min_items=1, max_items=100)


class BulkUpdateCertificates(BaseModel):
    """批量更新证照"""
    certificate_ids: List[int] = Field(..., min_items=1, max_items=100, description="证照ID列表")
    data: CompanyCertificateUpdate = Field(..., description="更新数据")


class BulkDeleteRequest(BaseModel):
    """批量删除请求"""
    ids: List[int] = Field(..., min_items=1, max_items=100, description="ID列表")


# ==================== 统计响应 ====================
class CompanyStatsResponse(BaseModel):
    """单位统计信息"""
    total_count: int = Field(..., description="单位总数")
    active_count: int = Field(..., description="正常单位数")
    suspended_count: int = Field(..., description="停用单位数")
    blacklisted_count: int = Field(..., description="黑名单单位数")
    low_risk_count: int = Field(..., description="低风险单位数")
    medium_risk_count: int = Field(..., description="中风险单位数")
    high_risk_count: int = Field(..., description="高风险单位数")
    by_type: dict = Field(..., description="按类型统计")


class CertificateStatsResponse(BaseModel):
    """证照统计信息"""
    total_count: int = Field(..., description="证照总数")
    valid_count: int = Field(..., description="有效证照数")
    expired_count: int = Field(..., description="过期证照数")
    expiring_soon_count: int = Field(..., description="即将到期证照数")
    pending_review_count: int = Field(..., description="待审核证照数")
    by_type: dict = Field(..., description="按类型统计")
    by_status: dict = Field(..., description="按状态统计")


__all__ = [
    # 单位相关
    "CompanyBase", "CompanyCreate", "CompanyUpdate", "CompanyInDB", "CompanyResponse",
    # 证照相关
    "CompanyCertificateBase", "CompanyCertificateCreate", "CompanyCertificateUpdate",
    "CompanyCertificateInDB", "CompanyCertificateResponse",
    # 查询参数
    "PaginationParams", "SortParams", "CompanyQueryParams", "CertificateQueryParams",
    # 批量操作
    "BulkCreateCertificates", "BulkUpdateCertificates", "BulkDeleteRequest",
    # 统计
    "CompanyStatsResponse", "CertificateStatsResponse",
]