<template>
  <div class="login-form-container">
    <div class="login-title">
      <div
        class="title flex-center mb-8"
        style="position: relative; cursor: pointer"
        @click="goHome"
      >
        <div class="logo mr-8"></div>
        <div class="app-logo-font">{{ title || defaultTitle }}</div>
        <el-tag class="app-logo-versionTag">v3.4.9</el-tag>
      </div>
      <div class="sub-title text-center" v-if="subTitle">
        <el-text type="info">{{ subTitle }}</el-text>
      </div>
    </div>
    <img
      v-if="logoAndCopyright.isShowLogoAndCopyright"
      src="../../assets/logo-jr.png"
      style="position: absolute; top: 20px; left: 20px"
    />
    <el-card class="login-card">
      <slot></slot>
    </el-card>
    <div
      v-if="logoAndCopyright.isShowLogoAndCopyright"
      style="
        position: absolute;
        bottom: 10px;
        left: 50%;
        transform: translateX(-50%);
        color: #909399;
      "
    >
      Copyright © 2023-2025 杰软科技（集团）有限公司
    </div>
  </div>
</template>
<script setup lang="ts">
import useStore from '@/stores'
import { useRouter } from 'vue-router'

const defaultTitle = import.meta.env.VITE_APP_TITLE
defineOptions({ name: 'LoginContainer' })
defineProps({
  title: String,
  subTitle: String
})
const { logoAndCopyright } = useStore()
const router = useRouter()

const goHome = () => {
  router.push({ name: 'home' })
}
</script>
<style lang="scss" scope>
.login-form-container {
  width: 480px;

  .app-logo-font {
    background: #2f99ff;
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: Arial Black;
    font-style: normal;
    font-weight: 900;
  }
  .app-logo-versionTag {
    position: absolute;
    top: -4px;
    right: 66px;
  }
  .login-title {
    margin-bottom: 32px;

    .title {
      font-size: 32px;
      .logo {
        background-image: url('@/assets/logo.png');
        background-size: 100% 100%;
        width: 30px;
        height: 30px;
      }
    }
    .sub-title {
      font-size: 16px;
    }
  }
  .login-card {
    border-radius: 8px;
    padding: 18px;
  }
}
</style>
