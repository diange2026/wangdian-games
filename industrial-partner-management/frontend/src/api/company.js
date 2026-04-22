/**
 * 单位资质管理API接口
 * 企业级单位资质管理系统的前端API
 */

import request from '@/utils/request'
import { getToken } from '@/utils/auth'

// API基础路径
const API_BASE = '/api/v1/companies'

// ==================== 单位管理API ====================

/**
 * 获取单位列表
 * @param {Object} params - 查询参数
 * @returns {Promise} 单位列表
 */
export function fetchCompanyList(params = {}) {
  return request({
    url: API_BASE,
    method: 'get',
    params: {
      page: params.page || 1,
      limit: params.limit || 20,
      company_code: params.companyCode,
      company_name: params.companyName,
      company_type: params.companyType,
      status: params.status,
      risk_level: params.riskLevel,
      contact_person: params.contactPerson,
      contact_phone: params.contactPhone,
      sort_by: params.sortBy,
      sort_order: params.sortOrder
    }
  })
}

/**
 * 获取单位详情
 * @param {number} companyId - 单位ID
 * @param {Object} options - 选项
 * @returns {Promise} 单位详情
 */
export function fetchCompanyDetail(companyId, options = {}) {
  const params = {}
  
  if (options.includeCertificates !== false) {
    params.include_certificates = true
  }
  
  if (options.includeAuditLogs) {
    params.include_audit_logs = true
  }
  
  if (options.includeRiskAnalysis) {
    params.include_risk_analysis = true
  }
  
  return request({
    url: `${API_BASE}/${companyId}`,
    method: 'get',
    params
  })
}

/**
 * 创建新单位
 * @param {Object} companyData - 单位数据
 * @returns {Promise} 创建结果
 */
export function createCompany(companyData) {
  return request({
    url: API_BASE,
    method: 'post',
    data: companyData
  })
}

/**
 * 更新单位信息
 * @param {number} companyId - 单位ID
 * @param {Object} updateData - 更新数据
 * @returns {Promise} 更新结果
 */
export function updateCompany(companyId, updateData) {
  return request({
    url: `${API_BASE}/${companyId}`,
    method: 'put',
    data: updateData
  })
}

/**
 * 删除单位
 * @param {number} companyId - 单位ID
 * @param {Object} options - 删除选项
 * @returns {Promise} 删除结果
 */
export function deleteCompany(companyId, options = {}) {
  const params = {}
  
  if (options.permanent) {
    params.permanent = true
  }
  
  return request({
    url: `${API_BASE}/${companyId}`,
    method: 'delete',
    params
  })
}

// ==================== 证照管理API ====================

/**
 * 获取单位证照列表
 * @param {number} companyId - 单位ID
 * @param {Object} params - 查询参数
 * @returns {Promise} 证照列表
 */
export function fetchCompanyCertificates(companyId, params = {}) {
  return request({
    url: `${API_BASE}/${companyId}/certificates`,
    method: 'get',
    params: {
      status: params.status,
      expiry_within_days: params.expiryWithinDays,
      renewal_status: params.renewalStatus,
      page: params.page || 1,
      limit: params.limit || 50
    }
  })
}

/**
 * 添加证照
 * @param {number} companyId - 单位ID
 * @param {Object} certificateData - 证照数据
 * @returns {Promise} 添加结果
 */
export function createCertificate(companyId, certificateData) {
  return request({
    url: `${API_BASE}/${companyId}/certificates`,
    method: 'post',
    data: certificateData
  })
}

/**
 * 更新证照信息
 * @param {number} certificateId - 证照ID
 * @param {Object} updateData - 更新数据
 * @returns {Promise} 更新结果
 */
export function updateCertificate(certificateId, updateData) {
  return request({
    url: `${API_BASE}/certificates/${certificateId}`,
    method: 'put',
    data: updateData
  })
}

/**
 * 删除证照
 * @param {number} certificateId - 证照ID
 * @returns {Promise} 删除结果
 */
export function deleteCertificate(certificateId) {
  return request({
    url: `${API_BASE}/certificates/${certificateId}`,
    method: 'delete'
  })
}

/**
 * 上传证照文件
 * @param {number} companyId - 单位ID
 * @param {File} file - 文件对象
 * @returns {Promise} 上传结果
 */
export function uploadCertificateFile(companyId, file) {
  const formData = new FormData()
  formData.append('file', file)
  
  return request({
    url: `${API_BASE}/${companyId}/certificates/upload`,
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data',
      'Authorization': `Bearer ${getToken()}`
    }
  })
}

// ==================== 预警管理API ====================

/**
 * 获取单位预警列表
 * @param {number} companyId - 单位ID
 * @param {Object} params - 查询参数
 * @returns {Promise} 预警列表
 */
export function fetchCompanyAlerts(companyId, params = {}) {
  return request({
    url: `${API_BASE}/${companyId}/alerts`,
    method: 'get',
    params: {
      alert_type: params.alertType,
      level: params.level,
      status: params.status,
      start_date: params.startDate,
      end_date: params.endDate,
      page: params.page || 1,
      limit: params.limit || 20
    }
  })
}

/**
 * 处理预警
 * @param {number} alertId - 预警ID
 * @param {Object} actionData - 处理数据
 * @returns {Promise} 处理结果
 */
export function resolveAlert(alertId, actionData = {}) {
  return request({
    url: `${API_BASE}/alerts/${alertId}/resolve`,
    method: 'post',
    data: actionData
  })
}

// ==================== 数据统计API ====================

/**
 * 获取单位统计数据
 * @returns {Promise} 统计结果
 */
export function fetchCompanyStatistics() {
  return request({
    url: `${API_BASE}/statistics`,
    method: 'get'
  })
}

/**
 * 获取证照统计报告
 * @param {Object} params - 查询参数
 * @returns {Promise} 统计报告
 */
export function fetchCertificateReport(params = {}) {
  return request({
    url: `${API_BASE}/certificates/report`,
    method: 'get',
    params: {
      start_date: params.startDate,
      end_date: params.endDate,
      report_type: params.reportType
    }
  })
}

// ==================== 数据导出API ====================

/**
 * 导出单位数据
 * @param {Object} exportRequest - 导出请求参数
 * @returns {Promise} 导出结果
 */
export function exportCompanies(exportRequest) {
  return request({
    url: `${API_BASE}/export`,
    method: 'post',
    data: exportRequest,
    responseType: 'blob'
  })
}

/**
 * 导入单位数据
 * @param {File} file - 导入文件
 * @returns {Promise} 导入结果
 */
export function importCompanies(file) {
  const formData = new FormData()
  formData.append('file', file)
  
  return request({
    url: `${API_BASE}/import`,
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data',
      'Authorization': `Bearer ${getToken()}`
    }
  })
}

// ==================== 智能分析API ====================

/**
 * 获取风险分析报告
 * @param {number} companyId - 单位ID
 * @returns {Promise} 风险分析结果
 */
export function fetchRiskAnalysis(companyId) {
  return request({
    url: `${API_BASE}/${companyId}/risk-analysis`,
    method: 'get'
  })
}

/**
 * 获取合规性检查结果
 * @param {number} companyId - 单位ID
 * @returns {Promise} 合规性检查结果
 */
export function fetchComplianceCheck(companyId) {
  return request({
    url: `${API_BASE}/${companyId}/compliance-check`,
    method: 'get'
  })
}

// ==================== 批量操作API ====================

/**
 * 批量更新单位
 * @param {Object} updateData - 批量更新数据
 * @returns {Promise} 更新结果
 */
export function bulkUpdateCompanies(updateData) {
  return request({
    url: `${API_BASE}/bulk-update`,
    method: 'put',
    data: updateData
  })
}

/**
 * 批量删除单位
 * @param {Array<number>} companyIds - 单位ID数组
 * @returns {Promise} 删除结果
 */
export function bulkDeleteCompanies(companyIds) {
  return request({
    url: `${API_BASE}/bulk-delete`,
    method: 'delete',
    data: { company_ids: companyIds }
  })
}

// ==================== 实时监控API ====================

/**
 * 订阅单位状态变化
 * @param {number} companyId - 单位ID
 * @param {Function} callback - 回调函数
 * @returns {Object} 订阅对象
 */
export function subscribeCompanyChanges(companyId, callback) {
  // 使用 WebSocket 或 SSE 实现
  const eventSource = new EventSource(`${API_BASE}/${companyId}/subscribe`)
  
  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data)
    callback(data)
  }
  
  return {
    close: () => eventSource.close()
  }
}

// ==================== 通用工具函数 ====================

/**
 * 验证单位编码是否可用
 * @param {string} companyCode - 单位编码
 * @returns {Promise} 验证结果
 */
export function validateCompanyCodeAvailable(companyCode) {
  return request({
    url: `${API_BASE}/validate-code`,
    method: 'get',
    params: { company_code: companyCode }
  })
}

/**
 * 搜索单位
 * @param {string} keyword - 搜索关键词
 * @returns {Promise} 搜索结果
 */
export function searchCompanies(keyword) {
  return request({
    url: `${API_BASE}/search`,
    method: 'get',
    params: { keyword }
  })
}

// ==================== 文件处理API ====================

/**
 * 下载证照文件
 * @param {number} certificateId - 证照ID
 * @returns {Promise} 文件数据
 */
export function downloadCertificateFile(certificateId) {
  return request({
    url: `${API_BASE}/certificates/${certificateId}/download`,
    method: 'get',
    responseType: 'blob'
  })
}

/**
 * 预览证照文件
 * @param {number} certificateId - 证照ID
 * @returns {Promise} 文件预览结果
 */
export function previewCertificateFile(certificateId) {
  return request({
    url: `${API_BASE}/certificates/${certificateId}/preview`,
    method: 'get',
    responseType: 'blob'
  })
}

// ==================== 工作流API ====================

/**
 * 提交单位审核
 * @param {number} companyId - 单位ID
 * @param {Object} reviewData - 审核数据
 * @returns {Promise} 审核结果
 */
export function submitCompanyReview(companyId, reviewData = {}) {
  return request({
    url: `${API_BASE}/${companyId}/submit-review`,
    method: 'post',
    data: reviewData
  })
}

/**
 * 批准单位
 * @param {number} companyId - 单位ID
 * @returns {Promise} 批准结果
 */
export function approveCompany(companyId) {
  return request({
    url: `${API_BASE}/${companyId}/approve`,
    method: 'post'
  })
}

/**
 * 拒绝单位
 * @param {number} companyId - 单位ID
 * @param {Object} rejectionData - 拒绝数据
 * @returns {Promise} 拒绝结果
 */
export function rejectCompany(companyId, rejectionData = {}) {
  return request({
    url: `${API_BASE}/${companyId}/reject`,
    method: 'post',
    data: rejectionData
  })
}

// ==================== 集成工具函数 ====================

/**
 * 格式化单位响应数据

 * @param {Object} data - 原始数据
 * @returns {Object} 格式化后的数据
 */

export function formatCompanyResponse(data) {
  return {
    id: data.id,
    companyCode: data.company_code,
    companyName: data.company_name,
    companyType: data.company_type,
    businessNature: data.business_nature,
    registrationCapital: data.registration_capital,
    actualCapital: data.actual_capital,
    registeredAddress: data.registered_address,
    businessAddress: data.business_address,
    legalPerson: data.legal_person,
    legalPersonIdCard: data.legal_person_id_card,
    creditCode: data.credit_code,
    businessScope: data.business_scope,
    contactPerson: data.contact_person,
    contactPhone: data.contact_phone,
    contactEmail: data.contact_email,
    financialContact: data.financial_contact,
    financialPhone: data.financial_phone,
    technicalContact: data.technical_contact,
    technicalPhone: data.technical_phone,
    riskLevel: data.risk_level,
    riskScore: data.risk_score,
    cooperationLevel: data.cooperation_level,
    cooperationStartDate: data.cooperation_start_date,
    status: data.status,
    approvalStatus: data.approval_status,
    remarks: data.remarks,
    createdBy: data.created_by,
    updatedBy: data.updated_by,
    createdAt: data.created_at,
    updatedAt: data.updated_at
  }
}

/**
 * 格式化证照响应数据
 * @param {Object} data - 原始数据
 * @returns {Object} 格式化后的数据
 */
export function formatCertificateResponse(data) {
  return {
    id: data.id,
    companyId: data.company_id,
    certificateType: data.certificate_type,
    certificateName: data.certificate_name,
    certificateNumber: data.certificate_number,
    issuingAuthority: data.issuing_authority,
    issueDate: data.issue_date,
    expiryDate: data.expiry_date,
    certificateStatus: data.certificate_status,
    renewalStatus: data.renewal_status,
    renewalReminderDays: data.renewal_reminder_days,
    fileUrl: data.file_url,
    fileName: data.file_name,
    fileSize: data.file_size,
    fileHash: data.file_hash,
    lastRenewalDate: data.last_renewal_date,
    renewalSubmittedAt: data.renewal_submitted_at,
    reviewNotes: data.review_notes,
    reviewerId: data.reviewer_id,
    reviewerName: data.reviewer_name,
    reviewedAt: data.reviewed_at,
    remarks: data.remarks,
    createdBy: data.created_by,
    updatedBy: data.updated_by,
    createdAt: data.created_at,
    updatedAt: data.updated_at
  }
}

// 导出所有API
export default {
  // 单位管理
  fetchCompanyList,
  fetchCompanyDetail,
  createCompany,
  updateCompany,
  deleteCompany,
  
  // 证照管理
  fetchCompanyCertificates,
  createCertificate,
  updateCertificate,
  deleteCertificate,
  uploadCertificateFile,
  
  // 预警管理
  fetchCompanyAlerts,
  resolveAlert,
  
  // 数据统计
  fetchCompanyStatistics,
  fetchCertificateReport,
  
  // 数据导出导入
  exportCompanies,
  importCompanies,
  
  // 智能分析
  fetchRiskAnalysis,
  fetchComplianceCheck,
  
  // 批量操作
  bulkUpdateCompanies,
  bulkDeleteCompanies,
  
  // 实时监控
  subscribeCompanyChanges,
  
  // 工具函数
  validateCompanyCodeAvailable,
  searchCompanies,
  downloadCertificateFile,
  previewCertificateFile,
  
  // 工作流
  submitCompanyReview,
  approveCompany,
  rejectCompany,
  
  // 格式化工具
  formatCompanyResponse,
  formatCertificateResponse
}