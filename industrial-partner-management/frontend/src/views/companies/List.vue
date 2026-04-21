<template>
  <div class="company-list-container">
    <!-- 头部操作栏 -->
    <div class="list-header">
      <div class="header-left">
        <h2 class="title">单位列表</h2>
        <span class="count-text">共 {{ total }} 个单位</span>
      </div>
      <div class="header-right">
        <el-button type="primary" :icon="Plus" @click="handleCreate">
          新建单位
        </el-button>
        <el-button :icon="Refresh" @click="refreshList">
          刷新
        </el-button>
      </div>
    </div>

    <!-- 搜索和过滤区域 -->
    <div class="filter-section">
      <el-form :inline="true" :model="queryParams" class="filter-form">
        <el-form-item label="单位编码">
          <el-input
            v-model="queryParams.company_code"
            placeholder="请输入单位编码"
            clearable
            @keyup.enter="handleSearch"
            @clear="handleSearch"
          />
        </el-form-item>
        <el-form-item label="单位名称">
          <el-input
            v-model="queryParams.company_name"
            placeholder="请输入单位名称"
            clearable
            @keyup.enter="handleSearch"
            @clear="handleSearch"
          />
        </el-form-item>
        <el-form-item label="单位类型">
          <el-select
            v-model="queryParams.company_type"
            placeholder="请选择单位类型"
            clearable
            @change="handleSearch"
          >
            <el-option label="供应商" value="supplier" />
            <el-option label="承包商" value="contractor" />
            <el-option label="服务商" value="service_provider" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select
            v-model="queryParams.status"
            placeholder="请选择状态"
            clearable
            @change="handleSearch"
          >
            <el-option label="正常" value="active" />
            <el-option label="未激活" value="inactive" />
            <el-option label="停用" value="suspended" />
            <el-option label="黑名单" value="blacklisted" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="handleReset">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 单位列表 -->
    <div class="list-content">
      <el-table
        :data="companies"
        v-loading="loading"
        stripe
        style="width: 100%"
        @row-click="handleRowClick"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="company_code" label="单位编码" width="150" sortable />
        <el-table-column prop="company_name" label="单位名称" min-width="200" show-overflow-tooltip />
        <el-table-column prop="company_type" label="单位类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getCompanyTypeTagType(row.company_type)">
              {{ getCompanyTypeLabel(row.company_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="contact_person" label="联系人" width="120" />
        <el-table-column prop="contact_phone" label="联系电话" width="130" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTagType(row.status)">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="risk_level" label="风险等级" width="100">
          <template #default="{ row }">
            <el-tag :type="getRiskLevelTagType(row.risk_level)">
              {{ getRiskLevelLabel(row.risk_level) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="certificate_count" label="证照数量" width="100">
          <template #default="{ row }">
            <el-link type="primary" @click.stop="viewCertificates(row)">
              {{ row.certificate_count || 0 }}
            </el-link>
          </template>
        </el-table-column>
        <el-table-column prop="cooperation_end_date" label="合作截止" width="120">
          <template #default="{ row }">
            {{ formatDate(row.cooperation_end_date) }}
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="160" sortable>
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              link
              size="small"
              @click.stop="handleView(row)"
            >
              查看
            </el-button>
            <el-button
              type="warning"
              link
              size="small"
              @click.stop="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              type="success"
              link
              size="small"
              @click.stop="handleCertificates(row)"
            >
              证照
            </el-button>
            <el-dropdown @command="handleCommand($event, row)">
              <el-button type="info" link size="small">
                更多<el-icon class="el-icon--right"><ArrowDown /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="change_status">状态变更</el-dropdown-item>
                  <el-dropdown-item command="export_data">导出数据</el-dropdown-item>
                  <el-dropdown-item
                    command="delete"
                    divided
                    class="text-danger"
                  >
                    删除
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-section">
        <el-pagination
          v-model:current-page="queryParams.page"
          v-model:page-size="queryParams.page_size"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handlePageSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </div>

    <!-- 单位详情抽屉 -->
    <el-drawer
      v-model="detailDrawerVisible"
      title="单位详情"
      direction="rtl"
      size="50%"
      destroy-on-close
    >
      <CompanyDetail
        v-if="detailDrawerVisible"
        :company-id="selectedCompanyId"
        @close="detailDrawerVisible = false"
        @updated="refreshList"
      />
    </el-drawer>

    <!-- 创建/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="800px"
      destroy-on-close
      @close="handleDialogClose"
    >
      <CompanyForm
        v-if="dialogVisible"
        :company-id="editingCompanyId"
        :mode="dialogMode"
        @success="handleFormSuccess"
        @cancel="dialogVisible = false"
      />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import {
  Plus,
  Search,
  Refresh,
  ArrowDown,
  Document,
  Edit,
  View,
  Delete
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { Company } from '@/types/company'
import { useCompanyStore } from '@/store/company'
import CompanyDetail from './components/CompanyDetail.vue'
import CompanyForm from './components/CompanyForm.vue'
import dayjs from 'dayjs'
import 'dayjs/locale/zh-cn'

dayjs.locale('zh-cn')

const router = useRouter()
const companyStore = useCompanyStore()

// 状态
const loading = ref(false)
const companies = ref<Company[]>([])
const total = ref(0)
const selectedCompanies = ref<Company[]>([])

// 查询参数
const queryParams = ref({
  page: 1,
  page_size: 20,
  company_code: '',
  company_name: '',
  company_type: '',
  status: '',
  risk_level: '',
  sort_by: 'created_at',
  sort_order: 'desc'
})

// 对话框状态
const dialogVisible = ref(false)
const dialogMode = ref<'create' | 'edit'>('create')
const dialogTitle = computed(() => dialogMode.value === 'create' ? '创建单位' : '编辑单位')
const editingCompanyId = ref<number | null>(null)

// 详情抽屉
const detailDrawerVisible = ref(false)
const selectedCompanyId = ref<number | null>(null)

// 获取列表数据
const getCompanyList = async () => {
  loading.value = true
  try {
    const params = {
      ...queryParams.value,
      page: queryParams.value.page,
      page_size: queryParams.value.page_size
    }
    
    // 模拟数据，实际应该调用API
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // 模拟数据
    companies.value = [
      {
        id: 1,
        company_code: 'COMP2024001',
        company_name: '上海建工集团有限公司',
        company_type: 'contractor',
        legal_person: '张三',
        contact_person: '李四',
        contact_phone: '13800138001',
        contact_email: 'contact@shjg.com',
        registered_address: '上海市黄浦区中山东一路1号',
        business_address: '上海市浦东新区世纪大道100号',
        business_scope: '建筑工程施工、设计、监理',
        status: 'active',
        cooperation_start_date: '2023-01-15',
        cooperation_end_date: '2026-01-14',
        risk_level: 'low',
        audit_score: 95.5,
        remarks: '长期合作伙伴，信誉良好',
        created_by: 1,
        updated_by: 1,
        created_at: '2023-01-15T10:30:00',
        updated_at: '2024-12-20T14:25:00',
        certificate_count: 12,
        valid_certificate_count: 10,
        expiring_certificate_count: 2
      },
      {
        id: 2,
        company_code: 'COMP2024002',
        company_name: '北京安全技术服务有限公司',
        company_type: 'service_provider',
        legal_person: '王五',
        contact_person: '赵六',
        contact_phone: '13900139001',
        contact_email: 'service@bjsafety.com',
        registered_address: '北京市朝阳区建国门外大街1号',
        business_address: '北京市海淀区中关村大街1号',
        business_scope: '安全技术服务、培训、咨询',
        status: 'active',
        cooperation_start_date: '2022-05-10',
        cooperation_end_date: '2025-05-09',
        risk_level: 'medium',
        audit_score: 88.0,
        remarks: '专业安全服务提供商',
        created_by: 1,
        updated_by: 1,
        created_at: '2022-05-10T09:15:00',
        updated_at: '2024-11-15T11:30:00',
        certificate_count: 8,
        valid_certificate_count: 7,
        expiring_certificate_count: 1
      },
      {
        id: 3,
        company_code: 'COMP2024003',
        company_name: '广州设备供应有限公司',
        company_type: 'supplier',
        legal_person: '孙七',
        contact_person: '周八',
        contact_phone: '13700137001',
        contact_email: 'sales@gzequip.com',
        registered_address: '广州市天河区珠江新城花城大道1号',
        business_address: '广州市白云区白云大道南1号',
        business_scope: '机械设备销售、租赁、维修',
        status: 'active',
        cooperation_start_date: '2023-06-01',
        cooperation_end_date: '2026-05-31',
        risk_level: 'low',
        audit_score: 92.0,
        remarks: '设备质量可靠，服务及时',
        created_by: 1,
        updated_by: 1,
        created_at: '2023-06-01T14:20:00',
        updated_at: '2024-10-10T16:45:00',
        certificate_count: 5,
        valid_certificate_count: 5,
        expiring_certificate_count: 0
      }
    ]
    
    total.value = companies.value.length
  } catch (error) {
    console.error('获取单位列表失败:', error)
    ElMessage.error('获取单位列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  queryParams.value.page = 1
  getCompanyList()
}

// 重置搜索条件
const handleReset = () => {
  queryParams.value = {
    page: 1,
    page_size: 20,
    company_code: '',
    company_name: '',
    company_type: '',
    status: '',
    risk_level: '',
    sort_by: 'created_at',
    sort_order: 'desc'
  }
  getCompanyList()
}

// 刷新列表
const refreshList = () => {
  getCompanyList()
}

// 创建单位
const handleCreate = () => {
  dialogMode.value = 'create'
  editingCompanyId.value = null
  dialogVisible.value = true
}

// 查看详情
const handleView = (row: Company) => {
  selectedCompanyId.value = row.id
  detailDrawerVisible.value = true
}

// 编辑单位
const handleEdit = (row: Company) => {
  dialogMode.value = 'edit'
  editingCompanyId.value = row.id
  dialogVisible.value = true
}

// 管理证照
const handleCertificates = (row: Company) => {
  router.push({
    name: 'CertificateList',
    query: {
      company_id: row.id,
      company_name: row.company_name
    }
  })
}

// 查看证照
const viewCertificates = (row: Company) => {
  handleCertificates(row)
}

// 行点击处理
const handleRowClick = (row: Company) => {
  // 可以点击整行查看详情
  handleView(row)
}

// 选择变化处理
const handleSelectionChange = (selection: Company[]) => {
  selectedCompanies.value = selection
}

// 更多操作命令处理
const handleCommand = (command: string, row: Company) => {
  switch (command) {
    case 'change_status':
      handleChangeStatus(row)
      break
    case 'export_data':
      handleExportData(row)
      break
    case 'delete':
      handleDelete(row)
      break
  }
}

// 状态变更
const handleChangeStatus = async (row: Company) => {
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
    refreshList()
  } catch (error) {
    // 用户取消了操作
  }
}

// 导出数据
const handleExportData = (row: Company) => {
  ElMessage.info('导出功能开发中')
}

// 删除单位
const handleDelete = async (row: Company) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除单位 "${row.company_name}" 吗？此操作将停用该单位，但不会删除相关证照记录。`,
      '删除确认',
      {
        confirmButtonText: '确认删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 模拟删除操作
    await new Promise(resolve => setTimeout(resolve, 500))
    
    ElMessage.success('单位已停用')
    refreshList()
  } catch (error) {
    // 用户取消了删除
  }
}

// 表单成功处理
const handleFormSuccess = () => {
  dialogVisible.value = false
  refreshList()
}

// 对话框关闭处理
const handleDialogClose = () => {
  editingCompanyId.value = null
}

// 分页处理
const handlePageSizeChange = (newSize: number) => {
  queryParams.value.page_size = newSize
  getCompanyList()
}

const handlePageChange = (newPage: number) => {
  queryParams.value.page = newPage
  getCompanyList()
}

// 工具函数
const formatDate = (dateStr: string | null) => {
  if (!dateStr) return '-'
  return dayjs(dateStr).format('YYYY-MM-DD')
}

const formatDateTime = (dateStr: string) => {
  return dayjs(dateStr).format('YYYY-MM-DD HH:mm:ss')
}

const getCompanyTypeTagType = (type: string) => {
  const types: Record<string, string> = {
    supplier: 'success',
    contractor: 'primary',
    service_provider: 'warning',
    other: 'info'
  }
  return types[type] || 'info'
}

const getCompanyTypeLabel = (type: string) => {
  const labels: Record<string, string> = {
    supplier: '供应商',
    contractor: '承包商',
    service_provider: '服务商',
    other: '其他'
  }
  return labels[type] || '未知'
}

const getStatusTagType = (status: string) => {
  const types: Record<string, string> = {
    active: 'success',
    inactive: 'info',
    suspended: 'warning',
    blacklisted: 'danger'
  }
  return types[status] || 'info'
}

const getStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    active: '正常',
    inactive: '未激活',
    suspended: '停用',
    blacklisted: '黑名单'
  }
  return labels[status] || '未知'
}

const getRiskLevelTagType = (level: string) => {
  const types: Record<string, string> = {
    low: 'success',
    medium: 'warning',
    high: 'danger'
  }
  return types[level] || 'info'
}

const getRiskLevelLabel = (level: string) => {
  const labels: Record<string, string> = {
    low: '低风险',
    medium: '中风险',
    high: '高风险'
  }
  return labels[level] || '未知'
}

// 初始化
onMounted(() => {
  getCompanyList()
})
</script>

<style scoped lang="scss">
.company-list-container {
  padding: 20px;
  background: #f5f7fa;
  min-height: calc(100vh - 60px);
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  
  .header-left {
    .title {
      font-size: 18px;
      font-weight: 600;
      margin-bottom: 8px;
      color: #303133;
    }
    
    .count-text {
      font-size: 14px;
      color: #909399;
    }
  }
}

.filter-section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  
  .filter-form {
    margin: 0;
  }
}

.list-content {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  
  :deep(.el-table) {
    .el-table__row {
      cursor: pointer;
      
      &:hover {
        background-color: #f5f7fa;
      }
    }
  }
}

.pagination-section {
  padding: 20px;
  display: flex;
  justify-content: center;
  background: white;
}

// 响应式设计
@media (max-width: 768px) {
  .list-header {
    flex-direction: column;
    align-items: flex-start;
    
    .header-right {
      margin-top: 15px;
      width: 100%;
      
      .el-button {
        width: 100%;
        margin-bottom: 10px;
      }
    }
  }
  
  .filter-form {
    .el-form-item {
      width: 100%;
      margin-bottom: 10px;
    }
  }
}

// 文本危险色
.text-danger {
  color: #f56c6c;
  
  &:hover {
    color: #e45656;
  }
}
</style>