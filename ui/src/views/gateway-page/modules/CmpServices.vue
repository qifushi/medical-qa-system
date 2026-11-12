<template>
  <div class="cmp-services">
    <div class="module-title">打造丰富的场景应用智能体，实现多元高效的智能服务</div>
    <div class="service-card">
      <div class="card-left">
        <div class="card-item" @click="goApplication('industryTalk')">
          <div class="card-img">
            <img src="~@/assets/gatewayPage/roll3.png" alt="" />
          </div>
          <div class="card-title">行业知识对话</div>
          <div class="card-des">增进对该行业的理解和认识</div>
        </div>
      </div>
      <div class="card-right">
        <div
          class="card-item"
          v-for="(item, index) in serviceList"
          :key="index"
          @click="goApplication(item.routerName, item.title)"
          :class="item.isGrayColor ? 'imgGray' : ''"
        >
          <div class="card-img">
            <img :class="item.isGrayColor ? 'imgGray' : ''" :src="item.icon" alt="" />
          </div>
          <div class="card-title">{{ item.title }}</div>
          <div class="card-des">{{ item.desc }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import icon4 from '@/assets/gatewayPage/roll4.png'
import icon5 from '@/assets/gatewayPage/roll5.png'
import icon6 from '@/assets/gatewayPage/roll6.png'
import icon7 from '@/assets/gatewayPage/roll7.png'
import icon8 from '@/assets/gatewayPage/roll8.png'
import icon9 from '@/assets/gatewayPage/roll9.png'
import icon13 from '@/assets/gatewayPage/roll13.png'
import useStore from '@/stores'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

const { application } = useStore()

const serviceList = [
  {
    title: '长文本生成',
    desc: '长文本生成即AI创作长篇内容',
    icon: icon4,
    routerName: 'textGeneration'
  },
  {
    title: '智能查询分析',
    desc: '用AI技术对数据进行自动检索和深入分析',
    icon: icon5,
    routerName: 'smartQuery'
  },
  {
    title: '智能PPT助手',
    desc: '自动生成PPT内容、支持在线编辑PPT的工具',
    icon: icon13,
    routerName: 'createAippt'
  },
  {
    title: '文档阅读助手',
    desc: '用人工智能技术帮助用户快速理解和处理文档内容的工具',
    icon: icon7,
    routerName: 'documentRead'
  },
  {
    title: '知贝',
    desc: '医疗助手模块',
    icon: icon6,
    routerName: 'graphAssistant',
    isGrayColor: false
  },
  {
    title: '(多模态)合规审查助手',
    desc: '用AI技术对音频、视频、图片、文档等不同模态的内容进行检查...',
    icon: icon9,
    routerName: ''
  },
  // {
  //   title: '多语言助手',
  //   desc: '旨在跨越语言障碍，提供全球化的服务和支持',
  //   icon: icon8,
  //   routerName: ''
  // }
]
const { user } = useStore()
const router = useRouter()

const token = user.getToken()

const goApplication = (routerName: string, title?: string) => {
  if (!token) {
    ElMessage.error('还没登录，请先登陆')
    // 将路由路径作为参数传递给登录页面（登陆页面redirect参数）
    router.push(`/login?redirect=${routerName}`)
  } else {
    if (routerName === 'textGeneration') {
      // 暂定跳转到大纲应用中
      router.push({
        name: 'textGeneration',
        params: { id: 'c24a374e-329f-11ef-8f88-0242ac110005' }
      })
    } else if (routerName === 'graphAssistant') {
      // 知贝医疗助手
      router.push({ name: routerName })
    } else {
      router.push({ name: routerName })
    }
  }
  // window.open(`${application.location}${open_id}`)
}
</script>

<style lang="scss" scoped>
.imgGray {
  filter: grayscale(100%); /* 将图片转换为灰度 */
}
.module-title {
  font-weight: bold;
  font-size: 28px;
  text-align: center;
  margin-bottom: 65px;
  user-select: none;
}
.service-card {
  display: flex;
  gap: 12px;
  padding-bottom: 126px;
  .card-item {
    box-sizing: border-box;
    padding: 24px;
    border-radius: 3px;
    background-size: 100% 100%;
    color: #333;
    user-select: none;
    transition: all 0.3s;
    &:hover {
      transform: translateY(-6px);
      cursor: pointer;
    }
    .card-img {
      width: 32px;
      margin-bottom: 2px;
      img {
        width: 100%;
      }
    }
    .card-title {
      font-size: 18px;
      font-weight: bold;
      margin-bottom: 10px;
    }
    .card-des {
      font-size: 15px;
      line-height: 20px;
      color: #999;
    }
  }
  .card-left {
    width: 25%;
    box-sizing: border-box;
    .card-item {
      background-image: url('@/assets/gatewayPage/block1.png');
      height: 100%;
      padding: 24px;
      padding-left: 48px;
      padding-top: 48px;
    }
  }
  .card-right {
    width: 75%;
    display: flex;
    flex-wrap: wrap;
    gap: 12px;

    .card-item {
      width: calc(33% - 6px);
      padding: 24px;

      min-width: 200px;
      // background-image: url('@/assets/gatewayPage/block5.png');

      &:nth-child(1) {
        background-image: url('@/assets/gatewayPage/block2.png');
      }
      &:nth-child(2) {
        background-image: url('@/assets/gatewayPage/block3.png');
      }
      &:nth-child(3) {
        background-image: url('@/assets/gatewayPage/block4.png');
      }
      &:nth-child(4) {
        background-image: url('@/assets/gatewayPage/block5.png');
      }
      &:nth-child(5) {
        background-image: url('@/assets/gatewayPage/block6.png');
      }
      &:nth-child(6) {
        background-image: url('@/assets/gatewayPage/block7.png');
      }
    }
  }
}
@media (max-width: 560px) {
  .module-title {
    margin-bottom: 24px;
    font-size: 18px;
  }
  .service-card {
    padding-bottom: 24px;
    flex-direction: column;
    .card-left {
      width: 100%;
      // display: none;
    }
    .card-right {
      width: 100%;
      justify-content: space-between;
      .card-item {
        width: calc(50% - 6px);
        min-width: 0;
      }
    }
  }
}
@media (max-width: 870px) {
  .service-card {
    .card-right {
      .card-item {
        width: calc(50% - 6px);
        min-width: 0;
      }
    }
  }
}
</style>
