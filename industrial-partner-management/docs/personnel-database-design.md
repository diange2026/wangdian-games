# 人员资质管理 - 数据库设计文档

## 概述
人员资质管理模块负责管理所有相关方人员的资质信息，包括人员基本信息、证书管理、证书有效期跟踪和资质到期预警。

## 表结构设计

### 1. `personnel` - 人员基本信息表
存储人员的基本信息，包括姓名、身份证号、联系方式等。

| 字段名 | 数据类型 | 约束 | 说明 |
|--------|----------|------|------|
| id | BIGINT UNSIGNED | PRIMARY KEY AUTO_INCREMENT | 人员ID，主键 |
| company_id | BIGINT UNSIGNED | NOT NULL, FOREIGN KEY (companies.id) | 所属单位ID |
| personnel_code | VARCHAR(50) | NOT NULL, UNIQUE | 人员编号，唯一标识 |
| name | VARCHAR(100) | NOT NULL | 姓名 |
| id_card | VARCHAR(18) | NOT NULL, UNIQUE | 身份证号，唯一 |
| gender | ENUM('male', 'female', 'other') | NOT NULL DEFAULT 'male' | 性别 |
| birth_date | DATE | NULL | 出生日期 |
| phone | VARCHAR(20) | NULL | 联系电话 |
| email | VARCHAR(100) | NULL | 电子邮箱 |
| position | VARCHAR(100) | NULL | 岗位/职务 |
| work_type | VARCHAR(50) | NULL | 工种/岗位类型 |
| hire_date | DATE | NULL | 入职日期 |
| employment_status | ENUM('active', 'inactive', 'suspended', 'terminated') | NOT NULL DEFAULT 'active' | 在职状态 |
| status | ENUM('pending_review', 'approved', 'rejected', 'expired') | NOT NULL DEFAULT 'pending_review' | 审核状态 |
| photo_url | VARCHAR(500) | NULL | 照片URL |
| created_by | VARCHAR(100) | NULL | 创建人 |
| updated_by | VARCHAR(100) | NULL | 更新人 |
| created_at | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |
| deleted_at | TIMESTAMP | NULL | 软删除时间 |

**索引**:
- `idx_personnel_company_id` (company_id)
- `idx_personnel_personnel_code` (personnel_code)
- `idx_personnel_name` (name)
- `idx_personnel_id_card` (id_card)
- `idx_personnel_status` (status)
- `idx_personnel_employment_status` (employment_status)

### 2. `personnel_certificates` - 人员证书表
存储人员的各类证书信息，如特种作业证、职业资格证、安全培训证等。

| 字段名 | 数据类型 | 约束 | 说明 |
|--------|----------|------|------|
| id | BIGINT UNSIGNED | PRIMARY KEY AUTO_INCREMENT | 证书ID，主键 |
| personnel_id | BIGINT UNSIGNED | NOT NULL, FOREIGN KEY (personnel.id) | 人员ID |
| certificate_type | VARCHAR(50) | NOT NULL | 证书类型（如：特种作业证、职业资格证、安全培训证） |
| certificate_name | VARCHAR(200) | NOT NULL | 证书名称 |
| certificate_number | VARCHAR(100) | NOT NULL | 证书编号 |
| issuing_authority | VARCHAR(200) | NULL | 发证机构 |
| issue_date | DATE | NOT NULL | 发证日期 |
| expiry_date | DATE | NOT NULL | 到期日期 |
| certificate_status | ENUM('valid', 'expired', 'suspended', 'revoked') | NOT NULL DEFAULT 'valid' | 证书状态 |
| approval_status | ENUM('pending_review', 'approved', 'rejected') | NOT NULL DEFAULT 'pending_review' | 审核状态 |
| file_url | VARCHAR(500) | NULL | 证书扫描件URL |
| file_name | VARCHAR(200) | NULL | 证书文件名称 |
| file_size | INT | NULL | 文件大小（字节） |
| review_notes | TEXT | NULL | 审核意见 |
| reviewed_by | VARCHAR(100) | NULL | 审核人 |
| reviewed_at | TIMESTAMP | NULL | 审核时间 |
| created_by | VARCHAR(100) | NULL | 创建人 |
| updated_by | VARCHAR(100) | NULL | 更新人 |
| created_at | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |
| deleted_at | TIMESTAMP | NULL | 软删除时间 |

**索引**:
- `idx_personnel_certificates_personnel_id` (personnel_id)
- `idx_personnel_certificates_certificate_number` (certificate_number)
- `idx_personnel_certificates_expiry_date` (expiry_date)
- `idx_personnel_certificates_certificate_status` (certificate_status)
- `idx_personnel_certificates_approval_status` (approval_status)
- `idx_personnel_certificates_certificate_type` (certificate_type)

### 3. `personnel_certificate_alerts` - 人员证书预警配置表
存储证书到期预警的配置规则。

| 字段名 | 数据类型 | 约束 | 说明 |
|--------|----------|------|------|
| id | BIGINT UNSIGNED | PRIMARY KEY AUTO_INCREMENT | 预警配置ID |
| certificate_type | VARCHAR(50) | NOT NULL | 证书类型 |
| alert_type | ENUM('first_alert', 'second_alert', 'third_alert') | NOT NULL | 预警类型 |
| days_before | INT | NOT NULL | 到期前天数 |
| alert_channel | ENUM('email', 'sms', 'wechat', 'system') | NOT NULL DEFAULT 'system' | 预警渠道 |
| alert_template | VARCHAR(200) | NOT NULL | 预警模板名称 |
| is_enabled | BOOLEAN | NOT NULL DEFAULT TRUE | 是否启用 |
| created_by | VARCHAR(100) | NULL | 创建人 |
| updated_by | VARCHAR(100) | NULL | 更新人 |
| created_at | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

**索引**:
- `idx_personnel_certificate_alerts_certificate_type` (certificate_type)
- `idx_personnel_certificate_alerts_alert_type` (alert_type)
- `uniq_certificate_type_alert_type` (certificate_type, alert_type) - 唯一约束

### 4. `personnel_certificate_alert_logs` - 人员证书预警记录表
记录证书到期预警的发送历史。

| 字段名 | 数据类型 | 约束 | 说明 |
|--------|----------|------|------|
| id | BIGINT UNSIGNED | PRIMARY KEY AUTO_INCREMENT | 预警记录ID |
| certificate_id | BIGINT UNSIGNED | NOT NULL, FOREIGN KEY (personnel_certificates.id) | 证书ID |
| personnel_id | BIGINT UNSIGNED | NOT NULL, FOREIGN KEY (personnel.id) | 人员ID |
| alert_config_id | BIGINT UNSIGNED | NOT NULL, FOREIGN KEY (personnel_certificate_alerts.id) | 预警配置ID |
| alert_type | ENUM('first_alert', 'second_alert', 'third_alert') | NOT NULL | 预警类型 |
| alert_date | DATE | NOT NULL | 预警日期 |
| expiry_date | DATE | NOT NULL | 证书到期日期 |
| days_left | INT | NOT NULL | 剩余天数 |
| alert_channel | ENUM('email', 'sms', 'wechat', 'system') | NOT NULL | 预警渠道 |
| alert_content | TEXT | NOT NULL | 预警内容 |
| sent_to | VARCHAR(200) | NULL | 发送对象（邮箱/手机号等） |
| is_sent | BOOLEAN | NOT NULL DEFAULT FALSE | 是否已发送 |
| sent_at | TIMESTAMP | NULL | 发送时间 |
| created_at | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**索引**:
- `idx_personnel_certificate_alert_logs_certificate_id` (certificate_id)
- `idx_personnel_certificate_alert_logs_personnel_id` (personnel_id)
- `idx_personnel_certificate_alert_logs_alert_date` (alert_date)
- `idx_personnel_certificate_alert_logs_is_sent` (is_sent)

### 5. `personnel_training_records` - 人员培训记录表
记录人员的安全培训、再培训等信息。

| 字段名 | 数据类型 | 约束 | 说明 |
|--------|----------|------|------|
| id | BIGINT UNSIGNED | PRIMARY KEY AUTO_INCREMENT | 培训记录ID |
| personnel_id | BIGINT UNSIGNED | NOT NULL, FOREIGN KEY (personnel.id) | 人员ID |
| training_type | VARCHAR(50) | NOT NULL | 培训类型（如：入场培训、安全培训、专项培训） |
| training_name | VARCHAR(200) | NOT NULL | 培训名称 |
| training_date | DATE | NOT NULL | 培训日期 |
| training_duration | DECIMAL(5,2) | NULL | 培训时长（小时） |
| training_institution | VARCHAR(200) | NULL | 培训机构 |
| trainer | VARCHAR(100) | NULL | 培训讲师 |
| training_score | DECIMAL(5,2) | NULL | 培训成绩/分数 |
| is_passed | BOOLEAN | NULL | 是否通过 |
| certificate_number | VARCHAR(100) | NULL | 培训证书编号 |
| certificate_url | VARCHAR(500) | NULL | 培训证书URL |
| notes | TEXT | NULL | 备注 |
| created_by | VARCHAR(100) | NULL | 创建人 |
| updated_by | VARCHAR(100) | NULL | 更新人 |
| created_at | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |
| deleted_at | TIMESTAMP | NULL | 软删除时间 |

**索引**:
- `idx_personnel_training_records_personnel_id` (personnel_id)
- `idx_personnel_training_records_training_date` (training_date)
- `idx_personnel_training_records_training_type` (training_type)

## 关系说明

1. **人员与单位的关系**：
   - 一个人员属于一个单位（多对一）
   - 一个单位有多个人员（一对多）

2. **人员与证书的关系**：
   - 一个人员可以有多个证书（一对多）
   - 一个证书属于一个人员（多对一）

3. **证书与预警的关系**：
   - 一个证书可以触发多个预警（一对多）
   - 一个预警记录对应一个证书（多对一）

4. **人员与培训的关系**：
   - 一个人员可以有多个培训记录（一对多）
   - 一个培训记录属于一个人员（多对一）

## 数据完整性约束

### 外键约束
1. `personnel.company_id` → `companies.id`
2. `personnel_certificates.personnel_id` → `personnel.id`
3. `personnel_certificate_alert_logs.certificate_id` → `personnel_certificates.id`
4. `personnel_certificate_alert_logs.personnel_id` → `personnel.id`
5. `personnel_certificate_alert_logs.alert_config_id` → `personnel_certificate_alerts.id`
6. `personnel_training_records.personnel_id` → `personnel.id`

### 唯一约束
1. `personnel.personnel_code` - 人员编号唯一
2. `personnel.id_card` - 身份证号唯一
3. `personnel_certificates.certificate_number` - 证书编号唯一
4. `personnel_certificate_alerts(certificate_type, alert_type)` - 同一证书类型和预警类型配置唯一

### 检查约束
1. `personnel.birth_date` ≤ `CURRENT_DATE` - 出生日期不能晚于当前日期
2. `personnel.hire_date` ≥ `personnel.birth_date` - 入职日期不能早于出生日期
3. `personnel_certificates.expiry_date` > `personnel_certificates.issue_date` - 到期日期晚于发证日期

## 预警配置规则

### 默认预警配置
| 证书类型 | 预警类型 | 到期前天数 | 预警渠道 | 是否启用 |
|----------|----------|------------|----------|----------|
| 特种作业证 | first_alert | 30 | system | TRUE |
| 特种作业证 | second_alert | 15 | system | TRUE |
| 特种作业证 | third_alert | 7 | system | TRUE |
| 职业资格证 | first_alert | 30 | system | TRUE |
| 职业资格证 | second_alert | 15 | system | TRUE |
| 职业资格证 | third_alert | 7 | system | TRUE |
| 安全培训证 | first_alert | 30 | system | TRUE |
| 安全培训证 | second_alert | 15 | system | TRUE |
| 安全培训证 | third_alert | 7 | system | TRUE |

## 数据初始化脚本

见 `scripts/init-personnel-database.sql` 文件，包含：
1. 创建表结构
2. 创建索引
3. 设置外键约束
4. 插入默认预警配置
5. 插入测试数据

## 性能优化建议

1. **查询优化**：
   - 频繁查询的字段建立索引
   - 避免全表扫描，使用覆盖索引
   - 定期分析表统计信息

2. **分区策略**：
   - `personnel_certificate_alert_logs` 表可按 `alert_date` 进行分区
   - `personnel_training_records` 表可按 `training_date` 进行分区

3. **归档策略**：
   - 超过3年的预警记录可以归档到历史表
   - 超过5年的培训记录可以归档到历史表

## 安全考虑

1. **敏感数据保护**：
   - 身份证号、手机号等敏感信息在日志中脱敏
   - 传输过程中使用HTTPS加密
   - 存储过程中对敏感字段进行加密

2. **访问控制**：
   - 基于角色的权限控制（RBAC）
   - 操作日志审计
   - 数据权限隔离（部门/项目级别）

3. **数据备份**：
   - 每日自动备份
   - 异地容灾备份
   - 定期恢复测试