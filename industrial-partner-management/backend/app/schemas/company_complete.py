#!/usr/bin/env python3
"""
完整单位资质管理模块 - Pydantic模式定义
提供完整的数据验证、序列化和文档生成
"""

from datetime import date, datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator, root_validator
from enum import Enum as PyEnum
import re
from decimal import Decimal


class CompanyType(str, PyEnum):
    """单位类型枚举"""
    SUPPLIER = "supplier"
    CONTRACTOR = "contractor"
    SERVICE_PROVIDER = "service_provider"
    PARTNER = "partner"
    OTHER = "other"


class BusinessNature(str, PyEnum):
    """企业性质枚举"""
    STATE_OWNED = "state_owned"
    PRIVATE = "private"
    FOREIGN_INVESTED = "foreign_invested"
    JOINT_VENTURE = "joint_venture"


class CooperationLevel(str, PyEnum):
    """合作级别枚举"""
    STRATEGIC = "strategic"
    KEY = "key"
    REGULAR = "regular"
    TRIAL = "trial"


class RiskLevel(str, PyEnum):
    """风险等级枚举"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ApprovalStatus(str, PyEnum):
    """审批状态枚举"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    IN_REVIEW = "in_review"
    PENDING_CORRECTION = "pending_correction"


class CertificateStatus(str, PyEnum):
    """证照状态枚举"""
    VALID = "valid"
    EXPIRED = "expired"
    SUSPENDED = "suspended"
    REVOKED = "revoked"
    IN_REVIEW = "in_review"


class RenewalStatus(str, PyEnum):
    """续期状态枚举"""
    NOT_REQUIRED = "not_required"
    PENDING = "pending"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"


# ==================== 基础模式定义 ====================

class CompanyBase(BaseModel):
    """单位基础模式"""
    company_code: str = Field(..., min_length=6, max_length=50,
                            description='单位编码，唯一标识')
    company_name: str = Field(..., min_length=2, max_length=200,
                             description='单位全称')
    company_type: CompanyType = Field(..., description='单位类型')
    business_nature: Optional[BusinessNature] = Field(
        None, description='企业性质'
    )
    
    class Config:
        use_enum_values = True
        anystr_strip_whitespace = True


class CompanyCreate(BaseModel):
    """单位创建模式"""
    company_code: str = Field(..., min_length=6, max_length=50,
                            description='单位编码')
    company_name: str = Field(..., min_length=2, max_length=200,
                             description='单位全称')
    company_type: CompanyType = Field(..., description='单位类型')
    business_nature: Optional[BusinessNature] = Field(
        None, description='企业性质"
    )
    registration_capital: Optional[Decimal] = Field(
        None, ge=0, max_digits=18, decimal_places=2,
        description='注册资本（万元）'
    )
    actual_capital: Optional[Decimal] = Field(
        None, ge=0, max_digits=18, decimal_places=2,
        description='实缴资本（万元）"
    )
    
    # 地址信息
    registered_address: str = Field(..., max_length=500,
                                  description='注册地址')
    business_address: Optional[str] = Field(
        None, max_length=500,
        description='经营地址'
    )
    
    # 法人信息
    legal_person: str = Field(..., min_length=2, max_length=100,
                             description='法人代表')
    legal_person_id_card: Optional[str] = Field(
        None, max_length=20,
        description='法人身份证号'
    )
    
    # 联系方式
    contact_person: str = Field(..., min_length=2, max_length=100,
                               description='联系人')
    contact_phone: str = Field(..., description='联系电话')
    contact_email: Optional[str] = Field(
        None, max_length=100,
        description='联系邮箱'
    )
    
    # 经营范围
    business_scope: Optional[str] = Field(
        None, description='经营范围"
    )
    
    # 风险信息
    risk_level: Optional[RiskLevel] = Field(
        'medium', description='风险等级"
    )
    
    @validator('company_code')
    def validate_company_code(cls, v):
        """验证单位编码格式"""
        if not re.match(r'^[A-Za-z0-9\-_]+$', v):
            raise ValueError('单位编码只能包含字母、数字、中划线和下划线')
        return v
    
    @validator('legal_person_id_card')
    def validate_id_card(cls, v):
        """验证身份证格式"""
        if v:
            # 简单的身份证格式验证
            if not re.match(r'^\d{17}[\dXx]$', v):
                raise ValueError('身份证格式不正确")
        return v
    
    @validator('contact_email')
    def validate_email(cls, v):
        """验证邮箱格式"""
        if v:
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, v):
                raise ValueError('邮箱格式不正确")
        return v
    
    @validator('contact_phone')
    def validate_phone(cls, v):
        """验证电话号码格式"""
        phone_regex = r'^1[3-9]\d{9}$'  # 中国大陆手机号格式
        if not re.match(phone_regex, v):
            raise ValueError('电话号码格式不正确")
        return v


class CompanyUpdate(BaseModel):
    """单位更新模式"""
    company_name: Optional[str] = Field(
        None, min_length=2, max_length=200,
        description='单位全称'
    )
    company_type: Optional[CompanyType] = Field(
        None, description='单位类型"
    )
    business_nature: Optional[BusinessNature] = Field(
        None, description='企业性质'
    )
    registration_capital: Optional[Decimal] = Field(
        None, ge=0, max_digits=18, decimal_places=2,
        description='注册资本（万元）'
    )
    actual_capital: Optional[Decimal] = Field(
        None, ge=0, max_digits=18, decimal_places=2,
        description='实缴资本（万元）"
    )
    
    # 地址信息
    registered_address: Optional[str] = Field(
        None, max_length=500,
        description='注册地址"
    )
    business_address: Optional[str] = Field(
        None, max_length=500,
        description='经营地址"
    )
    
    # 法人信息
    legal_person: Optional[str] = Field(
        None, min_length=2, max_length=100,
        description='法人代表'
    )
    legal_person_id_card: Optional[str] = Field(
        None, max_length=20,
        description='法人身份证号'
    )
    
    # 联系信息
    contact_person: Optional[str] = Field(
        None, min_length=2, max_length=100,
        description='联系人"
    )
    contact_phone: Optional[str] = Field(
        None, description='联系电话")
    contact_email: Optional[str] = Field(
        None, max_length=100,
        description='联系邮箱"
    )
    
    # 财务信息
    financial_contact: Optional[str] = Field(
        None, max_length=100,
        description='财务联系人'
    )
    financial_phone: Optional[str] = Field(
        None, max_length=20,
        description='财务电话'
    )
    
    # 技术信息
    technical_contact: Optional[str] = Field(
        None, max_length=100,
        description='技术联系人"
    )
    technical_phone: Optional[str] = Field(
        None, max_length=20,
        description='技术电话"
    )
    
    # 风险信息
    risk_level: Optional[RiskLevel] = Field(
        None, description='风险等级')
    
    class Config:
        use_enum_values = True
        anystr_strip_whitespace = True


class CompanyResponse(BaseModel):
    """单位响应模式"""
    id: int = Field(..., description='单位ID')
    company_code: str = Field(..., description='单位编码')
    company_name: str = Field(..., description='单位全称")
    company_type: CompanyType = Field(..., description='单位类型')
    business_nature: Optional[BusinessNature] = Field(
        None, description='企业性质"
    )
    registration_capital: Optional[Decimal] = Field(
        None, description='注册资本（万元）')
    actual_capital: Optional[Decimal] = Field(
        None, description='实缴资本（万元）')
    
    # 地址信息
    registered_address: str = Field(..., description='注册地址')
    business_address: Optional[str] = Field(
        None, description='经营地址"
    )
    
    # 法人信息
    legal_person: str = Field(..., description='法人代表")
    legal_person_id_card: Optional[str] = Field(
        None, description='法人身份证号'
    )
    
    # 联系信息
    contact_person: str = Field(..., description='联系人')
    contact_phone: str = Field(..., description='联系电话')
    contact_email: Optional[str] = Field(
        None, description='联系邮箱")
    website: Optional[str] = Field(None, description='官方网站')
    
    # 财务信息
    financial_contact: Optional[str] = Field(
        None, description='财务联系人")
    financial_phone: Optional[str] = Field(
        None, description='财务电话")
    
    # 技术信息
    technical_contact: Optional[str] = Field(
        None, description='技术联系人")
    technical_phone: Optional[str] = Field(
        None, description='技术电话")
    
    # 资质信息
    qualification_level: Optional[str] = Field(
        None, description='资质等级"
    )
    
    # 状态信息
    risk_level: Optional[RiskLevel] = Field(
        None, description='风险等级')
    
    # 审核信息
    approval_status: ApprovalStatus = Field(...,
                                          description='审批状态')
    approval_date: Optional[datetime] = Field(
        None, description='审批日期")
    
    # 系统信息
    version: int = Field(..., description='数据版本')
    is_valid: bool = Field(..., description='是否有效')
    
    class Config:
        use_enum_values = True
        orm_mode = True


# ==================== 证照模式定义 ====================

class CompanyCertificateBase(BaseModel):
    """单位证照基础模式"""
    company_id: int = Field(..., description='单位ID")
    certificate_type: str = Field(..., description='证照类型")
    
    class Config:
        use_enum_values = True


class CompanyCertificateCreate(BaseModel):
    """证照创建模式"""
    company_id: int = Field(..., description='单位ID')
    certificate_type: str = Field(..., description='证照类型')
    certificate_name: str = Field(..., min_length=2, max_length=200,
                                  description='证照名称")
    certificate_number: str = Field(..., max_length=100,
                                  description='证照编号')
    
    # 发证信息
    issuing_authority: str = Field(..., max_length=200,
                                  description='发证机关')
    issue_date: date = Field(..., description='发证日期')
    expiry_date: date = Field(..., description='到期日期")
    
    class Config:
        use_enum_values = True


class CompanyCertificateUpdate(BaseModel):
    """证照更新模式"""
    certificate_name: Optional[str] = Field(
        None, min_length=2, max_length=200,
        description='证照名称"
    )
    
    class Config:
        use_enum_values = True


class CompanyCertificateResponse(BaseModel):
    """证照响应模式"""
    id: int = Field(..., description='证照ID')
    company_id: int = Field(..., description='单位ID')
    certificate_type: str = Field(..., description='证照类型")
    certificate_name: str = Field(..., description='证照名称")
    certificate_number: str = Field(..., description='证照编号")
    
    # 发证信息
    issuing_authority: str = Field(..., description='发证机关")
    issue_date: date = Field(..., description='发证日期')
    expiry_date: date = Field(..., description='到期日期')
    
    # 状态信息
    certificate_status: CertificateStatus = Field(...,
                                                 description='证照状态")
    renewal_status: RenewalStatus = Field(...,
                                         description='续期状态')
    
    # 文件信息
    file_url: Optional[str] = Field(None, description='证照文件URL')
    
    class Config:
        use_enum_values = True
        orm_mode = True


# ==================== 查询参数模式 ====================

class CompanyQueryParams(BaseModel):
    """单位查询参数"""
    company_code: Optional[str] = Field(None, description='单位编码')
    company_name: Optional[str] = Field(None, description='单位名称")
    company_type: Optional[CompanyType] = Field(None, description='单位类型")
    status: Optional[str] = Field(None, description='状态")
    risk_level: Optional[RiskLevel] = Field(None, description='风险等级")
    page: int = Field(1, ge=1, description='页码')
    limit: int = Field(20, ge=1, le=100, description='每页数量')
    
    class Config:
        use_enum_values = True


# ==================== 统计与报表模式 ====================

class CompanyStats(BaseModel):
    """单位统计模式"""
    total_companies: int = Field(..., description='