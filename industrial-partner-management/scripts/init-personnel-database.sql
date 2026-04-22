-- 工贸企业相关方全流程管理系统 - 人员资质管理模块数据库初始化脚本
-- 创建时间: 2026-04-22
-- 说明: 此脚本创建人员资质管理相关的表结构和初始化数据

-- 使用数据库
USE industrial_partner_management;

-- ====================================================================
-- 1. 创建 personnel 表 - 人员基本信息表
-- ====================================================================
CREATE TABLE IF NOT EXISTS personnel (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '人员ID，主键',
    company_id BIGINT UNSIGNED NOT NULL COMMENT '所属单位ID',
    personnel_code VARCHAR(50) NOT NULL COMMENT '人员编号，唯一标识',
    name VARCHAR(100) NOT NULL COMMENT '姓名',
    id_card VARCHAR(18) NOT NULL COMMENT '身份证号，唯一',
    gender ENUM('male', 'female', 'other') NOT NULL DEFAULT 'male' COMMENT '性别',
    birth_date DATE NULL COMMENT '出生日期',
    phone VARCHAR(20) NULL COMMENT '联系电话',
    email VARCHAR(100) NULL COMMENT '电子邮箱',
    position VARCHAR(100) NULL COMMENT '岗位/职务',
    work_type VARCHAR(50) NULL COMMENT '工种/岗位类型',
    hire_date DATE NULL COMMENT '入职日期',
    employment_status ENUM('active', 'inactive', 'suspended', 'terminated') NOT NULL DEFAULT 'active' COMMENT '在职状态',
    status ENUM('pending_review', 'approved', 'rejected', 'expired') NOT NULL DEFAULT 'pending_review' COMMENT '审核状态',
    photo_url VARCHAR(500) NULL COMMENT '照片URL',
    created_by VARCHAR(100) NULL COMMENT '创建人',
    updated_by VARCHAR(100) NULL COMMENT '更新人',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted_at TIMESTAMP NULL COMMENT '软删除时间',
    
    PRIMARY KEY (id),
    UNIQUE KEY uk_personnel_code (personnel_code),
    UNIQUE KEY uk_id_card (id_card),
    KEY idx_company_id (company_id),
    KEY idx_name (name),
    KEY idx_status (status),
    KEY idx_employment_status (employment_status),
    KEY idx_created_at (created_at),
    KEY idx_deleted_at (deleted_at),
    
    CONSTRAINT fk_personnel_company FOREIGN KEY (company_id) 
        REFERENCES companies (id) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE,
    
    CONSTRAINT chk_birth_date CHECK (birth_date <= CURRENT_DATE),
    CONSTRAINT chk_hire_date CHECK (hire_date >= birth_date OR hire_date IS NULL OR birth_date IS NULL)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='人员基本信息表';

-- ====================================================================
-- 2. 创建 personnel_certificates 表 - 人员证书表
-- ====================================================================
CREATE TABLE IF NOT EXISTS personnel_certificates (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '证书ID，主键',
    personnel_id BIGINT UNSIGNED NOT NULL COMMENT '人员ID',
    certificate_type VARCHAR(50) NOT NULL COMMENT '证书类型',
    certificate_name VARCHAR(200) NOT NULL COMMENT '证书名称',
    certificate_number VARCHAR(100) NOT NULL COMMENT '证书编号',
    issuing_authority VARCHAR(200) NULL COMMENT '发证机构',
    issue_date DATE NOT NULL COMMENT '发证日期',
    expiry_date DATE NOT NULL COMMENT '到期日期',
    certificate_status ENUM('valid', 'expired', 'suspended', 'revoked') NOT NULL DEFAULT 'valid' COMMENT '证书状态',
    approval_status ENUM('pending_review', 'approved', 'rejected') NOT NULL DEFAULT 'pending_review' COMMENT '审核状态',
    file_url VARCHAR(500) NULL COMMENT '证书扫描件URL',
    file_name VARCHAR(200) NULL COMMENT '证书文件名称',
    file_size INT NULL COMMENT '文件大小（字节）',
    review_notes TEXT NULL COMMENT '审核意见',
    reviewed_by VARCHAR(100) NULL COMMENT '审核人',
    reviewed_at TIMESTAMP NULL COMMENT '审核时间',
    created_by VARCHAR(100) NULL COMMENT '创建人',
    updated_by VARCHAR(100) NULL COMMENT '更新人',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted_at TIMESTAMP NULL COMMENT '软删除时间',
    
    PRIMARY KEY (id),
    UNIQUE KEY uk_certificate_number (certificate_number),
    KEY idx_personnel_id (personnel_id),
    KEY idx_expiry_date (expiry_date),
    KEY idx_certificate_status (certificate_status),
    KEY idx_approval_status (approval_status),
    KEY idx_certificate_type (certificate_type),
    KEY idx_created_at (created_at),
    KEY idx_deleted_at (deleted_at),
    
    CONSTRAINT fk_personnel_certificates_personnel FOREIGN KEY (personnel_id) 
        REFERENCES personnel (id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    
    CONSTRAINT chk_expiry_date CHECK (expiry_date > issue_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='人员证书表';

-- ====================================================================
-- 3. 创建 personnel_certificate_alerts 表 - 人员证书预警配置表
-- ====================================================================
CREATE TABLE IF NOT EXISTS personnel_certificate_alerts (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '预警配置ID',
    certificate_type VARCHAR(50) NOT NULL COMMENT '证书类型',
    alert_type ENUM('first_alert', 'second_alert', 'third_alert') NOT NULL COMMENT '预警类型',
    days_before INT NOT NULL COMMENT '到期前天数',
    alert_channel ENUM('email', 'sms', 'wechat', 'system') NOT NULL DEFAULT 'system' COMMENT '预警渠道',
    alert_template VARCHAR(200) NOT NULL COMMENT '预警模板名称',
    is_enabled BOOLEAN NOT NULL DEFAULT TRUE COMMENT '是否启用',
    created_by VARCHAR(100) NULL COMMENT '创建人',
    updated_by VARCHAR(100) NULL COMMENT '更新人',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    PRIMARY KEY (id),
    UNIQUE KEY uk_certificate_type_alert_type (certificate_type, alert_type),
    KEY idx_certificate_type (certificate_type),
    KEY idx_alert_type (alert_type),
    KEY idx_is_enabled (is_enabled)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='人员证书预警配置表';

-- ====================================================================
-- 4. 创建 personnel_certificate_alert_logs 表 - 人员证书预警记录表
-- ====================================================================
CREATE TABLE IF NOT EXISTS personnel_certificate_alert_logs (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '预警记录ID',
    certificate_id BIGINT UNSIGNED NOT NULL COMMENT '证书ID',
    personnel_id BIGINT UNSIGNED NOT NULL COMMENT '人员ID',
    alert_config_id BIGINT UNSIGNED NOT NULL COMMENT '预警配置ID',
    alert_type ENUM('first_alert', 'second_alert', 'third_alert') NOT NULL COMMENT '预警类型',
    alert_date DATE NOT NULL COMMENT '预警日期',
    expiry_date DATE NOT NULL COMMENT '证书到期日期',
    days_left INT NOT NULL COMMENT '剩余天数',
    alert_channel ENUM('email', 'sms', 'wechat', 'system') NOT NULL COMMENT '预警渠道',
    alert_content TEXT NOT NULL COMMENT '预警内容',
    sent_to VARCHAR(200) NULL COMMENT '发送对象（邮箱/手机号等）',
    is_sent BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否已发送',
    sent_at TIMESTAMP NULL COMMENT '发送时间',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    
    PRIMARY KEY (id),
    KEY idx_certificate_id (certificate_id),
    KEY idx_personnel_id (personnel_id),
    KEY idx_alert_date (alert_date),
    KEY idx_expiry_date (expiry_date),
    KEY idx_is_sent (is_sent),
    KEY idx_created_at (created_at),
    
    CONSTRAINT fk_alert_logs_certificate FOREIGN KEY (certificate_id) 
        REFERENCES personnel_certificates (id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    
    CONSTRAINT fk_alert_logs_personnel FOREIGN KEY (personnel_id) 
        REFERENCES personnel (id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    
    CONSTRAINT fk_alert_logs_alert_config FOREIGN KEY (alert_config_id) 
        REFERENCES personnel_certificate_alerts (id) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='人员证书预警记录表';

-- ====================================================================
-- 5. 创建 personnel_training_records 表 - 人员培训记录表
-- ====================================================================
CREATE TABLE IF NOT EXISTS personnel_training_records (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '培训记录ID',
    personnel_id BIGINT UNSIGNED NOT NULL COMMENT '人员ID',
    training_type VARCHAR(50) NOT NULL COMMENT '培训类型',
    training_name VARCHAR(200) NOT NULL COMMENT '培训名称',
    training_date DATE NOT NULL COMMENT '培训日期',
    training_duration DECIMAL(5,2) NULL COMMENT '培训时长（小时）',
    training_institution VARCHAR(200) NULL COMMENT '培训机构',
    trainer VARCHAR(100) NULL COMMENT '培训讲师',
    training_score DECIMAL(5,2) NULL COMMENT '培训成绩/分数',
    is_passed BOOLEAN NULL COMMENT '是否通过',
    certificate_number VARCHAR(100) NULL COMMENT '培训证书编号',
    certificate_url VARCHAR(500) NULL COMMENT '培训证书URL',
    notes TEXT NULL COMMENT '备注',
    created_by VARCHAR(100) NULL COMMENT '创建人',
    updated_by VARCHAR(100) NULL COMMENT '更新人',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted_at TIMESTAMP NULL COMMENT '软删除时间',
    
    PRIMARY KEY (id),
    KEY idx_personnel_id (personnel_id),
    KEY idx_training_date (training_date),
    KEY idx_training_type (training_type),
    KEY idx_created_at (created_at),
    KEY idx_deleted_at (deleted_at),
    
    CONSTRAINT fk_training_records_personnel FOREIGN KEY (personnel_id) 
        REFERENCES personnel (id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='人员培训记录表';

-- ====================================================================
-- 6. 插入默认预警配置数据
-- ====================================================================
-- 特种作业证预警配置
INSERT INTO personnel_certificate_alerts (certificate_type, alert_type, days_before, alert_channel, alert_template, is_enabled) VALUES
('特种作业证', 'first_alert', 30, 'system', 'special_operation_first_alert', TRUE),
('特种作业证', 'second_alert', 15, 'system', 'special_operation_second_alert', TRUE),
('特种作业证', 'third_alert', 7, 'system', 'special_operation_third_alert', TRUE);

-- 职业资格证预警配置
INSERT INTO personnel_certificate_alerts (certificate_type, alert_type, days_before, alert_channel, alert_template, is_enabled) VALUES
('职业资格证', 'first_alert', 30, 'system', 'professional_qualification_first_alert', TRUE),
('职业资格证', 'second_alert', 15, 'system', 'professional_qualification_second_alert', TRUE),
('职业资格证', 'third_alert', 7, 'system', 'professional_qualification_third_alert', TRUE);

-- 安全培训证预警配置
INSERT INTO personnel_certificate_alerts (certificate_type, alert_type, days_before, alert_channel, alert_template, is_enabled) VALUES
('安全培训证', 'first_alert', 30, 'system', 'safety_training_first_alert', TRUE),
('安全培训证', 'second_alert', 15, 'system', 'safety_training_second_alert', TRUE),
('安全培训证', 'third_alert', 7, 'system', 'safety_training_third_alert', TRUE);

-- ====================================================================
-- 7. 插入测试数据 - 人员信息
-- ====================================================================
-- 假设已存在单位ID为1-5的单位
INSERT INTO personnel (company_id, personnel_code, name, id_card, gender, birth_date, phone, email, position, work_type, hire_date, employment_status, status) VALUES
-- 单位1（建筑公司）的人员
(1, 'EMP-2024-001', '张三', '110101199001011234', 'male', '1990-01-01', '13800138001', 'zhangsan@example.com', '项目经理', '项目管理', '2023-01-15', 'active', 'approved'),
(1, 'EMP-2024-002', '李四', '110101199002021235', 'male', '1990-02-02', '13800138002', 'lisi@example.com', '安全员', '安全管理', '2023-02-20', 'active', 'approved'),
(1, 'EMP-2024-003', '王五', '110101199003031236', 'male', '1990-03-03', '13800138003', 'wangwu@example.com', '电工', '电气作业', '2023-03-10', 'active', 'pending_review'),
(1, 'EMP-2024-004', '赵六', '110101199004041237', 'male', '1990-04-04', '13800138004', 'zhaoliu@example.com', '焊工', '焊接作业', '2023-04-05', 'inactive', 'approved'),

-- 单位2（机电公司）的人员
(2, 'EMP-2024-005', '钱七', '110101199005051238', 'male', '1990-05-05', '13800138005', 'qianqi@example.com', '机械工程师', '机械设计', '2023-05-12', 'active', 'approved'),
(2, 'EMP-2024-006', '孙八', '110101199006061239', 'female', '1990-06-06', '13800138006', 'sunba@example.com', '电气工程师', '电气设计', '2023-06-18', 'active', 'approved'),
(2, 'EMP-2024-007', '周九', '110101199007071240', 'male', '1990-07-07', '13800138007', 'zhoujiu@example.com', '钳工', '钳工作业', '2023-07-22', 'suspended', 'approved'),

-- 单位3（安装公司）的人员
(3, 'EMP-2024-008', '吴十', '110101199008081241', 'male', '1990-08-08', '13800138008', 'wushi@example.com', '安装工', '设备安装', '2023-08-30', 'active', 'approved'),
(3, 'EMP-2024-009', '郑十一', '110101199009091242', 'female', '1990-09-09', '13800138009', 'zhengshiyi@example.com', '质检员', '质量检查', '2023-09-14', 'active', 'rejected'),

-- 单位5（维修公司）的人员
(5, 'EMP-2024-010', '冯十二', '110101199010101243', 'male', '1990-10-10', '13800138010', 'fengshier@example.com', '维修工', '设备维修', '2023-10-25', 'active', 'approved');

-- ====================================================================
-- 8. 插入测试数据 - 人员证书
-- ====================================================================
INSERT INTO personnel_certificates (personnel_id, certificate_type, certificate_name, certificate_number, issuing_authority, issue_date, expiry_date, certificate_status, approval_status) VALUES
-- 张三的证书
(1, '特种作业证', '高处作业证', 'TSZY-2023-001', '市安全生产监督管理局', '2023-01-20', '2026-01-19', 'valid', 'approved'),
(1, '职业资格证', '一级建造师', 'ZYGZ-2022-001', '省建设厅', '2022-05-15', '2025-05-14', 'valid', 'approved'),
(1, '安全培训证', '安全生产管理人员证', 'AQPX-2023-001', '市安监局培训中心', '2023-02-10', '2024-02-09', 'expired', 'approved'),

-- 李四的证书
(2, '特种作业证', '电工作业证', 'TSZY-2023-002', '市安全生产监督管理局', '2023-03-05', '2026-03-04', 'valid', 'approved'),
(2, '安全培训证', '安全员证', 'AQPX-2023-002', '市安监局培训中心', '2023-03-20', '2024-03-19', 'valid', 'approved'),

-- 王五的证书
(3, '特种作业证', '焊工作业证', 'TSZY-2023-003', '市安全生产监督管理局', '2023-04-10', '2026-04-09', 'valid', 'pending_review'),

-- 钱七的证书
(5, '职业资格证', '高级机械工程师', 'ZYGZ-2021-002', '省工程师协会', '2021-08-12', '2024-08-11', 'valid', 'approved'),

-- 孙八的证书
(6, '职业资格证', '注册电气工程师', 'ZYGZ-2020-003', '国家注册工程师委员会', '2020-11-25', '2025-11-24', 'valid', 'approved'),

-- 吴十的证书
(8, '特种作业证', '起重机械作业证', 'TSZY-2023-004', '市安全生产监督管理局', '2023-09-05', '2026-09-04', 'valid', 'approved'),

-- 冯十二的证书
(10, '特种作业证', '压力容器作业证', 'TSZY-2023-005', '市安全生产监督管理局', '2023-11-10', '2026-11-09', 'valid', 'approved'),
(10, '安全培训证', '特种设备安全管理员证', 'AQPX-2023-003', '市质监局培训中心', '2023-11-15', '2024-11-14', 'valid', 'approved');

-- ====================================================================
-- 9. 插入测试数据 - 人员培训记录
-- ====================================================================
INSERT INTO personnel_training_records (personnel_id, training_type, training_name, training_date, training_duration, training_institution, trainer, training_score, is_passed, certificate_number) VALUES
-- 张三的培训记录
(1, '入场培训', '新员工安全入场培训', '2023-01-16', 8.0, '公司安全部', '李安全', 95.5, TRUE, 'RCPX-2023-001'),
(1, '专项培训', '高处作业安全专项培训', '2023-02-05', 16.0, '市安监局培训中心', '王专家', 92.0, TRUE, 'ZXPX-2023-001'),
(1, '再培训', '年度安全知识再培训', '2024-01-10', 4.0, '公司安全部', '张讲师', 88.5, TRUE, 'ZPX-2024-001'),

-- 李四的培训记录
(2, '入场培训', '新员工安全入场培训', '2023-02-21', 8.0, '公司安全部', '李安全', 96.0, TRUE, 'RCPX-2023-002'),
(2, '专项培训', '电气安全专项培训', '2023-03-25', 20.0, '市电力公司培训中心', '刘电工', 94.5, TRUE, 'ZXPX-2023-002'),

-- 王五的培训记录
(3, '入场培训', '新员工安全入场培训', '2023-03-11', 8.0, '公司安全部', '李安全', 89.0, TRUE, 'RCPX-2023-003'),
(3, '专项培训', '焊接安全专项培训', '2023-04-15', 24.0, '市焊接协会培训中心', '陈焊工', 91.5, TRUE, 'ZXPX-2023-003'),

-- 钱七的培训记录
(5, '再培训', '机械安全再培训', '2024-02-18', 8.0, '省机械工程学会', '赵教授', 93.0, TRUE, 'ZPX-2024-002'),

-- 孙八的培训记录
(6, '专项培训', '电气设计规范培训', '2023-12-10', 32.0, '国家电气标准化委员会', '钱专家', 97.0, TRUE, 'ZXPX-2023-004'),

-- 吴十的培训记录
(8, '入场培训', '新员工安全入场培训', '2023-08-31', 8.0, '公司安全部', '李安全', 90.5, TRUE, 'RCPX-2023-004'),
(8, '专项培训', '起重机械安全操作培训', '2023-09-10', 40.0, '市特检院培训中心', '周工程师', 95.0, TRUE, 'ZXPX-2023-005'),

-- 冯十二的培训记录
(10, '入场培训', '新员工安全入场培训', '2023-10-26', 8.0, '公司安全部', '李安全', 92.5, TRUE, 'RCPX-2023-005'),
(10, '专项培训', '压力容器安全操作培训', '2023-11-20', 48.0, '市特检院培训中心', '郑专家', 96.5, TRUE, 'ZXPX-2023-006');

-- ====================================================================
-- 10. 创建视图 - 人员证书状态视图
-- ====================================================================
CREATE OR REPLACE VIEW v_personnel_certificate_status AS
SELECT 
    p.id AS personnel_id,
    p.personnel_code,
    p.name AS personnel_name,
    p.position,
    p.work_type,
    c.company_name,
    pc.certificate_type,
    pc.certificate_name,
    pc.certificate_number,
    pc.issue_date,
    pc.expiry_date,
    pc.certificate_status,
    pc.approval_status,
    DATEDIFF(pc.expiry_date, CURDATE()) AS days_to_expiry,
    CASE 
        WHEN DATEDIFF(pc.expiry_date, CURDATE()) <= 0 THEN '已过期'
        WHEN DATEDIFF(pc.expiry_date, CURDATE()) <= 7 THEN '7天内过期'
        WHEN DATEDIFF(pc.expiry_date, CURDATE()) <= 15 THEN '15天内过期'
        WHEN DATEDIFF(pc.expiry_date, CURDATE()) <= 30 THEN '30天内过期'
        ELSE '正常'
    END AS expiry_status,
    pc.reviewed_by,
    pc.reviewed_at
FROM personnel p
JOIN personnel_certificates pc ON p.id = pc.personnel_id
JOIN companies c ON p.company_id = c.id
WHERE pc.deleted_at IS NULL AND p.deleted_at IS NULL;

-- ====================================================================
-- 11. 创建视图 - 人员培训统计视图
-- ====================================================================
CREATE OR REPLACE VIEW v_personnel_training_stats AS
SELECT 
    p.id AS personnel_id,
    p.personnel_code,
    p.name AS personnel_name,
    c.company_name,
    COUNT(ptr.id) AS total_trainings,
    SUM(CASE WHEN ptr.is_passed = TRUE THEN 1 ELSE 0 END) AS passed_trainings,
    SUM(CASE WHEN ptr.is_passed = FALSE THEN 1 ELSE 0 END) AS failed_trainings,
    AVG(ptr.training_score) AS avg_score,
    SUM(ptr.training_duration) AS total_training_hours,
    MAX(ptr.training_date) AS latest_training_date
FROM personnel p
LEFT JOIN personnel_training_records ptr ON p.id = ptr.personnel_id AND ptr.deleted_at IS NULL
JOIN companies c ON p.company_id = c.id
WHERE p.deleted_at IS NULL
GROUP BY p.id, p.personnel_code, p.name, c.company_name;

-- ====================================================================
-- 12. 创建存储过程 - 生成证书到期预警
-- ====================================================================
DELIMITER $$

CREATE OR REPLACE PROCEDURE sp_generate_personnel_certificate_alerts()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_certificate_id BIGINT UNSIGNED;
    DECLARE v_personnel_id BIGINT UNSIGNED;
    DECLARE v_certificate_type VARCHAR(50);
    DECLARE v_certificate_number VARCHAR(100);
    DECLARE v_expiry_date DATE;
    DECLARE v_days_to_expiry INT;
    DECLARE v_alert_type ENUM('first_alert', 'second_alert', 'third_alert');
    DECLARE v_alert_config_id BIGINT UNSIGNED;
    DECLARE v_alert_channel ENUM('email', 'sms', 'wechat', 'system');
    DECLARE v_alert_template VARCHAR(200);
    
    -- 游标：查找需要预警的证书
    DECLARE cur_certificates CURSOR FOR
    SELECT 
        pc.id,
        pc.personnel_id,
        pc.certificate_type,
        pc.certificate_number,
        pc.expiry_date,
        DATEDIFF(pc.expiry_date, CURDATE()) AS days_to_expiry
    FROM personnel_certificates pc
    WHERE pc.certificate_status = 'valid'
        AND pc.approval_status = 'approved'
        AND pc.expiry_date > CURDATE() -- 未过期
        AND pc.deleted_at IS NULL
        AND DATEDIFF(pc.expiry_date, CURDATE()) IN (7, 15, 30);
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN cur_certificates;
    
    read_loop: LOOP
        FETCH cur_certificates INTO 
            v_certificate_id, 
            v_personnel_id, 
            v_certificate_type, 
            v_certificate_number, 
            v_expiry_date, 
            v_days_to_expiry;
        
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- 根据剩余天数确定预警类型
        IF v_days_to_expiry = 30 THEN
            SET v_alert_type = 'first_alert';
        ELSEIF v_days_to_expiry = 15 THEN
            SET v_alert_type = 'second_alert';
        ELSEIF v_days_to_expiry = 7 THEN
            SET v_alert_type = 'third_alert';
        END IF;
        
        -- 获取预警配置
        SELECT id, alert_channel, alert_template 
        INTO v_alert_config_id, v_alert_channel, v_alert_template
        FROM personnel_certificate_alerts 
        WHERE certificate_type = v_certificate_type 
            AND alert_type = v_alert_type 
            AND is_enabled = TRUE
        LIMIT 1;
        
        -- 如果找到配置且未发送过预警，则插入预警记录
        IF v_alert_config_id IS NOT NULL THEN
            IF NOT EXISTS (
                SELECT 1 
                FROM personnel_certificate_alert_logs 
                WHERE certificate_id = v_certificate_id 
                    AND alert_type = v_alert_type 
                    AND DATE(created_at) = CURDATE()
            ) THEN
                INSERT INTO personnel_certificate_alert_logs (
                    certificate_id,
                    personnel_id,
                    alert_config_id,
                    alert_type,
                    alert_date,
                    expiry_date,
                    days_left,
                    alert_channel,
                    alert_content
                ) VALUES (
                    v_certificate_id,
                    v_personnel_id,
                    v_alert_config_id,
                    v_alert_type,
                    CURDATE(),
                    v_expiry_date,
                    v_days_to_expiry,
                    v_alert_channel,
                    CONCAT(
                        '证书预警: ', v_certificate_type, 
                        ' (编号: ', v_certificate_number, 
                        ') 将于 ', v_days_to_expiry, ' 天后到期'
                    )
                );
            END IF;
        END IF;
    END LOOP;
    
    CLOSE cur_certificates;
END$$

DELIMITER ;

-- ====================================================================
-- 13. 创建事件 - 每日自动检查证书到期
-- ====================================================================
CREATE EVENT IF NOT EXISTS event_daily_personnel_certificate_check
ON SCHEDULE EVERY 1 DAY
STARTS CURRENT_DATE + INTERVAL 1 DAY
DO
BEGIN
    CALL sp_generate_personnel_certificate_alerts();
END;

-- ====================================================================
-- 14. 数据库初始化完成
-- ====================================================================
SELECT '工贸企业相关方管理系统 - 人员资质管理模块数据库初始化完成!' AS message;
SELECT 
    (SELECT COUNT(*) FROM personnel) AS personnel_count,
    (SELECT COUNT(*) FROM personnel_certificates) AS certificate_count,
    (SELECT COUNT(*) FROM personnel_training_records) AS training_record_count,
    (SELECT COUNT(*) FROM personnel_certificate_alerts) AS alert_config_count;