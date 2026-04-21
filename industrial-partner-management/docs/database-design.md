# 数据库设计文档

## 数据库概览
- **数据库类型**: MySQL 8.0
- **字符集**: utf8mb4
- **排序规则**: utf8mb4_unicode_ci
- **事务**: 支持事务和行级锁

## 核心表设计

### 1. 单位表 (companies)
存储相关方单位的基本信息
```sql
CREATE TABLE companies (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '单位ID',
    company_code VARCHAR(50) NOT NULL UNIQUE COMMENT '单位编码',
    company_name VARCHAR(200) NOT NULL COMMENT '单位名称',
    company_type ENUM('supplier', 'contractor', 'service_provider', 'other') NOT NULL COMMENT '单位类型',
    legal_person VARCHAR(100) COMMENT '法人代表',
    contact_person VARCHAR(100) NOT NULL COMMENT '联系人',
    contact_phone VARCHAR(20) NOT NULL COMMENT '联系电话',
    contact_email VARCHAR(100) COMMENT '联系邮箱',
    registered_address VARCHAR(500) COMMENT '注册地址',
    business_address VARCHAR(500) COMMENT '经营地址',
    business_scope TEXT COMMENT '经营范围',
    status ENUM('active', 'inactive', 'suspended', 'blacklisted') DEFAULT 'active' COMMENT '状态',
    cooperation_start_date DATE COMMENT '合作开始日期',
    cooperation_end_date DATE COMMENT '合作结束日期',
    risk_level ENUM('low', 'medium', 'high') DEFAULT 'medium' COMMENT '风险等级',
    audit_score DECIMAL(5,2) DEFAULT 0.00 COMMENT '审核评分',
    remarks TEXT COMMENT '备注',
    created_by BIGINT UNSIGNED COMMENT '创建人',
    updated_by BIGINT UNSIGNED COMMENT '更新人',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_company_code (company_code),
    INDEX idx_company_name (company_name),
    INDEX idx_company_type (company_type),
    INDEX idx_status (status),
    INDEX idx_risk_level (risk_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='相关方单位表';
```

### 2. 单位证照表 (company_certificates)
存储单位的各类证照信息
```sql
CREATE TABLE company_certificates (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '证照ID',
    company_id BIGINT UNSIGNED NOT NULL COMMENT '单位ID',
    certificate_type ENUM(
        'business_license',      -- 营业执照
        'safety_production',     -- 安全生产许可证
        'qualification_level',   -- 资质等级证书
        'tax_registration',      -- 税务登记证
        'organization_code',     -- 组织机构代码证
        'other'                  -- 其他证照
    ) NOT NULL COMMENT '证照类型',
    certificate_name VARCHAR(200) NOT NULL COMMENT '证照名称',
    certificate_number VARCHAR(100) NOT NULL COMMENT '证照编号',
    issuing_authority VARCHAR(200) COMMENT '发证机关',
    issue_date DATE COMMENT '发证日期',
    expiry_date DATE NOT NULL COMMENT '有效期至',
    is_long_term BOOLEAN DEFAULT FALSE COMMENT '是否长期有效',
    certificate_status ENUM('valid', 'expired', 'expiring_soon', 'revoked') DEFAULT 'valid' COMMENT '证照状态',
    storage_path VARCHAR(500) COMMENT '证照文件存储路径',
    file_name VARCHAR(200) COMMENT '文件名',
    file_size BIGINT UNSIGNED COMMENT '文件大小(字节)',
    file_md5 VARCHAR(32) COMMENT '文件MD5',
    review_status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending' COMMENT '审核状态',
    review_notes TEXT COMMENT '审核意见',
    reviewed_by BIGINT UNSIGNED COMMENT '审核人',
    reviewed_at TIMESTAMP NULL COMMENT '审核时间',
    created_by BIGINT UNSIGNED COMMENT '创建人',
    updated_by BIGINT UNSIGNED COMMENT '更新人',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_company_id (company_id),
    INDEX idx_certificate_type (certificate_type),
    INDEX idx_expiry_date (expiry_date),
    INDEX idx_certificate_status (certificate_status),
    INDEX idx_review_status (review_status),
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    UNIQUE KEY uk_certificate_number (certificate_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='单位证照表';
```

### 3. 证照预警配置表 (certificate_alerts)
配置证照到期预警规则
```sql
CREATE TABLE certificate_alerts (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '预警ID',
    alert_name VARCHAR(100) NOT NULL COMMENT '预警名称',
    alert_type ENUM('company_certificate', 'person_certificate', 'contract') NOT NULL COMMENT '预警类型',
    days_before_expiry INT NOT NULL COMMENT '到期前天数',
    alert_level ENUM('info', 'warning', 'danger') NOT NULL COMMENT '预警级别',
    notification_methods JSON COMMENT '通知方式配置',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    created_by BIGINT UNSIGNED COMMENT '创建人',
    updated_by BIGINT UNSIGNED COMMENT '更新人',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_alert_type (alert_type),
    INDEX idx_is_active (is_active),
    UNIQUE KEY uk_alert_config (alert_type, days_before_expiry)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='证照预警配置表';
```

### 4. 证照预警记录表 (certificate_alert_logs)
记录证照预警发送历史
```sql
CREATE TABLE certificate_alert_logs (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    certificate_id BIGINT UNSIGNED NOT NULL COMMENT '证照ID',
    certificate_type ENUM('company_certificate', 'person_certificate') NOT NULL COMMENT '证照类型',
    alert_config_id BIGINT UNSIGNED NOT NULL COMMENT '预警配置ID',
    alert_date DATE NOT NULL COMMENT '预警日期',
    expiry_date DATE NOT NULL COMMENT '到期日期',
    days_remaining INT NOT NULL COMMENT '剩余天数',
    alert_level ENUM('info', 'warning', 'danger') NOT NULL COMMENT '预警级别',
    notification_status ENUM('pending', 'sent', 'failed') DEFAULT 'pending' COMMENT '通知状态',
    sent_at TIMESTAMP NULL COMMENT '发送时间',
    recipients JSON COMMENT '接收人列表',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_certificate_id (certificate_id),
    INDEX idx_alert_date (alert_date),
    INDEX idx_notification_status (notification_status),
    FOREIGN KEY (alert_config_id) REFERENCES certificate_alerts(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='证照预警记录表';
```

### 5. 文件存储表 (file_storage)
统一管理所有上传的文件
```sql
CREATE TABLE file_storage (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '文件ID',
    file_name VARCHAR(255) NOT NULL COMMENT '文件名',
    original_name VARCHAR(255) NOT NULL COMMENT '原始文件名',
    file_type VARCHAR(100) NOT NULL COMMENT '文件类型',
    file_size BIGINT UNSIGNED NOT NULL COMMENT '文件大小(字节)',
    file_md5 VARCHAR(32) NOT NULL UNIQUE COMMENT '文件MD5',
    storage_path VARCHAR(500) NOT NULL COMMENT '存储路径',
    storage_type ENUM('local', 's3', 'oss', 'cos') DEFAULT 'local' COMMENT '存储类型',
    bucket_name VARCHAR(100) COMMENT '存储桶名称',
    object_key VARCHAR(500) COMMENT '对象键',
    mime_type VARCHAR(100) COMMENT 'MIME类型',
    is_encrypted BOOLEAN DEFAULT FALSE COMMENT '是否加密',
    encryption_key VARCHAR(100) COMMENT '加密密钥',
    access_level ENUM('public', 'private', 'protected') DEFAULT 'private' COMMENT '访问级别',
    uploader_id BIGINT UNSIGNED NOT NULL COMMENT '上传人',
    related_table VARCHAR(50) COMMENT '关联表名',
    related_id BIGINT UNSIGNED COMMENT '关联记录ID',
    download_count INT DEFAULT 0 COMMENT '下载次数',
    view_count INT DEFAULT 0 COMMENT '查看次数',
    is_deleted BOOLEAN DEFAULT FALSE COMMENT '是否删除',
    deleted_at TIMESTAMP NULL COMMENT '删除时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_file_md5 (file_md5),
    INDEX idx_uploader_id (uploader_id),
    INDEX idx_related_record (related_table, related_id),
    INDEX idx_is_deleted (is_deleted),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文件存储表';
```

## 索引设计原则
1. 主键使用自增BIGINT UNSIGNED
2. 频繁查询的字段建立索引
3. 外键字段建立索引
4. 状态字段建立索引
5. 时间范围查询字段建立索引

## 数据完整性约束
1. 所有表都有created_at和updated_at时间戳
2. 重要业务数据有软删除标记
3. 外键约束确保数据一致性
4. 唯一约束防止重复数据
5. 枚举类型限制数据范围