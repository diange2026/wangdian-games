<template>
  <div class="company-detail-container" v-loading="loading">
    <!-- 头部信息 -->
    <div class="detail-header">
      <div class="header-left">
        <h2 class="company-name">{{ company?.company_name }}</h2>
        <div class="company-info">
          <el-tag :type="getCompanyTypeTagType(company?.company_type)" size="small">
            {{ getCompanyTypeLabel(company?.company_type) }}
          </el-tag>
          <el-tag :type="getStatusTagType(company?.status)" size="small">
            {{ getStatusLabel(company?.status) }}
          </el-tag>
          <el-tag :type="getRiskLevelTagType(company?.risk_level)" size="small">
            {{ getRiskLevelLabel(company?.risk_level) }}
          </el-tag>
          <span class="company-code">{{ company?.company_code }}</span>
        </div>
      </div>
      <div class="header-right">
        <el-button type="primary" :icon="Edit" @click="handleEdit">
          编辑
        </el-button>
        <el-dropdown @command="handleCommand">
          <el-button>
            更多操作<el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="view_certificates">
                <el-icon><Document /></el-icon>
                查看证照
              </el-dropdown-item>
              <el-dropdown-item command="export_data">
                <el-icon><Download /></el-icon>
                导出数据
              </el-dropdown-item>
              <el-dropdown-item command="change_status" divided>
                <el-icon><Switch /></el-icon>
                状态变更
              </el-dropdown-item>
              <el-dropdown-item command="delete" class="text-danger">
                <el-icon><Delete /></el-icon>
                删除
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <!-- 主要内容区 -->
    <div class="detail-content">
      <!-- 基本信息卡片 -->
      <el-card class="info-card">
        <template #header>
          <div class="card-header">
            <span class="card-title">基本信息</span>
          </div>
        </template>
        
        <el-descriptions :column="2" border>
          <el-descriptions-item label="单位编码">
            {{ company?.company_code || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="单位类型">
            <el-tag :type="getCompanyTypeTagType(company?.company_type)" size="small">
              {{ getCompanyTypeLabel(company?.company_type) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="法人代表">
            {{ company?.legal_person || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="联系人">
            {{ company?.contact_person || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="联系电话">
            {{ company?.contact_phone || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="联系邮箱">
            {{ company?.contact_email || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="注册地址">
            {{ company?.registered_address || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="经营地址">
            {{ company?.business_address || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="经营范围" :span="2">
            <div class="business-scope">
              {{ company?.business_scope || '-' }}
            </div>
          </el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 合作信息卡片 -->
      <el-card class="info-card">
        <template #header>
          <div class="card-header">
            <span class="card-title">合作信息</span>
          </div>
        </template>
        
        <el-descriptions :column="2" border>
          <el-descriptions-item label="合作开始日期">
            {{ formatDate(company?.cooperation_start_date) }}
          </el-descriptions-item>
          <el-descriptions-item label="合作结束日期">
            {{ formatDate(company?.cooperation_end_date) }}
          </el-descriptions-item>
          <el-descriptions-item label="审核评分">
            <el-rate
              v-model="company?.audit_score"
              disabled
              :max="5"
              show-score
              text-color="#ff9900"
              score-template="{value} 分"
            />
          </el-descriptions-item>
          <el-descriptions-item label="风险等级">
            <el-tag :type="getRiskLevelTagType(company?.risk_level)">
              {{ getRiskLevelLabel(company?.risk_level) }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 证照概览卡片 -->
      <el-card class="info-card">
        <template #header>
          <div class="card-header">
            <span class="card-title">证照概览</span>
            <el-button
              type="primary"
              link
              size="small"
              @click="handleViewCertificates"
            >
              管理证照
            </el-button>
          </div>
        </template>
        
        <div class="certificate-summary">
          <div class="summary-item">
            <div class="item-label">证照总数</div>
            <div class="item-value">{{ company?.certificate_count || 0 }}</div>
          </div>
          <div class="summary-item">
            <div class="item-label">有效证照</div>
            <div class="item-value text-success">
              {{ company?.valid_certificate_count || 0 }}
            </div>
          </div>
          <div class="summary-item">
            <div class="item-label">即将到期</div>
            <div class="item-value text-warning">
              {{ company?.expiring_certificate_count || 0 }}
            </div>
          </div>
          <div class="summary-item">
            <div class="item-label">已过期</div>
            <div class="item-value text-danger">
              {{ company?.certificate_count - company?.valid_certificate_count - company?.expiring_certificate_count || 0 }}
            </div>
          </div>
        </div>
        
        <!-- 简单的证照列表 -->
        <div class="certificate-list" v-if="certificates.length > 0">
          <h4>最新证照</h4>
          <el-table :data="certificates" stripe size="small">
            <el-table-column prop="certificate_name" label="证照名称" width="180" />
            <el-table-column prop="certificate_number" label="证照编号" width="150" />
            <el-table-column prop="certificate_status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getCertificateStatusTagType(row.certificate_status)" size="small">
                  {{ getCertificateStatusLabel(row.certificate_status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="expiry_date" label="有效期至" width="120">
              <template #default="{ row }">
                {{ formatDate(row.expiry_date) }}
              </template>
            </el-table-column>
            <el-table-column prop="review_status" label="审核状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getReviewStatusTagType(row.review_status)" size="small">
                  {{ getReviewStatusLabel(row.review_status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="viewCertificate(row)">
                  查看
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <div v-else class="empty-state">
          <el-empty description="暂无证照记录" />
        </div>
      </el-card>

      <!-- 备注信息卡片 -->
      <el-card class="info-card">
        <template #header>
          <div class="card-header">
            <span class="card-title">备注信息</span>
          </div>
        </template>
        
        <div class="remarks-content">
          <pre class="remarks-text">{{ company?.remarks || '无' }}</pre>
        </div>
      </el-card>

      <!-- 审计信息卡片 -->
      <el-card class="info-card">
        <template #header>
          <div class="card-header">
            <span class="card-title">审计信息</span>
          </div>
        </template>
        
        <el-descriptions :column="1" border>
          <el-descriptions-item label="创建人">
            {{ company?.created_by ? `用户 ${company.created_by}` : '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="更新时间">
            {{ company?.updated_by ? `用户 ${company.updated_by}` : '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">
            {{ formatDateTime(company?.created_at) }}
          </el-descriptions-item>
          <el-descriptions-item label="最后更新时间">
            {{ formatDateTime(company?.updated_at) }}
          </el-descriptions-item>
        </el-descriptions>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import {
  Edit,
  ArrowDown,
  Document,
  Download,
  Switch,
  Delete
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { Company, CompanyCertificate } from '@/types/company'
import dayjs from 'dayjs'

interface Props {
  companyId: number
}

const props = defineProps<Props>()
const emit = defineEmits(['close', 'updated'])

const router = useRouter()
const loading = ref(false)
const company = ref<Company | null>(null)
const certificates = ref<CompanyCertificate[]>([])

// 获取公司详情
const getCompanyDetail = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // 模拟数据
    company.value = {
      id: props.companyId,
      company_code: `COMP202400${props.companyId}`,
      company_name: props.companyId === 1 
        ? '上海建工集团有限公司' 
        : props.companyId === 2
        ? '北京安全技术服务有限公司'
        : '广州设备供应有限公司',
      company_type: props.companyId === 1 
        ? 'contractor' 
        : props.companyId === 2
        ? 'service_provider'
        : 'supplier',
      legal_person: props.companyId === 1 ? '张三' : '王五',
      contact_person: props.companyId === 1 ? '李四' : '赵六',
      contact_phone: props.companyId === 1 
        ? '13800138001' 
        : '13900139001',
      contact_email: props.companyId === 1 
        ? 'contact@shjg.com' 
        : 'service@bjsafety.com',
      registered_address: '示例地址',
      business_address: '示例地址',
      business_scope: '示例经营范围',
      status: 'active',
      cooperation_start_date: '2023-01-15',
      cooperation_end_date: '2026-01-14',
      risk_level: props.companyId === 1 ? 'low' : 'medium',
      audit_score: 95.5,
      remarks: '长期合作伙伴，信誉良好',
      created_by: 1,
      updated_by: 1,
      created_at: '2023-01-15T10:30:00',
      updated_at: '2024-12-20T14:25:00',
      certificate_count: 12,
      valid_certificate_count: 10,
      expiring_certificate_count: 2
    }
    
    // 模拟证照数据
    certificates.value = [
      {
        id: 1,
        company_id: props.companyId,
        certificate_type: 'business_license',
        certificate_name: '营业执照',
        certificate_number: '913101015555555555',
        issuing_authority: '上海市市场监督管理局',
        issue_date: '2023-01-15',
        expiry_date: '2028-01-14',
        is_long_term: false,
        certificate_status: 'valid',
        storage_path: '/uploads/certificates/1.pdf',
        file_name: '营业执照.pdf',
        file_size: 1024000,
        file_md5: 'abcdef123456',
        review_status: 'approved',
        review_notes: '审核通过',
        reviewed_by: 1,
        reviewed_at: '2023-01-16T10:00:00',
        created_by: 1,
        updated_by: 1,
        created_at: '2023-01-15T10:30:00',
        updated_at: '2024-12-20T14:25:00'
      },
      {
        id: 2,
        company_id: props.companyId,
        certificate_type: 'safety_production',
        certificate_name: '安全生产许可证',
        certificate_number: '(沪)JZ安许证字[2023]000001',
        issuing_authority: '上海市应急管理局',
        issue_date: '2023-03-20',
        expiry_date: '2026-03-19',
        is_long_term: false,
        certificate_status: 'expiring_soon',
        storage_path: '/uploads/certificates/2.pdf',
        file_name: '安全生产许可证.pdf',
        file_size: 950000,
        file_md5: 'fedcba654321',
        review_status: 'approved',
        review_notes: '即将到期，请注意续期',
        reviewed_by: 1,
        reviewed_at: '2023-03-21T14:30:00',
        created_by: 1,
        updated_by: 1,
        created_at: '2023-03-20T09:15:00',
        updated_at: '2024-12-20T14:25:00'
      }
    ]
  } catch (error) {
    console.error('获取公司详情失败:', error)
    ElMessage.error('获取公司详情失败')
  } finally {
    loading.value = false
  }
}

// 编辑处理
const handleEdit = () => {
  emit('updated')
}

// 查看证照
const handleViewCertificates = () => {
  router.push({
    name: 'CertificateList',
    query: {
      company_id: props.companyId,
      company_name: company.value?.company_name
    }
  })
}

// 查看单个证照
const viewCertificate = (cert: CompanyCertificate) => {
  // 这里可以打开证照详情对话框或页面
  ElMessage.info(`查看证照: ${cert.certificate_name}`)
}

// 命令处理
const handleCommand = (command: string) => {
  switch (command) {
    case 'view_certificates':
      handleViewCertificates()
      break
    case 'export_data':
      handleExportData()
      break
    case 'change_status':
      handleChangeStatus()
      break
    case 'delete':
      handleDelete()
      break
  }
}

// 导出数据
const handleExportData = () => {
  ElMessage.info('导出功能开发中')
}

// 状态变更
const handleChangeStatus = async () => {
  try {
    await ElMessageBox.prompt('请输入状态变更原因', '状态变更', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      inputPlaceholder: '请输入原因',
      inputValidator: (value) => {
        if (!value || value.trim().length < 5) {
          return '原因至少需要5个字符'
        }
        return true
      }
    })
    
    ElMessage.success('状态变更成功')
  } catch (error) {
    // 用户取消了操作
  }
}

// 删除处理
const handleDelete = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要删除单位 "${company.value?.company_name}" 吗？此操作将停用该单位，但不会删除相关证照记录。`,
      '删除确认',
      {
        confirmButtonText: '确认删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    ElMessage.success('单位已停用')
    emit('close')
  } catch (error) {
    // 用户取消了删除
  }
}

// 工具函数
const formatDate = (dateStr: string | null | undefined) => {
  if (!dateStr) return '-'
  return dayjs(dateStr).format('YYYY-MM-DD')
}

const formatDateTime = (dateStr: string | undefined) => {
  if (!dateStr) return '-'
  return dayjs(dateStr).format('YYYY-MM-DD HH:mm:ss')
}

const getCompanyTypeTagType = (type?: string) => {
  const types: Record<string, string> = {
    supplier: 'success',
    contractor: 'primary',
    service_provider: 'warning',
    other: 'info'
  }
  return types[type || ''] || 'info'
}

const getCompanyTypeLabel = (type?: string) => {
  const labels: Record<string, string> = {
    supplier: '供应商',
    contractor: '承包商',
    service_provider: '服务商',
    other: '其他'
  }
  return labels[type || ''] || '未知'
}

const getStatusTagType = (status?: string) => {
  const types: Record<string, string> = {
    active: 'success',
    inactive: 'info',
    suspended: 'warning',
    blacklisted: 'danger'
  }
  return types[status || ''] || 'info'
}

const getStatusLabel = (status?: string) => {
  const labels: Record<string, string> = {
    active: '正常',
    inactive: '未激活',
    suspended: '停用',
    blacklisted: '黑名单'
  }
  return labels[status || ''] || '未知'
}

const getRiskLevelTagType = (level?: string) => {
  const types: Record<string, string> = {
    low: 'success',
    medium: 'warning',
    high: 'danger'
  }
  return types[level || ''] || 'info'
}

const getRiskLevelLabel = (level?: string) => {
  const labels: Record<string, string> = {
    low: '低风险',
    medium: '中风险',
    high: '高风险'
  }
  return labels[level || ''] || '未知'
}

const getCertificateStatusTagType = (status: string) => {
  const types: Record<string, string> = {
    valid: 'success',
    expired: 'danger',
    expiring_soon: 'warning',
    revoked: 'info'
  }
  return types[status] || 'info'
}

const getCertificateStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    valid: '有效',
    expired: '已过期',
    expiring_soon: '即将到期',
    revoked: '已吊销'
  }
  return labels[status] || '未知'
}

const getReviewStatusTagType = (status: string) => {
  const types: Record<string, string> = {
    pending: 'info',
    approved: 'success',
    rejected: 'danger'
  }
  return types[status] || 'info'
}

const getReviewStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    pending: '待审核',
    approved: '已通过',
    rejected: '已拒绝'
  }
  return labels[status] || '未知'
}

// 监听companyId变化
watch(() => props.companyId, () => {
  getCompanyDetail()
})

// 初始化
onMounted(() => {
  getCompanyDetail()
})
</script>

<style scoped lang="scss">
.company-detail-container {
  min-height: 100%;
  background: #f5f7fa;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: white;
  border-bottom: 1px solid #ebeef5;
  
  .header-left {
    .company-name {
      font-size: 20px;
      font-weight: 600;
      margin-bottom: 8px;
      color: #303133;
    }
    
    .company-info {
      display: flex;
      align-items: center;
      gap: 8px;
      
      .company-code {
        font-size: 14px;
        color: #909399;
      }
    }
  }
  
  .header-right {
    display: flex;
    gap: 10px;
  }
}

.detail-content {
  padding: 20px;
}

.info-card {
  margin-bottom: 20px;
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .card-title {
      font-weight: 600;
      color: #303133;
    }
  }
}

.certificate-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
  
  .summary-item {
    text-align: center;
    padding: 15px;
    background: #f8f9fa;
    border-radius: 8px;
    
    .item-label {
      font-size: 14px;
      color: #909399;
      margin-bottom: 8px;
    }
    
    .item-value {
      font-size: 24px;
      font-weight: 600;
      color: #409eff;
    }
  }
}

.certificate-list {
  margin-top: 20px;
  
  h4 {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 15px;
    color: #303133;
  }
}

.empty-state {
  padding: 40px 0;
  text-align: center;
  
  :deep(.el-empty__description) {
    margin-top: 10px;
  }
}

.remarks-content {
  padding: 10px;
  
  .remarks-text {
    font-family: monospace;
    font-size: 14px;
    line-height: 1.6;
    color: #606266;
    white-space: pre-wrap;
    word-wrap: break-word;
  }
}

// 颜色类
.text-success {
  color: #67c23a;
}

.text-warning {
  color: #e6a23c;
}

.text-danger {
  color: #f56c6c;
}

// 响应式设计
@media (max-width: 768px) {
  .detail-header {
    flex-direction: column;
    align-items: flex-start;
    
    .header-right {
      margin-top: 15px;
      width: 100%;
      
      .el-button, .el-dropdown {
        width: 100%;
      }
    }
  }
  
  .certificate-summary {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>