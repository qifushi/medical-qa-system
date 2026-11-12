<template>
  <el-dropdown trigger="click" type="primary">
    <div class="flex-center cursor">
      <AppAvatar class="avatar-user">
        <img src="@/assets/user-icon.png" alt="" />
      </AppAvatar>
      <span class="ml-8">{{ user.userInfo?.username }}</span>
      <el-icon class="el-icon--right">
        <CaretBottom />
      </el-icon>
    </div>

    <template #dropdown>
      <el-dropdown-menu class="avatar-dropdown">
        <div class="userInfo">
          <p class="bold mb-4" style="font-size: 14px">{{ user.userInfo?.username }}</p>
          <p>
            <el-text type="info">
              {{ user.userInfo?.email }}
            </el-text>
          </p>
        </div>

        <el-dropdown-item class="border-t p-8" @click="toModelPanel">
          {{ $t('layout.topbar.avatar.modelPanel') }}
        </el-dropdown-item>
        <el-dropdown-item class="border-t p-8" @click="openResetPassword">
          {{ $t('layout.topbar.avatar.resetPassword') }}
        </el-dropdown-item>
        <!-- 关于 -->
        <!-- <el-dropdown-item class="border-t" @click="openAbout"> {{ $t("layout.topbar.avatar.about") }} </el-dropdown-item> -->
        <el-dropdown-item class="border-t" @click="openPersonalInformation">
          个人信息
        </el-dropdown-item>
        <el-dropdown-item class="border-t" @click="logout">
          {{ $t('layout.topbar.avatar.logout') }}
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
  <ResetPassword ref="resetPasswordRef"></ResetPassword>
  <UserPwdDialog ref="UserPwdDialogRef" />
  <PersonalInformationDialog ref="PersonalInformationRef" />
</template>
<script setup lang="ts">
import useStore from '@/stores'
import UserPwdDialog from '@/views/user-manage/component/UserPwdDialog.vue'
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import PersonalInformationDialog from './PersonaInformationDialog.vue'
import ResetPassword from './ResetPassword.vue'

const { user } = useStore()
const router = useRouter()

const UserPwdDialogRef = ref()
const resetPasswordRef = ref<InstanceType<typeof ResetPassword>>()
const PersonalInformationRef = ref()

const openResetPassword = () => {
  resetPasswordRef.value?.open()
}
const toModelPanel = () => {
  router.push('/model-control-desk')
}

const openPersonalInformation = () => {
  PersonalInformationRef.value?.open()
}
const logout = () => {
  user.logout().then(() => {
    router.push({ name: 'login' })
  })
}

onMounted(() => {
  if (user.userInfo?.is_edit_password) {
    UserPwdDialogRef.value.open(user.userInfo)
  }
})
</script>
<style lang="scss" scoped>
.avatar-dropdown {
  min-width: 210px;
  .userInfo {
    padding: 12px 11px;
  }
  :deep(.el-dropdown-menu__item) {
    padding: 12px 11px;
  }
}
.avatar-user {
  background-color: #fff !important;
}
</style>
