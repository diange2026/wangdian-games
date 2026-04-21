from sqlalchemy import (
    Column, BigInteger, String, Text, Date, Enum, Boolean, 
    DECIMAL, ForeignKey, Index, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import ENUM
from app.db.session import Base
from datetime import datetime
from enum import Enum as PyEnum


class CompanyType(PyEnum):
    SUPPLIER = "supplier"  # 供应商
    CONTRACTOR = "contractor"  # 承包商
    SERVICE_PROVIDER = "service_provider"  # 服务商
    OTHER = "other"  # 其他


class CompanyStatus(PyEnum):
    ACTIVE = "active"  # 正常
    INACTIVE = "inactive"  # 未激活
    SUSPENDED = "suspended"  # 停用
    BLACKLISTED = "blacklisted"  # 黑名单


class RiskLevel(PyEnum):
    LOW = "low"  # 低风险
    MEDIUM = "medium"  # 中风险
    HIGH = "high"  # 高风险


class Company(Base):
    __tablename__ = "companies"
    __table_args__ = (
        Index("idx_company_code", "company_code"),
        Index("idx_company_name", "company_name"),
        Index("idx_company_type", "company_type"),
        Index("idx_status", "status"),
        Index("idx_risk_level", "risk_level"),
    )
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="单位ID")
    company_code = Column(String(50), unique=True, nullable=False, comment="单位编码")
    company_name = Column(String(200), nullable=False, comment="单位名称")
    company_type = Column(
        ENUM(CompanyType, values_callable=lambda x: [e.value for e in CompanyType]),
        nullable=False,
        comment="单位类型"
    )
    legal_person = Column(String(100), comment="法人代表")
    contact_person = Column(String(100), nullable=False, comment="联系人")
    contact_phone = Column(String(20), nullable=False, comment="联系电话")
    contact_email = Column(String(100), comment="联系邮箱")
    registered_address = Column(String(500), comment="注册地址")
    business_address = Column(String(500), comment="经营地址")
    business_scope = Column(Text, comment="经营范围")
    status = Column(
        ENUM(CompanyStatus, values_callable=lambda x: [e.value for e in CompanyStatus]),
        default=CompanyStatus.ACTIVE.value,
        comment="状态"
    )
    cooperation_start_date = Column(Date, comment="合作开始日期")
    cooperation_end_date = Column(Date, comment="合作结束日期")
    risk_level = Column(
        ENUM(RiskLevel, values_callable=lambda x: [e.value for e in RiskLevel]),
        default=RiskLevel.MEDIUM.value,
        comment="风险等级"
    )
    audit_score = Column(DECIMAL(5, 2), default=0.00, comment="审核评分")
    remarks = Column(Text, comment="备注")
    created_by = Column(BigInteger, comment="创建人")
    updated_by = Column(BigInteger, comment="更新人")
    created_at = Column(Date, default=datetime.now, comment="创建时间")
    updated_at = Column(Date, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关系
    certificates = relationship("CompanyCertificate", back_populates="company", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.company_name}', code='{self.company_code}')>"


class CertificateType(PyEnum):
    BUSINESS_LICENSE = "business_license"  # 营业执照
    SAFETY_PRODUCTION = "safety_production"  # 安全生产许可证
    QUALIFICATION_LEVEL = "qualification_level"  # 资质等级证书
    TAX_REGISTRATION = "tax_registration"  # 税务登记证
    ORGANIZATION_CODE = "organization_code"  # 组织机构代码证
    OTHER = "other"  # 其他证照


class CertificateStatus(PyEnum):
    VALID = "valid"  # 有效
    EXPIRED = "expired"  # 过期
    EXPIRING_SOON = "expiring_soon"  # 即将到期
    REVOKED = "revoked"  # 吊销


class ReviewStatus(PyEnum):
    PENDING = "pending"  # 待审核
    APPROVED = "approved"  # 审核通过
    REJECTED = "rejected"  # 审核拒绝


class CompanyCertificate(Base):
    __tablename__ = "company_certificates"
    __table_args__ = (
        Index("idx_company_id", "company_id"),
        Index("idx_certificate_type", "certificate_type"),
        Index("idx_expiry_date", "expiry_date"),
        Index("idx_certificate_status", "certificate_status"),
        Index("idx_review_status", "review_status"),
        UniqueConstraint("certificate_number", name="uk_certificate_number"),
        {"comment": "单位证照表"}
    )
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="证照ID")
    company_id = Column(
        BigInteger,
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        comment="单位ID"
    )
    certificate_type = Column(
        ENUM(CertificateType, values_callable=lambda x: [e.value for e in CertificateType]),
        nullable=False,
        comment="证照类型"
    )
    certificate_name = Column(String(200), nullable=False, comment="证照名称")
    certificate_number = Column(String(100), nullable=False, comment="证照编号")
    issuing_authority = Column(String(200), comment="发证机关")
    issue_date = Column(Date, comment="发证日期")
    expiry_date = Column(Date, nullable=False, comment="有效期至")
    is_long_term = Column(Boolean, default=False, comment="是否长期有效")
    certificate_status = Column(
        ENUM(CertificateStatus, values_callable=lambda x: [e.value for e in CertificateStatus]),
        default=CertificateStatus.VALID.value,
        comment="证照状态"
    )
    storage_path = Column(String(500), comment="证照文件存储路径")
    file_name = Column(String(200), comment="文件名")
    file_size = Column(BigInteger, comment="文件大小(字节)")
    file_md5 = Column(String(32), comment="文件MD5")
    review_status = Column(
        ENUM(ReviewStatus, values_callable=lambda x: [e.value for e in ReviewStatus]),
        default=ReviewStatus.PENDING.value,
        comment="审核状态"
    )
    review_notes = Column(Text, comment="审核意见")
    reviewed_by = Column(BigInteger, comment="审核人")
    reviewed_at = Column(Date, comment="审核时间")
    created_by = Column(BigInteger, comment="创建人")
    updated_by = Column(BigInteger, comment="更新人")
    created_at = Column(Date, default=datetime.now, comment="创建时间")
    updated_at = Column(Date, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关系
    company = relationship("Company", back_populates="certificates")
    
    def __repr__(self):
        return f"<CompanyCertificate(id={self.id}, name='{self.certificate_name}', number='{self.certificate_number}')>"


# 导出所有枚举和模型
__all__ = [
    "CompanyType",
    "CompanyStatus",
    "RiskLevel",
    "Company",
    "CertificateType",
    "CertificateStatus",
    "ReviewStatus",
    "CompanyCertificate",
]