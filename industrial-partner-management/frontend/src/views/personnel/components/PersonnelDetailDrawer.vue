<template>
  <el-drawer
    v-model="visible"
    title="人员详细信息"
    :size="'800px'"
    direction="rtl"
    destroy-on-close
    @close="handleClose"
  >
    <div class="personnel-detail-container" v-loading="loading">
      <!-- 基本信息卡片 -->
      <div class="basic-info-card" v-if="personnelDetail">
        <div class="card-header">
          <h3 class="card-title">
            <i class="el-icon-user"></i>
            基本信息
          </h3>
          <el-button
            type="primary"
            size="small"
            @click="handleEdit"
            icon="el-icon-edit"
          >
            编辑
          </el-button>
        </div>

        <div class="info-grid">
          <div class="info-item">
            <label class="info-label">人员编号:</label>
            <span class="info-value">{{ personnelDetail.personnelCode }}</span>
          </div>
          <div class="info-item">
            <label class="info-label">姓名:</label>
            <span class="info-value">{{ personnelDetail.name }}</span>
          </div>
          <div class="info-item">
            <label class="info-label">所属单位:</label>
            <span class="info-value">{{ personnelDetail.company?.name || '未设置' }}</span>
          </div>
          <div class="info-item">
            <label class="info-label">身份证号:</label>
            <span class="info-value">{{ personnelDetail.idCard }}</span>
          </div>
          <div class="info-item">
            <label class="info-label">性别:</label>
            <span class="info-value">
              {{ personnelDetail.gender === 'male' ? '男' : '女' }}
            </span>
          </div>
          <div class="info-item">
            <label class="info-label">出生日期:</label>
            <span class="info-value">
              {{ formatDate(personnelDetail.birthDate) }}
            </span>
          </div>
          <div class="info-item">
            <label class="info-label">联系电话:</label>
            <span class="info-value">{{ personnelDetail.phone || '未设置' }}</span>
          </div>
          <div class="info-item">
            <label class="info-label">电子邮箱:</label>
            <span class="info-value">{{ personnelDetail.email || '未设置' }}</span>
          </div>
          <div class="info-item">
            <label class="info-label">岗位/职务:</label>
            <span class="info-value">{{ personnelDetail.position || '未设置' }}</span>
          </div>
          <div class="info-item">
            <label class="info-label">工种/岗位类型:</label>
            <span class="info-value">{{ personnelDetail.workType || '未设置' }}</span>
          </div>
          <div class="info-item">
            <label class="info-label">入职日期:</label>
            <span class="info-value">
              {{ formatDate(personnelDetail.hireDate) }}
            </span>
          </div>
          <div class="info-item">
            <label class="info-label">在职状态:</label>
            <el-tag
              :type="getEmploymentStatusType(personnelDetail.employmentStatus)"
              size="small"
            >
              {{ getEmploymentStatusText(personnelDetail.employmentStatus) }}
            </el-tag>
          </div>
          <div class="info-item">
            <label class="info-label">审核状态:</label>
            <el-tag
              :type="getStatusType(personnelDetail.status)"
              size="small"
            >
              {{ getStatusText(personnelDetail.status) }}
            </el-tag>
          </div>
        </div>

        <!-- 照片区域 -->
        <div class="photo-section" v-if="personnelDetail.photoUrl">
          <h4>人员照片</h4>
          <div class="photo-container">
            <el-image
              :src="personnelDetail.photoUrl"
              fit="cover"
              style="width: 150px; height: 200px; border-radius: 8px;"
            >
              <template #error>
                <div class="image-error">照片加载失败</div>
              </template>
            </el-image>
          </div>
        </div>
      </div>

      <!-- 证书管理标签页 -->
      <div class="tab-section">
        <el-tabs v-model="activeTab">
          <!-- 证书管理 -->
          <el-tab-pane label="证书管理" name="certificates">
            <div class="tab-header">
              <h4>证书列表</h4>
              <el-button
                type="primary"
                size="small"
                @click="handleAddCertificate"
                icon="el-icon-plus"
                :disabled="!personnelDetail"
              >
                添加证书
              </el-button>
            </div>

            <el-table
              :data="certificateList"
              v-loading="certificatesLoading"
              border
              size="small"
              style="width: 100%; margin-top: 10px;"
            >
              <el-table-column label="证书名称" prop="certificateName" min-width="150" />
              <el-table-column label="证书类型" prop="certificateType" width="120" />
              <el-table-column label="证书编号" prop="certificateNumber" width="150" />
              <el-table-column label="发证机构" prop="issuingAuthority" min-width="150" show-overflow-tooltip />
              <el-table-column label="发证日期" width="100">
                <template #default="{ row }">
                  {{ formatDate(row.issueDate) }}
                </template>
              </el-table-column>
              <el-table-column label="到期日期" width="100">
                <template #default="{ row }">
                  <span :class="{ 'expired-text': isExpired(row.expiryDate) }">
                    {{ formatDate(row.expiryDate) }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column label="证书状态" width="100">
                <template #default="{ row }">
                  <el-tag
                    :type="getCertificateStatusType(row.certificateStatus)"
                    size="small"
                  >
                    {{ getCertificateStatusText(row.certificateStatus) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="审核状态" width="100">
                <template #default="{ row }">
                  <el-tag
                    :type="getApprovalStatusType(row.approvalStatus)"
                    size="small"
                  >
                    {{ getApprovalStatusText(row.approvalStatus) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" fixed="right" width="150" align="center">
                <template #default="{ row }">
                  <el-button
                    type="text"
                    size="small"
                    @click="handleViewCertificate(row)"
                    icon="el-icon-view"
                  >
                    查看
                  </el-button>
                  <el-button
                    type="text"
                    size="small"
                    @click="handleEditCertificate(row)"
                    icon="el-icon-edit"
                  >
                    编辑
                  </el-button>
                </template>
              </el-table-column>
            </el-table>

            <!-- 证书统计 -->
            <div class="certificate-stats" v-if="certificateStats">
              <el-row :gutter="20" style="margin-top: 20px;">
                <el-col :span="6">
                  <div class="stat-item">
                    <div class="stat-label">总证书数</div>
                    <div class="stat-value">{{ certificateStats.totalCertificates || 0 }}</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-item">
                    <div class="stat-label">有效证书</div>
                    <div class="stat-value">{{ certificateStats.validCertificates || 0 }}</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-item">
                    <div class="stat-label">过期证书</div>
                    <div class="stat-value">{{ certificateStats.expiredCertificates || 0 }}</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-item">
                    <div class="stat-label">待审核证书</div>
                    <div class="stat-value">{{ certificateStats.pendingReviewCertificates || 0 }}</div>
                  </div>
                </el-col>
              </el-row>
            </div>
          </el-tab-pane>

          <!-- 培训记录 -->
          <el-tab-pane label="培训记录" name="trainings">
            <div class="tab-header">
              <h4>培训记录列表</h4>
              <el-button
                type="primary"
                size="small"
                @click="handleAddTraining"
                icon="el-icon-plus"
                :disabled="!personnelDetail"
              >
                添加培训记录
              </el-button>
            </div>

            <el-table
              :data="trainingList"
              v-loading="trainingsLoading"
              border
              size="small"
              style="width: 100%; margin-top: 10px;"
            >
              <el-table-column label="培训名称" prop="trainingName" min-width="150" />
              <el-table-column label="培训类型" prop="trainingType" width="100" />
              <el-table-column label="培训日期" width="100">
                <template #default="{ row }">
                  {{ formatDate(row.trainingDate) }}
                </template>
              </el-table-column>
              <el-table-column label="培训时长（小时）" width="120">
                <template #default="{ row }">
                  {{ row.trainingDuration || '-' }}
                </template>
              </el-table-column>
              <el-table-column label="培训机构" prop="trainingInstitution" min-width="150" show-overflow-tooltip />
              <el-table-column label="培训讲师" prop="trainer" width="100" />
              <el-table-column label="培训成绩" width="90">
                <template #default="{ row }">
                  {{ row.trainingScore ? row.trainingScore + '分' : '-' }}
                </template>
              </el-table-column>
              <el-table-column label="是否通过" width="90">
                <template #default="{ row }">
                  <el-tag
                    v-if="row.is_passed !== null"
                    :type="row.is_passed ? 'success' : 'danger'"
                    size="small"
                  >
                    {{ row.is_passed ? '通过' : '未通过' }}
                  </el-tag>
                  <span v-else>-</span>
                </template>
              </el-table-column>
              <el-table-column label="培训证书编号" prop="certificateNumber" width="150" />
              <el-table-column label="备注" prop="notes" min-width="200" show-overflow-tooltip />
              <el-table-column label="操作" fixed="right" width="120" align="center">
                <template #default="{ row }">
                  <el-button
                    type="text"
                    size="small"
                    @click="handleEditTraining(row)"
                    icon="el-icon-edit"
                  >
                    编辑
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>

          <!-- 预警记录 -->
          <el-tab-pane label="预警记录" name="alerts">
            <div class="tab-header">
              <h4>证书预警记录</h4>
            </div>

            <el-table
              :data="alertList"
              v-loading="alertsLoading"
              border
              size="small"
              style="width: 100%; margin-top: 10px;"
            >
              <el-table-column label="预警类型" prop="alertType" width="100">
                <template #default="{ row }">
                  {{ getAlertTypeText(row.alertType) }}
                </template>
              </el-table-column>
              <el-table-column label="证书名称" prop="certificate.certificateName" min-width="150" />
              <el-table-column label="预警日期" width="100">
                <template #default="{ row }">
                  {{ formatDate(row.alertDate) }}
                </template>
              </el-table-column>
              <el-table-column label="证书到期日期" width="110">
                <template #default="{ row }">
                  {{ formatDate(row.expiryDate) }}
                </template>
              </el-table-column>
              <el-table-column label="剩余天数" prop="daysLeft" width="90" align="center">
                <template #default="{ row }">
                  <el-tag
                    :type="row.daysLeft < 7 ? 'danger' : row.daysLeft < 30 ? 'warning' : 'success'"
                    size="small"
                  >
                    {{ row.daysLeft }}天
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="预警渠道" prop="alertChannel" width="100">
                <template #default="{ row }">
                  {{ getAlertChannelText(row.alertChannel) }}
                </template>
              </el-table-column>
              <el-table-column label="发送状态" width="100" align="center">
                <template #default="{ row }">
                  <el-tag
                    :type="row.isSent ? 'success' : 'warning'"
                    size="small"
                  >
                    {{ row.isSent ? '已发送' : '待发送' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="预警内容" prop="alertContent" min-width="200" show-overflow-tooltip />
              <el-table-column label="发送对象" prop="sentTo" width="150" show-overflow-tooltip />
              <el-table-column label="发送时间" width="160">
                <template #default="{ row }">
                  {{ row.sentAt ? formatDateTime(row.sentAt) : '-' }}
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </el-drawer>
</template>

<script setup lang="ts">
import { ref, watch, defineProps, defineEmits } from 'vue'
import { ElMessage } from 'element-plus'
import {
  getPersonnelDetail,
  getPersonnelCertificates,
  getPersonnelTrainings,
  getPersonnelCertificateStats
} from '@/api/personnel'
import type {
  PersonnelInDB,
  PersonnelCertificateInDB,
  PersonnelTrainingRecordInDB,
  PersonnelCertificateAlertLogInDB,
  CertificateStats
} from '@/types/personnel'

// 属性定义
const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  personnelId: {
    type: Number,
    default: null
  }
})

// 事件定义
const emit = defineEmits([
  'update:modelValue',
  'refresh',
  'edit'
])

// 响应式数据
const visible = ref(props.modelValue)
const loading = ref(false)
const personnelDetail = ref<PersonnelInDB | null>(null)

// 标签页相关
const activeTab = ref('certificates')
const certificatesLoading = ref(false)
const trainingsLoading = ref(false)
const alertsLoading = ref(false)
const certificateList = ref<PersonnelCertificateInDB[]>([])
const trainingList = ref<PersonnelTrainingRecordInDB[]>([])
const alertList = ref<PersonnelCertificateAlertLogInDB[]>([])
const certificateStats = ref<CertificateStats | null>(null)

// 监听属性变化
watch(() => props.modelValue, (val) => {
  visible.value = val
})

watch(() => props.personnelId, (val) => {
  if (val && visible.value) {
    loadPersonnelDetail()
  }
})

watch(visible, (val) => {
  emit('update:modelValue', val)
  if (val && props.personnelId) {
    loadPersonnelDetail()
  } else {
    resetData()
  }
})

watch(activeTab, (val) => {
  if (val && props.personnelId) {
    loadTabData(val)
  }
})

// 加载人员详情
const loadPersonnelDetail = async () => {
  if (!props.personnelId) return
  
  loading.value = true
  try {
    personnelDetail.value = await getPersonnelDetail(props.personnelId)
    loadTabData(activeTab.value)
  } catch (error) {
    console.error('加载人员详情失败:', error)
    ElMessage.error('加载人员详情失败')
  } finally {
    loading.value = false
  }
}

// 加载标签页数据
const loadTabData = async (tab: string) => {
  if (!props.personnelId) return

  switch (tab) {
    case 'certificates':
      await loadCertificates()
      await loadCertificateStats()
      break
    case 'trainings':
      await loadTrainings()
      break
    case 'alerts':
      await loadAlerts()
      break
  }
}

// 加载证书列表
const loadCertificates = async () => {
  certificatesLoading.value = true
  try {
    const response = await getPersonnelCertificates(props.personnelId!, {
      page: 1,
      pageSize: 100
    })
    certificateList.value = response.items || []
  } catch (error) {
    console.error('加载证书列表失败:', error)
  } finally {
    certificatesLoading.value = false
  }
}

// 加载证书统计
const loadCertificateStats = async () => {
  try {
    const response = await getPersonnelCertificateStats({ personnelId: props.personnelId })
    certificateStats.value = response
  } catch (error) {
    console.error('加载证书统计失败:', error)
  }
}

// 加载培训记录
const loadTrainings = async () => {
  trainingsLoading.value = true
  try {
    const response = await getPersonnelTrainings(props.personnelId!, {
      page: 1,
      pageSize: 50
    })
    trainingList.value = response.items || []
  } catch (error) {
    console.error('加载培训记录失败:', error)
  } finally {
    trainingsLoading.value = false
  }
}

// 加载预警记录
const loadAlerts = async () => {
  alertsLoading.value = true
  try {
    // 这里需要根据实际情况调用API
    // 暂时使用空数据
    alertList.value = []
  } catch (error) {
    console.error('加载预警记录失败:', error)
  } finally {
    alertsLoading.value = false
  }
}

// 重置数据
const resetData = () => {
  personnelDetail.value = null
  certificateList.value = []
  trainingList.value = []
  alertList.value = []
  certificateStats.value = null
  activeTab.value = 'certificates'
}

// 关闭抽屉
const handleClose = () => {
  visible.value = false
}

// 编辑人员
const handleEdit = () => {
  emit('edit', personnelDetail.value)
}

// 添加证书
const handleAddCertificate = () => {
  ElMessage.info('添加证书功能开发中...')
}

// 查看证书
const handleViewCertificate = (certificate: PersonnelCertificateInDB) => {
  console.log('查看证书:', certificate)
}

// 编辑证书
const handleEditCertificate = (certificate: PersonnelCertificateInDB) => {
  ElMessage.info('编辑证书功能开发中...')
}

// 添加培训记录
const handleAddTraining = () => {
  ElMessage.info('添加培训记录功能开发中...')
}

// 编辑培训记录
const handleEditTraining = (training: PersonnelTrainingRecordInDB) => {
  ElMessage.info('编辑培训记录功能开发中...')
}

// 工具函数
const formatDate = (date: string | Date | null) => {
  if (!date) return '-'
  const d = new Date(date)
  return d.toLocaleDateString('zh-CN')
}

const formatDateTime = (dateTime: string) => {
  if (!dateTime) return '-'
  const date = new Date(dateTime)
  return date.toLocaleString('zh-CN')
}

const isExpired = (expiryDate: string | Date) => {
  if (!expiryDate) return false
  const today = new Date()
  const expiry = new Date(expiryDate)
  return expiry < today
}

const getEmploymentStatusType = (status: string) => {
  const typeMap: Record<string, string> = {
    active: 'success',
    inactive: 'info',
    suspended: 'warning',
    terminated: 'danger'
  }
  return typeMap[status] || 'info'
}

const getEmploymentStatusText = (status: string) => {
  const textMap: Record<string, string> = {
    active: '在职',
    inactive: '离职',
    suspended: '停职',
    terminated: '解雇'
  }
  return textMap[status] || '未知'
}

const getStatusType = (status: string) => {
  const typeMap: Record<string, string> = {
    pending_review: 'warning',
    approved: 'success',
    rejected: 'danger',
    expired: 'info'
  }
  return typeMap[status] || 'info'
}

const getStatusText = (status: string) => {
  const textMap: Record<string, string> = {
    pending_review: '待审核',
    approved: '已通过',
    rejected: '已拒绝',
    expired: '已过期'
  }
  return textMap[status] || '未知'
}

const getCertificateStatusType = (status: string) => {
  const typeMap: Record<string, string> = {
    valid: 'success',
    expired: 'danger',
    suspended: 'warning',
    revoked: 'info'
  }
  return typeMap[status] || 'info'
}

const getCertificateStatusText = (status: string) => {
  const textMap: Record<string, string> = {
    valid: '有效',
    expired: '过期',
    suspended: '停用',
    revoked: '吊销'
  }
  return textMap[status] || '未知'
}

const getApprovalStatusType = (status: string) => {
  const typeMap: Record<string, string> = {
    pending_review: 'warning',
    approved: 'success',
    rejected: 'danger'
  }
  return typeMap[status] || 'info'
}

const getApprovalStatusText = (status: string) => {
  const textMap: Record<string, string> = {
    pending_review: '待审核',
    approved: '已通过',
    rejected: '已拒绝'
  }
  return textMap[status] || '未知'
}

const getAlertTypeText = (type: string) => {
  const textMap: Record<string, string> = {
    first_alert: '首次预警',
    second_alert: '二次预警',
    third_alert: '最终预警'
  }
  return textMap[type] || '未知'
}

const getAlertChannelText = (channel: string) => {
  const textMap: Record<string, string> = {
    email: '邮件',
    sms: '短信',
    wechat: '微信',
    system: '系统通知'
  }
  return textMap[channel] || '未知'
}
</script>

<style scoped>
.personnel-detail-container {
  padding: 20px;
}

.basic-info-card {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  display: flex;
  align-items: center;
  gap: 10px;
}

.card-title i {
  color: #409eff;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.info-item {
  display: flex;
  align-items: center;
  padding: 8px 0;
}

.info-label {
  font-weight: 600;
  color: #606266;
  min-width: 120px;
  margin-right: 10px;
}

.info-value {
  color: #303133;
  flex: 1;
}

.photo-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

.photo-section h4 {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 10px;
}

.photo-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #ebeef5;
}

.image-error {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 200px;
  background: #f5f7fa;
  border-radius: 8px;
  color: #909399;
}

.tab-section {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.tab-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.tab-header h4 {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.stat-item {
  text-align: center;
  padding: 10px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.expired-text {
  color: #f56c6c;
  font-weight: 500;
}
</style>