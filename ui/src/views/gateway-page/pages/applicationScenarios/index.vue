<template>
  <div class="applicationScenarios">
    <CmpHeader />
    <div class="banner-container">
      <img class="banner-img" :src="visualModelBanner" alt="" />
      <div class="banner-text-content">
        <h1 class="banner-title">视觉模型检测对象行为异常</h1>
        <div class="banner-desc">视听双鉴辨异常，考场秩序有保障</div>
      </div>
    </div>
    <CmpBreadcrumb :items="breadcrumbItems" separatorIcon="ArrowRight" theme="light" />

    <div class="main-page-content">
      <MdPreview
        noIconfont
        ref="editorRef"
        editorId="preview-only"
        :modelValue="mdContentRaw"
        class="maxkb-md"
        :codeFoldable="false"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { HomeFilled, Document, Setting } from '@element-plus/icons-vue'
import CmpHeader from '@/views/gateway-page/modules/CmpHeader.vue'
import mdContentRaw from './modules/README.md?raw'
import visualModelBanner from '@/assets/gatewayPage/visualModel_banner.png'
import CmpBreadcrumb from '../../modules/CmpBreadcrumb.vue'

import 'md-editor-v3/lib/style.css'

const breadcrumbItems = ref([
  { title: '首页', path: '/gateway-page' },
  { title: '应用场景', path: '/gateway-application-overview' },
  { title: '视觉模型检测对象行为异常', path: '/gateway-application-scenarios-visualModel' },
  { title: '试一试', path: '' }
])
</script>

<style lang="scss" scoped>
.applicationScenarios {
  // height: 100vh;
  box-sizing: border-box;
  overflow-y: auto;
  padding-top: 78px;
  .banner-container {
    box-shadow: 0 8px 24px 0 rgba(0, 0, 0, 0.08);
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 14px;
    justify-content: center;
    min-height: 260px;
    min-width: 1250px;
    height: 400px;
    user-select: none;
    .banner-img {
      width: 100%;
      position: absolute;
      left: 0;
      top: 78px;
      z-index: 1;
      -o-object-fit: cover;
      object-fit: cover;
      min-height: 260px;
      min-width: 1250px;
      height: 400px;
    }
    .banner-text-content {
      z-index: 1;
      margin: 0px auto;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      align-items: flex-start;
      width: clamp(1200px, 75vw, 1800px);
    }
    .banner-title {
      color: #fff;
      font-size: 40px;
      font-weight: 500;
      margin-bottom: 8px;
    }
    .banner-desc {
      line-height: 36px;
      opacity: 0.7;
      font-size: 18px;
      color: #fff;
    }
    .banner-btn {
      margin-top: 24px;
      padding: 8px 30px;
      border: 1px #fff solid;
      color: #fff;
      cursor: pointer;
      &:hover {
        background: rgba(255, 255, 255, 0.08);
      }
    }
  }
  .main-page-content {
    max-width: 1200px;
    box-sizing: border-box;
    margin: 0 auto;
    padding: 0 24px;
    &::-webkit-scrollbar {
      width: 12px;
      height: 0;
    }
  }
}
</style>
