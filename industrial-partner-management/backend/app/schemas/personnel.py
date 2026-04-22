from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, Field, validator
from enum import Enum
from app.models.personnel import (
    GenderEnum, EmploymentStatusEnum, PersonnelStatusEnum,
    CertificateStatusEnum, ApprovalStatusEnum, AlertTypeEnum, AlertChannelEnum
)


# ============================================
# 通用基础模型
# ============================================

class BaseSchema(BaseModel):
    """基础模型"""
    class Config:
        from_attributes = True
        use_enum_values = True


# ============================================
# 人员相关模型
# ============================================

class PersonnelBase(BaseSchema):
    """人员基础信息"""
    personnel_code: str = Field(..., min_length=1, max_length=50, description="人员编号")
    name: str = Field(..., min_length=1, max_length=100, description="姓名")
    id_card: str = Field(..., min_length=15, max_length=18, description="身份证号")
    gender: GenderEnum = Field(default=GenderEnum.MALE, description="性别")
    birth_date: Optional[date] = Field(None, description="出生日期")
    phone: Optional[str] = Field(None, max_length=20, description="联系电话")
    email: Optional[str] = Field(None, max_length=100, description="电子邮箱")
    position: Optional[str] = Field(None, max_length=100, description="岗位/职务")
    work_type: Optional[str] = Field(None, max_length=50, description="工种/岗位类型")
    hire_date: Optional[date] = Field(None, description="入职日期")
    employment_status: EmploymentStatusEnum = Field(default=EmploymentStatusEnum.ACTIVE, description="在职状态")
    status: PersonnelStatusEnum = Field(default=PersonnelStatusEnum.PENDING_REVIEW, description="审核状态")
    photo_url: Optional[str] = Field(None, max_length=500, description="照片URL")
    
    @validator("id_card")
    def validate_id_card(cls, v):
        # 简单的身份证号验证
        if not v.isdigit() and not (len(v) == 18 and v[-1] in ('X', 'x')):
            raise ValueError("身份证号格式不正确")
        return v.upper() if v else v
    
    @validator("email")
    def validate_email(cls, v):
        if v and "@" not in v:
            raise ValueError("邮箱格式不正确")
        return v
    
    @validator("birth_date")
    def validate_birth_date(cls, v):
        if v and v > date.today():
            raise ValueError("出生日期不能晚于今天")
        return v
    
    @validator("hire_date")
    def validate_hire_date(cls, v, values):
        if v and "birth_date" in values and values["birth_date"]:
            if v < values["birth_date"]:
                raise ValueError("入职日期不能早于出生日期")
        return v


class PersonnelCreate(PersonnelBase):
    """创建人员"""
    company_id: int = Field(..., description="所属单位ID")
    created_by: Optional[str] = Field(None, max_length=100, description="创建人")


class PersonnelUpdate(BaseSchema):
    """更新人员信息"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="姓名")
    gender: Optional[GenderEnum] = Field(None, description="性别")
    birth_date: Optional[date] = Field(None, description="出生日期")
    phone: Optional[str] = Field(None, max_length=20, description="联系电话")
    email: Optional[str] = Field(None, max_length=100, description="电子邮箱")
    position: Optional[str] = Field(None, max_length=100, description="岗位/职务")
    work_type: Optional[str] = Field(None, max_length=50, description="工种/岗位类型")
    hire_date: Optional[date] = Field(None, description="入职日期")
    employment_status: Optional[EmploymentStatusEnum] = Field(None, description="在职状态")
    status: Optional[PersonnelStatusEnum] = Field(None, description="审核状态")
    photo_url: Optional[str] = Field(None, max_length=500, description="照片URL")
    updated_by: Optional[str] = Field(None, max_length=100, description="更新人")


class PersonnelInDB(PersonnelBase):
    """数据库中的完整人员信息"""
    id: int = Field(..., description="人员ID")
    company_id: int = Field(..., description="所属单位ID")
    created_by: Optional[str] = Field(None, description="创建人")
    updated_by: Optional[str] = Field(None, description="更新人")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    deleted_at: Optional[datetime] = Field(None, description="软删除时间")


class PersonnelSimple(PersonnelBase):
    """简化的人员信息（用于列表显示）"""
    id: int = Field(..., description="人员ID")
    company_id: int = Field(..., description="所属单位ID")
    company_name: Optional[str] = Field(None, description="单位名称")


# ============================================
# 人员证书相关模型
# ============================================

class PersonnelCertificateBase(BaseSchema):
    """人员证书基础信息"""
    certificate_type: str = Field(..., min_length=1, max_length=50, description="证书类型")
    certificate_name: str = Field(..., min_length=1, max_length=200, description="证书名称")
    certificate_number: str = Field(..., min_length=1, max_length=100, description="证书编号")
    issuing_authority: Optional[str] = Field(None, max_length=200, description="发证机构")
    issue_date: date = Field(..., description="发证日期")
    expiry_date: date = Field(..., description="到期日期")
    certificate_status: CertificateStatusEnum = Field(default=CertificateStatusEnum.VALID, description="证书状态")
    approval_status: ApprovalStatusEnum = Field(default=ApprovalStatusEnum.PENDING_REVIEW, description="审核状态")
    
    # 文件相关字段
    file_url: Optional[str] = Field(None, max_length=500, description="证书扫描件URL")
    file_name: Optional[str] = Field(None, max_length=200, description="证书文件名称")
    file_size: Optional[int] = Field(None, ge=0, description="文件大小（字节）")
    
    # 审核相关字段
    review_notes: Optional[str] = Field(None, description="审核意见")
    
    @validator("expiry_date")
    def validate_expiry_date(cls, v, values):
        if "issue_date" in values and values["issue_date"]:
            if v <= values["issue_date"]:
                raise ValueError("到期日期必须晚于发证日期")
        return v


class PersonnelCertificateCreate(PersonnelCertificateBase):
    """创建人员证书"""
    personnel_id: int = Field(..., description="人员ID")
    created_by: Optional[str] = Field(None, max_length=100, description="创建人")


class PersonnelCertificateUpdate(BaseSchema):
    """更新人员证书信息"""
    certificate_type: Optional[str] = Field(None, min_length=1, max_length=50, description="证书类型")
    certificate_name: Optional[str] = Field(None, min_length=1, max_length=200, description="证书名称")
    issuing_authority: Optional[str] = Field(None, max_length=200, description="发证机构")
    issue_date: Optional[date] = Field(None, description="发证日期")
    expiry_date: Optional[date] = Field(None, description="到期日期")
    certificate_status: Optional[CertificateStatusEnum] = Field(None, description="证书状态")
    approval_status: Optional[ApprovalStatusEnum] = Field(None, description="审核状态")
    
    # 文件相关字段
    file_url: Optional[str] = Field(None, max_length=500, description="证书扫描件URL")
    file_name: Optional[str] = Field(None, max_length=200, description="证书文件名称")
    file_size: Optional[int] = Field(None, ge=0, description="文件大小（字节）")
    
    # 审核相关字段
    review_notes: Optional[str] = Field(None, description="审核意见")
    reviewed_by: Optional[str] = Field(None, max_length=100, description="审核人")
    
    updated_by: Optional[str] = Field(None, max_length=100, description="更新人")


class PersonnelCertificateInDB(PersonnelCertificateBase):
    """数据库中的完整证书信息"""
    id: int = Field(..., description="证书ID")
    personnel_id: int = Field(..., description="人员ID")
    reviewed_by: Optional[str] = Field(None, description="审核人")
    reviewed_at: Optional[datetime] = Field(None, description="审核时间")
    created_by: Optional[str] = Field(None, description="创建人")
    updated_by: Optional[str] = Field(None, description="更新人")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    deleted_at: Optional[datetime] = Field(None, description="软删除时间")


class PersonnelCertificateWithPersonnel(PersonnelCertificateInDB):
    """包含人员信息的证书信息"""
    personnel_name: Optional[str] = Field(None, description="人员姓名")
    personnel_code: Optional[str] = Field(None, description="人员编号")


# ============================================
# 证书预警相关模型
# ============================================

class PersonnelCertificateAlertBase(BaseSchema):
    """证书预警配置基础信息"""
    certificate_type: str = Field(..., min_length=1, max_length=50, description="证书类型")
    alert_type: AlertTypeEnum = Field(..., description="预警类型")
    days_before: int = Field(..., ge=1, le=365, description="到期前天数")
    alert_channel: AlertChannelEnum = Field(default=AlertChannelEnum.SYSTEM, description="预警渠道")
    alert_template: str = Field(..., min_length=1, max_length=200, description="预警模板名称")
    is_enabled: bool = Field(default=True, description="是否启用")


class PersonnelCertificateAlertCreate(PersonnelCertificateAlertBase):
    """创建证书预警配置"""
    created_by: Optional[str] = Field(None, max_length=100, description="创建人")


class PersonnelCertificateAlertUpdate(BaseSchema):
    """更新证书预警配置"""
    days_before: Optional[int] = Field(None, ge=1, le=365, description="到期前天数")
    alert_channel: Optional[AlertChannelEnum] = Field(None, description="预警渠道")
    alert_template: Optional[str] = Field(None, min_length=1, max_length=200, description="预警模板名称")
    is_enabled: Optional[bool] = Field(None, description="是否启用")
    updated_by: Optional[str] = Field(None, max_length=100, description="更新人")


class PersonnelCertificateAlertInDB(PersonnelCertificateAlertBase):
    """数据库中的完整预警配置信息"""
    id: int = Field(..., description="预警配置ID")
    created_by: Optional[str] = Field(None, description="创建人")
    updated_by: Optional[str] = Field(None, description="更新人")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


class PersonnelCertificateAlertLogBase(BaseSchema):
    """证书预警记录基础信息"""
    alert_type: AlertTypeEnum = Field(..., description="预警类型")
    alert_date: date = Field(..., description="预警日期")
    expiry_date: date = Field(..., description="证书到期日期")
    days_left: int = Field(..., ge=0, description="剩余天数")
    alert_channel: AlertChannelEnum = Field(..., description="预警渠道")
    alert_content: str = Field(..., description="预警内容")
    sent_to: Optional[str] = Field(None, max_length=200, description="发送对象")
    is_sent: bool = Field(default=False, description="是否已发送")


class PersonnelCertificateAlertLogCreate(PersonnelCertificateAlertLogBase):
    """创建证书预警记录"""
    certificate_id: int = Field(..., description="证书ID")
    personnel_id: int = Field(..., description="人员ID")
    alert_config_id: int = Field(..., description="预警配置ID")


class PersonnelCertificateAlertLogInDB(PersonnelCertificateAlertLogBase):
    """数据库中的完整预警记录信息"""
    id: int = Field(..., description="预警记录ID")
    certificate_id: int = Field(..., description="证书ID")
    personnel_id: int = Field(..., description="人员ID")
    alert_config_id: int = Field(..., description="预警配置ID")
    sent_at: Optional[datetime] = Field(None, description="发送时间")
    created_at: datetime = Field(..., description="创建时间")


# ============================================
# 人员培训记录相关模型
# ============================================

class PersonnelTrainingRecordBase(BaseSchema):
    """人员培训记录基础信息"""
    training_type: str = Field(..., min_length=1, max_length=50, description="培训类型")
    training_name: str = Field(..., min_length=1, max_length=200, description="培训名称")
    training_date: date = Field(..., description="培训日期")
    training_duration: Optional[float] = Field(None, ge=0, le=999.99, description="培训时长（小时）")
    training_institution: Optional[str] = Field(None, max_length=200, description="培训机构")
    trainer: Optional[str] = Field(None, max_length=100, description="培训讲师")
    training_score: Optional[float] = Field(None, ge=0, le=100, description="培训成绩/分数")
    is_passed: Optional[bool] = Field(None, description="是否通过")
    certificate_number: Optional[str] = Field(None, max_length=100, description="培训证书编号")
    certificate_url: Optional[str] = Field(None, max_length=500, description="培训证书URL")
    notes: Optional[str] = Field(None, description="备注")
    
    @validator("training_date")
    def validate_training_date(cls, v):
        if v > date.today():
            raise ValueError("培训日期不能晚于今天")
        return v


class PersonnelTrainingRecordCreate(PersonnelTrainingRecordBase):
    """创建人员培训记录"""
    personnel_id: int = Field(..., description="人员ID")
    created_by: Optional[str] = Field(None, max_length=100, description="创建人")


class PersonnelTrainingRecordUpdate(BaseSchema):
    """更新人员培训记录"""
    training_type: Optional[str] = Field(None, min_length=1, max_length=50, description="培训类型")
    training_name: Optional[str] = Field(None, min_length=1, max_length=200, description="培训名称")
    training_date: Optional[date] = Field(None, description="培训日期")
    training_duration: Optional[float] = Field(None, ge=0, le=999.99, description="培训时长（小时）")
    training_institution: Optional[str] = Field(None, max_length=200, description="培训机构")
    trainer: Optional[str] = Field(None, max_length=100, description="培训讲师")
    training_score: Optional[float] = Field(None, ge=0, le=100, description="培训成绩/分数")
    is_passed: Optional[bool] = Field(None, description="是否通过")
    certificate_number: Optional[str] = Field(None, max_length=100, description="培训证书编号")
    certificate_url: Optional[str] = Field(None, max_length=500, description="培训证书URL")
    notes: Optional[str] = Field(None, description="备注")
    updated_by: Optional[str] = Field(None, max_length=100, description="更新人")


class PersonnelTrainingRecordInDB(PersonnelTrainingRecordBase):
    """数据库中的完整培训记录信息"""
    id: int = Field(..., description="培训记录ID")
    personnel_id: int = Field(..., description="人员ID")
    created_by: Optional[str] = Field(None, description="创建人")
    updated_by: Optional[str] = Field(None, description="更新人")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    deleted_at: Optional[datetime] = Field(None, description="软删除时间")


# ============================================
# 查询和分页模型
# ============================================

class PersonnelQueryParams(BaseSchema):
    """人员查询参数"""
    company_id: Optional[int] = Field(None, description="单位ID")
    name: Optional[str] = Field(None, description="姓名")
    personnel_code: Optional[str] = Field(None, description="人员编号")
    id_card: Optional[str] = Field(None, description="身份证号")
    employment_status: Optional[EmploymentStatusEnum] = Field(None, description="在职状态")
    status: Optional[PersonnelStatusEnum] = Field(None, description="审核状态")
    work_type: Optional[str] = Field(None, description="工种")
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=20, ge=1, le=100, description="每页大小")


class PersonnelCertificateQueryParams(BaseSchema):
    """人员证书查询参数"""
    personnel_id: Optional[int] = Field(None, description="人员ID")
    certificate_type: Optional[str] = Field(None, description="证书类型")
    certificate_status: Optional[CertificateStatusEnum] = Field(None, description="证书状态")
    approval_status: Optional[ApprovalStatusEnum] = Field(None, description="审核状态")
    expiry_start_date: Optional[date] = Field(None, description="到期开始日期")
    expiry_end_date: Optional[date] = Field(None, description="到期结束日期")
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=20, ge=1, le=100, description="每页大小")


class PersonnelTrainingRecordQueryParams(BaseSchema):
    """人员培训记录查询参数"""
    personnel_id: Optional[int] = Field(None, description="人员ID")
    training_type: Optional[str] = Field(None, description="培训类型")
    training_start_date: Optional[date] = Field(None, description="培训开始日期")
    training_end_date: Optional[date] = Field(None, description="培训结束日期")
    is_passed: Optional[bool] = Field(None, description="是否通过")
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=20, ge=1, le=100, description="每页大小")


class PaginatedResponse(BaseSchema):
    """分页响应基础模型"""
    total: int = Field(..., description="总记录数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页大小")
    total_pages: int = Field(..., description="总页数")


class PersonnelPaginatedResponse(PaginatedResponse):
    """人员分页响应"""
    items: List[PersonnelSimple] = Field(..., description="人员列表")


class PersonnelCertificatePaginatedResponse(PaginatedResponse):
    """人员证书分页响应"""
    items: List[PersonnelCertificateWithPersonnel] = Field(..., description="证书列表")


class PersonnelTrainingRecordPaginatedResponse(PaginatedResponse):
    """人员培训记录分页响应"""
    items: List[PersonnelTrainingRecordInDB] = Field(..., description="培训记录列表")


# ============================================
# 统计和报表模型
# ============================================

class PersonnelStats(BaseSchema):
    """人员统计信息"""
    total_personnel: int = Field(..., description="总人员数")
    active_personnel: int = Field(..., description="在职人员数")
    pending_review_personnel: int = Field(..., description="待审核人员数")
    expired_certificates: int = Field(..., description="过期证书数")
    expiring_soon_certificates: int = Field(..., description="即将过期证书数（30天内）")


class CertificateStats(BaseSchema):
    """证书统计信息"""
    total_certificates: int = Field(..., description="总证书数")
    valid_certificates: int = Field(..., description="有效证书数")
    expired_certificates: int = Field(..., description="过期证书数")
    pending_review_certificates: int = Field(..., description="待审核证书数")
    by_type: dict = Field(..., description="按类型统计")


class TrainingStats(BaseSchema):
    """培训统计信息"""
    total_trainings: int = Field(..., description="总培训记录数")
    passed_trainings: int = Field(..., description="通过培训数")
    failed_trainings: int = Field(..., description="未通过培训数")
    avg_score: float = Field(..., description="平均分数")
    total_training_hours: float = Field(..., description="总培训时长")


class AlertStats(BaseSchema):
    """预警统计信息"""
    total_alerts: int = Field(..., description="总预警数")
    sent_alerts: int = Field(..., description="已发送预警数")
    pending_alerts: int = Field(..., description="待发送预警数")
    by_type: dict = Field(..., description="按类型统计")


# ============================================
# 批量操作模型
# ============================================

class BulkPersonnelCreate(BaseSchema):
    """批量创建人员"""
    items: List[PersonnelCreate] = Field(..., min_items=1, max_items=100, description="人员列表")


class BulkPersonnelCertificateCreate(BaseSchema):
    """批量创建人员证书"""
    items: List[PersonnelCertificateCreate] = Field(..., min_items=1, max_items=100, description="证书列表")


class BulkPersonnelTrainingRecordCreate(BaseSchema):
    """批量创建人员培训记录"""
    items: List[PersonnelTrainingRecordCreate] = Field(..., min_items=1, max_items=100, description="培训记录列表")


class BulkUpdateStatus(BaseSchema):
    """批量更新状态"""
    ids: List[int] = Field(..., min_items=1, max_items=100, description="ID列表")
    status: PersonnelStatusEnum = Field(..., description="新状态")
    updated_by: Optional[str] = Field(None, max_length=100, description="更新人")


class BulkUpdateCertificateStatus(BaseSchema):
    """批量更新证书状态"""
    ids: List[int] = Field(..., min_items=1, max_items=100, description="证书ID列表")
    certificate_status: Optional[CertificateStatusEnum] = Field(None, description="证书状态")
    approval_status: Optional[ApprovalStatusEnum] = Field(None, description="审核状态")
    review_notes: Optional[str] = Field(None, description="审核意见")
    reviewed_by: Optional[str] = Field(None, max_length=100, description="审核人")