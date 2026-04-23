<template>
  <div class="personnel-management-container">
    <!-- 页面标题和操作栏 -->
    <div class="page-header">
      <h1 class="page-title">
        <i class="el-icon-user"></i>
        人员资质管理
      </h1>
      <div class="action-bar">
        <el-button type="primary" @click="handleAddPersonnel" icon="el-icon-plus">
          新增人员
        </el-button>
        <el-button @click="handleExport" icon="el-icon-download">
          导出
        </el-button>
        <el-button @click="handleRefresh" icon="el-icon-refresh">
          刷新
        </el-button>
      </div>
    </div>

    <!-- 筛选条件 -->
    <div class="filter-card">
      <el-form :model="queryParams" ref="queryForm" :inline="true" label-width="80px">
        <el-form-item label="所属单位" prop="companyId">
          <el-select
            v-model="queryParams.companyId"
            placeholder="请选择单位"
            clearable
            style="width: 200px"
            @change="handleQuery"
          >
            <el-option
              v-for="company in companyList"
              :key="company.id"
              :label="company.name"
              :value="company.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input
            v-model="queryParams.name"
            placeholder="请输入姓名"
            clearable
            style="width: 200px"
            @keyup.enter="handleQuery"
          />
        </el-form-item>
        <el-form-item label="人员编号" prop="personnelCode">
          <el-input
            v-model="queryParams.personnelCode"
            placeholder="请输入人员编号"
            clearable
            style="width: 200px"
            @keyup.enter="handleQuery"
          />
        </el-form-item>
        <el-form-item label="在职状态" prop="employmentStatus">
          <el-select
            v-model="queryParams.employmentStatus"
            placeholder="请选择状态"
            clearable
            style="width: 200px"
            @change="handleQuery"
          >
            <el-option label="在职" value="active" />
            <el-option label="离职" value="inactive" />
            <el-option label="停职" value="suspended" />
            <el-option label="解雇" value="terminated" />
          </el-select>
        </el-form-item>
        <el-form-item label="审核状态" prop="status">
          <el-select
            v-model="queryParams.status"
            placeholder="请选择审核状态"
            clearable
            style="width: 200px"
            @change="handleQuery"
          >
            <el-option label="待审核" value="pending_review" />
            <el-option label="已通过" value="approved" />
            <el-option label="已拒绝" value="rejected" />
            <el-option label="已过期" value="expired" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleQuery" icon="el-icon-search">
            搜索
          </el-button>
          <el-button @click="resetQuery" icon="el-icon-refresh">
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-card">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-item stat-total">
            <div class="stat-icon">
              <i class="el-icon-user-solid"></i>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.totalPersonnel || 0 }}</div>
              <div class="stat-label">总人员数</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item stat-active">
            <div class="stat-icon">
              <i class="el-icon-success"></i>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.activePersonnel || 0 }}</div>
              <div class="stat-label">在职人员</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item stat-pending">
            <div class="stat-icon">
              <i class="el-icon-time"></i>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.pendingReviewPersonnel || 0 }}</div>
              <div class="stat-label">待审核人员</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item stat-warning">
            <div class="stat-icon">
              <i class="el-icon-warning-outline"></i>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.expiringSoonCertificates || 0 }}</div>
              <div class="stat-label">即将过期证书</div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 人员数据表格 -->
    <div class="data-table-card">
      <el-table
        :data="personnelList"
        v-loading="loading"
        border
        stripe
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column label="人员编号" prop="personnelCode" width="120" align="center" />
        <el-table-column label="姓名" prop="name" width="100">
          <template #default="{ row }">
            <div class="personnel-name">
              <el-avatar v-if="row.photoUrl" :src="row.photoUrl" size="small"></el-avatar>
              <el-avatar v-else size="small">{{ row.name.charAt(0) }}</el-avatar>
              <span class="name-text">{{ row.name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="所属单位" prop="companyName" width="180" show-overflow-tooltip />
        <el-table-column label="身份证号" prop="idCard" width="180" />
        <el-table-column label="性别" prop="gender" width="80" align="center">
          <template #default="{ row }">
            <el-tag :type="row.gender === 'male' ? 'primary' : 'danger'" size="small">
              {{ row.gender === 'male' ? '男' : '女' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="岗位/职务" prop="position" width="120" show-overflow-tooltip />
        <el-table-column label="在职状态" prop="employmentStatus" width="100" align="center">
          <template #default="{ row }">
            <el-tag
              :type="getEmploymentStatusType(row.employmentStatus)"
              size="small"
            >
              {{ getEmploymentStatusText(row.employmentStatus) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="审核状态" prop="status" width="100" align="center">
          <template #default="{ row }">
            <el-tag
              :type="getStatusType(row.status)"
              size="small"
            >
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" prop="createdAt" width="160">
          <template #default="{ row }">
            {{ formatDateTime(row.createdAt) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="220" align="center">
          <template #default="{ row }">
            <el-button
              type="text"
              size="small"
              @click="handleView(row)"
              icon="el-icon-view"
            >
              查看
            </el-button>
            <el-button
              type="text"
              size="small"
              @click="handleEdit(row)"
              icon="el-icon-edit"
            >
              编辑
            </el-button>
            <el-button
              type="text"
              size="small"
              @click="handleManageCertificates(row)"
              icon="el-icon-document"
            >
              证书
            </el-button>
            <el-button
              type="text"
              size="small"
              @click="handleDelete(row)"
              icon="el-icon-delete"
              style="color: #f56c6c"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="queryParams.page"
          v-model:page-size="queryParams.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <!-- 人员详情抽屉 -->
    <personnel-detail-drawer
      v-model="detailDrawerVisible"
      :personnel-id="currentPersonnelId"
      @refresh="getList"
    />

    <!-- 人员表单对话框 -->
    <personnel-form-dialog
      v-model="formDialogVisible"
      :personnel-data="currentPersonnel"
      @success="handleFormSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getPersonnelList, getPersonnelStats, deletePersonnel } from '@/api/personnel'
import { getCompanyList } from '@/api/company'
import PersonnelDetailDrawer from './components/PersonnelDetailDrawer.vue'
import PersonnelFormDialog from './components/PersonnelFormDialog.vue'
import type { PersonnelSimple } from '@/types/personnel'

// 响应式数据
const loading = ref(false)
const personnelList = ref<PersonnelSimple[]>([])
const companyList = ref<any[]>([])
const total = ref(0)
const selectedRows = ref<PersonnelSimple[]>([])
const detailDrawerVisible = ref(false)
const formDialogVisible = ref(false)
const currentPersonnelId = ref<number | null>(null)
const currentPersonnel = ref<Partial<PersonnelSimple> | null>(null)

// 统计信息
const stats = reactive({
  totalPersonnel: 0,
  activePersonnel: 0,
  pendingReviewPersonnel: 0,
  expiredCertificates: 0,
  expiringSoonCertificates: 0
})

// 查询参数
const queryParams = reactive({
  companyId: undefined as number | undefined,
  name: '',
  personnelCode: '',
  employmentStatus: '',
  status: '',
  page: 1,
  pageSize: 20
})

// 生命周期钩子
onMounted(() => {
  getCompanyOptions()
  getList()
  getStats()
})

// 获取单位列表
const getCompanyOptions = async () => {
  try {
    const response = await getCompanyList({ page: 1, pageSize: 1000 })
    companyList.value = response.items || []
  } catch (error) {
    console.error('获取单位列表失败:', error)
  }
}

// 获取人员列表
const getList = async () => {
  loading.value = true
  try {
    const response = await getPersonnelList(queryParams)
    personnelList.value = response.items || []
    total.value = response.total || 0
  } catch (error) {
    console.error('获取人员列表失败:', error)
    ElMessage.error('获取人员列表失败')
  } finally {
    loading.value = false
  }
}

// 获取统计信息
const getStats = async () => {
  try {
    const response = await getPersonnelStats({ companyId: queryParams.companyId })
    Object.assign(stats, response)
  } catch (error) {
    console.error('获取统计信息失败:', error)
  }
}

// 查询处理
const handleQuery = () => {
  queryParams.page = 1
  getList()
  getStats()
}

// 重置查询
const resetQuery = () => {
  Object.assign(queryParams, {
    companyId: undefined,
    name: '',
    personnelCode: '',
    employmentStatus: '',
    status: '',
    page: 1,
    pageSize: 20
  })
  handleQuery()
}

// 分页大小变化
const handleSizeChange = (val: number) => {
  queryParams.pageSize = val
  queryParams.page = 1
  getList()
}

// 页码变化
const handleCurrentChange = (val: number) => {
  queryParams.page = val
  getList()
}

// 表格选择变化
const handleSelectionChange = (selection: PersonnelSimple[]) => {
  selectedRows.value = selection
}

// 查看详情
const handleView = (row: PersonnelSimple) => {
  currentPersonnelId.value = row.id
  detailDrawerVisible.value = true
}

// 编辑人员
const handleEdit = (row: PersonnelSimple) => {
  currentPersonnel.value = { ...row }
  formDialogVisible.value = true
}

// 新增人员
const handleAddPersonnel = () => {
  currentPersonnel.value = null
  formDialogVisible.value = true
}

// 管理证书
const handleManageCertificates = (row: PersonnelSimple) => {
  // 这里可以跳转到证书管理页面
  ElMessage.info('证书管理功能开发中...')
}

// 删除人员
const handleDelete = (row: PersonnelSimple) => {
  ElMessageBox.confirm(
    `确定要删除人员 "${row.name}" 吗？删除后无法恢复！`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deletePersonnel(row.id)
      ElMessage.success('删除成功')
      getList()
      getStats()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {
    // 用户取消操作
  })
}

// 导出数据
const handleExport = () => {
  ElMessage.info('导出功能开发中...')
}

// 刷新数据
const handleRefresh = () => {
  getList()
  getStats()
}

// 表单提交成功处理
const handleFormSuccess = () => {
  getList()
  getStats()
}

// 工具函数
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

const formatDateTime = (dateTime: string) => {
  if (!dateTime) return ''
  const date = new Date(dateTime)
  return date.toLocaleString('zh-CN')
}
</script>

<style scoped>
.personnel-management-container {
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
  display: flex;
  align-items: center;
  gap: 10px;
}

.page-title i {
  color: #409eff;
}

.action-bar {
  display: flex;
  gap: 10px;
}

.filter-card {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.stats-card {
  margin-bottom: 20px;
}

.stat-item {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  font-size: 24px;
  color: #fff;
}

.stat-total .stat-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-active .stat-icon {
  background: linear-gradient(135deg, #5cb85c 0%, #4cae4c 100%);
}

.stat-pending .stat-icon {
  background: linear-gradient(135deg, #f0ad4e 0%, #eea236 100%);
}

.stat-warning .stat-icon {
  background: linear-gradient(135deg, #f0ad4e 0%, #d9534f 100%);
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  line-height: 1;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.data-table-card {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.personnel-name {
  display: flex;
  align-items: center;
  gap: 8px;
}

.name-text {
  font-weight: 500;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>