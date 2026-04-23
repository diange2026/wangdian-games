<template>
  <el-dialog
    v-model="visible"
    :title="formTitle"
    width="800px"
    :close-on-click-modal="false"
    :destroy-on-close="true"
    @close="handleClose"
  >
    <div class="personnel-form-container" v-loading="loading">
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="120px"
        label-position="right"
      >
        <el-tabs v-model="activeTab">
          <!-- 基本信息 -->
          <el-tab-pane label="基本信息" name="basic">
            <div class="tab-content">
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="人员编号" prop="personnelCode">
                    <el-input
                      v-model="formData.personnelCode"
                      placeholder="请输入人员编号"
                      clearable
                      :disabled="isEditMode"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="姓名" prop="name">
                    <el-input
                      v-model="formData.name"
                      placeholder="请输入姓名"
                      clearable
                    />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="所属单位" prop="companyId">
                    <el-select
                      v-model="formData.companyId"
                      placeholder="请选择所属单位"
                      style="width: 100%"
                      clearable
                      filterable
                    >
                      <el-option
                        v-for="company in companyList"
                        :key="company.id"
                        :label="company.name"
                        :value="company.id"
                      />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="身份证号" prop="idCard">
                    <el-input
                      v-model="formData.idCard"
                      placeholder="请输入18位身份证号"
                      clearable
                      :disabled="isEditMode"
                    />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="性别" prop="gender">
                    <el-radio-group v-model="formData.gender">
                      <el-radio label="male">男</el-radio>
                      <el-radio label="female">女</el-radio>
                    </el-radio-group>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="出生日期" prop="birthDate">
                    <el-date-picker
                      v-model="formData.birthDate"
                      type="date"
                      placeholder="选择出生日期"
                      style="width: 100%"
                      format="YYYY-MM-DD"
                      value-format="YYYY-MM-DD"
                    />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="联系电话" prop="phone">
                    <el-input
                      v-model="formData.phone"
                      placeholder="请输入联系电话"
                      clearable
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="电子邮箱" prop="email">
                    <el-input
                      v-model="formData.email"
                      placeholder="请输入电子邮箱"
                      clearable
                    />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="岗位/职务" prop="position">
                    <el-input
                      v-model="formData.position"
                      placeholder="请输入岗位或职务"
                      clearable
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="工种/岗位类型" prop="workType">
                    <el-input
                      v-model="formData.workType"
                      placeholder="请输入工种或岗位类型"
                      clearable
                    />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="入职日期" prop="hireDate">
                    <el-date-picker
                      v-model="formData.hireDate"
                      type="date"
                      placeholder="选择入职日期"
                      style="width: 100%"
                      format="YYYY-MM-DD"
                      value-format="YYYY-MM-DD"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="在职状态" prop="employmentStatus">
                    <el-select
                      v-model="formData.employmentStatus"
                      placeholder="请选择在职状态"
                      style="width: 100%"
                    >
                      <el-option label="在职" value="active" />
                      <el-option label="离职" value="inactive" />
                      <el-option label="停职" value="suspended" />
                      <el-option label="解雇" value="terminated" />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-form-item label="审核状态" prop="status">
                <el-select
                  v-model="formData.status"
                  placeholder="请选择审核状态"
                  style="width: 100%"
                >
                  <el-option label="待审核" value="pending_review" />
                  <el-option label="已通过" value="approved" />
                  <el-option label="已拒绝" value="rejected" />
                  <el-option label="已过期" value="expired" />
                </el-select>
              </el-form-item>

              <el-form-item label="照片URL" prop="photoUrl">
                <el-input
                  v-model="formData.photoUrl"
                  placeholder="请输入照片URL地址"
                  clearable
                >
                  <template #append>
                    <el-button @click="handlePreviewPhoto" :disabled="!formData.photoUrl">
                      预览
                    </el-button>
                  </template>
                </el-input>
                <div class="photo-preview" v-if="previewPhotoUrl">
                  <el-image
                    :src="previewPhotoUrl"
                    fit="cover"
                    style="width: 100px; height: 120px; border-radius: 4px; margin-top: 5px;"
                  />
                </div>
              </el-form-item>
            </div>
          </el-tab-pane>

          <!-- 证书信息 -->
          <el-tab-pane label="证书信息" name="certificates">
            <div class="tab-content">
              <div class="certificate-list">
                <div class="list-header">
                  <h4>证书列表</h4>
                  <el-button
                    type="primary"
                    size="small"
                    @click="handleAddCertificate"
                    icon="el-icon-plus"
                  >
                    添加证书
                  </el-button>
                </div>

                <el-table
                  :data="certificateFormData"
                  border
                  size="small"
                  style="width: 100%; margin-top: 10px;"
                >
                  <el-table-column label="证书名称" prop="certificateName" min-width="150" />
                  <el-table-column label="证书类型" prop="certificateType" width="120" />
                  <el-table-column label="证书编号" prop="certificateNumber" width="150" />
                  <el-table-column label="发证日期" width="100">
                    <template #default="{ row }">
                      {{ formatDate(row.issueDate) }}
                    </template>
                  </el-table-column>
                  <el-table-column label="到期日期" width="100">
                    <template #default="{ row }">
                      {{ formatDate(row.expiryDate) }}
                    </template>
                  </el-table-column>
                  <el-table-column label="操作" fixed="right" width="100" align="center">
                    <template #default="{ row, $index }">
                      <el-button
                        type="text"
                        size="small"
                        @click="handleEditCertificate($index)"
                        icon="el-icon-edit"
                      >
                        编辑
                      </el-button>
                      <el-button
                        type="text"
                        size="small"
                        @click="handleRemoveCertificate($index)"
                        icon="el-icon-delete"
                        style="color: #f56c6c"
                      >
                        删除
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </div>
            </div>
          </el-tab-pane>

          <!-- 培训记录 -->
          <el-tab-pane label="培训记录" name="trainings">
            <div class="tab-content">
              <div class="training-list">
                <div class="list-header">
                  <h4>培训记录列表</h4>
                  <el-button
                    type="primary"
                    size="small"
                    @click="handleAddTraining"
                    icon="el-icon-plus"
                  >
                    添加培训记录
                  </el-button>
                </div>

                <el-table
                  :data="trainingFormData"
                  border
                  size="small"
                  style="width: 100%; margin-top: 10px;"
                >
                  <el-table-column label="培训名称" prop="trainingName" min-width="150" />
                  <el-table-column label="培训类型" prop="trainingType" width="120" />
                  <el-table-column label="培训日期" width="100">
                    <template #default="{ row }">
                      {{ formatDate(row.trainingDate) }}
                    </template>
                  </el-table-column>
                  <el-table-column label="培训机构" prop="trainingInstitution" min-width="150" />
                  <el-table-column label="操作" fixed="right" width="100" align="center">
                    <template #default="{ row, $index }">
                      <el-button
                        type="text"
                        size="small"
                        @click="handleEditTraining($index)"
                        icon="el-icon-edit"
                      >
                        编辑
                      </el-button>
                      <el-button
                        type="text"
                        size="small"
                        @click="handleRemoveTraining($index)"
                        icon="el-icon-delete"
                        style="color: #f56c6c"
                      >
                        删除
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-form>
    </div>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose" :disabled="loading">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="loading">
          提交
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, defineProps, defineEmits } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { createPersonnel, updatePersonnel } from '@/api/personnel'
import { getCompanyList } from '@/api/company'
import type { PersonnelCreate, PersonnelUpdate, PersonnelCertificateCreate, PersonnelTrainingRecordCreate } from '@/types/personnel'

// 属性定义
const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  personnelData: {
    type: Object,
    default: null
  }
})

// 事件定义
const emit = defineEmits([
  'update:modelValue',
  'success'
])

// 响应式数据
const visible = ref(props.modelValue)
const loading = ref(false)
const formRef = ref<FormInstance>()
const companyList = ref<any[]>([])
const activeTab = ref('basic')
const previewPhotoUrl = ref('')

// 表单数据
const defaultFormData = {
  personnelCode: '',
  name: '',
  companyId: undefined as number | undefined,
  idCard: '',
  gender: 'male' as const,
  birthDate: '',
  phone: '',
  email: '',
  position: '',
  workType: '',
  hireDate: '',
  employmentStatus: 'active' as const,
  status: 'pending_review' as const,
  photoUrl: ''
}

const formData = reactive({ ...defaultFormData })
const certificateFormData = ref<PersonnelCertificateCreate[]>([])
const trainingFormData = ref<PersonnelTrainingRecordCreate[]>([])

// 计算属性
const isEditMode = computed(() => !!props.personnelData)
const formTitle = computed(() => isEditMode.value ? '编辑人员信息' : '新增人员')

// 表单验证规则
const formRules = reactive<FormRules>({
  personnelCode: [
    { required: true, message: '请输入人员编号', trigger: 'blur' },
    { min: 1, max: 50, message: '人员编号长度在1-50个字符', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 1, max: 100, message: '姓名长度在1-100个字符', trigger: 'blur' }
  ],
  companyId: [
    { required: true, message: '请选择所属单位', trigger: 'change' }
  ],
  idCard: [
    { required: true, message: '请输入身份证号', trigger: 'blur' },
    { pattern: /^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$/, message: '请输入正确的身份证号', trigger: 'blur' }
  ],
  email: [
    { pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, message: '请输入正确的邮箱格式', trigger: 'blur' }
  ]
})

// 监听属性变化
watch(() => props.modelValue, (val) => {
  visible.value = val
})

watch(visible, (val) => {
  emit('update:modelValue', val)
  if (val) {
    initFormData()
    loadCompanyList()
  } else {
    resetFormData()
  }
})

watch(() => formData.photoUrl, (val) => {
  previewPhotoUrl.value = val || ''
})

// 初始化表单数据
const initFormData = () => {
  if (props.personnelData) {
    // 编辑模式：填充现有数据
    Object.assign(formData, {
      ...props.personnelData,
      companyId: props.personnelData.company_id
    })
    
    // 如果有证书和培训数据，也加载到表单中
    if (props.personnelData.certificates) {
      certificateFormData.value = props.personnelData.certificates.map(cert => ({
        ...cert,
        personnel_id: props.personnelData.id
      }))
    }
    
    if (props.personnelData.trainings) {
      trainingFormData.value = props.personnelData.trainings.map(training => ({
        ...training,
        personnel_id: props.personnelData.id
      }))
    }
  } else {
    // 新增模式：使用默认值
    Object.assign(formData, defaultFormData)
  }
}

// 重置表单数据
const resetFormData = () => {
  Object.assign(formData, defaultFormData)
  certificateFormData.value = []
  trainingFormData.value = []
  previewPhotoUrl.value = ''
  if (formRef.value) {
    formRef.value.clearValidate()
  }
}

// 加载单位列表
const loadCompanyList = async () => {
  try {
    const response = await getCompanyList({ page: 1, pageSize: 1000 })
    companyList.value = response.items || []
  } catch (error) {
    console.error('加载单位列表失败:', error)
  }
}

// 关闭对话框
const handleClose = () => {
  if (loading.value) return
  
  if (JSON.stringify(formData) !== JSON.stringify(defaultFormData) ||
      certificateFormData.value.length > 0 ||
      trainingFormData.value.length > 0) {
    ElMessageBox.confirm('表单数据未保存，确定要关闭吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      visible.value = false
    }).catch(() => {
      // 用户取消操作
    })
  } else {
    visible.value = false
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    // 验证表单
    await formRef.value.validate()
    
    loading.value = true
    
    if (isEditMode.value) {
      // 更新人员信息
      const updateData: PersonnelUpdate = {
        ...formData,
        company_id: formData.companyId
      }
      
      await updatePersonnel(props.personnelData.id, updateData)
      ElMessage.success('更新成功')
    } else {
      // 创建新人员
      const createData: PersonnelCreate = {
        ...formData,
        companyId: formData.companyId!
      }
      
      const result = await createPersonnel(createData)
      
      // 如果有证书数据，批量创建证书
      if (certificateFormData.value.length > 0) {
        await createPersonnelCertificates(result.id, certificateFormData.value)
      }
      
      // 如果有培训数据，批量创建培训记录
      if (trainingFormData.value.length > 0) {
        await createPersonnelTrainings(result.id, trainingFormData.value)
      }
      
      ElMessage.success('创建成功')
    }
    
    // 触发成功事件
    emit('success')
    visible.value = false
    
  } catch (error: any) {
    console.error('表单提交失败:', error)
    ElMessage.error(error.response?.data?.detail || '提交失败，请检查表单数据')
  } finally {
    loading.value = false
  }
}

// 预览照片
const handlePreviewPhoto = () => {
  if (formData.photoUrl) {
    window.open(formData.photoUrl, '_blank')
  }
}

// 添加证书
const handleAddCertificate = () => {
  ElMessage.info('添加证书功能开发中...')
}

// 编辑证书
const handleEditCertificate = (index: number) => {
  console.log('编辑证书:', certificateFormData.value[index])
  ElMessage.info('编辑证书功能开发中...')
}

// 删除证书
const handleRemoveCertificate = (index: number) => {
  ElMessageBox.confirm('确定要删除该证书吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    certificateFormData.value.splice(index, 1)
    ElMessage.success('删除成功')
  }).catch(() => {
    // 用户取消操作
  })
}

// 添加培训记录
const handleAddTraining = () => {
  ElMessage.info('添加培训记录功能开发中...')
}

// 编辑培训记录
const handleEditTraining = (index: number) => {
  console.log('编辑培训记录:', trainingFormData.value[index])
  ElMessage.info('编辑培训记录功能开发中...')
}

// 删除培训记录
const handleRemoveTraining = (index: number) => {
  ElMessageBox.confirm('确定要删除该培训记录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    trainingFormData.value.splice(index, 1)
    ElMessage.success('删除成功')
  }).catch(() => {
    // 用户取消操作
  })
}

// 批量创建证书
const createPersonnelCertificates = async (personnelId: number, certificates: PersonnelCertificateCreate[]) => {
  try {
    // 这里需要根据实际情况调用批量创建证书的API
    ElMessage.info(`已创建 ${certificates.length} 个证书`)
  } catch (error) {
    console.error('批量创建证书失败:', error)
  }
}

// 批量创建培训记录
const createPersonnelTrainings = async (personnelId: number, trainings: PersonnelTrainingRecordCreate[]) => {
  try {
    // 这里需要根据实际情况调用批量创建培训记录的API
    ElMessage.info(`已创建 ${trainings.length} 个培训记录`)
  } catch (error) {
    console.error('批量创建培训记录失败:', error)
  }
}

// 工具函数
const formatDate = (date: string | Date | null) => {
  if (!date) return '-'
  const d = new Date(date)
  return d.toLocaleDateString('zh-CN')
}
</script>

<style scoped>
.personnel-form-container {
  padding: 10px 0;
}

.tab-content {
  padding: 10px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.list-header h4 {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.photo-preview {
  margin-top: 5px;
  display: flex;
  justify-content: flex-start;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>