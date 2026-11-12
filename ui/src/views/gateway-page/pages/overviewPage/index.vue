<template>
  <div class="applicationScenarios">
    <CmpHeader />
    <div class="banner-container">
      <img class="banner-img" :src="banner" alt="" />
      <!-- <div class="banner-text-content">
        <h1 class="banner-title">引用场景</h1>
        <div class="banner-desc">视听双鉴辨异常，考场秩序有保障</div>
        <div class="banner-btn" @click="handleTry">试一试</div>
      </div> -->
    </div>
    <div class="main-page-content">
      <div class="page-title">应用场景</div>
      <div class="card-list">
        <div
          class="card-item"
          v-for="item in cardData"
          :key="item.id"
          :data-id="item.id"
          @mouseover="hoverItem(item.id)"
          @mouseout="leaveItem(item.id)"
          @click="handleClick(item)"
        >
          <img class="card-img" :src="item.imgSrc" alt="" />
          <div class="card-info">
            <h2 class="card-title">{{ item.title }}</h2>
            <p class="card-desc">{{ item.description }}</p>
          </div>
        </div>
      </div>
    </div>
    <CmpContactInfo />
    <CmpCopyright />
  </div>
</template>

<script setup lang="ts">
import CmpHeader from '@/views/gateway-page/modules/CmpHeader.vue'
import banner from '@/assets/gatewayPage/banner-overview.jpg'
import img4 from '@/assets/gatewayPage/overview-img4.jpg'
import img3 from '@/assets/gatewayPage/overview-img3.jpg'
import img2 from '@/assets/gatewayPage/overview-img2.jpeg'
import img1 from '@/assets/gatewayPage/overview-img1.jpeg'

import { useRouter } from 'vue-router'
import CmpContactInfo from '../../modules/CmpContactInfo.vue'
import CmpCopyright from '../../modules/CmpCopyright.vue'
const router = useRouter()
// 模拟数据
const cardData = [
  {
    id: 1,
    imgSrc: img1,
    title: '视觉模型检测对象行为异常',
    url: '/gateway-application-scenarios-visualModel',
    description:
      '基于OpenCV与深度学习架构的智能行为异常检测系统，通过融合YOLOv8目标检测与MMPose姿态估计技术，构建了覆盖考场作弊识别、公共安全预警的多场景解决方案。系统核心采用视频流实时分析框架，可精准识别考生异常动作（如偷看手机、传递物品）、异常姿态（长时间低头/侧身）等作弊特征，同步集成音频分析模块捕捉电子设备通讯声。在扩展应用层面，系统通过动态骨架追踪技术实现打架斗殴、人员摔倒等突发事件的毫秒级响应。相比传统人工监控，本方案具备多路视频并行处理能力，单服务器可支持20路1080P视频流的实时分析，作弊行为识别准确率达92.7%，违规事件追溯效率提升8倍，可应用于标准化考场及智慧园区建设。'
  },
  {
    id: 2,
    imgSrc: img2,
    title: '基于多模态大模型的缺陷检测系统',
    url: '',
    description:
      '融合视觉Transformer与图神经网络的多模态质检方案，通过高分辨率图像分割技术实现微米级缺陷识别。系统支持动态学习产线新增缺陷类型，平均检测精度达99.2%，误检率低于0.5%。已在3C电子制造产线部署，替代传统AOI设备，单线年节省质检成本120万元。'
  },
  {
    id: 3,
    imgSrc: img3,
    title: '大模型驱动的实时反欺诈引擎',
    url: '',
    description:
      '采用时序图神经网络架构的金融风控系统，通过分析10+维度的用户行为特征构建动态风险画像。支持毫秒级欺诈交易拦截，模型召回率提升至98.7%，日均阻止欺诈损失超200万元。集成联邦学习模块确保客户隐私数据不出域，符合金融监管要求。'
  },
  {
    id: 4,
    imgSrc: img4,
    title: '多模态医学影像分析平台',
    url: '',
    description:
      '基于3D卷积神经网络与Transformer的跨模态分析系统，支持CT/MRI/X光影像的病灶自动定位与量化分析。在肺结节检测任务中达到96.5%的敏感度，假阳性率降低至0.8片/例。通过知识蒸馏技术将模型压缩至原体积1/5，满足边缘设备部署需求。'
  }
]
const hoverItem = (id: number) => {
  const item = document.querySelector(`.card-item[data-id="${id}"]`) as HTMLElement
  item.style.backgroundColor = '#f0f0f0'
}

const leaveItem = (id: number) => {
  const item = document.querySelector(`.card-item[data-id="${id}"]`) as HTMLElement
  item.style.backgroundColor = 'transparent'
}
const handleClick = (record: any) => {
  if (record.url) router.push(record.url)
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
  }

  .main-page-content {
    max-width: 1200px;
    box-sizing: border-box;
    margin: 0 auto;
    padding: 0 24px 24px;
    .page-title {
      font-size: 30px;
      margin: 20px 0;
    }
    .card-list {
      display: flex;
      flex-direction: column;
      gap: 20px;

      .card-item {
        display: flex;
        gap: 20px;
        padding: 40px 20px;
        border-radius: 5px;
        background: #fff;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        cursor: pointer;

        .card-img {
          width: 200px;
          height: 150px;
          object-fit: cover;
        }

        .card-info {
          flex: 1;
          display: flex;
          flex-direction: column;

          .card-title {
            font-size: 18px;
            font-weight: 500;
            margin-bottom: 10px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            width: 300px; // 固定标题宽度
          }

          .card-desc {
            font-size: 14px;
            color: #555;
          }
        }
      }
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
