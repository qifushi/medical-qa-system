<template>
  <el-dialog v-model="personalInformationDialogVisible" title="个人信息">
    <el-form
      ref="personalInformationFormRef"
      class="reset-password-form mb-24"
      label-width="auto"
      :model="personalInformationForm"
    >
      <el-form-item prop="" label="姓名" style="margin-bottom: 8px">
        <el-input v-model="personalInformationForm.nick_name" class="input-item"> </el-input>
      </el-form-item>
      <el-form-item prop="" label="手机号码" style="margin-bottom: 8px">
        <el-input v-model="personalInformationForm.phone" class="input-item"> </el-input>
      </el-form-item>
      <el-form-item prop="" label="应用背景色" style="margin-bottom: 8px">
        <el-color-picker
          v-model="personalInformationForm.app_theme_color"
          show-alpha
          :predefine="predefineColors"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click.prevent="personalInformationDialogVisible = false"> 取消 </el-button>
        <el-button type="primary" @click="submit(personalInformationFormRef)" :loading="loading">
          保存
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>
<script setup lang="ts">
import UserApi from '@/api/user'
import useStore from '@/stores'
import { MsgSuccess } from '@/utils/message'
import type { FormInstance } from 'element-plus'
import { ref } from 'vue'
const { user } = useStore()

const personalInformationDialogVisible = ref(false)
const loading = ref(false)

const personalInformationForm = ref<any>({
  id: user.userInfo?.id,
  nick_name: user.userInfo?.nick_name,
  phone: user.userInfo?.phone,
  app_theme_color: user.userInfo?.app_theme_color
})
const predefineColors = ref([
  '#ff4500',
  '#ff8c00',
  '#ffd700',
  '#90ee90',
  '#00ced1',
  '#1e90ff',
  '#c71585',
])
const personalInformationFormRef = ref()

const open = () => {
  personalInformationDialogVisible.value = true
}

const submit = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      UserApi.putPersonalInformation(
        personalInformationForm.value.id,
        personalInformationForm.value,
        loading
      ).then((res:any) => {
        MsgSuccess('编辑成功')
        // 修改app_theme_color 通知application页面刷新
        user.changeAppThemeColor(personalInformationForm.value.app_theme_color)
        personalInformationDialogVisible.value = false
      })
    }
  })
}

defineExpose({ open })
</script>
<style></style>
