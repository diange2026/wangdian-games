import request from '@/utils/request'
import type {
  PersonnelPaginatedResponse,
  PersonnelInDB,
  PersonnelStats,
  PersonnelCertificatePaginatedResponse,
  PersonnelCertificateInDB,
  PersonnelTrainingRecordPaginatedResponse,
  PersonnelTrainingRecordInDB,
  CertificateStats,
  PersonnelCreate,
  PersonnelUpdate,
  PersonnelCertificateCreate,
  PersonnelCertificateUpdate,
  PersonnelTrainingRecordCreate,
  PersonnelTrainingRecordUpdate,
  PersonnelQueryParams,
  PersonnelCertificateQueryParams,
  PersonnelTrainingRecordQueryParams,
  BulkPersonnelCreate,
  BulkPersonnelCertificateCreate,
  BulkUpdateStatus,
  BulkUpdateCertificateStatus
} from '@/types/personnel'

// ============================================
// 人员管理API
// ============================================

/**
 * 获取人员列表
 */
export function getPersonnelList(params: PersonnelQueryParams): Promise<PersonnelPaginatedResponse> {
  return request({
    url: '/api/v1/personnel/',
    method: 'get',
    params
  })
}

/**
 * 获取人员详情
 */
export function getPersonnelDetail(personnelId: number): Promise<PersonnelInDB> {
  return request({
    url: `/api/v1/personnel/${personnelId}`,
    method: 'get'
  })
}

/**
 * 创建人员
 */
export function createPersonnel(data: PersonnelCreate): Promise<PersonnelInDB> {
  return request({
    url: '/api/v1/personnel/',
    method: 'post',
    data
  })
}

/**
 * 更新人员信息
 */
export function updatePersonnel(personnelId: number, data: PersonnelUpdate): Promise<PersonnelInDB> {
  return request({
    url: `/api/v1/personnel/${personnelId}`,
    method: 'put',
    data
  })
}

/**
 * 删除人员（软删除）
 */
export function deletePersonnel(personnelId: number): Promise<void> {
  return request({
    url: `/api/v1/personnel/${personnelId}`,
    method: 'delete'
  })
}

/**
 * 批量创建人员
 */
export function bulkCreatePersonnel(data: BulkPersonnelCreate): Promise<PersonnelInDB[]> {
  return request({
    url: '/api/v1/personnel/bulk',
    method: 'post',
    data
  })
}

/**
 * 批量更新人员状态
 */
export function bulkUpdatePersonnelStatus(data: BulkUpdateStatus): Promise<{
  message: string
  updated_count: number
  total_count: number
}> {
  return request({
    url: '/api/v1/personnel/bulk/status',
    method: 'put',
    data
  })
}

/**
 * 获取人员统计信息
 */
export function getPersonnelStats(params?: { companyId?: number }): Promise<PersonnelStats> {
  return request({
    url: '/api/v1/personnel/stats/personnel',
    method: 'get',
    params
  })
}

// ============================================
// 人员证书管理API
// ============================================

/**
 * 获取人员证书列表
 */
export function getPersonnelCertificates(personnelId: number, params: PersonnelCertificateQueryParams): Promise<PersonnelCertificatePaginatedResponse> {
  return request({
    url: `/api/v1/personnel/${personnelId}/certificates`,
    method: 'get',
    params
  })
}

/**
 * 获取证书详情
 */
export function getPersonnelCertificate(certificateId: number): Promise<PersonnelCertificateInDB> {
  return request({
    url: `/api/v1/personnel/certificates/${certificateId}`,
    method: 'get'
  })
}

/**
 * 为人员创建证书
 */
export function createPersonnelCertificate(personnelId: number, data: PersonnelCertificateCreate): Promise<PersonnelCertificateInDB> {
  return request({
    url: `/api/v1/personnel/${personnelId}/certificates`,
    method: 'post',
    data
  })
}

/**
 * 更新证书信息
 */
export function updatePersonnelCertificate(certificateId: number, data: PersonnelCertificateUpdate): Promise<PersonnelCertificateInDB> {
  return request({
    url: `/api/v1/personnel/certificates/${certificateId}`,
    method: 'put',
    data
  })
}

/**
 * 删除证书（软删除）
 */
export function deletePersonnelCertificate(certificateId: number): Promise<void> {
  return request({
    url: `/api/v1/personnel/certificates/${certificateId}`,
    method: 'delete'
  })
}

/**
 * 批量创建人员证书
 */
export function bulkCreatePersonnelCertificates(data: BulkPersonnelCertificateCreate): Promise<PersonnelCertificateInDB[]> {
  return request({
    url: '/api/v1/personnel/certificates/bulk',
    method: 'post',
    data
  })
}

/**
 * 批量更新证书状态
 */
export function bulkUpdateCertificateStatus(data: BulkUpdateCertificateStatus): Promise<{
  message: string
  updated_count: number
  total_count: number
}> {
  return request({
    url: '/api/v1/personnel/certificates/bulk/status',
    method: 'put',
    data
  })
}

/**
 * 获取证书统计信息
 */
export function getPersonnelCertificateStats(params?: {
  companyId?: number
  personnelId?: number
}): Promise<CertificateStats> {
  return request({
    url: '/api/v1/personnel/stats/certificates',
    method: 'get',
    params
  })
}

// ============================================
// 人员培训记录API
// ============================================

/**
 * 获取人员培训记录列表
 */
export function getPersonnelTrainings(personnelId: number, params: PersonnelTrainingRecordQueryParams): Promise<PersonnelTrainingRecordPaginatedResponse> {
  return request({
    url: `/api/v1/personnel/${personnelId}/trainings`,
    method: 'get',
    params
  })
}

/**
 * 为人员创建培训记录
 */
export function createPersonnelTraining(personnelId: number, data: PersonnelTrainingRecordCreate): Promise<PersonnelTrainingRecordInDB> {
  return request({
    url: `/api/v1/personnel/${personnelId}/trainings`,
    method: 'post',
    data
  })
}

/**
 * 更新培训记录
 */
export function updatePersonnelTraining(trainingId: number, data: PersonnelTrainingRecordUpdate): Promise<PersonnelTrainingRecordInDB> {
  return request({
    url: `/api/v1/personnel/trainings/${trainingId}`,
    method: 'put',
    data
  })
}

/**
 * 删除培训记录（软删除）
 */
export function deletePersonnelTraining(trainingId: number): Promise<void> {
  return request({
    url: `/api/v1/personnel/trainings/${trainingId}`,
    method: 'delete'
  })
}

/**
 * 批量创建人员培训记录
 */
export function bulkCreatePersonnelTrainings(data: BulkPersonnelTrainingRecordCreate): Promise<PersonnelTrainingRecordInDB[]> {
  return request({
    url: '/api/v1/personnel/trainings/bulk',
    method: 'post',
    data
  })
}

// ============================================
// 证书预警管理API
// ============================================

/**
 * 获取预警配置列表
 */
export function getAlertConfigs(params?: {
  certificate_type?: string
  is_enabled?: boolean
}) {
  return request({
    url: '/api/v1/personnel/alerts/config',
    method: 'get',
    params
  })
}

/**
 * 创建预警配置
 */
export function createAlertConfig(data: any) {
  return request({
    url: '/api/v1/personnel/alerts/config',
    method: 'post',
    data
  })
}

/**
 * 更新预警配置
 */
export function updateAlertConfig(configId: number, data: any) {
  return request({
    url: `/api/v1/personnel/alerts/config/${configId}`,
    method: 'put',
    data
  })
}

// ============================================
// 导出和导入API
// ============================================

/**
 * 导出人员数据
 */
export function exportPersonnelData(params: PersonnelQueryParams): Promise<Blob> {
  return request({
    url: '/api/v1/personnel/export',
    method: 'get',
    params,
    responseType: 'blob'
  })
}

/**
 * 导入人员数据
 */
export function importPersonnelData(data: FormData): Promise<{
  message: string
  success_count: number
  error_count: number
  errors?: string[]
}> {
  return request({
    url: '/api/v1/personnel/import',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

/**
 * 导出证书数据
 */
export function exportCertificateData(params: PersonnelCertificateQueryParams): Promise<Blob> {
  return request({
    url: '/api/v1/personnel/certificates/export',
    method: 'get',
    params,
    responseType: 'blob'
  })
}

/**
 * 下载证书模板
 */
export function downloadCertificateTemplate(): Promise<Blob> {
  return request({
    url: '/api/v1/personnel/certificates/template',
    method: 'get',
    responseType: 'blob'
  })
}