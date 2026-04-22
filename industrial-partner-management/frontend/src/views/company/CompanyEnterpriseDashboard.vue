<template>
  <div class="company-enterprise-dashboard">
    <!-- 页面头部 -->
    <div class="dashboard-header">
      <div class="header-left">
        <h1 class="page-title">
          <i class="el-icon-office-building"></i>
          企业单位资质管理系统
        </h1>
        <p class="page-subtitle">全方位、全生命周期、全景式单位资质管理平台</p>
      </div>
      <div class="header-right">
        <el-button type="primary" icon="el-icon-plus" @click="handleCreateCompany">
          新增单位
        </el-button>
        <el-button icon="el-icon-upload" @click="handleImport">
          批量导入
        </el-button>
        <el-button icon="el-icon-download" @click="handleExport">
          数据导出
        </el-button>
        <el-button icon="el-icon-setting" @click="handleSettings">
          系统设置
        </el-button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="statistics-cards">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="6" :lg="6">
          <div class="stat-card total-companies">
            <div class="stat-icon">
              <i class="el-icon-office-building"></i>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ statistics.totalCompanies }}</div>
              <div class="stat-label">总单位数</div>
            </div>
            <div class="stat-trend">
              <span class="trend-up">↑12%</span> 较上月
            </div>
          </div>
        </el-col>
        
        <el-col :xs="24" :sm="12" :md="6" :lg="6">
          <div class="stat-card active-companies">
            <div class="stat-icon">
              <i class="el-icon-success"></i>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ statistics.activeCompanies }}</div>
              <div class="stat-label">正常单位</div>
            </div>
            <div class="stat-trend">
              <span class="trend-up">↑8%</span> 较上月
            </div>
          </div>
        </el-col>
        
        <el-col :xs="24" :sm="12" :md="6" :lg="6">
          <div class="stat-card expiring-certificates">
            <div class="stat-icon">
              <i class="el-icon-warning"></i>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ statistics.expiringCertificates }}</div>
              <div class="stat-label">即将到期证照</div>
            </div>
            <div class="stat-trend">
              <span class="trend-warning">需处理</span>
            </div>
          </div>
        </el-col>
        
        <el-col :xs="24" :sm="12" :md="6" :lg="6">
          <div class="stat-card high-risk-companies">
            <div class="stat-icon">
              <i class="el-icon-error"></i>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ statistics.highRiskCompanies }}</div>
              <div class="stat-label">高风险单位</div>
            </div>
            <div class="stat-trend">
              <span class="trend-danger">需关注</span>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 主内容区 -->
    <div class="main-content">
      <el-row :gutter="20">
        <!-- 左侧：单位列表和搜索 -->
        <el-col :xs="24" :sm="24" :md="8" :lg="8">
          <div class="company-list-panel">
            <div class="search-box">
              <el-input
                v-model="searchKeyword"
                placeholder="搜索单位编码、名称、联系人..."
                prefix-icon="el-icon-search"
                clearable
                @input="handleSearch"
              >
                <template #append>
                  <el-button icon="el-icon-search" @click="handleSearch"></el-button>
                </template>
              </el-input>
            </div>

            <!-- 快速筛选 -->
            <div class="quick-filters">
              <el-button-group>
                <el-button 
                  :type="filterType === 'all' ? 'primary' : ''"
                  @click="handleFilter('all')"
                >
                  全部
                </el-button>
                <el-button 
                  :type="filterType === 'active' ? 'primary' : ''"
                  @click="handleFilter('active')"
                >
                  正常
                </el-button>
                <el-button 
                  :type="filterType === 'high-risk' ? 'primary' : ''"
                  @click="handleFilter('high-risk')"
                >
                  高风险
                </el-button>
                <el-button 
                  :type="filterType === 'expiring' ? 'primary' : ''"
                  @click="handleFilter('expiring')"
                >
                  证照到期
                </el-button>
              </el-button-group>
            </div>

            <!-- 单位列表 -->
            <div class="company-list">
              <el-scrollbar height="500px">
                <div 
                  v-for="company in filteredCompanies" 
                  :key="company.id"
                  class="company-item"
                  :class="{ 
                    'active': selectedCompanyId === company.id,
                    'high-risk': company.riskLevel === 'high'
                  }"
                  @click="selectCompany(company)"
                >
                  <div class="company-item-header">
                    <div class="company-code">{{ company.companyCode }}</div>
                    <div class="company-status">
                      <el-tag 
                        :type="getStatusTagType(company.status)"
                        size="small"
                      >
                        {{ getStatusText(company.status) }}
                      </el-tag>
                    </div>
                  </div>
                  <div class="company-name">{{ company.companyName }}</div>
                  <div class="company-info">
                    <span class="info-item">
                      <i class="el-icon-user"></i>
                      {{ company.contactPerson }}
                    </span>
                    <span class="info-item">
                      <i class="el-icon-phone"></i>
                      {{ company.contactPhone }}
                    </span>
                  </div>
                  <div class="company-risk">
                    <el-tag 
                      :type="getRiskTagType(company.riskLevel)"
                      size="small"
                    >
                      风险: {{ getRiskText(company.riskLevel) }}
                    </el-tag>
                    <span class="cert-count">
                      {{ company.certificateCount }} 个证照
                    </span>
                  </div>
                </div>
              </el-scrollbar>
            </div>
          </div>
        </el-col>

        <!-- 右侧：单位详情和证照管理 -->
        <el-col :xs="24" :sm="24" :md="16" :lg="16">
          <div class="company-detail-panel" v-if="selectedCompany">
            <!-- 单位详情标签页 -->
            <el-tabs v-model="activeTab" class="company-tabs">
              <!-- 单位基本信息 -->
              <el-tab-pane label="基本信息" name="basic">
                <div class="detail-section">
                  <div class="section-header">
                    <h3>
                      <i class="el-icon-info"></i>
                      单位基本信息
                    </h3>
                    <el-button 
                      type="primary" 
                      size="small"
                      icon="el-icon-edit"
                      @click="handleEditCompany"
                    >
                      编辑信息
                    </el-button>
                  </div>
                  
                  <el-descriptions 
                    :column="2" 
                    border
                    class="company-description"
                  >
                    <el-descriptions-item label="单位编码">
                      <el-tag type="info">{{ selectedCompany.companyCode }}</el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="单位名称">
                      {{ selectedCompany.companyName }}
                    </el-descriptions-item>
                    <el-descriptions-item label="单位类型">
                      <el-tag>{{ getCompanyTypeText(selectedCompany.companyType) }}</el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="企业性质">
                      {{ getBusinessNatureText(selectedCompany.businessNature) }}
                    </el-descriptions-item>
                    <el-descriptions-item label="注册资本">
                      {{ selectedCompany.registrationCapital }} 万元
                    </el-descriptions-item>
                    <el-descriptions-item label="实缴资本">
                      {{ selectedCompany.actualCapital }} 万元
                    </el-descriptions-item>
                    <el-descriptions-item label="统一信用代码">
                      {{ selectedCompany.creditCode || '未填写' }}
                    </el-descriptions-item>
                    <el-descriptions-item label="法人代表">
                      {{ selectedCompany.legalPerson }}
                    </el-descriptions-item>
                    <el-descriptions-item label="注册地址">
                      {{ selectedCompany.registeredAddress }}
                    </el-descriptions-item>
                    <el-descriptions-item label="经营地址">
                      {{ selectedCompany.businessAddress || '同注册地址' }}
                    </el-descriptions-item>
                    <el-descriptions-item label="经营范围">
                      <div class="business-scope">
                        {{ selectedCompany.businessScope || '未填写' }}
                      </div>
                    </el-descriptions-item>
                  </el-descriptions>
                </div>

                <!-- 联系信息 -->
                <div class="detail-section">
                  <div class="section-header">
                    <h3>
                      <i class="el-icon-phone"></i>
                      联系信息
                    </h3>
                  </div>
                  
                  <el-row :gutter="20">
                    <el-col :span="12">
                      <div class="contact-info">
                        <h4>主要联系人</h4>
                        <p><i class="el-icon-user"></i> {{ selectedCompany.contactPerson }}</p>
                        <p><i class="el-icon-phone"></i> {{ selectedCompany.contactPhone }}</p>
                        <p><i class="el-icon-message"></i> {{ selectedCompany.contactEmail }}</p>
                      </div>
                    </el-col>
                    <el-col :span="12">
                      <div class="contact-info">
                        <h4>财务联系人</h4>
                        <p><i class="el-icon-user"></i> {{ selectedCompany.financialContact || '未设置' }}</p>
                        <p><i class="el-icon-phone"></i> {{ selectedCompany.financialPhone || '未设置' }}</p>
                      </div>
                    </el-col>
                    <el-col :span="12" v-if="selectedCompany.technicalContact">
                      <div class="contact-info">
                        <h4>技术联系人</h4>
                        <p><i class="el-icon-user"></i> {{ selectedCompany.technicalContact }}</p>
                        <p><i class="el-icon-phone"></i> {{ selectedCompany.technicalPhone }}</p>
                      </div>
                    </el-col>
                  </el-row>
                </div>

                <!-- 风险分析 -->
                <div class="detail-section">
                  <div class="section-header">
                    <h3>
                      <i class="el-icon-warning"></i>
                      风险分析
                    </h3>
                  </div>
                  
                  <div class="risk-analysis">
                    <el-row :gutter="20">
                      <el-col :span="8">
                        <div class="risk-card" :class="getRiskCardClass(selectedCompany.riskLevel)">
                          <div class="risk-title">风险等级</div>
                          <div class="risk-value">{{ getRiskText(selectedCompany.riskLevel) }}</div>
                          <div class="risk-score">评分: {{ selectedCompany.riskScore || 50 }}</div>
                        </div>
                      </el-col>
                      <el-col :span="16">
                        <div class="risk-indicators">
                          <h4>风险指标</h4>
                          <div class="indicator-list">
                            <div 
                              v-for="(indicator, index) in selectedCompany.riskIndicators" 
                              :key="index"
                              class="indicator-item"
                            >
                              <span class="indicator-name">{{ indicator.name }}</span>
                              <el-progress 
                                :percentage="indicator.score" 
                                :status="getIndicatorStatus(indicator.score)"
                                :show-text="false"
                              />
                              <span class="indicator-score">{{ indicator.score }}分</span>
                            </div>
                          </div>
                        </div>
                      </el-col>
                    </el-row>
                  </div>
                </div>
              </el-tab-pane>

              <!-- 证照管理 -->
              <el-tab-pane label="资质证照" name="certificates">
                <div class="certificate-management">
                  <div class="certificate-header">
                    <h3>
                      <i class="el-icon-document"></i>
                      资质证照管理
                    </h3>
                    <div class="certificate-actions">
                      <el-button 
                        type="primary" 
                        icon="el-icon-plus"
                        @click="handleAddCertificate"
                      >
                        新增证照
                      </el-button>
                      <el-button 
                        icon="el-icon-refresh"
                        @click="refreshCertificates"
                      >
                        刷新列表
                      </el-button>
                    </div>
                  </div>

                  <!-- 证照统计 -->
                  <div class="certificate-stats">
                    <el-row :gutter="20">
                      <el-col :span="6">
                        <div class="stat-item">
                          <div class="stat-label">有效证照</div>
                          <div class="stat-value">{{ certificateStats.valid }}</div>
                        </div>
                      </el-col>
                      <el-col :span="6">
                        <div class="stat-item">
                          <div class="stat-label">即将到期</div>
                          <div class="stat-value warning">{{ certificateStats.expiring }}</div>
                        </div>
                      </el-col>
                      <el-col :span="6">
                        <div class="stat-item">
                          <div class="stat-label">已过期</div>
                          <div class="stat-value danger">{{ certificateStats.expired }}</div>
                        </div>
                      </el-col>
                      <el-col :span="6">
                        <div class="stat-item">
                          <div class="stat-label">等待续期</div>
                          <div class="stat-value info">{{ certificateStats.pendingRenewal }}</div>
                        </div>
                      </el-col>
                    </el-row>
                  </div>

                  <!-- 证照列表 -->
                  <div class="certificate-list">
                    <el-table 
                      :data="certificates" 
                      style="width: 100%"
                      :row-class-name="certificateRowClassName"
                    >
                      <el-table-column label="证照名称" prop="certificateName" width="200">
                        <template #default="scope">
                          <div class="certificate-name-cell">
                            <i class="el-icon-document" :class="getCertificateIconClass(scope.row.certificateType)"></i>
                            <span>{{ scope.row.certificateName }}</span>
                          </div>
                        </template>
                      </el-table-column>
                      <el-table-column label="证照编号" prop="certificateNumber" width="150" />
                      <el-table-column label="发证机关" prop="issuingAuthority" width="180" />
                      <el-table-column label="发证日期" prop="issueDate" width="120">
                        <template #default="scope">
                          {{ formatDate(scope.row.issueDate) }}
                        </template>
                      </el-table-column>
                      <el-table-column label="到期日期" prop="expiryDate" width="120">
                        <template #default="scope">
                          <div :class="getExpiryDateClass(scope.row)">
                            {{ formatDate(scope.row.expiryDate) }}
                          </div>
                        </template>
                      </el-table-column>
                      <el-table-column label="状态" prop="certificateStatus" width="100">
                        <template #default="scope">
                          <el-tag 
                            :type="getCertificateStatusTagType(scope.row.certificateStatus)"
                            size="small"
                          >
                            {{ getCertificateStatusText(scope.row.certificateStatus) }}
                          </el-tag>
                        </template>
                      </el-table-column>
                      <el-table-column label="续期状态" prop="renewalStatus" width="100">
                        <template #default="scope">
                          <el-tag 
                            :type="getRenewalStatusTagType(scope.row.renewalStatus)"
                            size="small"
                          >
                            {{ getRenewalStatusText(scope.row.renewalStatus) }}
                          </el-tag>
                        </template>
                      </el-table-column>
                      <el-table-column label="操作" width="150">
                        <template #default="scope">
                          <el-button-group>
                            <el-button 
                              size="mini" 
                              icon="el-icon-view"
                              @click="handleViewCertificate(scope.row)"
                            >
                              查看
                            </el-button>
                            <el-button 
                              size="mini" 
                              icon="el-icon-edit"
                              @click="handleEditCertificate(scope.row)"
                            >
                              编辑
                            </el-button>
                            <el-button 
                              size="mini" 
                              type="danger" 
                              icon="el-icon-delete"
                              @click="handleDeleteCertificate(scope.row)"
                            >
                              删除
                            </el-button>
                          </el-button-group>
                        </template>
                      </el-table-column>
                    </el-table>
                  </div>
                </div>
              </el-tab-pane>

              <!-- 预警监控 -->
              <el-tab-pane label="预警监控" name="alerts">
                <div class="alert-monitoring">
                  <div class="alert-header">
                    <h3>
                      <i class="el-icon-bell"></i>
                      智能预警监控
                    </h3>
                    <div class="alert-filters">
                      <el-select v-model="alertFilter" placeholder="筛选预警类型" size="small">
                        <el-option label="全部预警" value="all" />
                        <el-option label="证照到期" value="expiry" />
                        <el-option label="风险变化" value="risk" />
                        <el-option label="合规检查" value="compliance" />
                      </el-select>
                    </div>
                  </div>

                  <!-- 预警统计 -->
                  <div class="alert-stats">
                    <el-row :gutter="20">
                      <el-col :span="8">
                        <div class="alert-stat-item critical">
                          <div class="stat-icon">
                            <i class="el-icon-warning"></i>
                          </div>
                          <div class="stat-content">
                            <div class="stat-value">{{ alertStats.critical }}</div>
                            <div class="stat-label">严重预警</div>
                          </div>
                        </div>
                      </el-col>
                      <el-col :span="8">
                        <div class="alert-stat-item warning">
                          <div class="stat-icon">
                            <i class="el-icon-warning-outline"></i>
                          </div>
                          <div class="stat-content">
                            <div class="stat-value">{{ alertStats.warning }}</div>
                            <div class="stat-label">警告预警</div>
                          </div>
                        </div>
                      </el-col>
                      <el-col :span="8">
                        <div class="alert-stat-item info">
                          <div class="stat-icon">
                            <i class="el-icon-info"></i>
                          </div>
                          <div class="stat-content">
                            <div class="stat-value">{{ alertStats.info }}</div>
                            <div class="stat-label">信息预警</div>
                          </div>
                        </div>
                      </el-col>
                    </el-row>
                  </div>

                  <!-- 预警列表 -->
                  <div class="alert-list">
                    <el-timeline>
                      <el-timeline-item
                        v-for="(alert, index) in filteredAlerts"
                        :key="index"
                        :timestamp="formatTime(alert.timestamp)"
                        :type="getAlertType(alert.level)"
                        :icon="getAlertIcon(alert.level)"
                        placement="top"
                      >
                        <el-card :shadow="alert.level === 'critical' ? 'always' : 'hover'">
                          <template #header>
                            <div class="alert-card-header">
                              <span class="alert-title">{{ alert.title }}</span>
                              <el-tag 
                                :type="getAlertTagType(alert.level)"
                                size="small"
                              >
                                {{ getAlertLevelText(alert.level) }}
                              </el-tag>
                            </div>
                          </template>
                          <div class="alert-content">
                            <p>{{ alert.description }}</p>
                            <div class="alert-actions">
                              <el-button 
                                size="small" 
                                type="primary"
                                @click="handleResolveAlert(alert)"
                              >
                                处理
                              </el-button>
                              <el-button 
                                size="small" 
                                type="info"
                                @click="handleIgnoreAlert(alert)"
                              >
                                忽略
                              </el-button>
                              <el-button 
                                size="small" 
                                type="text"
                                @click="handleViewAlertDetails(alert)"
                              >
                                查看详情
                              </el-button>
                            </div>
                          </div>
                        </el-card>
                      </el-timeline-item>
                    </el-timeline>
                  </div>
                </div>
              </el-tab-pane>

              <!-- 审计日志 -->
              <el-tab-pane label="审计日志" name="audit">
                <div class="audit-log">
                  <div class="audit-header">
                    <h3>
                      <i class="el-icon-notebook-2"></i>
                      操作审计日志
                    </h3>
                    <div class="audit-filters">
                      <el-date-picker
                        v-model="auditDateRange"
                        type="daterange"
                        range-separator="至"
                        start-placeholder="开始日期"
                        end-placeholder="结束日期"
                        size="small"
                      />
                    </div>
                  </div>

                  <!-- 审计日志列表 -->
                  <div class="audit-log-list">
                    <el-table :data="auditLogs" style="width: 100%">
                      <el-table-column label="操作时间" prop="createdAt" width="180">
                        <template #default="scope">
                          {{ formatDateTime(scope.row.createdAt) }}
                        </template>
                      </el-table-column>
                      <el-table-column label="操作人" prop="userName" width="120" />
                      <el-table-column label="操作类型" prop="action" width="120">
                        <template #default="scope">
                          <el-tag :type="getActionTagType(scope.row.action)">
                            {{ getActionText(scope.row.action) }}
                          </el-tag>
                        </template>
                      </el-table-column>
                      <el-table-column label="操作内容" prop="description">
                        <template #default="scope">
                          <div class="audit-description">
                            {{ scope.row.description }}
                          </div>
                        </template>
                      </el-table-column>
                      <el-table-column label="数据变更" width="150">
                        <template #default="scope">
                          <el-button 
                            type="text" 
                            size="small"
                            @click="handleViewAuditDetails(scope.row)"
                          >
                            查看变更详情
                          </el-button>
                        </template>
                      </el-table-column>
                    </el-table>
                  </div>
                </div>
              </el-tab-pane>
            </el-tabs>
          </div>

          <!-- 没有选中单位时的提示 -->
          <div v-else class="empty-state">
            <div class="empty-content">
              <i class="el-icon-office-building empty-icon"></i>
              <h3>请选择一个单位</h3>
              <p>从左侧列表中选择一个单位查看详细信息</p>
              <el-button type="primary" @click="handleCreateCompany">
                或者创建一个新单位
              </el-button>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 创建/编辑单位对话框 -->
    <el-dialog
      v-model="companyDialog.visible"
      :title="companyDialog.title"
      width="800px"
      :before-close="handleCompanyDialogClose"
    >
      <CompanyForm
        v-if="companyDialog.visible"
        :company="companyDialog.data"
        :mode="companyDialog.mode"
        @submit="handleCompanyFormSubmit"
        @cancel="handleCompanyDialogClose"
      />
    </el-dialog>

    <!-- 创建/编辑证照对话框 -->
    <el-dialog
      v-model="certificateDialog.visible"
      :title="certificateDialog.title"
      width="600px"
      :before-close="handleCertificateDialogClose"
    >
      <CertificateForm
        v-if="certificateDialog.visible"
        :certificate="certificateDialog.data"
        :company-id="selectedCompanyId"
        :mode="certificateDialog.mode"
        @submit="handleCertificateFormSubmit"
        @cancel="handleCertificateDialogClose"
      />
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import CompanyForm from './components/CompanyForm.vue'
import CertificateForm from './components/CertificateForm.vue'
import {
  fetchCompanyList,
  fetchCompanyDetail,
  createCompany,
  updateCompany,
  deleteCompany,
  fetchCompanyCertificates,
  createCertificate,
  updateCertificate,
  deleteCertificate,
  fetchCompanyAlerts,
  fetchAuditLogs
} from '@/api/company'

export default {
  name: 'CompanyEnterpriseDashboard',
  components: {
    CompanyForm,
    CertificateForm
  },
  setup() {
    // 搜索和过滤状态
    const searchKeyword = ref('')
    const filterType = ref('all')
    const activeTab = ref('basic')
    const alertFilter = ref('all')
    const auditDateRange = ref([])

    // 数据状态
    const companies = ref([])
    const selectedCompanyId = ref(null)
    const selectedCompany = ref(null)
    const certificates = ref([])
    const alerts = ref([])
    const auditLogs = ref([])

    // 统计信息
    const statistics = reactive({
      totalCompanies: 0,
      activeCompanies: 0,
      expiringCertificates: 0,
      highRiskCompanies: 0
    })

    const certificateStats = reactive({
      valid: 0,
      expiring: 0,
      expired: 0,
      pendingRenewal: 0
    })

    const alertStats = reactive({
      critical: 0,
      warning: 0,
      info: 0
    })

    // 对话框状态
    const companyDialog = reactive({
      visible: false,
      title: '',
      mode: 'create',
      data: null
    })

    const certificateDialog = reactive({
      visible: false,
      title: '',
      mode: 'create',
      data: null
    })

    // 计算属性
    const filteredCompanies = computed(() => {
      let filtered = companies.value

      // 根据搜索关键词过滤
      if (searchKeyword.value) {
        const keyword = searchKeyword.value.toLowerCase()
        filtered = filtered.filter(company =>
          company.companyCode.toLowerCase().includes(keyword) ||
          company.companyName.toLowerCase().includes(keyword) ||
          company.contactPerson.toLowerCase().includes(keyword) ||
          company.contactPhone.includes(keyword)
        )
      }

      // 根据过滤类型过滤
      switch (filterType.value) {
        case 'active':
          filtered = filtered.filter(company => company.status === 'active')
          break
        case 'high-risk':
          filtered = filtered.filter(company => company.riskLevel === 'high')
          break
        case 'expiring':
          filtered = filtered.filter(company => company.certificateCount > 0 && company.hasExpiringCertificates)
          break
      }

      return filtered
    })

    const filteredAlerts = computed(() => {
      if (alertFilter.value === 'all') {
        return alerts.value
      }
      return alerts.value.filter(alert => alert.type === alertFilter.value)
    })

    // 生命周期钩子
    onMounted(() => {
      loadInitialData()
    })

    // 方法
    const loadInitialData = async () => {
      try {
        await Promise.all([
          loadCompanies(),
          loadStatistics()
        ])
      } catch (error) {
        ElMessage.error('加载数据失败: ' + error.message)
      }
    }

    const loadCompanies = async () => {
      try {
        const response = await fetchCompanyList()
        companies.value = response.data
        statistics.totalCompanies = companies.value.length
      } catch (error) {
        ElMessage.error('加载单位列表失败')
      }
    }

    const loadCompanyDetail = async (companyId) => {
      try {
        const response = await fetchCompanyDetail(companyId, {
          includeCertificates: true,
          includeAuditLogs: false
        })
        
        selectedCompany.value = response.data.company
        certificates.value = response.data.certificates
        calculateCertificateStats()
      } catch (error) {
        ElMessage.error('加载单位详情失败')
      }
    }

    const loadAlerts = async (companyId) => {
      try {
        const response = await fetchCompanyAlerts(companyId)
        alerts.value = response.data
        calculateAlertStats()
      } catch (error) {
        ElMessage.error('加载预警信息失败')
      }
    }

    const loadAuditLogs = async (companyId) => {
      try {
        const response = await fetchAuditLogs(companyId, {
          startDate: auditDateRange.value[0],
          endDate: auditDateRange.value[1]
        })
        auditLogs.value = response.data
      } catch (error) {
        ElMessage.error('加载审计日志失败')
      }
    }

    const loadStatistics = async () => {
      // 模拟统计计算
      statistics.activeCompanies = companies.value.filter(c => c.status === 'active').length
      statistics.highRiskCompanies = companies.value.filter(c => c.riskLevel === 'high').length
      // 这里应该从后端获取实际统计数据
    }

    const calculateCertificateStats = () => {
      const now = new Date()
      const thirtyDaysLater = new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000)

      certificateStats.valid = certificates.value.filter(c => c.certificateStatus === 'valid').length
      certificateStats.expiring = certificates.value.filter(c => 
        c.certificateStatus === 'valid' && 
        new Date(c.expiryDate) <= thirtyDaysLater
      ).length
      certificateStats.expired = certificates.value.filter(c => c.certificateStatus === 'expired').length
      certificateStats.pendingRenewal = certificates.value.filter(c => c.renewalStatus === 'pending').length
    }

    const calculateAlertStats = () => {
      alertStats.critical = alerts.value.filter(a => a.level === 'critical').length
      alertStats.warning = alerts.value.filter(a => a.level === 'warning').length
      alertStats.info = alerts.value.filter(a => a.level === 'info').length
    }

    // 事件处理方法
    const handleSearch = () => {
      // 搜索逻辑已经在计算属性中实现
    }

    const handleFilter = (type) => {
      filterType.value = type
    }

    const selectCompany = async (company) => {
      selectedCompanyId.value = company.id
      await loadCompanyDetail(company.id)
      await loadAlerts(company.id)
      await loadAuditLogs(company.id)
    }

    const handleCreateCompany = () => {
      companyDialog.visible = true
      companyDialog.title = '创建新单位'
      companyDialog.mode = 'create'
      companyDialog.data = null
    }

    const handleEditCompany = () => {
      companyDialog.visible = true
      companyDialog.title = '编辑单位信息'
      companyDialog.mode = 'edit'
      companyDialog.data = { ...selectedCompany.value }
    }

    const handleCompanyFormSubmit = async (formData) => {
      try {
        if (companyDialog.mode === 'create') {
          await createCompany(formData)
          ElMessage.success('单位创建成功')
        } else {
          await updateCompany(selectedCompanyId.value, formData)
          ElMessage.success('单位信息更新成功')
        }
        
        companyDialog.visible = false
        await loadCompanies()
        if (selectedCompanyId.value) {
          await loadCompanyDetail(selectedCompanyId.value)
        }
      } catch (error) {
        ElMessage.error('操作失败: ' + error.message)
      }
    }

    const handleCompanyDialogClose = () => {
      companyDialog.visible = false
    }

    const handleAddCertificate = () => {
      certificateDialog.visible = true
      certificateDialog.title = '新增证照'
      certificateDialog.mode = 'create'
      certificateDialog.data = null
    }

    const handleCertificateFormSubmit = async (formData) => {
      try {
        if (certificateDialog.mode === 'create') {
          await createCertificate(selectedCompanyId.value, formData)
          ElMessage.success('证照添加成功')
        } else {
          await updateCertificate(certificateDialog.data.id, formData)
          ElMessage.success('证照更新成功')
        }
        
        certificateDialog.visible = false
        await loadCompanyDetail(selectedCompanyId.value)
      } catch (error) {
        ElMessage.error('操作失败: ' + error.message)
      }
    }

    const handleCertificateDialogClose = () => {
      certificateDialog.visible = false
    }

    // 其他辅助方法
    const getStatusTagType = (status) => {
      const map = {
        active: 'success',
        inactive: 'info',
        suspended: 'warning',
        blacklisted: 'danger'
      }
      return map[status] || 'info'
    }

    const getStatusText = (status) => {
      const map = {
        active: '正常',
        inactive: '未激活',
        suspended: '停用',
        blacklisted: '黑名单'
      }
      return map[status] || status
    }

    const getRiskTagType = (riskLevel) => {
      const map = {
        low: 'success',
        medium: 'warning',
        high: 'danger',
        critical: 'danger'
      }
      return map[riskLevel] || 'info'
    }

    const getRiskText = (riskLevel) => {
      const map = {
        low: '低风险',
        medium: '中风险',
        high: '高风险',
        critical: '极高风险'
      }
      return map[riskLevel] || riskLevel
    }

    const getRiskCardClass = (riskLevel) => {
      const map = {
        low: 'risk-low',
        medium: 'risk-medium',
        high: 'risk-high',
        critical: 'risk-critical'
      }
      return map[riskLevel] || 'risk-medium'
    }

    const getCompanyTypeText = (type) => {
      const map = {
        supplier: '供应商',
        contractor: '承包商',
        service_provider: '服务商',
        partner: '合作伙伴',
        other: '其他'
      }
      return map[type] || type
    }

    const getBusinessNatureText = (nature) => {
      const map = {
        state_owned: '国有企业',
        private: '民营企业',
        foreign_invested: '外资企业',
        joint_venture: '合资企业'
      }
      return map[nature] || nature
    }

    const getCertificateStatusTagType = (status) => {
      const map = {
        valid: 'success',
        expired: 'danger',
        suspended: 'warning',
        revoked: 'info',
        in_review: 'info'
      }
      return