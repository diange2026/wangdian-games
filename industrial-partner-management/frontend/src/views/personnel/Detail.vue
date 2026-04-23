<template>
  <div class="personnel-detail-page-container">
    <div class="page-header">
      <h1 class="page-title">人员详情</h1>
      <div class="action-bar">
        <el-button @click="goBack" icon="el-icon-back">返回</el-button>
        <el-button type="primary" @click="handleEdit" icon="el-icon-edit" v-if="personnelData">
          编辑
        </el-button>
        <el-button @click="handlePrint" icon="el-icon-printer">打印</el-button>
        <el-button @click="handleExport" icon="el-icon-download">导出</el-button>
      </div>
    </div>

    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>

    <div v-else-if="personnelData" class="detail-content">
      <!-- 基本信息卡片 -->
      <el-card class="card-section">
        <template #header>
          <div class="card-header">
            <h3 class="card-title">基本信息</h3>
          </div>
        </template>
        <el-row :gutter="20">
          <el-col :span="8">
            <div class="info-item">
              <label class="info-label">人员编号:</label>
              <span class="info-value">{{ personnelData.personnel_code }}</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <label class="info-label">姓名:</label>
              <span class="info-value">{{ personnelData.name }}</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <label class="info-label">所属单位:</label>
              <span class="info-value">{{ personnelData.company?.name || '未设置' }}</span>
            </div>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <div class="info-item">
              <label class="info-label">身份证号:</label>
              <span class="info-value">{{ personnelData.id_card }}</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <label class="info-label">性别:</label>
              <span class="info-value">
                {{ personnelData.gender === 'male' ? '男' : '女' }}
              </span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <label class="info-label">出生日期:</label>
              <span class="info-value">
                {{ formatDate(personnelData.birth_date) }}
              </span>
            </div>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <div class="info-item">
              <label class="info-label">联系电话:</label>
              <span class="info-value">{{ personnelData.phone || '未设置' }}</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <label class="info-label">电子邮箱:</label>
              <span class="info-value">{{ personnelData.email || '未设置' }}</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <label class="info-label">岗位/职务:</label>
              <span class="info-value">{{ personnelData.position || '未设置' }}</span>
            </div>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <div class="info-item">
              <label class="info-label">工种/岗位类型:</label>
              <span class="info-value">{{ personnelData.work_type || '未设置' }}</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <label class="info-label">入职日期:</label>
              <span class="info-value">
                {{ formatDate(personnelData.hire_date) }}
              </span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <label class="info-label">在职状态:</label>
              <el-tag
                :type="getEmploymentStatusType(personnelData.employment_status)"
                size="small"
              >
                {{ getEmploymentStatusText(personnelData.employment_status) }}
              </el-tag>
            </div>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <div class="info-item">
              <label class="info-label">审核状态:</label>
              <el-tag
                :type="getStatusType(personnelData.status)"
                size="small"
              >
                {{ getStatusText(personnelData.status) }}
              </el-tag>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <label class="info-label">创建时间:</label>
              <span class="info-value">
                {{ formatDateTime(personnelData.created_at) }}
              </span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <label class="info-label">更新时间:</label>
              <span class="info-value">
                {{ formatDateTime(personnelData.updated_at) }}
              </span>
            </div>
          </el-col>
        </el-row>
      </el-card>

      <!-- 证书信息 -->
      <el-card class="card-section">
        <template #header>
          <div class="card-header">
            <h3 class="card-title">证书信息</h3>
            <el-button type="primary" size="small" @click="handleAddCertificate">
              添加证书
            </el-button>
          </div>
        </template>
        <el-table
          :data="certificateList"
          v-loading="certificatesLoading"
          border
          size="small"
          style="width: 100%"
        >
          <el-table-column label="证书名称" prop="certificate_name" min-width="150" />
          <el-table-column label="证书类型" prop="certificate_type" width="120" />
          <el-table-column label="证书编号" prop="certificate_number" width="150" />
          <el-table-column label="发证日期" width="100">
            <template #default="{ row }">
              {{ formatDate(row.issue_date) }}
            </template>
          </el-table-column>
          <el-table-column label="到期日期" width="100">
            <template #default="{ row }">
              <span :class="{ 'expired-text': isExpired(row.expiry_date) }">
                {{ formatDate(row.expiry_date) }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="证书状态" width="100">
            <template #default="{ row }">
              <el-tag
                :type="getCertificateStatusType(row.certificate_status)"
                size="small"
              >
                {{ getCertificateStatusText(row.certificate_status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="审核状态" width="100">
            <template #default="{ row }">
              <el-tag
                :type="getApprovalStatusType(row.approval_status)"
                size="small"
              >
                {{ getApprovalStatusText(row.approval_status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="发证机构" prop="issuing_authority" min-width="150" show-overflow-tooltip />
          <el-table-column label="操作" fixed="right" width="120" align="center">
            <template #default="{ row }">
              <el-button type="text" size="small" @click="handleViewCertificate(row)">
                查看
              </el-button>
              <el-button type="text" size="small" @click="handleEditCertificate(row)">
                编辑
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <!-- 培训记录 -->
      <el-card class="card-section">
        <template #header>
          <div class="card-header">
            <h3 class="card-title">培训记录</h3>
            <el-button type="primary" size="small" @click="handleAddTraining">
              添加培训记录
            </el-button>
          </div>
        </template>
        <el-table
          :data="trainingList"
          v-loading="trainingsLoading"
          border
          size="small"
          style="width: 100%"
        >
          <el-table-column label="培训名称" prop="training_name" min-width="150" />
          <el-table-column label="培训类型" prop="training_type" width="120" />
          <el-table-column label="培训日期" width="100">
            <template #default="{ row }">
              {{ formatDate(row.training_date) }}
            </template>
          </el-table-column>
          <el-table-column label="培训机构" prop="training_institution" min-width="150" show-overflow-tooltip />
          <el-table-column label="培训时长" width="100">
            <template #default="{ row }">
              {{ row.training_duration ? row.training_duration + '小时' : '-' }}
            </template>
          </el-table-column>
          <el-table-column label="培训成绩" width="90">
            <template #default="{ row }">
              {{ row.training_score ? row.training_score + '分' : '-' }}
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
          <el-table-column label="备注" prop="notes" min-width="200" show-overflow-tooltip />
          <el-table-column label="操作" fixed="right" width="100" align="center">
            <template #default="{ row }">
              <el-button type="text" size="small" @click="handleEditTraining(row)">
                编辑
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>

    <div v-else class="error-container">
      <el-empty description="人员不存在或已被删除" />
      <el-button type="primary" @click="goBack">返回人员列表</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getPersonnelDetail, getPersonnelCertificates, getPersonnelTrainings } from '@/api/personnel'
import type { PersonnelInDB, PersonnelCertificateInDB, PersonnelTrainingRecordInDB } from '@/types/personnel'

const route = useRoute()
const router = useRouter()
const loading = ref(true)
const personnelData = ref<PersonnelInDB | null>(null)
const certificateList = ref<PersonnelCertificateInDB[]>([])
const trainingList = ref<PersonnelTrainingRecordInDB[]>([])
const certificatesLoading = ref(false)
const trainingsLoading = ref(false)

const personnelId = computed(() => {
  const id = route.params.id
  return id ? Number(id) : 0
})

onMounted(async () => {
  if (personnelId.value) {
    await loadPersonnelDetail()
  } else {
    ElMessage.error('无效的人员ID')
    router.push({ name: 'PersonnelList' })
  }
})

const loadPersonnelDetail = async () => {
  loading.value = true
  try {
    personnelData.value = await getPersonnelDetail(personnelId.value)
    await loadCertificates()
    await loadTrainings()
  } catch (error) {
    console.error('加载人员详情失败:', error)
    ElMessage.error('加载人员详情失败')
  } finally {
    loading.value = false
  }
}

const loadCertificates = async () => {
  certificatesLoading.value = true
  try {
    const response = await getPersonnelCertificates(personnelId.value, {
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

const loadTrainings = async () => {
  trainingsLoading.value = true
  try {
    const response = await getPersonnelTrainings(personnelId.value, {
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

const goBack = () => {
  router.push({ name: 'PersonnelList' })
}

const handleEdit = () => {
  router.push({
    name: 'PersonnelEdit',
    params: { id: personnelId.value }
  })
}

const handlePrint = () => {
  ElMessage.info('打印功能开发中...')
}

const handleExport = () => {
  ElMessage.info('导出功能开发中...')
}

const handleAddCertificate = () => {
  ElMessage.info('添加证书功能开发中...')
}

const handleViewCertificate = (certificate: PersonnelCertificateInDB) => {
  console.log('查看证书:', certificate)
  ElMessage.info('证书详情功能开发中...')
}

const handleEditCertificate = (certificate: PersonnelCertificateInDB) => {
  console.log('编辑证书:', certificate)
  ElMessage.info('编辑证书功能开发中...')
}

const handleAddTraining = () => {
  ElMessage.info('添加培训记录功能开发中...')
}

const handleEditTraining = (training: PersonnelTrainingRecordInDB) => {
  console.log('编辑培训记录:', training)
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
</script>

<style scoped>
.personnel-detail-page-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 84px);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.action-bar {
  display: flex;
  gap: 10px;
}

.loading-container,
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100px 20px;
}

.error-container {
  text-align: center;
}

.error-container .el-button {
  margin-top: 20px;
}

.detail-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.card-section {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.info-item {
  margin-bottom: 12px;
  padding: 8px 0;
}

.info-label {
  font-weight: 600;
  color: #606266;
  margin-right: 10px;
  min-width: 100px;
  display: inline-block;
}

.info-value {
  color: #303133;
}

.expired-text {
  color: #f56c6c;
  font-weight: 500;
}
</style>