<template>
  <div class="edit-personnel-container">
    <h1 class="page-title">编辑人员</h1>
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>
    <div v-else-if="personnelData">
      <personnel-form-dialog
        v-model="formVisible"
        :personnel-data="personnelData"
        @success="handleFormSuccess"
      />
    </div>
    <div v-else class="error-container">
      <el-empty description="人员不存在或已被删除" />
      <el-button type="primary" @click="goBack">返回人员列表</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getPersonnelDetail } from '@/api/personnel'
import PersonnelFormDialog from './components/PersonnelFormDialog.vue'
import type { PersonnelInDB } from '@/types/personnel'

const route = useRoute()
const router = useRouter()
const loading = ref(true)
const personnelData = ref<PersonnelInDB | null>(null)
const formVisible = ref(false)

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
    formVisible.value = true
  } catch (error) {
    console.error('加载人员详情失败:', error)
    ElMessage.error('加载人员详情失败')
  } finally {
    loading.value = false
  }
}

const handleFormSuccess = () => {
  ElMessage.success('人员信息更新成功')
  router.push({ name: 'PersonnelList' })
}

const goBack = () => {
  router.push({ name: 'PersonnelList' })
}
</script>

<style scoped>
.edit-personnel-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 84px);
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 20px;
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
</style>