// ============================================
// 人员管理相关类型定义
// ============================================

// 基础枚举类型
export enum GenderEnum {
  MALE = 'male',
  FEMALE = 'female',
  OTHER = 'other'
}

export enum EmploymentStatusEnum {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  SUSPENDED = 'suspended',
  TERMINATED = 'terminated'
}

export enum PersonnelStatusEnum {
  PENDING_REVIEW = 'pending_review',
  APPROVED = 'approved',
  REJECTED = 'rejected',
  EXPIRED = 'expired'
}

export enum CertificateStatusEnum {
  VALID = 'valid',
  EXPIRED = 'expired',
  SUSPENDED = 'suspended',
  REVOKED = 'revoked'
}

export enum ApprovalStatusEnum {
  PENDING_REVIEW = 'pending_review',
  APPROVED = 'approved',
  REJECTED = 'rejected'
}

export enum AlertTypeEnum {
  FIRST_ALERT = 'first_alert',
  SECOND_ALERT = 'second_alert',
  THIRD_ALERT = 'third_alert'
}

export enum AlertChannelEnum {
  EMAIL = 'email',
  SMS = 'sms',
  WECHAT = 'wechat',
  SYSTEM = 'system'
}

// ============================================
// 人员相关接口
// ============================================

export interface PersonnelBase {
  personnel_code: string
  name: string
  id_card: string
  gender: GenderEnum
  birth_date?: string | null
  phone?: string | null
  email?: string | null
  position?: string | null
  work_type?: string | null
  hire_date?: string | null
  employment_status: EmploymentStatusEnum
  status: PersonnelStatusEnum
  photo_url?: string | null
}

export interface PersonnelCreate extends PersonnelBase {
  company_id: number
  created_by?: string | null
}

export interface PersonnelUpdate {
  name?: string | null
  gender?: GenderEnum | null
  birth_date?: string | null
  phone?: string | null
  email?: string | null
  position?: string | null
  work_type?: string | null
  hire_date?: string | null
  employment_status?: EmploymentStatusEnum | null
  status?: PersonnelStatusEnum | null
  photo_url?: string | null
  updated_by?: string | null
}

export interface PersonnelInDB extends PersonnelBase {
  id: number
  company_id: number
  company?: {
    id: number
    name: string
  }
  created_by?: string | null
  updated_by?: string | null
  created_at: string
  updated_at: string
  deleted_at?: string | null
}

export interface PersonnelSimple extends PersonnelBase {
  id: number
  company_id: number
  company_name?: string
  created_at: string
}

// ============================================
// 人员证书相关接口
// ============================================

export interface PersonnelCertificateBase {
  certificate_type: string
  certificate_name: string
  certificate_number: string
  issuing_authority?: string | null
  issue_date: string
  expiry_date: string
  certificate_status: CertificateStatusEnum
  approval_status: ApprovalStatusEnum
  file_url?: string | null
  file_name?: string | null
  file_size?: number | null
  review_notes?: string | null
}

export interface PersonnelCertificateCreate extends PersonnelCertificateBase {
  personnel_id: number
  created_by?: string | null
}

export interface PersonnelCertificateUpdate {
  certificate_type?: string | null
  certificate_name?: string | null
  issuing_authority?: string | null
  issue_date?: string | null
  expiry_date?: string | null
  certificate_status?: CertificateStatusEnum | null
  approval_status?: ApprovalStatusEnum | null
  file_url?: string | null
  file_name?: string | null
  file_size?: number | null
  review_notes?: string | null
  reviewed_by?: string | null
  updated_by?: string | null
}

export interface PersonnelCertificateInDB extends PersonnelCertificateBase {
  id: number
  personnel_id: number
  reviewed_by?: string | null
  reviewed_at?: string | null
  created_by?: string | null
  updated_by?: string | null
  created_at: string
  updated_at: string
  deleted_at?: string | null
}

export interface PersonnelCertificateWithPersonnel extends PersonnelCertificateInDB {
  personnel_name?: string
  personnel_code?: string
}

// ============================================
// 证书预警相关接口
// ============================================

export interface PersonnelCertificateAlertBase {
  certificate_type: string
  alert_type: AlertTypeEnum
  days_before: number
  alert_channel: AlertChannelEnum
  alert_template: string
  is_enabled: boolean
}

export interface PersonnelCertificateAlertCreate extends PersonnelCertificateAlertBase {
  created_by?: string | null
}

export interface PersonnelCertificateAlertUpdate {
  days_before?: number | null
  alert_channel?: AlertChannelEnum | null
  alert_template?: string | null
  is_enabled?: boolean | null
  updated_by?: string | null
}

export interface PersonnelCertificateAlertInDB extends PersonnelCertificateAlertBase {
  id: number
  created_by?: string | null
  updated_by?: string | null
  created_at: string
  updated_at: string
}

// ============================================
// 证书预警记录相关接口
// ============================================

export interface PersonnelCertificateAlertLogBase {
  alert_type: AlertTypeEnum
  alert_date: string
  expiry_date: string
  days_left: number
  alert_channel: AlertChannelEnum
  alert_content: string
  sent_to?: string | null
  is_sent: boolean
}

export interface PersonnelCertificateAlertLogCreate extends PersonnelCertificateAlertLogBase {
  certificate_id: number
  personnel_id: number
  alert_config_id: number
}

export interface PersonnelCertificateAlertLogInDB extends PersonnelCertificateAlertLogBase {
  id: number
  certificate_id: number
  personnel_id: number
  alert_config_id: number
  sent_at?: string | null
  created_at: string
  certificate?: PersonnelCertificateInDB
}

// ============================================
// 人员培训记录相关接口
// ============================================

export interface PersonnelTrainingRecordBase {
  training_type: string
  training_name: string
  training_date: string
  training_duration?: number | null
  training_institution?: string | null
  trainer?: string | null
  training_score?: number | null
  is_passed?: boolean | null
  certificate_number?: string | null
  certificate_url?: string | null
  notes?: string | null
}

export interface PersonnelTrainingRecordCreate extends PersonnelTrainingRecordBase {
  personnel_id: number
  created_by?: string | null
}

export interface PersonnelTrainingRecordUpdate {
  training_type?: string | null
  training_name?: string | null
  training_date?: string | null
  training_duration?: number | null
  training_institution?: string | null
  trainer?: string | null
  training_score?: number | null
  is_passed?: boolean | null
  certificate_number?: string | null
  certificate_url?: string | null
  notes?: string | null
  updated_by?: string | null
}

export interface PersonnelTrainingRecordInDB extends PersonnelTrainingRecordBase {
  id: number
  personnel_id: number
  created_by?: string | null
  updated_by?: string | null
  created_at: string
  updated_at: string
  deleted_at?: string | null
}

// ============================================
// 查询参数接口
// ============================================

export interface PersonnelQueryParams {
  company_id?: number | null
  name?: string | null
  personnel_code?: string | null
  id_card?: string | null
  employment_status?: EmploymentStatusEnum | null
  status?: PersonnelStatusEnum | null
  work_type?: string | null
  page: number
  page_size: number
}

export interface PersonnelCertificateQueryParams {
  personnel_id?: number | null
  certificate_type?: string | null
  certificate_status?: CertificateStatusEnum | null
  approval_status?: ApprovalStatusEnum | null
  expiry_start_date?: string | null
  expiry_end_date?: string | null
  page: number
  page_size: number
}

export interface PersonnelTrainingRecordQueryParams {
  personnel_id?: number | null
  training_type?: string | null
  training_start_date?: string | null
  training_end_date?: string | null
  is_passed?: boolean | null
  page: number
  page_size: number
}

// ============================================
// 分页响应接口
// ============================================

export interface PaginatedResponse {
  total: number
  page: number
  page_size: number
  total_pages: number
}

export interface PersonnelPaginatedResponse extends PaginatedResponse {
  items: PersonnelSimple[]
}

export interface PersonnelCertificatePaginatedResponse extends PaginatedResponse {
  items: PersonnelCertificateWithPersonnel[]
}

export interface PersonnelTrainingRecordPaginatedResponse extends PaginatedResponse {
  items: PersonnelTrainingRecordInDB[]
}

// ============================================
// 统计信息接口
// ============================================

export interface PersonnelStats {
  total_personnel: number
  active_personnel: number
  pending_review_personnel: number
  expired_certificates: number
  expiring_soon_certificates: number
}

export interface CertificateStats {
  total_certificates: number
  valid_certificates: number
  expired_certificates: number
  pending_review_certificates: number
  by_type: Record<string, number>
}

export interface TrainingStats {
  total_trainings: number
  passed_trainings: number
  failed_trainings: number
  avg_score: number
  total_training_hours: number
}

export interface AlertStats {
  total_alerts: number
  sent_alerts: number
  pending_alerts: number
  by_type: Record<string, number>
}

// ============================================
// 批量操作接口
// ============================================

export interface BulkPersonnelCreate {
  items: PersonnelCreate[]
}

export interface BulkPersonnelCertificateCreate {
  items: PersonnelCertificateCreate[]
}

export interface BulkPersonnelTrainingRecordCreate {
  items: PersonnelTrainingRecordCreate[]
}

export interface BulkUpdateStatus {
  ids: number[]
  status: PersonnelStatusEnum
  updated_by?: string | null
}

export interface BulkUpdateCertificateStatus {
  ids: number[]
  certificate_status?: CertificateStatusEnum | null
  approval_status?: ApprovalStatusEnum | null
  review_notes?: string | null
  reviewed_by?: string | null
}

// ============================================
// 通用响应接口
// ============================================

export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  message?: string
  error?: string
  status_code?: number
}

export interface ErrorResponse {
  detail: string
  status: number
  timestamp: string
  path: string
}

// ============================================
// 单位相关接口（用于下拉选择）
// ============================================

export interface Company {
  id: number
  name: string
  code?: string
  type?: string
  status?: string
  created_at?: string
}

export interface CompanyPaginatedResponse extends PaginatedResponse {
  items: Company[]
}