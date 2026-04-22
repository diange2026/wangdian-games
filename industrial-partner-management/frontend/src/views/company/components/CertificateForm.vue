<template>
  <div class="certificate-form">
    <el-form
      ref="certificateFormRef"
      :model="formData"
      :rules="formRules"
      label-width="120px"
      label-position="left"
      size="medium"
      :disabled="loading"
    >
      <!-- 证照基本信息 -->
      <el-form-item label="证照名称" prop="certificateName">
        <el-input
          v-model="formData.certificateName"
          placeholder="请输入证照名称"
        />
        <template #label>
          <span class="form-label required">证照名称</span>
        </template>
      </el-form-item>

      <el-form-item label="证照类型" prop="certificateType">
        <el-select
          v-model="formData.certificateType"
          placeholder="请选择证照类型"
          style="width: 100%"
        >
          <el-option label="营业执照" value="business_license" />
          <el-option label="税务登记证" value="tax_certificate" />
          <el-option label="安全生产许可证" value="safety_license" />
          <el-option label="环保证书" value="environment_protection" />
          <el-option label="其他证书" value="other" />
        </el-select>
        <template #label>
          <span class="form-label required">证照类型</span>
        </template>
      </el-form-item>

      <el-form-item label="证照编号" prop="certificateNumber">
        <el-input
          v-model="formData.certificateNumber"
          placeholder="请输入证照编号"
        />
        <template #label>
          <span class="form-label required">证照编号</span>
        </template>
      </el-form-item>

      <!-- 发证机关 -->
      <el-form-item label="发证机关" prop="issuingAuthority">
        <el-input
          v-model="formData.issuingAuthority"
          placeholder="请输入发证机关"
        />
        <template #label>
          <span class="form-label required">发证机关</span>
        </template>
      </el-form-item>

      <!-- 发证日期和到期日期 -->
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="发证日期" prop="issueDate">
            <el-date-picker
              v-model="formData.issueDate"
              type="date"
              placeholder="请选择发证日期"
              style="width: 100%"
              value-format="YYYY-MM-DD"
            />
            <template #label>
              <span class="form-label required">发证日期</span>
            </template>
          </el-form-item>
        </el-col>
        
        <el-col :span="12">
          <el-form-item label="到期日期" prop="expiryDate">
            <el-date-picker
              v-model="formData.expiryDate"
              type="date"
              placeholder="请选择到期日期"
              style="width: 100%"
              value-format="YYYY-MM-DD"
            />
            <template #label>
              <span class="form-label required">到期日期</span>
            </template>
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 证照状态 -->
      <el-form-item label="证照状态" prop="certificateStatus">
        <el-select
          v-model="formData.certificateStatus"
          placeholder="请选择证照状态"
          style="width: 100%"
        >
          <el-option label="有效" value="valid" />
          <el-option label="已过期" value="expired" />
          <el-option label="暂停" value="suspended" />
          <el-option label="吊销" value="revoked" />
          <el-option label="审核中" value="in_review" />
        </el-select>
      </el-form-item>

      <!-- 续期状态 -->
      <el-form-item label="续期状态" prop="renewalStatus">
        <el-select
          v-model="formData.renewalStatus"
          placeholder="请选择续期状态"
          style="width: 100%"
        >
          <el-option label="无需续期" value="not_required" />
          <el-option label="待续期" value="pending" />
          <el-option label="已提交续期" value="submitted" />
          <el-option label="续期已批准" value="approved" />
          <el-option label="续期被拒绝" value="rejected" />
        </el-select>
      </el-form-item>

      <!-- 文件上传 -->
      <el-form-item label="证照文件" prop="file">
        <el-upload
          v-model:file-list="fileList"
          class="upload-demo"
          :action="uploadAction"
          :headers="uploadHeaders"
          :before-upload="beforeUpload"
          :on-success="handleUploadSuccess"
          :on-error="handleUploadError"
          :on-remove="handleFileRemove"
          :limit="1"
          :accept="acceptFileTypes"
        >
          <el-button type="primary" icon="el-icon-upload">
            点击上传证照文件
          </el-button>
          <template #tip>
            <div class="el-upload__tip">
              支持 JPG、PNG、PDF 格式，文件大小不超过 10MB
            </div>
          </template>
        </el-upload>
      </el-form-item>

      <!-- 文件预览 -->
      <el-form-item v-if="currentFileUrl || formData.fileUrl" label="文件预览">
        <div class="file-preview">
          <div v-if="isImageFile" class="image-preview">
            <img :src="currentFileUrl || formData.fileUrl" alt="证照文件" />
          </div>
          <div v-else-if="isPdfFile" class="pdf-preview">
            <i class="el-icon-document"></i>
            <span>PDF文件: {{ formData.fileName || '未命名文件' }}</span>
            <a :href="currentFileUrl || formData.fileUrl" target="_blank" class="view-link">
              查看文件
            </a>
          </div>
          <div v-else-if="currentFileUrl || formData.fileUrl" class="other-preview">
            <i class="el-icon-document"></i>
            <span>{{ formData.fileName || '未命名文件' }}</span>
            <a :href="currentFileUrl || formData.fileUrl" target="_blank" class="view-link">
              下载文件
            </a>
          </div>
          <div v-else class="no-file">
            <i class="el-icon-picture-outline"></i>
            <span>暂无文件</span>
          </div>
        </div>
      </el-form-item>

      <!-- 续期提醒设置 -->
      <el-divider>续期提醒设置</el-divider>
      
      <el-form-item label="续期提醒天数" prop="renewalReminderDays">
        <el-input-number
          v-model="formData.renewalReminderDays"
          :min="1"
          :max="365"
          :step="1"
          placeholder="请设置续期提醒天数"
          style="width: 100%"
        >
          <template #append>天</template>
        </el-input-number>
        <div class="form-item-tip">
          在证照到期前多少天开始提醒续期
        </div>
      </el-form-item>

      <!-- 上次续期信息 -->
      <el-row :gutter="20" v-if="mode === 'edit'">
        <el-col :span="12">
          <el-form-item label="上次续期日期" prop="lastRenewalDate">
            <el-date-picker
              v-model="formData.lastRenewalDate"
              type="date"
              placeholder="上次续期日期"
              style="width: 100%"
              value-format="YYYY-MM-DD"
              :disabled="true"
            />
          </el-form-item>
        </el-col>
        
        <el-col :span="12">
          <el-form-item label="续期提交时间" prop="renewalSubmittedAt">
            <el-date-picker
              v-model="formData.renewalSubmittedAt"
              type="datetime"
              placeholder="续期提交时间"
              style="width: 100%"
              value-format="YYYY-MM-DD HH:mm:ss"
              :disabled="true"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 审核信息 -->
      <el-divider v-if="mode === 'edit'">审核信息</el-divider>
      
      <el-form-item v-if="mode === 'edit'" label="审核意见" prop="reviewNotes">
        <el-input
          v-model="formData.reviewNotes"
          type="textarea"
          placeholder="审核意见"
          :rows="3"
          :readonly="true"
        />
      </el-form-item>

      <el-row :gutter="20" v-if="mode === 'edit' && (formData.reviewerId || formData.reviewedAt)">
        <el-col :span="12">
          <el-form-item label="审核人" prop="reviewerId">
            <el-input
              v-model="formData.reviewerName"
              placeholder="审核人"
              :readonly="true"
            />
          </el-form-item>
        </el-col>
        
        <el-col :span="12">
          <el-form-item label="审核时间" prop="reviewedAt">
            <el-date-picker
              v-model="formData.reviewedAt"
              type="datetime"
              placeholder="审核时间"
              style="width: 100%"
              value-format="YYYY-MM-DD HH:mm:ss"
              :disabled="true"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 备注 -->
      <el-form-item label="备注" prop="remarks">
        <el-input
          v-model="formData.remarks"
          type="textarea"
          placeholder="请输入备注信息"
          :rows="3"
        />
      </el-form-item>
    </el-form>

    <!-- 表单操作按钮 -->
    <div class="form-actions">
      <el-button type="primary" :loading="loading" @click="handleSubmit">
        {{ submitButtonText }}
      </el-button>
      <el-button @click="handleCancel">
        取消
      </el-button>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getToken } from '@/utils/auth'

export default {
  name: 'CertificateForm',
  props: {
    certificate: {
      type: Object,
      default: () => ({})
    },
    companyId: {
      type: Number,
      required: true
    },
    mode: {
      type: String,
      default: 'create',
      validator: (value) => ['create', 'edit'].includes(value)
    }
  },
  emits: ['submit', 'cancel'],
  setup(props, { emit }) {
    // 表单引用
    const certificateFormRef = ref(null)
    
    // 表单数据
    const formData = reactive({
      certificateName: '',
      certificateType: 'business_license',
      certificateNumber: '',
      issuingAuthority: '',
      issueDate: new Date().toISOString().split('T')[0],
      expiryDate: new Date(new Date().setFullYear(new Date().getFullYear() + 1)).toISOString().split('T')[0],
      certificateStatus: 'valid',
      renewalStatus: 'not_required',
      renewalReminderDays: 30,
      fileUrl: '',
      fileName: '',
      fileSize: 0,
      fileHash: '',
      lastRenewalDate: null,
      renewalSubmittedAt: null,
      reviewNotes: '',
      reviewerId: null,
      reviewerName: '',
      reviewedAt: null,
      remarks: ''
    })

    // 文件上传相关
    const fileList = ref([])
    const currentFileUrl = ref('')
    const uploadHeaders = ref({
      Authorization: `Bearer ${getToken()}`
    })

    // 表单验证规则
    const formRules = reactive({
      certificateName: [
        { required: true, message: '请输入证照名称', trigger: 'blur' },
        { min: 2, max: 200, message: '长度在 2 到 200 个字符', trigger: 'blur' }
      ],
      certificateType: [
        { required: true, message: '请选择证照类型', trigger: 'change' }
      ],
      certificateNumber: [
        { required: true, message: '请输入证照编号', trigger: 'blur' },
        { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
      ],
      issuingAuthority: [
        { required: true, message: '请输入发证机关', trigger: 'blur' },
        { min: 2, max: 200, message: '长度在 2 到 200 个字符', trigger: 'blur' }
      ],
      issueDate: [
        { required: true, message: '请选择发证日期', trigger: 'change' }
      ],
      expiryDate: [
        { required: true, message: '请选择到期日期', trigger: 'change' },
        { 
          validator: (rule, value, callback) => {
            if (new Date(value) <= new Date(formData.issueDate)) {
              callback(new Error('到期日期必须晚于发证日期'))
            } else {
              callback()
            }
          },
          trigger: 'change'
        }
      ]
    })

    // 加载状态
    const loading = ref(false)

    // 计算属性
    const submitButtonText = computed(() => {
      return props.mode === 'create' ? '添加证照' : '更新证照'
    })

    const uploadAction = computed(() => {
      return `${process.env.VUE_APP_BASE_API}/api/v1/companies/${props.companyId}/certificates/upload`
    })

    const acceptFileTypes = computed(() => {
      return 'image/jpeg,image/png,image/jpg,application/pdf'
    })

    const isImageFile = computed(() => {
      const url = currentFileUrl.value || formData.fileUrl
      return url && /\.(jpg|jpeg|png|gif|bmp|webp)$/i.test(url)
    })

    const isPdfFile = computed(() => {
      const url = currentFileUrl.value || formData.fileUrl
      return url && /\.pdf$/i.test(url)
    })

    // 监听父组件传入的 certificate 数据
    watch(() => props.certificate, (newCertificate) => {
      if (newCertificate && Object.keys(newCertificate).length > 0) {
        Object.keys(formData).forEach(key => {
          if (newCertificate[key] !== undefined) {
            formData[key] = newCertificate[key]
          }
        })
      }
    }, { immediate: true })

    // 生命周期钩子
    onMounted(() => {
      if (props.mode === 'edit' && Object.keys(props.certificate).length === 0) {
        ElMessage.warning('未接收到有效的证照数据')
      }
    })

    // 方法
    const beforeUpload = (file) => {
      // 验证文件类型
      const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png'
      const isPdf = file.type === 'application/pdf'
      
      if (!isJpgOrPng && !isPdf) {
        ElMessage.error('只能上传 JPG、PNG 或 PDF 格式的文件!')
        return false
      }
      
      // 验证文件大小 (10MB)
      const isLt10M = file.size / 1024 / 1024 < 10
      if (!isLt10M) {
        ElMessage.error('文件大小不能超过 10MB!')
        return false
      }
      
      return true
    }

    const handleUploadSuccess = (response, file) => {
      if (response.success) {
        currentFileUrl.value = response.data.url
        formData.fileUrl = response.data.url
        formData.fileName = response.data.filename
        formData.fileSize = response.data.size
        formData.fileHash = response.data.hash
        
        ElMessage.success('文件上传成功')
      } else {
        ElMessage.error(response.message || '文件上传失败')
      }
    }

    const handleUploadError = (error) => {
      ElMessage.error('文件上传失败: ' + error.message)
    }

    const handleFileRemove = () => {
      currentFileUrl.value = ''
      formData.fileUrl = ''
      formData.fileName = ''
      formData.fileSize = 0
      formData.fileHash = ''
    }

    const handleSubmit = async () => {
      try {
        // 验证表单
        if (!certificateFormRef.value) return
        
        const isValid = await certificateFormRef.value.validate()
        if (!isValid) {
          ElMessage.warning('请填写完整的表单信息')
          return
        }

        // 设置加载状态
        loading.value = true

        // 准备提交数据
        const submitData = {
          companyId: props.companyId,
          ...formData,
          // 确保数字字段格式正确
          renewalReminderDays: Number(formData.renewalReminderDays) || 30
        }

        // 清理空值
        Object.keys(submitData).forEach(key => {
          if (submitData[key] === null || submitData[key] === undefined || submitData[key] === '') {
            delete submitData[key]
          }
        })

        // 触发提交事件
        emit('submit', submitData)
      } catch (error) {
        ElMessage.error('表单验证失败: ' + error.message)
      } finally {
        loading.value = false
      }
    }

    const handleCancel = () => {
      emit('cancel')
    }

    return {
      certificateFormRef,
      formData,
      formRules,
      fileList,
      currentFileUrl,
      uploadHeaders,
      loading,
      submitButtonText,
      uploadAction,
      acceptFileTypes,
      isImageFile,
      isPdfFile,
      beforeUpload,
      handleUploadSuccess,
      handleUploadError,
      handleFileRemove,
      handleSubmit,
      handleCancel
    }
  }
}
</script>

<style scoped>
.certificate-form {
  padding: 20px 0;
}

.form-label {
  font-weight: 600;
}

.form-label.required::before {
  content: '*';
  color: #f56c6c;
  margin-right: 4px;
}

.form-item-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.file-preview {
  display: flex;
  align-items: center;
  padding: 12px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  background-color: #f5f7fa;
}

.file-preview .image-preview img {
  max-width: 200px;
  max-height: 200px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}

.file-preview .pdf-preview,
.file-preview .other-preview,
.file-preview .no-file {
  display: flex;
  align-items: center;
  gap: 8px;
}

.file-preview .view-link {
  margin-left: 12px;
  color: #409eff;
  text-decoration: none;
}

.file-preview .view-link:hover {
  text-decoration: underline;
}

.file-preview .no-file {
  color: #909399;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  padding-top: 24px;
  border-top: 1px solid #ebeef5;
  margin-top: 20px;
}

:deep(.el-divider__text) {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  background-color: #fff;
}

:deep(.el-input__inner),
:deep(.el-textarea__inner) {
  border-color: #dcdfe6;
}

:deep(.el-input__inner:hover),
:deep(.el-textarea__inner:hover) {
  border-color: #c0c4cc;
}

:deep(.el-input__inner:focus),
:deep(.el-textarea__inner:focus) {
  border-color: #409eff;
}

:deep(.el-upload) {
  width: 100%;
}

:deep(.el-upload .el-upload-dragger) {
  width: 100%;
}
</style>