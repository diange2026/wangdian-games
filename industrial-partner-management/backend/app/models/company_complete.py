#!/usr/bin/env python3
"""
完整单位资质管理模块 - 数据模型
企业级单位资质全生命周期管理系统
"""

from datetime import date, datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import (
    Column, String, Integer, BigInteger, DECIMAL, Text,
    Date, DateTime, Boolean, Enum, ForeignKey, JSON, Text
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import BIGINT, DECIMAL

from app.db.base_class import Base
from app.models.mixins import AuditMixin, SoftDeleteMixin


class CompanyComplete(Base, AuditMixin, SoftDeleteMixin):
    """
    单位完整信息模型
    包含单位所有维度的信息，支持全方位资质管理
    """
    __tablename__ = "company_complete"
    
    # 主键与编码系统
    id = Column(BIGINT(unsigned=True), primary_key=True, index=True, autoincrement=True,
               comment='单位ID，主键')
    company_code = Column(String(50), unique=True, index=True, nullable=False,
                          comment='单位编码，唯一标识')
    
    # 单位基本信息
    company_name = Column(String(200), nullable=False, comment='单位全称')
    company_short_name = Column(String(100), comment='单位简称')
    
    # 单位类型与性质
    company_type = Column(
        Enum('supplier', 'contractor', 'service_provider', 'partner', 'other'),
        nullable=False, comment='单位类型'
    )
    business_nature = Column(
        Enum('state_owned', 'private', 'foreign_invested', 'joint_venture'),
        comment='企业性质'
    )
    
    # 注册与资本信息
    registration_capital = Column(
        DECIMAL(18, 2), comment='注册资本（万元）'
    )
    actual_capital = Column(
        DECIMAL(18, 2), comment='实缴资本（万元）'
    )
    
    # 地址信息
    registered_address = Column(String(500), nullable=False,
                            comment='注册地址（与工商登记一致）')
    business_address = Column(String(500), comment='经营地址')
    production_address = Column(String(500), comment='生产地址')
    
    # 法人信息
    legal_person = Column(String(100), nullable=False, comment='法定代表人')
    legal_person_id_card = Column(String(20), comment='法人身份证号')
    legal_person_phone = Column(String(20), comment='法人联系电话')
    
    # 信用信息
    credit_code = Column(String(30), unique=True, index=True,
                       comment='统一社会信用代码')
    registration_authority = Column(String(200), comment='登记机关')
    registration_date = Column(Date, comment='登记日期')
    
    # 经营范围
    business_scope = Column(Text, comment='经营范围（按工商登记）')
    
    # 联系信息
    contact_person = Column(String(100), nullable=False, comment='联系人')
    contact_phone = Column(String(20), nullable=False, comment='联系电话')
    contact_email = Column(String(100), comment='联系邮箱')
    website = Column(String(200), comment='官方网站')
    
    # 财务信息
    financial_contact = Column(String(100), comment='财务联系人')
    financial_phone = Column(String(20), comment='财务电话')
    
    # 技术信息
    technical_contact = Column(String(100), comment='技术联系人')
    technical_phone = Column(String(20), comment='技术电话')
    
    # 资质与证照信息
    qualification_level = Column(
        Enum('AAA', 'AA', 'A', 'B', 'C', 'other'),
        comment='资质等级'
    )
    qualification_category = Column(String(100), comment='资质类别')
    qualification_cert_no = Column(String(50), comment='资质证书编号')
    
    # 经营状态
    business_status = Column(
        Enum('operating', 'suspended', 'cancelled', 'bankrupt'),
        default='operating', comment='经营状态'
    )
    
    # 合作信息
    cooperation_level = Column(
        Enum('strategic', 'key', 'regular', 'trial'),
        comment='合作级别'
    )
    cooperation_start_date = Column(Date, comment='合作开始日期')
    cooperation_end_date = Column(Date, comment='合作结束日期')
    
    # 风险信息
    risk_level = Column(
        Enum('low', 'medium', 'high', 'critical'),
        default='medium', comment='风险等级'
    )
    risk_score = Column(DECIMAL(5, 2), default=50.00, comment='风险评分')
    risk_indicators = Column(Text, comment='风险指标（JSON数组）')
    
    # 审核信息
    approval_status = Column(
        Enum('pending', 'approved', 'rejected', 'in_review', 'pending_correction'),
        default='pending', comment='审批状态'
    )
    approval_date = Column(DateTime, comment='审批日期')
    approval_user_id = Column(BIGINT(unsigned=True), comment='审批人ID')
    
    # 审计信息
    version = Column(Integer, default=1, comment='数据版本')
    is_valid = Column(Boolean, default=True, comment='是否有效')
    
    # 关联关系
    certificates = relationship(
        "CompanyCertificateComplete",
        backref=backref("company", lazy="joined"),
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    def __repr__(self) -> str:
        return f"<CompanyComplete(id={self.id}, code={self.company_code}, name={self.company_name})>"


class CompanyCertificateComplete(Base, AuditMixin, SoftDeleteMixin):
    """
    单位完整资质证照模型
    管理所有类型的证照，支持全生命周期追踪
    """
    __tablename__ = "company_certificate_complete"
    
    # 主键
    id = Column(BIGINT(unsigned=True), primary_key=True, index=True, autoincrement=True,
               comment='证照ID')
    company_id = Column(
        BIGINT(unsigned=True),
        ForeignKey('company_complete.id', ondelete='CASCADE'),
        nullable=False,
        comment='单位ID'
    )
    
    # 证照基本信息
    certificate_type = Column(
        Enum('business_license', 'tax_certificate', 'safety_license', 'environment_protection', 'other'),
        nullable=False,
        comment='证照类型'
    )
    certificate_name = Column(String(200), nullable=False, comment='证照名称')
    certificate_number = Column(String(100), nullable=False, comment='证照编号')
    
    # 发证信息
    issuing_authority = Column(String(200), nullable=False, comment='发证机关')
    issue_date = Column(Date, nullable=False, comment='发证日期')
    expiry_date = Column(Date, nullable=False, comment='到期日期')
    
    # 证照状态
    certificate_status = Column(
        Enum('valid', 'expired', 'suspended', 'revoked', 'in_review'),
        default='valid',
        comment='证照状态'
    )
    
    # 续期管理
    renewal_status = Column(
        Enum('not_required', 'pending', 'submitted', 'approved', 'rejected'),
        default='not_required',
        comment='续期状态'
    )
    renewal_submitted_at = Column(DateTime, comment='续期申请提交时间')
    renewal_reviewed_at = Column(DateTime, comment='续期审批时间')
    
    # 文件信息
    file_url = Column(String(500), comment='证照文件URL')
    file_name = Column(String(200), comment='文件名')
    file_size = Column(Integer, comment='文件大小（字节）')
    file_hash = Column(String(64), comment='文件哈希（SHA-256）'
    
    # 版本信息
    version = Column(Integer, default=1, comment='证照版本')
    
    # 关联关系
    __table_args__ = (
        # 添加复合索引
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}
    )
    
    def __repr__(self) -> str:
        return f"<CompanyCertificateComplete(id={self.id}, type={self.certificate_type})>"


class CompanyAuditLog(Base):
    """
    单位审计日志模型
    记录所有关键操作的完整审计轨迹
    """
    __tablename__ = "company_audit_log"
    
    # 主键
    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True,
               comment='审计日志ID')
    
    # 审计目标
    company_id = Column(
        BIGINT(unsigned=True), comment='单位ID'
    )
    company_code = Column(String(50), comment='单位编码')
    
    # 操作信息
    user_id = Column(BIGINT(unsigned=True), comment='操作人ID')
    user_name = Column(String(100), comment='操作人姓名')
    action = Column(
        Enum('create', 'update', 'delete', 'approve', 'reject', 'renew', 'suspend'),
        comment='操作类型'
    )
    
    # 变更详情
    old_data = Column(JSON, comment='变更前数据（JSON格式）')
    new_data = Column(JSON, comment='变更后数据（JSON格式）")
    diff = Column(Text, comment='数据差异详情（JSON格式）")
    
    # 时间戳
    created_at = Column(DateTime, server_default=func.now(),
                       comment='操作时间')
    
    def __repr__(self) -> str:
        return f"<CompanyAuditLog(id={self.id}, action={self.action}, company={self.company_code})>"