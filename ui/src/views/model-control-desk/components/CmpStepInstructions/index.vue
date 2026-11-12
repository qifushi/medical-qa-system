<template>
  <el-dialog v-model="dialogVisible" width="800" :before-close="handleClose">
    <template #header>
      <div style="font-size: 18px">
        {{ title }}
      </div>
    </template>
    <div class="step-container">
      <!-- 进度指示 -->
      <div class="progress-bar">
        <div
          class="progress-item"
          :class="['progress-item', { active: step.id <= activeStep }]"
          v-for="step in stepList"
          :key="step.id"
        >
          <div class="step-dot"></div>
          <div>{{ step.title }}</div>
        </div>
      </div>
      <div style="overflow: hidden">
        <!-- 步骤内容过渡 -->
        <transition :name="transitionName" mode="out-in">
          <div class="step-content" :key="activeStep">
            <div class="content-left">
              <img :src="currentStep.imgUrl" alt="步骤示意图" />
            </div>
            <div class="content-right">
              <div class="step-top">
                <span class="step-index">{{ currentStep.id }}</span>
                <div class="step-title">
                  {{ currentStep.title }}
                </div>
              </div>
              <p class="step-description">{{ currentStep.des }}</p>
            </div>
          </div>
        </transition>
      </div>

      <!-- 操作区域 -->
      <div class="action-area">
        <el-checkbox v-model="dontShowAgain">不再显示</el-checkbox>
        <div class="action-buttons">
          <el-button @click="handleClose">跳过</el-button>
          <el-button :disabled="isFirstStep" @click="handlePrev">上一步</el-button>
          <el-button type="primary" @click="handleNext">{{
            isLastStep ? '完成' : '下一步'
          }}</el-button>
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import img1 from '@/assets/model-control-desk/step1.png'
import img2 from '@/assets/model-control-desk/step2.png'
import img3 from '@/assets/model-control-desk/step3.png'
import img4 from '@/assets/model-control-desk/step4.png'
import img5 from '@/assets/model-control-desk/step5.png'
import useStore from '@/stores'

interface StepItem {
  id: number
  title: string
  des: string
  imgUrl: string
}
const route = useRoute()
const { modelControlDesk } = useStore()
const dialogVisible = ref<boolean>(false)
const dontShowAgain = ref<boolean>(false)
const transitionName = ref<string>('slide-next')
const activeStep = ref<number>(1)

const stepList = ref<StepItem[]>([
  {
    id: 1,
    title: '创建数据源',
    des: '准备好对应的数据库数据或者本地文件数据，通过新建数据源选择目标数据库或者文件格式进行配置。',
    imgUrl: img1
  },
  {
    id: 2,
    title: '数据准备',
    des: '批量构建数据集，并生成COT。通过可视化界面，可便捷管理数据集的版本、标注状态。',
    imgUrl: img2
  },
  {
    id: 3,
    title: '模型训练',
    des: '适配 deepseek-r1、LLaMA、Qwen、MiniCPM、ChatGLM 等主流架构，全参数微调、LoRA冻结微调、QLoRA量化微调，支持奖励模型训练、PPO 训练、DPO 训练、KTO 训练、ORPO 训练等训练方法。',
    imgUrl: img3
  },
  {
    id: 4,
    title: '模型评测',
    des: '加载微调模型功能，界面支持一键启动评测任务，支持BLEU-4、rouge-1，rouge-2等评测指标。',
    imgUrl: img4
  },
  {
    id: 5,
    title: '模型发布',
    des: '一键导出并发布模型至Smart Brain应用控制台，实时监控模型状态。',
    imgUrl: img5
  }
])

// 计算属性（带类型）
const title = computed<string>(() => {
  let targetStep = stepList.value.find((item) => item.id === activeStep.value)
  return `操作指引(${targetStep?.title})`
})
const currentStep = computed<any>(() => {
  let target = stepList.value.find((item) => item.id === activeStep.value)
  return target
})
const isFirstStep = computed<boolean>(() => activeStep.value === stepList.value[0].id)
const isLastStep = computed<boolean>(
  () => activeStep.value === stepList.value[stepList.value.length - 1].id
)

// 函数（带返回类型）
const handleOpen = (): void => {
  let noMorePrompts = localStorage.getItem('noMorePrompts')
  dontShowAgain.value = noMorePrompts == 'true'
  dialogVisible.value = true
  modelControlDesk.toggleModalVisible(true)
}
const init = (): void => {
  let noMorePrompts = localStorage.getItem('noMorePrompts')
  if (noMorePrompts != 'true' && route.name === 'ModelControlIndex') {
    handleOpen()
  }
}
const handleClose = (): void => {
  dialogVisible.value = false
  modelControlDesk.toggleModalVisible(false)
  localStorage.setItem('noMorePrompts', JSON.stringify(dontShowAgain.value))
  activeStep.value = 1
  dontShowAgain.value = false
}
const handleNext = (): void => {
  transitionName.value = 'slide-next'
  const currentIndex = stepList.value.findIndex((item) => item.id === activeStep.value)
  if (currentIndex >= 0 && currentIndex < stepList.value.length - 1) {
    activeStep.value = stepList.value[currentIndex + 1].id
  } else {
    handleClose()
  }
}
const handlePrev = (): void => {
  transitionName.value = 'slide-prev'
  const currentIndex = stepList.value.findIndex((item) => item.id === activeStep.value)
  if (currentIndex > 0) {
    activeStep.value = stepList.value[currentIndex - 1].id
  }
}

// 初始化调用
init()
watch(
  () => modelControlDesk.tepInstructionsModalVisible,
  (value) => {
    if (value) {
      handleOpen()
    }
  }
) // 监听逻辑保持不变
watch(
  () => route.fullPath,
  () => {
    if (dialogVisible.value) {
      handleClose()
    }
  }
)
</script>

<style lang="scss" scoped>
.step-container {
  position: relative;

  .progress-bar {
    display: flex;
    justify-content: center;
    gap: 16px;
    margin-bottom: 24px;
    font-size: 16px;
    .progress-item {
      display: flex;
      align-items: center;
      margin-right: 46px;
      position: relative;
      transition: color 0.3s;
      color: #333;
      &::after {
        content: '...........';
        position: absolute;
        height: 20px;
        line-height: 20px;
        right: -55px;
        margin-top: -8px;
      }
      &:last-child {
        margin-right: 0;
        &::after {
          content: '';
        }
      }
      &.active {
        color: #409eff;
        .step-dot {
          background: #409eff;
        }
      }
    }
    .step-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #ddd;
      transition: background 0.3s;
      margin-right: 6px;
    }
  }

  .step-content {
    display: flex;
    gap: 24px;
    height: 300px;

    .content-left {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 280px;
      margin-right: 24px;
      img {
        width: 100%;
        object-fit: contain;
        border-radius: 4px;
      }
    }

    .content-right {
      flex: 1;
      display: flex;
      flex-direction: column;
      padding-top: 88px;
      // justify-content: center;
      .step-top {
        display: flex;
        align-items: flex-end;
        margin-bottom: 8px;
        line-height: 48px;
        .step-index {
          position: relative;
          display: inline-block;
          font-weight: bold;
          z-index: 100;
          margin-right: 12px;
          font-size: 48px;
          color: rgb(150, 84, 251);
          font-style: italic; /* 新增倾斜效果 */
          &::after {
            z-index: -1;
            content: '';
            position: absolute;
            left: 4px;
            border-radius: 50%;
            top: 60%;
            margin-top: -12px;
            width: 24px;
            height: 24px;
            background-color: rgb(234, 226, 247);
          }
        }
        .step-title {
          font-size: 26px;
          font-weight: bold;
          color: rgb(5, 24, 83);
          margin-bottom: -6px;
        }
      }

      .step-description {
        line-height: 1.6;
        color: rgb(48, 48, 48);
        font-size: 16px;
        padding-left: 40px;

      }
    }
  }

  .action-area {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24px 24px 0;
    position: relative;
    &::after {
      content: '';
      height: 1px;
      background-color: #ddd;
      width: calc(100% + 48px);
      left: 0;
      margin-left: -24px;
      top: 0;
      position: absolute;
    }
  }
}

// 过渡动画
.slide-next-enter-active,
.slide-next-leave-active,
.slide-prev-enter-active,
.slide-prev-leave-active {
  transition: all 0.5s ease;
}

.slide-next-enter-from {
  transform: translateX(100%);
  opacity: 0;
}
.slide-next-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}

.slide-prev-enter-from {
  transform: translateX(-100%);
  opacity: 0;
}
.slide-prev-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style>
