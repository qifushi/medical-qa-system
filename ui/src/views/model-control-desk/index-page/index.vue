<template>
  <div>
    <CmpBanner />
    <div class="page-content">
      <div class="cmp-title">模型训练快捷直达</div>
      <div class="step-cards">
        <div
          v-for="(step, index) in stepList"
          :key="index"
          class="step-card"
          ref="cardRefs"
          :style="{ '--delay': index * 0.1 + 's' }"
        >
          <div class="card-image">
            <img :src="step.imgUrl" :alt="step.title" />
          </div>
          <div class="card-content">
            <h3 class="card-title">{{ step.title }}</h3>
            <p class="card-description">{{ step.des }}</p>
          </div>
          <button class="try-button" @click="handlePage(step)">试一试</button>
        </div>
      </div>
      <div class="cmp-title">全流程可视化模型训练框架</div>
      <ModelProcess />
    </div>
    <CmpContactInfo />
    <CmpCopyrightJieruan />
  </div>
</template>

<script setup>
import CmpBanner from './modules/CmpBanner.vue'
import { ref, onMounted, onBeforeUnmount, defineOptions } from 'vue'
import img2 from '@/assets/model-control-desk/step2.png'
import img3 from '@/assets/model-control-desk/step3.png'
import img4 from '@/assets/model-control-desk/step4.png'
import { useRoute, useRouter } from 'vue-router'
import CmpContactInfo from '@/views/gateway-page/modules/CmpContactInfo.vue'
import CmpCopyrightJieruan from '@/views/gateway-page/modules/CmpCopyrightJieruan.vue'
import ModelProcess from './modules/modelProcess/index.vue'
defineOptions({
  name: 'ModelControlIndex'
})
// 步骤数据
const stepList = ref([
  {
    id: 2,
    title: '数据准备',
    des: '批量构建数据集，并生成COT。通过可视化界面，可便捷管理数据集的版本、标注状态。',
    imgUrl: img2,
    url: '/model-control-desk/data-treating'
  },
  {
    id: 3,
    title: '模型训练',
    des: '适配 deepseek-r1、LLaMA、Qwen、等主流架构，全参数微调、LoRA冻结微调、QLoRA量化微调，支持奖励模型训练、PPO 训练、DPO 训练等训练方法。',
    imgUrl: img3,
    url: '/model-control-desk/model-training'
  },
  {
    id: 4,
    title: '模型评测',
    des: '加载微调模型功能，界面支持一键启动评测任务，支持BLEU-4、rouge-1，rouge-2等评测指标。',
    imgUrl: img4,
    url: '/model-control-desk/model-evaluation'
  }
])
const router = useRouter()
const handlePage = (record) => {
  if (record.url) {
    router.push(record.url)
  }
}

// 卡片元素引用
const cardRefs = ref([])
// 记录卡片是否已显示
const shownCards = ref([])

// 检查元素是否在视口中
const isInViewport = (el) => {
  if (!el) return false
  const rect = el.getBoundingClientRect()
  return (
    rect.top <= (window.innerHeight || document.documentElement.clientHeight) * 0.75 &&
    rect.bottom >= 0
  )
}

const handleScroll = () => {
  // 获取所有标题元素
  const titles = document.querySelectorAll('.cmp-title')

  titles.forEach((title) => {
    if (!title.classList.contains('show') && isInViewport(title)) {
      title.classList.add('show')
    }
  })

  cardRefs.value.forEach((card, index) => {
    if (!shownCards.value[index] && isInViewport(card)) {
      card.classList.add('show')
      shownCards.value[index] = true
    }
  })
}
// 节流函数
const throttle = (func, limit) => {
  let lastFunc
  let lastRan
  return function () {
    const context = this
    const args = arguments
    if (!lastRan) {
      func.apply(context, args)
      lastRan = Date.now()
    } else {
      clearTimeout(lastFunc)
      lastFunc = setTimeout(
        function () {
          if (Date.now() - lastRan >= limit) {
            func.apply(context, args)
            lastRan = Date.now()
          }
        },
        limit - (Date.now() - lastRan)
      )
    }
  }
}

// 初始化卡片状态
onMounted(() => {
  shownCards.value = new Array(stepList.value.length).fill(false)

  // 添加滚动监听
  const throttledScroll = throttle(handleScroll, 100)
  window.addEventListener('scroll', throttledScroll)

  // 初始检查一次
  handleScroll()
})

// 清理事件监听
onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style lang="scss" scoped>
.page-content {
  max-width: 1200px;
  margin: 50px auto;
  padding: 0 20px;
}

.step-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr); // 每行三个卡片
  gap: 30px; // 卡片间距
  margin-bottom: 80px;
  @media (max-width: 992px) {
    grid-template-columns: repeat(2, 1fr); // 中等屏幕每行两个
  }

  @media (max-width: 576px) {
    grid-template-columns: 1fr; // 小屏幕每行一个
  }
}
.try-button {
  position: absolute;
  bottom: 15px;
  right: 15px;
  background-color: #1890ff; /* 蓝色背景 */
  color: white;
  border: none;
  border-radius: 4px;
  padding: 6px 12px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;

  /* 鼠标悬停效果 */
  &:hover {
    background-color: #40a9ff; /* 浅蓝色 */
    transform: translateY(-2px);
    box-shadow: 0 2px 8px rgba(24, 144, 255, 0.3);
  }

  /* 点击效果 */
  &:active {
    transform: translateY(0);
    box-shadow: none;
  }
}
.step-card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  transform: translateY(50px);
  opacity: 0;
  position: relative;
  padding-bottom: 30px;
  // 鼠标悬停效果
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);

    .card-image img {
      transform: scale(1.05);
    }
  }

  // 出场动画
  &.show {
    animation: fadeUp 0.6s ease forwards;
    animation-delay: var(--delay); // 使用CSS变量控制延迟
  }
}

.card-image {
  height: 260px;
  overflow: hidden;
  border-bottom: 1px solid #ddd;

  img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    transition: transform 0.5s ease;
  }
}

.card-content {
  padding: 20px;

  .card-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 12px;
    color: #333;
  }

  .card-description {
    font-size: 14px;
    line-height: 1.6;
    color: #666;
  }
}
.cmp-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin: 0 auto 40px; // 居中关键：auto水平外边距
  position: relative;
  padding-bottom: 10px;
  text-align: center; // 文本居中
  display: block; // 确保居中生效
  width: fit-content; // 宽度适应内容
  transition: all 0.3s ease;
  transform: translateY(20px);
  opacity: 0;
  // 居中的渐变下划线
  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%; // 居中关键：从左50%开始
    transform: translateX(-50%); // 居中关键：向左偏移50%
    width: 60%; // 比文本稍短的线条
    height: 3px;
    background: linear-gradient(90deg, #1890ff, #40a9ff);
    border-radius: 2px;
  }

  // 小屏幕适配
  @media (max-width: 992px) {
    font-size: 22px;
    margin-bottom: 25px;

    &::after {
      width: 70%; // 在小屏幕上加宽线条
    }
  }

  @media (max-width: 576px) {
    font-size: 20px;
    margin-bottom: 20px;
    padding-bottom: 8px;

    &::after {
      height: 2px;
      width: 80%; // 在手机上更宽
    }
  }

  &.show {
    animation: titleFadeIn 0.6s ease forwards;
  }

  @keyframes titleFadeIn {
    0% {
      opacity: 0;
      transform: translateY(20px);
    }
    100% {
      opacity: 1;
      transform: translateY(0);
    }
  }
}
// 淡入上浮动画
@keyframes fadeUp {
  0% {
    opacity: 0;
    transform: translateY(50px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
@media (max-width: 576px) {
  .try-button {
    padding: 4px 8px;
    font-size: 12px;
  }
}
</style>
