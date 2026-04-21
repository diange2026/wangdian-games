-- 工贸企业相关方全流程管理系统数据库初始化脚本
-- 版本: 1.0.0
-- 创建时间: 2026-04-21

-- 创建数据库
CREATE DATABASE IF NOT EXISTS `industrial_partner_management`
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE `industrial_partner_management`;

-- 设置SQL模式
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================
-- 1. 单位表 (companies)
-- ============================================
CREATE TABLE IF NOT EXISTS `companies` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '单位ID',
    `company_code` VARCHAR(50) NOT NULL UNIQUE COMMENT '单位编码',
    `company_name` VARCHAR(200) NOT NULL COMMENT '单位名称',
    `company_type` ENUM('supplier', 'contractor', 'service_provider', 'other') NOT NULL COMMENT '单位类型',
    `legal_person` VARCHAR(100) COMMENT '法人代表',
    `contact_person` VARCHAR(100) NOT NULL COMMENT '联系人',
    `contact_phone` VARCHAR(20) NOT NULL COMMENT '联系电话',
    `contact_email` VARCHAR(100) COMMENT '联系邮箱',
    `registered_address` VARCHAR(500) COMMENT '注册地址',
    `business_address` VARCHAR(500) COMMENT '经营地址',
    `business_scope` TEXT COMMENT '经营范围',
    `status` ENUM('active', 'inactive', 'suspended', 'blacklisted') DEFAULT 'active' COMMENT '状态',
    `cooperation_start_date` DATE COMMENT '合作开始日期',
    `cooperation_end_date` DATE COMMENT '合作结束日期',
    `risk_level` ENUM('low', 'medium', 'high') DEFAULT 'medium' COMMENT '风险等级',
    `audit_score` DECIMAL(5,2) DEFAULT 0.00 COMMENT '审核评分',
    `remarks` TEXT COMMENT '备注',
    `created_by` BIGINT UNSIGNED COMMENT '创建人',
    `updated_by` BIGINT UNSIGNED COMMENT '更新人',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_company_code` (`company_code`),
    INDEX `idx_company_name` (`company_name`),
    INDEX `idx_company_type` (`company_type`),
    INDEX `idx_status` (`status`),
    INDEX `idx_risk_level` (`risk_level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='相关方单位表';

-- ============================================
-- 2. 单位证照表 (company_certificates)
-- ============================================
CREATE TABLE IF NOT EXISTS `company_certificates` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '证照ID',
    `company_id` BIGINT UNSIGNED NOT NULL COMMENT '单位ID',
    `certificate_type` ENUM(
        'business_license',      -- 营业执照
        'safety_production',     -- 安全生产许可证
        'qualification_level',   -- 资质等级证书
        'tax_registration',      -- 税务登记证
        'organization_code',     -- 组织机构代码证
        'other'                  -- 其他证照
    ) NOT NULL COMMENT '证照类型',
    `certificate_name` VARCHAR(200) NOT NULL COMMENT '证照名称',
    `certificate_number` VARCHAR(100) NOT NULL COMMENT '证照编号',
    `issuing_authority` VARCHAR(200) COMMENT '发证机关',
    `issue_date` DATE COMMENT '发证日期',
    `expiry_date` DATE NOT NULL COMMENT '有效期至',
    `is_long_term` BOOLEAN DEFAULT FALSE COMMENT '是否长期有效',
    `certificate_status` ENUM('valid', 'expired', 'expiring_soon', 'revoked') DEFAULT 'valid' COMMENT '证照状态',
    `storage_path` VARCHAR(500) COMMENT '证照文件存储路径',
    `file_name` VARCHAR(200) COMMENT '文件名',
    `file_size` BIGINT UNSIGNED COMMENT '文件大小(字节)',
    `file_md5` VARCHAR(32) COMMENT '文件MD5',
    `review_status` ENUM('pending', 'approved', 'rejected') DEFAULT 'pending' COMMENT '审核状态',
    `review_notes` TEXT COMMENT '审核意见',
    `reviewed_by` BIGINT UNSIGNED COMMENT '审核人',
    `reviewed_at` TIMESTAMP NULL COMMENT '审核时间',
    `created_by` BIGINT UNSIGNED COMMENT '创建人',
    `updated_by` BIGINT UNSIGNED COMMENT '更新人',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_company_id` (`company_id`),
    INDEX `idx_certificate_type` (`certificate_type`),
    INDEX `idx_expiry_date` (`expiry_date`),
    INDEX `idx_certificate_status` (`certificate_status`),
    INDEX `idx_review_status` (`review_status`),
    FOREIGN KEY (`company_id`) REFERENCES `companies`(`id`) ON DELETE CASCADE,
    UNIQUE KEY `uk_certificate_number` (`certificate_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='单位证照表';

-- ============================================
-- 3. 证照预警配置表 (certificate_alerts)
-- ============================================
CREATE TABLE IF NOT EXISTS `certificate_alerts` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '预警ID',
    `alert_name` VARCHAR(100) NOT NULL COMMENT '预警名称',
    `alert_type` ENUM('company_certificate', 'person_certificate', 'contract') NOT NULL COMMENT '预警类型',
    `days_before_expiry` INT NOT NULL COMMENT '到期前天数',
    `alert_level` ENUM('info', 'warning', 'danger') NOT NULL COMMENT '预警级别',
    `notification_methods` JSON COMMENT '通知方式配置',
    `is_active` BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    `created_by` BIGINT UNSIGNED COMMENT '创建人',
    `updated_by` BIGINT UNSIGNED COMMENT '更新人',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_alert_type` (`alert_type`),
    INDEX `idx_is_active` (`is_active`),
    UNIQUE KEY `uk_alert_config` (`alert_type`, `days_before_expiry`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='证照预警配置表';

-- ============================================
-- 4. 证照预警记录表 (certificate_alert_logs)
-- ============================================
CREATE TABLE IF NOT EXISTS `certificate_alert_logs` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    `certificate_id` BIGINT UNSIGNED NOT NULL COMMENT '证照ID',
    `certificate_type` ENUM('company_certificate', 'person_certificate') NOT NULL COMMENT '证照类型',
    `alert_config_id` BIGINT UNSIGNED NOT NULL COMMENT '预警配置ID',
    `alert_date` DATE NOT NULL COMMENT '预警日期',
    `expiry_date` DATE NOT NULL COMMENT '到期日期',
    `days_remaining` INT NOT NULL COMMENT '剩余天数',
    `alert_level` ENUM('info', 'warning', 'danger') NOT NULL COMMENT '预警级别',
    `notification_status` ENUM('pending', 'sent', 'failed') DEFAULT 'pending' COMMENT '通知状态',
    `sent_at` TIMESTAMP NULL COMMENT '发送时间',
    `recipients` JSON COMMENT '接收人列表',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX `idx_certificate_id` (`certificate_id`),
    INDEX `idx_alert_date` (`alert_date`),
    INDEX `idx_notification_status` (`notification_status`),
    FOREIGN KEY (`alert_config_id`) REFERENCES `certificate_alerts`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='证照预警记录表';

-- ============================================
-- 5. 文件存储表 (file_storage)
-- ============================================
CREATE TABLE IF NOT EXISTS `file_storage` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '文件ID',
    `file_name` VARCHAR(255) NOT NULL COMMENT '文件名',
    `original_name` VARCHAR(255) NOT NULL COMMENT '原始文件名',
    `file_type` VARCHAR(100) NOT NULL COMMENT '文件类型',
    `file_size` BIGINT UNSIGNED NOT NULL COMMENT '文件大小(字节)',
    `file_md5` VARCHAR(32) NOT NULL UNIQUE COMMENT '文件MD5',
    `storage_path` VARCHAR(500) NOT NULL COMMENT '存储路径',
    `storage_type` ENUM('local', 's3', 'oss', 'cos') DEFAULT 'local' COMMENT '存储类型',
    `bucket_name` VARCHAR(100) COMMENT '存储桶名称',
    `object_key` VARCHAR(500) COMMENT '对象键',
    `mime_type` VARCHAR(100) COMMENT 'MIME类型',
    `is_encrypted` BOOLEAN DEFAULT FALSE COMMENT '是否加密',
    `encryption_key` VARCHAR(100) COMMENT '加密密钥',
    `access_level` ENUM('public', 'private', 'protected') DEFAULT 'private' COMMENT '访问级别',
    `uploader_id` BIGINT UNSIGNED NOT NULL COMMENT '上传人',
    `related_table` VARCHAR(50) COMMENT '关联表名',
    `related_id` BIGINT UNSIGNED COMMENT '关联记录ID',
    `download_count` INT DEFAULT 0 COMMENT '下载次数',
    `view_count` INT DEFAULT 0 COMMENT '查看次数',
    `is_deleted` BOOLEAN DEFAULT FALSE COMMENT '是否删除',
    `deleted_at` TIMESTAMP NULL COMMENT '删除时间',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_file_md5` (`file_md5`),
    INDEX `idx_uploader_id` (`uploader_id`),
    INDEX `idx_related_record` (`related_table`, `related_id`),
    INDEX `idx_is_deleted` (`is_deleted`),
    INDEX `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文件存储表';

-- ============================================
-- 6. 插入默认预警配置数据
-- ============================================
INSERT INTO `certificate_alerts` 
    (`alert_name`, `alert_type`, `days_before_expiry`, `alert_level`, `notification_methods`, `is_active`) 
VALUES
    ('单位证照30天预警', 'company_certificate', 30, 'info', '["email", "system_message"]', TRUE),
    ('单位证照15天预警', 'company_certificate', 15, 'warning', '["email", "system_message", "sms"]', TRUE),
    ('单位证照7天预警', 'company_certificate', 7, 'danger', '["email", "system_message", "sms", "wechat"]', TRUE),
    ('人员证书30天预警', 'person_certificate', 30, 'info', '["email", "system_message"]', TRUE),
    ('人员证书15天预警', 'person_certificate', 15, 'warning', '["email", "system_message", "sms"]', TRUE),
    ('人员证书7天预警', 'person_certificate', 7, 'danger', '["email", "system_message", "sms", "wechat"]', TRUE),
    ('合同到期30天预警', 'contract', 30, 'info', '["email", "system_message"]', TRUE),
    ('合同到期15天预警', 'contract', 15, 'warning', '["email", "system_message", "sms"]', TRUE),
    ('合同到期7天预警', 'contract', 7, 'danger', '["email", "system_message", "sms", "wechat"]', TRUE);

-- ============================================
-- 7. 插入测试单位数据
-- ============================================
INSERT INTO `companies` 
    (`company_code`, `company_name`, `company_type`, `legal_person`, `contact_person`, `contact_phone`, `contact_email`, `status`, `risk_level`) 
VALUES
    ('COMP2024001', '上海建工集团有限公司', 'contractor', '张三', '李四', '13800138001', 'contact@shjg.com', 'active', 'low'),
    ('COMP2024002', '北京安全技术服务有限公司', 'service_provider', '王五', '赵六', '13900139001', 'service@bjsafety.com', 'active', 'medium'),
    ('COMP2024003', '广州设备供应有限公司', 'supplier', '孙七', '周八', '13700137001', 'sales@gzequip.com', 'active', 'low'),
    ('COMP2024004', '深圳电力工程有限公司', 'contractor', '吴九', '郑十', '13600136001', 'info@szpower.com', 'suspended', 'high'),
    ('COMP2024005', '南京环保科技股份有限公司', 'service_provider', '钱十一', '孙十二', '13500135001', 'tech@njep.com', 'active', 'medium');

-- ============================================
-- 8. 插入测试证照数据
-- ============================================
INSERT INTO `company_certificates` 
    (`company_id`, `certificate_type`, `certificate_name`, `certificate_number`, `issuing_authority`, `issue_date`, `expiry_date`, `certificate_status`, `review_status`) 
VALUES
    (1, 'business_license', '营业执照', '913101015555555555', '上海市市场监督管理局', '2023-01-15', '2028-01-14', 'valid', 'approved'),
    (1, 'safety_production', '安全生产许可证', '(沪)JZ安许证字[2023]000001', '上海市应急管理局', '2023-03-20', '2026-03-19', 'valid', 'approved'),
    (2, 'business_license', '营业执照', '911101085555555555', '北京市市场监督管理局', '2022-05-10', '2027-05-09', 'valid', 'approved'),
    (2, 'qualification_level', '安全技术服务资质证书', 'AQFW2023001', '国家应急管理部', '2023-02-28', '2025-02-27', 'expiring_soon', 'approved'),
    (3, 'business_license', '营业执照', '914401015555555555', '广州市市场监督管理局', '2023-06-01', '2028-05-31', 'valid', 'pending'),
    (4, 'safety_production', '安全生产许可证', '(粤)JZ安许证字[2022]000123', '广东省应急管理厅', '2022-08-15', '2024-08-14', 'expired', 'rejected');

-- 恢复外键检查
SET FOREIGN_KEY_CHECKS = 1;

-- ============================================
-- 9. 创建数据库用户和权限
-- ============================================
-- 创建只读用户（用于报表查询）
CREATE USER IF NOT EXISTS 'partner_readonly'@'%' IDENTIFIED BY 'Readonly@2024';
GRANT SELECT ON `industrial_partner_management`.* TO 'partner_readonly'@'%';

-- 创建应用用户（用于业务操作）
CREATE USER IF NOT EXISTS 'partner_app'@'%' IDENTIFIED BY 'AppPassword@2024';
GRANT SELECT, INSERT, UPDATE, DELETE ON `industrial_partner_management`.* TO 'partner_app'@'%';

-- 刷新权限
FLUSH PRIVILEGES;

-- ============================================
-- 10. 查看数据库创建结果
-- ============================================
SHOW TABLES;

SELECT 
    TABLE_NAME,
    TABLE_ROWS,
    AVG_ROW_LENGTH,
    DATA_LENGTH,
    INDEX_LENGTH,
    (DATA_LENGTH + INDEX_LENGTH) AS TOTAL_SIZE,
    TABLE_COLLATION
FROM 
    information_schema.TABLES 
WHERE 
    TABLE_SCHEMA = 'industrial_partner_management'
ORDER BY 
    TABLE_NAME;

-- 查看预警配置
SELECT * FROM `certificate_alerts` ORDER BY `alert_type`, `days_before_expiry`;

-- 查看测试数据统计
SELECT 
    'companies' AS table_name,
    COUNT(*) AS record_count
FROM `companies`
UNION ALL
SELECT 
    'company_certificates',
    COUNT(*)
FROM `company_certificates`
UNION ALL
SELECT 
    'certificate_alerts',
    COUNT(*)
FROM `certificate_alerts`;

-- 输出初始化完成信息
SELECT '数据库初始化完成！' AS message;