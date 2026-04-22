from sqlalchemy import (
    Column, Integer, String, Date, Enum, Boolean, Text, 
    ForeignKey, DECIMAL, TIMESTAMP, Index, CheckConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum

# 枚举定义
class GenderEnum(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class EmploymentStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"

class PersonnelStatusEnum(str, enum.Enum):
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"

class CertificateStatusEnum(str, enum.Enum):
    VALID = "valid"
    EXPIRED = "expired"
    SUSPENDED = "suspended"
    REVOKED = "revoked"

class ApprovalStatusEnum(str, enum.Enum):
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"

class AlertTypeEnum(str, enum.Enum):
    FIRST_ALERT = "first_alert"
    SECOND_ALERT = "second_alert"
    THIRD_ALERT = "third_alert"

class AlertChannelEnum(str, enum.Enum):
    EMAIL = "email"
    SMS = "sms"
    WECHAT = "wechat"
    SYSTEM = "system"

class Personnel(Base):
    """人员基本信息表"""
    __tablename__ = "personnel"
    
    # 主键和基础字段
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="人员ID")
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, comment="所属单位ID")
    personnel_code = Column(String(50), unique=True, nullable=False, comment="人员编号")
    name = Column(String(100), nullable=False, comment="姓名")
    id_card = Column(String(18), unique=True, nullable=False, comment="身份证号")
    gender = Column(Enum(GenderEnum), nullable=False, default=GenderEnum.MALE, comment="性别")
    birth_date = Column(Date, nullable=True, comment="出生日期")
    phone = Column(String(20), nullable=True, comment="联系电话")
    email = Column(String(100), nullable=True, comment="电子邮箱")
    position = Column(String(100), nullable=True, comment="岗位/职务")
    work_type = Column(String(50), nullable=True, comment="工种/岗位类型")
    hire_date = Column(Date, nullable=True, comment="入职日期")
    employment_status = Column(Enum(EmploymentStatusEnum), nullable=False, default=EmploymentStatusEnum.ACTIVE, comment="在职状态")
    status = Column(Enum(PersonnelStatusEnum), nullable=False, default=PersonnelStatusEnum.PENDING_REVIEW, comment="审核状态")
    photo_url = Column(String(500), nullable=True, comment="照片URL")
    
    # 审计字段
    created_by = Column(String(100), nullable=True, comment="创建人")
    updated_by = Column(String(100), nullable=True, comment="更新人")
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment="创建时间")
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    deleted_at = Column(TIMESTAMP, nullable=True, comment="软删除时间")
    
    # 关系
    company = relationship("Company", back_populates="personnel")
    certificates = relationship("PersonnelCertificate", back_populates="personnel", cascade="all, delete-orphan")
    training_records = relationship("PersonnelTrainingRecord", back_populates="personnel", cascade="all, delete-orphan")
    alert_logs = relationship("PersonnelCertificateAlertLog", back_populates="personnel", cascade="all, delete-orphan")
    
    # 索引
    __table_args__ = (
        Index("idx_personnel_company_id", "company_id"),
        Index("idx_personnel_name", "name"),
        Index("idx_personnel_status", "status"),
        Index("idx_personnel_employment_status", "employment_status"),
        Index("idx_personnel_created_at", "created_at"),
        Index("idx_personnel_deleted_at", "deleted_at"),
        # 检查约束
        CheckConstraint("birth_date <= CURRENT_DATE", name="chk_birth_date"),
        CheckConstraint("hire_date >= birth_date OR hire_date IS NULL OR birth_date IS NULL", name="chk_hire_date")
    )
    
    def __repr__(self):
        return f"<Personnel(id={self.id}, name={self.name}, personnel_code={self.personnel_code})>"


class PersonnelCertificate(Base):
    """人员证书表"""
    __tablename__ = "personnel_certificates"
    
    # 主键和基础字段
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="证书ID")
    personnel_id = Column(Integer, ForeignKey("personnel.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, comment="人员ID")
    certificate_type = Column(String(50), nullable=False, comment="证书类型")
    certificate_name = Column(String(200), nullable=False, comment="证书名称")
    certificate_number = Column(String(100), unique=True, nullable=False, comment="证书编号")
    issuing_authority = Column(String(200), nullable=True, comment="发证机构")
    issue_date = Column(Date, nullable=False, comment="发证日期")
    expiry_date = Column(Date, nullable=False, comment="到期日期")
    certificate_status = Column(Enum(CertificateStatusEnum), nullable=False, default=CertificateStatusEnum.VALID, comment="证书状态")
    approval_status = Column(Enum(ApprovalStatusEnum), nullable=False, default=ApprovalStatusEnum.PENDING_REVIEW, comment="审核状态")
    
    # 文件相关字段
    file_url = Column(String(500), nullable=True, comment="证书扫描件URL")
    file_name = Column(String(200), nullable=True, comment="证书文件名称")
    file_size = Column(Integer, nullable=True, comment="文件大小（字节）")
    
    # 审核相关字段
    review_notes = Column(Text, nullable=True, comment="审核意见")
    reviewed_by = Column(String(100), nullable=True, comment="审核人")
    reviewed_at = Column(TIMESTAMP, nullable=True, comment="审核时间")
    
    # 审计字段
    created_by = Column(String(100), nullable=True, comment="创建人")
    updated_by = Column(String(100), nullable=True, comment="更新人")
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment="创建时间")
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    deleted_at = Column(TIMESTAMP, nullable=True, comment="软删除时间")
    
    # 关系
    personnel = relationship("Personnel", back_populates="certificates")
    alert_logs = relationship("PersonnelCertificateAlertLog", back_populates="certificate", cascade="all, delete-orphan")
    
    # 索引
    __table_args__ = (
        Index("idx_personnel_certificates_personnel_id", "personnel_id"),
        Index("idx_personnel_certificates_expiry_date", "expiry_date"),
        Index("idx_personnel_certificates_certificate_status", "certificate_status"),
        Index("idx_personnel_certificates_approval_status", "approval_status"),
        Index("idx_personnel_certificates_certificate_type", "certificate_type"),
        Index("idx_personnel_certificates_created_at", "created_at"),
        Index("idx_personnel_certificates_deleted_at", "deleted_at"),
        # 检查约束
        CheckConstraint("expiry_date > issue_date", name="chk_expiry_date")
    )
    
    def __repr__(self):
        return f"<PersonnelCertificate(id={self.id}, name={self.certificate_name}, number={self.certificate_number})>"


class PersonnelCertificateAlert(Base):
    """人员证书预警配置表"""
    __tablename__ = "personnel_certificate_alerts"
    
    # 主键和基础字段
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="预警配置ID")
    certificate_type = Column(String(50), nullable=False, comment="证书类型")
    alert_type = Column(Enum(AlertTypeEnum), nullable=False, comment="预警类型")
    days_before = Column(Integer, nullable=False, comment="到期前天数")
    alert_channel = Column(Enum(AlertChannelEnum), nullable=False, default=AlertChannelEnum.SYSTEM, comment="预警渠道")
    alert_template = Column(String(200), nullable=False, comment="预警模板名称")
    is_enabled = Column(Boolean, nullable=False, default=True, comment="是否启用")
    
    # 审计字段
    created_by = Column(String(100), nullable=True, comment="创建人")
    updated_by = Column(String(100), nullable=True, comment="更新人")
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment="创建时间")
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 索引和约束
    __table_args__ = (
        Index("idx_personnel_certificate_alerts_certificate_type", "certificate_type"),
        Index("idx_personnel_certificate_alerts_alert_type", "alert_type"),
        Index("idx_personnel_certificate_alerts_is_enabled", "is_enabled"),
        # 唯一约束：同一证书类型和预警类型配置唯一
        Index("uniq_certificate_type_alert_type", "certificate_type", "alert_type", unique=True)
    )
    
    def __repr__(self):
        return f"<PersonnelCertificateAlert(id={self.id}, type={self.certificate_type}, alert={self.alert_type})>"


class PersonnelCertificateAlertLog(Base):
    """人员证书预警记录表"""
    __tablename__ = "personnel_certificate_alert_logs"
    
    # 主键和基础字段
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="预警记录ID")
    certificate_id = Column(Integer, ForeignKey("personnel_certificates.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, comment="证书ID")
    personnel_id = Column(Integer, ForeignKey("personnel.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, comment="人员ID")
    alert_config_id = Column(Integer, ForeignKey("personnel_certificate_alerts.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, comment="预警配置ID")
    alert_type = Column(Enum(AlertTypeEnum), nullable=False, comment="预警类型")
    alert_date = Column(Date, nullable=False, comment="预警日期")
    expiry_date = Column(Date, nullable=False, comment="证书到期日期")
    days_left = Column(Integer, nullable=False, comment="剩余天数")
    alert_channel = Column(Enum(AlertChannelEnum), nullable=False, comment="预警渠道")
    alert_content = Column(Text, nullable=False, comment="预警内容")
    
    # 发送相关字段
    sent_to = Column(String(200), nullable=True, comment="发送对象（邮箱/手机号等）")
    is_sent = Column(Boolean, nullable=False, default=False, comment="是否已发送")
    sent_at = Column(TIMESTAMP, nullable=True, comment="发送时间")
    
    # 审计字段
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment="创建时间")
    
    # 关系
    certificate = relationship("PersonnelCertificate", back_populates="alert_logs")
    personnel = relationship("Personnel", back_populates="alert_logs")
    alert_config = relationship("PersonnelCertificateAlert")
    
    # 索引
    __table_args__ = (
        Index("idx_personnel_certificate_alert_logs_certificate_id", "certificate_id"),
        Index("idx_personnel_certificate_alert_logs_personnel_id", "personnel_id"),
        Index("idx_personnel_certificate_alert_logs_alert_date", "alert_date"),
        Index("idx_personnel_certificate_alert_logs_expiry_date", "expiry_date"),
        Index("idx_personnel_certificate_alert_logs_is_sent", "is_sent"),
        Index("idx_personnel_certificate_alert_logs_created_at", "created_at"),
    )
    
    def __repr__(self):
        return f"<PersonnelCertificateAlertLog(id={self.id}, certificate_id={self.certificate_id}, alert_type={self.alert_type})>"


class PersonnelTrainingRecord(Base):
    """人员培训记录表"""
    __tablename__ = "personnel_training_records"
    
    # 主键和基础字段
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="培训记录ID")
    personnel_id = Column(Integer, ForeignKey("personnel.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, comment="人员ID")
    training_type = Column(String(50), nullable=False, comment="培训类型")
    training_name = Column(String(200), nullable=False, comment="培训名称")
    training_date = Column(Date, nullable=False, comment="培训日期")
    training_duration = Column(DECIMAL(5, 2), nullable=True, comment="培训时长（小时）")
    training_institution = Column(String(200), nullable=True, comment="培训机构")
    trainer = Column(String(100), nullable=True, comment="培训讲师")
    training_score = Column(DECIMAL(5, 2), nullable=True, comment="培训成绩/分数")
    is_passed = Column(Boolean, nullable=True, comment="是否通过")
    certificate_number = Column(String(100), nullable=True, comment="培训证书编号")
    certificate_url = Column(String(500), nullable=True, comment="培训证书URL")
    notes = Column(Text, nullable=True, comment="备注")
    
    # 审计字段
    created_by = Column(String(100), nullable=True, comment="创建人")
    updated_by = Column(String(100), nullable=True, comment="更新人")
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment="创建时间")
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    deleted_at = Column(TIMESTAMP, nullable=True, comment="软删除时间")
    
    # 关系
    personnel = relationship("Personnel", back_populates="training_records")
    
    # 索引
    __table_args__ = (
        Index("idx_personnel_training_records_personnel_id", "personnel_id"),
        Index("idx_personnel_training_records_training_date", "training_date"),
        Index("idx_personnel_training_records_training_type", "training_type"),
        Index("idx_personnel_training_records_created_at", "created_at"),
        Index("idx_personnel_training_records_deleted_at", "deleted_at"),
    )
    
    def __repr__(self):
        return f"<PersonnelTrainingRecord(id={self.id}, personnel_id={self.personnel_id}, training={self.training_name})>"