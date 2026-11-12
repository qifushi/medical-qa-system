<template>
  <div class="applicationScenarios">
    <CmpHeader />
    <div class="banner-container">
      <img class="banner-img" :src="visualModelBanner" alt="" />
      <div class="banner-text-content">
        <h1 class="banner-title">视觉模型检测对象行为异常</h1>
        <div class="banner-desc">视听双鉴辨异常，考场秩序有保障</div>
        <div class="banner-btn" @click="handleTry">试一试</div>
      </div>
    </div>
    <CmpBreadcrumb :items="breadcrumbItems" separatorIcon="ArrowRight" theme="light" />
    <div class="main-page-content">
      <div class="text-container">
        <h1>产品概述</h1>
        <div class="text">
          视觉模型检测对象行为异常系统依托 OpenCV 计算机视觉技术与 YOLOv8、MMPose
          等先进深度学习模型，融合视频与音频流的多模态分析能力，通过实时智能分析，能快速识别危险或违规行为，可有效解决传统人工监考效率低、易疏漏、追溯困难等问题。
        </div>
        <img :src="visualModel_text_1" alt="" style="margin-top: 40px; max-width: 100%" />
      </div>
    </div>
    <div class="text-container" style="background: #f3f6fa">
      <h1>核心功能</h1>
      <div class="main-page-content">
        <div style="display: flex; gap: 20px; width: 100%">
          <div class="a">
            <img :src="visualModel_card_caiji" alt="" />
            <h1>多模态数据自动采集</h1>
            <div class="desc">
              以非接触、自动化方式同步采集摄像头视频流与麦克风音频流，构建多维度行为分析基础。
            </div>
          </div>
          <div class="a">
            <img :src="visualModel_card_ai" alt="" />
            <h1>视觉特征智能提取</h1>
            <div class="desc">
              基于 YOLOv8 目标检测模型，结合 MMPose
              人体姿态估计算法，精准捕捉头部角度、肢体动作等微表情特征。
            </div>
          </div>
          <div class="a">
            <img :src="visualModel_card_yujing" alt="" />
            <h1>实时监测预警</h1>
            <div class="desc">
              基于多维度特征融合分析实现毫秒级异常行为识别，依据风险等级自动触发弹窗、语音预警并记录完整干预链路。
            </div>
          </div>
          <div class="a">
            <img :src="visualModel_card_goujian" alt="" />
            <h1>异常行为模型构建</h1>
            <div class="desc">
              通过深度学习训练，构建「玩手机、偷窥、睡觉、打架」等异常行为特征库，支持自定义行为类别扩展。
            </div>
          </div>
        </div>
      </div>
    </div>
    <CmpContactInfo />
    <CmpCopyright />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { HomeFilled, Document, Setting } from '@element-plus/icons-vue'
import CmpHeader from '@/views/gateway-page/modules/CmpHeader.vue'
import visualModelBanner from '@/assets/gatewayPage/visualModel_banner.png'
import visualModel_text_1 from '@/assets/gatewayPage/visualModel_text_1.png'
import visualModel_card_goujian from '@/assets/gatewayPage/visualModel_card_goujian.png'
import visualModel_card_ai from '@/assets/gatewayPage/visualModel_card_ai.png'
import visualModel_card_caiji from '@/assets/gatewayPage/visualModel_card_caiji.png'
import visualModel_card_yujing from '@/assets/gatewayPage/visualModel_card_yujing.png'
import { useRouter } from 'vue-router'
import CmpContactInfo from '../../modules/CmpContactInfo.vue'
import CmpCopyright from '../../modules/CmpCopyright.vue'
import CmpBreadcrumb from '../../modules/CmpBreadcrumb.vue'
const router = useRouter()
const breadcrumbItems = ref([
  { title: '首页', path: '/gateway-page' },
  { title: '应用场景', path: '/gateway-application-overview' },
  { title: '视觉模型检测对象行为异常', path: '' }
])
const handleTry = () => {
  router.push('/gateway-application-scenarios')
}
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
  .text-container {
    display: flex;
    flex-direction: column;
    gap: 40px;
    padding: 70px 0;
    h1 {
      color: #000;
      font-size: 28px;
      line-height: 40px;
      letter-spacing: 0;
      text-align: center;
      font-weight: 500;
    }
    .text {
      color: #000;
      font-size: 16px;
      line-height: 28px;
      text-align: left;
    }
  }
  .a {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 20px 30px;
    border-radius: 5px;
    background: linear-gradient(180deg, #f8f8f8, #fff);
    border: 2px solid #fff;
    box-shadow: 0 10px 24px 0 rgba(232, 236, 245, 0.6);
    h1 {
      color: #000;
      font-size: 18px;
      line-height: normal;
      text-align: left;
      margin-top: 14px;
      margin-bottom: 8px;
    }
    img {
      width: 24px;
      height: 24px;
    }
    .desc {
      width: 100%;
      color: #595959;
      font-size: 14px;
      line-height: 24px;
      text-align: left;
      font-weight: 400;
    }
  }
}
</style>
