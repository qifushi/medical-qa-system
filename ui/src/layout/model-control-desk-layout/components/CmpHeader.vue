<template>
  <div ref="headerRef" :class="['cmp-header', shouldShowHomeStyle ? 'isHome' : '']">
    <div class="cmp-header-content">
      <div class="header-logo" @click="toPage('/model-control-desk/index')">
        <div class="header-logo-content logo-white">
          <img class=""   v-if="logoAndCopyright.isShowLogoAndCopyright" src="~@/assets/model-control-desk/jr-square.png" alt="" />
          <span>Model Studio</span>
        </div>
        <div class="header-logo-content logo-black">
          <img class=""  v-if="logoAndCopyright.isShowLogoAndCopyright"  src="~@/assets/model-control-desk/jr-square.png" alt="" />
          <span>Model Studio</span>
        </div>
      </div>

      <div class="nav-wrap">
        <div
          @click="toPage('/model-control-desk/index')"
          :class="['nav-item', activeNav == 'ModelControlIndex' ? 'active' : '']"
        >
          首页
        </div>
        <div
          class="nav-item"
          :class="[
            'nav-item',
            ['DataSource', 'DataSourceDetail'].includes(String(activeNav)) ? 'active' : ''
          ]"
          @click="toPage('/model-control-desk/data-source')"
        >
          数据源管理
        </div>
        <div
          class="nav-item"
          :class="['nav-item', activeNav == 'DataTreating' ? 'active' : '']"
          @click="toPage('/model-control-desk/data-treating')"
        >
          数据准备
        </div>
        <div
          class="nav-item"
          :class="[
            'nav-item',
            ['ModelTraining', 'ModelTrainingMajor', 'ModelTrainingSimpleness'].includes(
              String(activeNav)
            )
              ? 'active'
              : ''
          ]"
          @click="toPage('/model-control-desk/model-training')"
        >
          模型训练
        </div>
        <div
          class="nav-item"
          :class="['nav-item', activeNav == 'ModelEvaluation' ? 'active' : '']"
          @click="toPage('/model-control-desk/model-evaluation')"
        >
          模型评测
        </div>
        <div
          class="nav-item"
          :class="['nav-item', activeNav == 'ModelRelease' ? 'active' : '']"
          @click="toPage('/model-control-desk/model-release')"
        >
          模型发布
        </div>
      </div>
      <div class="user-wrap">
        <template v-if="user.userInfo">
          <el-dropdown trigger="click" type="primary">
            <div class="flex-center cursor userInfo">
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
                <el-dropdown-item class="border-t p-8" @click="toPage('/application')">
                  {{ $t('layout.topbar.avatar.controlPanel') }}
                </el-dropdown-item>
                <el-dropdown-item class="border-t p-8" @click="handleGuide">
                  操作指引
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
    <PersonalInformationDialog ref="refPersonalInformation" />
    <ResetPassword ref="refResetPassword" />
  </div>
</template>

<script setup lang="ts">
import PersonalInformationDialog from '@/layout/components/top-bar/avatar/PersonaInformationDialog.vue'
import ResetPassword from '@/layout/components/top-bar/avatar/ResetPassword.vue'
import useStore from '@/stores'
import { computed, ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const { logoAndCopyright, modelControlDesk } = useStore()

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

const toPage = (path: string) => {
  if (path === '/login') {
    user.logout()
  }
  path && router.push(path)
}

const headerRef = ref<HTMLElement | null>(null)
const scrollY = ref(0)

const shouldShowHomeStyle = computed(() => {
  return activeNav.value === 'ModelControlIndex' && scrollY.value <= 80
})

const handleScroll = () => {
  scrollY.value = window.scrollY || document.documentElement.scrollTop
}
const throttle = <T extends any[]>(
  func: (...args: T) => void,
  limit: number
): ((...args: T) => void) => {
  let lastFunc: ReturnType<typeof setTimeout> | null = null
  let lastRan: number | null = null

  return function (this: any, ...args: T) {
    const context = this

    if (!lastRan) {
      func.apply(context, args)
      lastRan = Date.now()
    } else {
      if (lastFunc) {
        clearTimeout(lastFunc)
      }

      lastFunc = setTimeout(
        function () {
          if (Date.now() - lastRan! >= limit) {
            func.apply(context, args)
            lastRan = Date.now()
          }
        },
        limit - (Date.now() - lastRan)
      )
    }
  }
}

onMounted(() => {
  window.addEventListener('scroll', throttle(handleScroll, 100))
  handleScroll()
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
})
const handleGuide = () => {
  modelControlDesk.toggleModalVisible(true)
}
</script>

<style lang="scss" scoped>
.cmp-header {
  position: fixed;
  left: 0;
  top: 0;
  width: 100vw;
  background: var(--app-header-bg-color);
  z-index: 999;
  box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.12);
  transition: all 0.3s;
  &.isHome {
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    .cmp-header-content {
      width: 1200px;
      height: 78px;

      .header-logo {
        color: #1d3885;
        .header-logo-content {
          &.logo-white {
            display: flex;
            img {
              width: 66px;
              margin-right: 4px;
            }
          }
          &.logo-black {
            display: none;
          }
        }
        img {
          // width: 60%;
          width: 54px;
        }
      }
      .nav-wrap {
        .nav-item {
          line-height: 78px;
          color: #1d3885;
          &.active,
          &:hover {
            background-color: rgba(49, 158, 255, 0.7);
            color: #fff;
          }
        }
      }
      .userInfo {
        color: #1d3885;
      }
    }
  }

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
    width: 100vw;
    box-sizing: border-box;
    padding-left: 20px;
    height: 56px;
    display: flex;
    align-items: center;
    transition: all 0.5s;
    margin: 0 auto;

    .header-logo {
      margin-right: 24px;
      // margin-left: 70px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      color: #1d3885;
      font-family: Arial Black;
      font-style: normal;
      font-weight: 900;
      font-size: 24px;
      .header-logo-content {
        display: flex;
        align-items: center;

        &.logo-white {
          display: none;
        }
        &.logo-black {
          display: flex;
        }
      }
      img {
        // width: 60%;
        width: 44px;
        object-fit: contain;
        margin-right: 8px;
        transition: all 0.3s;
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
        line-height: 56px;
        // padding: 0 32px;
        cursor: pointer;
        transition: all 0.2s;
        user-select: none;
        color: #1d3885;
        margin-left: 12px;
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
      width: 126px;
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
  width: 36px;
  height: 36px;
  box-sizing: border-box;
  padding: 6px;
  background-color: #fff !important;
}
@media (max-width: 1200px) {
  .cmp-header {
    .cmp-header-content {
      .header-logo-content {
        font-size: 16px;
      }
      .nav-wrap {
        .nav-item {
          margin-left: 12px;
        }
      }
    }
  }
}
@media (max-width: 840px) {
  .cmp-header {
    .cmp-header-content {
      .header-logo-content {
        font-size: 14px;
      }
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
