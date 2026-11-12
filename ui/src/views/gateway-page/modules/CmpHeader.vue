<template>
  <div class="cmp-header">
    <div class="cmp-header-content">
      <div v-if="logoAndCopyright.isShowLogoAndCopyright" class="header-logo" @click="goHome">
        <img src="~@/assets/gatewayPage/logo.png" alt="" />
      </div>
      <div v-else class="header-logo1" @click="goHome">
        <div class="app-logo-font">Smart Brain</div>
      </div>
      <div class="nav-wrap">
        <div @click="goHome" :class="['nav-item', activeNav == 'GatewayPage' ? 'active' : '']">
          首页
        </div>
        <div
          class="nav-item"
          :class="{ active: isShowScenarios() }"
          @click="goApplicationScenarios"
        >
          应用场景
        </div>
        <div class="nav-item">领域模型</div>
        <div
          class="nav-item"
          :class="['nav-item', activeNav == 'GatewayApplicationDigitalChat' ? 'active' : '']"
          @click="goDigital"
        >
          数字人
        </div>
      </div>
      <div class="user-wrap">
        <template v-if="user.userInfo">
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
                <el-dropdown-item class="border-t p-8" @click="toControlPanel">
                  {{ $t('layout.topbar.avatar.controlPanel') }}
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
        </template>
        <template v-else>
          <span class="btn" @click="handleLogin">登录</span>
          <!-- <el-divider direction="vertical" />
          <span class="btn">注册</span> -->
        </template>
      </div>
    </div>
  </div>
  <PersonalInformationDialog ref="refPersonalInformation" />
  <ResetPassword ref="refResetPassword" />
</template>

<script setup lang="ts">
import PersonalInformationDialog from '@/layout/components/top-bar/avatar/PersonaInformationDialog.vue'
import ResetPassword from '@/layout/components/top-bar/avatar/ResetPassword.vue'
import useStore from '@/stores'
import { computed, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const { logoAndCopyright } = useStore()

const activeNav = computed(() => {
  return route.name
})
const route = useRoute()
const router = useRouter()
const handleLogin = () => {
  const currentPath = window.location.pathname
  router.push({
    path: '/login',
    query: {
      redirect: currentPath.indexOf('/model-control-desk') > -1 ? 'ModelControlIndex' : 'home'
    }
  })
}
const { user } = useStore()
console.log('user', user)
const logout = () => {
  const currentPath = window.location.pathname
  user.logout().then(() => {
    router.push({
      path: '/login',
      query: {
        redirect: currentPath.indexOf('/model-control-desk') > -1 ? 'ModelControlIndex' : 'home'
      }
    })
  })
}
const refPersonalInformation = ref()
const openPersonalInformation = () => {
  refPersonalInformation.value?.open()
}
const refResetPassword = ref()
const openResetPassword = () => {
  refResetPassword.value?.open()
}
const toControlPanel = () => {
  router.push('/application')
}
const toModelPanel = () => {
  router.push('/model-control-desk')
}
const goDigital = () => {
  router.push({ name: 'GatewayApplicationDigitalChat' })
}

const goApplicationScenarios = () => {
  // router.push('/gateway-application-scenarios')
  router.push({ name: 'GatewayApplicationOverview' })
}
const goHome = () => {
  router.push('/')
}
const isShowScenarios = () => {
  return (
    activeNav.value == 'GatewayApplicationScenarios' ||
    activeNav.value == 'GatewayApplicationScenariosVisualModel' ||
    activeNav.value == 'GatewayApplicationOverview'
  )
}
</script>

<style lang="scss" scoped>
.cmp-header {
  position: fixed;
  left: 0;
  top: 0;
  width: 100vw;
  background-color: #fff;
  z-index: 999;
  box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.12);
  .app-logo-font {
    background: #2f99ff;
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: Arial Black;
    font-style: normal;
    font-weight: 900;
    font-size: 36px;
  }
  .cmp-header-content {
    max-width: 1200px;
    margin: 0 auto;
    height: 78px;
    display: flex;
    align-items: center;
    .header-logo {
      width: 240px;
      margin-right: 20px;
      // margin-left: 70px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      img {
        width: 60%;
      }
    }
    .header-logo1 {
      width: 240px;
      margin-right: 40px;
      // margin-left: 70px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      img {
        width: 100%;
      }
    }

    .nav-wrap {
      // width: calc(100% - 128px - 140px);
      flex: 1;
      height: 100%;
      display: flex;
      align-items: center;
      // justify-content: space-between;
      .nav-item {
        height: 100%;
        line-height: 78px;
        // padding: 0 32px;
        cursor: pointer;
        transition: all 0.2s;
        user-select: none;
        color: #1d3885;
        background-color: #fff;
        margin-left: 48px;
        width: 100px;
        text-align: center;
        &:first-child {
          margin-left: 0;
        }
        &.active,
        &:hover {
          background-color: #319eff;
          color: #fff;
        }
      }
    }
    .user-wrap {
      width: 84px;
      user-select: none;
      color: #666666;
      .btn {
        cursor: pointer;
      }
      & > .btn {
        &:hover {
          opacity: 0.8;
        }
      }
    }
  }
}
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
@media (max-width: 840px) {
  .cmp-header {
    .cmp-header-content {
      .header-logo {
        margin-right: 12px;
        margin-left: 0;
      }
      .nav-wrap {
        .nav-item {
          margin-left: 12px;
        }
      }
      .user-wrap {
        margin-left: 12px;
      }
    }
  }
}
@media (max-width: 560px) {
  .cmp-header {
    .cmp-header-content {
      .header-logo {
        display: none;
      }
      .nav-wrap {
        .nav-item {
          width: 70px;
          padding: 0;
          margin-left: 0;
        }
      }
    }
  }
}
</style>
