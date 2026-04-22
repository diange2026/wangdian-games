<template>
  <div class="company-form">
    <el-form
      ref="companyFormRef"
      :model="formData"
      :rules="formRules"
      label-width="120px"
      label-position="left"
      size="medium"
      :disabled="loading"
    >
      <!-- 单位基本信息 -->
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="单位编码" prop="companyCode">
            <el-input
              v-model="formData.companyCode"
              placeholder="请输入单位编码"
              :disabled="mode === 'edit'"
            />
            <template #label>
              <span class="form-label required">单位编码</span>
            </template>
          </el-form-item>
        </el-col>
        
        <el-col :span="12">
          <el-form-item label="单位名称" prop="companyName">
            <el-input
              v-model="formData.companyName"
              placeholder="请输入单位全称"
            />
            <template #label>
              <span class="form-label required">单位名称</span>
            </template>
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 单位类型与性质 -->
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="单位类型" prop="companyType">
            <el-select
              v-model="formData.companyType"
              placeholder="请选择单位类型"
              style="width: 100%"
            >
              <el-option label="供应商" value="supplier" />
              <el-option label="承包商" value="contractor" />
              <el-option label="服务商" value="service_provider" />
              <el-option label="合作伙伴" value="partner" />
              <el-option label="其他" value="other" />
            </el-select>
            <template #label>
              <span class="form-label required">单位类型</span>
            </template>
          </el-form-item>
        </el-col>
        
        <el-col :span="12">
          <el-form-item label="企业性质" prop="businessNature">
            <el-select
              v-model="formData.businessNature"
              placeholder="请选择企业性质"
              style="width: 100%"
            >
              <el-option label="国有企业" value="state_owned" />
              <el-option label="民营企业" value="private" />
              <el-option label="外资企业" value="foreign_invested" />
              <el-option label="合资企业" value="joint_venture" />
            </el-select>
            <template #label>
              <span class="form-label">企业性质</span>
            </template>
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 注册资本与实缴资本 -->
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="注册资本" prop="registrationCapital">
            <el-input-number
              v-model="formData.registrationCapital"
              placeholder="请输入注册资本"
              :min="0"
              :step="1"
              style="width: 100%"
              :precision="2"
            >
              <template #append>万元</template>
            </el-input-number>
          </el-form-item>
        </el-col>
        
        <el-col :span="12">
          <el-form-item label="实缴资本" prop="actualCapital">
            <el-input-number
              v-model="formData.actualCapital"
              placeholder="请输入实缴资本"
              :min="0"
              :step="1"
              style="width: 100%"
              :precision="2"
            >
              <template #append>万元</template>
            </el-input-number>
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 地址信息 -->
      <el-form-item label="注册地址" prop="registeredAddress">
        <el-input
          v-model="formData.registeredAddress"
          placeholder="请输入注册地址（应与工商登记一致）"
          type="textarea"
          :rows="2"
        />
        <template #label>
          <span class="form-label required">注册地址</span>
        </template>
      </el-form-item>

      <el-form-item label="经营地址" prop="businessAddress">
        <el-input
          v-model="formData.businessAddress"
          placeholder="请输入经营地址（如与注册地址不同请填写）"
          type="textarea"
          :rows="2"
        />
      </el-form-item>

      <!-- 法人信息 -->
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="法人代表" prop="legalPerson">
            <el-input
              v-model="formData.legalPerson"
              placeholder="请输入法人代表姓名"
            />
            <template #label>
              <span class="form-label required">法人代表</span>
            </template>
          </el-form-item>
        </el-col>
        
        <el-col :span="12">
          <el-form-item label="法人身份证号" prop="legalPersonIdCard">
            <el-input
              v-model="formData.legalPersonIdCard"
              placeholder="请输入法人身份证号"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 统一信用代码 -->
      <el-form-item label="统一信用代码" prop="creditCode">
        <el-input
          v-model="formData.creditCode"
          placeholder="请输入统一社会信用代码"
        />
        <template #label>
          <span class="form-label">统一信用代码</span>
        </template>
      </el-form-item>

      <!-- 经营范围 -->
      <el-form-item label="经营范围" prop="businessScope">
        <el-input
          v-model="formData.businessScope"
          placeholder="请输入经营范围（按工商登记填写）"
          type="textarea"
          :rows="3"
        />
      </el-form-item>

      <!-- 主要联系人 -->
      <el-divider>主要联系人信息</el-divider>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="联系人" prop="contactPerson">
            <el-input
              v-model="formData.contactPerson"
              placeholder="请输入联系人姓名"
            />
            <template #label>
              <span class="form-label required">联系人</span>
            </template>
          </el-form-item>
        </el-col>
        
        <el-col :span="12">
          <el-form-item label="联系电话" prop="contactPhone">
            <el-input
              v-model="formData.contactPhone"
              placeholder="请输入联系电话"
            />
            <template #label>
              <span class="form-label required">联系电话</span>
            </template>
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item label="联系邮箱" prop="contactEmail">
        <el-input
          v-model="formData.contactEmail"
          placeholder="请输入联系邮箱"
          type="email"
        />
      </el-form-item>

      <!-- 财务联系人 -->
      <el-divider>财务联系人信息</el-divider>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="财务联系人" prop="financialContact">
            <el-input
              v-model="formData.financialContact"
              placeholder="请输入财务联系人"
            />
          </el-form-item>
        </el-col>
        
        <el-col :span="12">
          <el-form-item label="财务电话" prop="financialPhone">
            <el-input
              v-model="formData.financialPhone"
              placeholder="请输入财务电话"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 技术联系人 -->
      <el-divider>技术联系人信息</el-divider>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="技术联系人" prop="technicalContact">
            <el-input
              v-model="formData.technicalContact"
              placeholder="请输入技术联系人"
            />
          </el-form-item>
        </el-col>
        
        <el-col :span="12">
          <el-form-item label="技术电话" prop="technicalPhone">
            <el-input
              v-model="formData.technicalPhone"
              placeholder="请输入技术电话"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 风险等级 -->
      <el-form-item label="风险等级" prop="riskLevel">
        <el-select
          v-model="formData.riskLevel"
          placeholder="请选择风险等级"
          style="width: 100%"
        >
          <el-option label="低风险" value="low" />
          <el-option label="中风险" value="medium" />
          <el-option label="高风险" value="high" />
          <el-option label="极高风险" value="critical" />
        </el-select>
      </el-form-item>

      <!-- 合作信息 -->
      <el-divider>合作信息</el-divider>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="合作级别" prop="cooperationLevel">
            <el-select
              v-model="formData.cooperationLevel"
              placeholder="请选择合作级别"
              style="width: 100%"
            >
              <el-option label="战略合作" value="strategic" />
              <el-option label="重点合作" value="key" />
              <el-option label="普通合作" value="regular" />
              <el-option label="试用合作" value="trial" />
            </el-select>
          </el-form-item>
        </el-col>
        
        <el-col :span="12">
          <el-form-item label="合作开始日期" prop="cooperationStartDate">
            <el-date-picker
              v-model="formData.cooperationStartDate"
              type="date"
              placeholder="请选择合作开始日期"
              style="width: 100%"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 备注 -->
      <el-form-item label="备注" prop="remarks">
        <el-input
          v-model="formData.remarks"
          placeholder="请输入备注信息"
          type="textarea"
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
import { ElMessage } from 'element-plus'
import { validateCompanyCode, validatePhoneNumber, validateEmail } from '@/utils/validation'

export default {
  name: 'CompanyForm',
  props: {
    company: {
      type: Object,
      default: () => ({})
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
    const companyFormRef = ref(null)
    
    // 表单数据
    const formData = reactive({
      companyCode: '',
      companyName: '',
      companyType: 'supplier',
      businessNature: 'private',
      registrationCapital: 0,
      actualCapital: 0,
      registeredAddress: '',
      businessAddress: '',
      legalPerson: '',
      legalPersonIdCard: '',
      creditCode: '',
      businessScope: '',
      contactPerson: '',
      contactPhone: '',
      contactEmail: '',
      financialContact: '',
      financialPhone: '',
      technicalContact: '',
      technicalPhone: '',
      riskLevel: 'medium',
      cooperationLevel: 'regular',
      cooperationStartDate: new Date().toISOString().split('T')[0],
      remarks: ''
    })

    // 表单验证规则
    const formRules = reactive({
      companyCode: [
        { required: true, message: '请输入单位编码', trigger: 'blur' },
        { min: 6, max: 50, message: '长度在 6 到 50 个字符', trigger: 'blur' },
        { validator: validateCompanyCode, trigger: 'blur' }
      ],
      companyName: [
        { required: true, message: '请输入单位名称', trigger: 'blur' },
        { min: 2, max: 200, message: '长度在 2 到 200 个字符', trigger: 'blur' }
      ],
      companyType: [
        { required: true, message: '请选择单位类型', trigger: 'change' }
      ],
      registeredAddress: [
        { required: true, message: '请输入注册地址', trigger: 'blur' },
        { min: 10, max: 500, message: '长度在 10 到 500 个字符', trigger: 'blur' }
      ],
      legalPerson: [
        { required: true, message: '请输入法人代表', trigger: 'blur' },
        { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
      ],
      contactPerson: [
        { required: true, message: '请输入联系人', trigger: 'blur' },
        { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
      ],
      contactPhone: [
        { required: true, message: '请输入联系电话', trigger: 'blur' },
        { validator: validatePhoneNumber, trigger: 'blur' }
      ],
      contactEmail: [
        { validator: validateEmail, trigger: 'blur' }
      ],
      creditCode: [
        { pattern: /^[A-Z0-9]{18}$/, message: '统一信用代码格式不正确', trigger: 'blur' }
      ]
    })

    // 加载状态
    const loading = ref(false)

    // 计算属性
    const submitButtonText = computed(() => {
      return props.mode === 'create' ? '创建单位' : '更新信息'
    })

    // 监听父组件传入的 company 数据
    watch(() => props.company, (newCompany) => {
      if (newCompany) {
        Object.keys(formData).forEach(key => {
          if (newCompany[key] !== undefined) {
            formData[key] = newCompany[key]
          }
        })
      }
    }, { immediate: true })

    // 生命周期钩子
    onMounted(() => {
      if (props.mode === 'edit' && Object.keys(props.company).length === 0) {
        ElMessage.warning('未接收到有效的单位数据')
      }
    })

    // 方法
    const handleSubmit = async () => {
      try {
        // 验证表单
        if (!companyFormRef.value) return
        
        const isValid = await companyFormRef.value.validate()
        if (!isValid) {
          ElMessage.warning('请填写完整的表单信息')
          return
        }

        // 设置加载状态
        loading.value = true

        // 准备提交数据
        const submitData = {
          ...formData,
          // 确保数字字段格式正确
          registrationCapital: Number(formData.registrationCapital) || 0,
          actualCapital: Number(formData.actualCapital) || 0
        }

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
      companyFormRef,
      formData,
      formRules,
      loading,
      submitButtonText,
      handleSubmit,
      handleCancel
    }
  }
}
</script>

<style scoped>
.company-form {
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
</style>