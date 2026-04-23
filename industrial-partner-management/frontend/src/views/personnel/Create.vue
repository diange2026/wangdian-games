<template>
  <div class="create-personnel-container">
    <h1 class="page-title">新增人员</h1>
    <personnel-form-dialog
      v-model="formVisible"
      :personnel-data="null"
      @success="handleFormSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import PersonnelFormDialog from './components/PersonnelFormDialog.vue'

const router = useRouter()
const formVisible = ref(true)

onMounted(() => {
  formVisible.value = true
})

const handleFormSuccess = () => {
  ElMessage.success('人员创建成功')
  router.push({ name: 'PersonnelList' })
}
</script>

<style scoped>
.create-personnel-container {
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
</style>