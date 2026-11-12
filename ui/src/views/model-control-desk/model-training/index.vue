<template>
  <div class="source-container">
    <div v-if="loading" class="fullscreen-loading">
      <div class="loading-content">
        <el-icon class="loading-icon" :size="40">
          <Loading />
        </el-icon>
        <div class="loading-text">{{ loadingText }}</div>
      </div>
    </div>

    <div class="btn-log" @click="handleLogClick">
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M3 4.5C3 3.67157 3.67157 3 4.5 3H19.5C20.3284 3 21 3.67157 21 4.5V19.5C21 20.3284 20.3284 21 19.5 21H4.5C3.67157 21 3 20.3284 3 19.5V4.5Z"
          stroke="#4d6bfe"
          stroke-width="1.5"
        />
        <path d="M3 8H21" stroke="#4d6bfe" stroke-width="1.5" stroke-linecap="round" />
        <path d="M7 12H17" stroke="#4d6bfe" stroke-width="1.5" stroke-linecap="round" />
        <path d="M7 16H14" stroke="#4d6bfe" stroke-width="1.5" stroke-linecap="round" />
      </svg>
    </div>
    <div class="page-title">模型训练</div>
    <div class="addBox-container">
      <div
        v-for="(btn, index) in dataSource"
        :key="index"
        :class="['btn-card', trainAble ? '' : 'disabled']"
        @mouseover="hoverIndex = index"
        @mouseleave="hoverIndex = -1"
        @click="handleCardClick(btn.type)"
      >
        <div style="display: flex; align-items: center; justify-content: center">
          <div class="icon-container">
            <svg
              v-if="btn.icon === 'lightning'"
              class="card-icon"
              :class="{ hover: hoverIndex === index }"
              viewBox="0 0 24 24"
            >
              <path d="M13 1L3 14H12L11 23L21 10H12L13 1Z" />
            </svg>
            <svg
              v-else-if="btn.icon === 'gear'"
              class="card-icon"
              :class="{ hover: hoverIndex === index }"
              viewBox="0 0 24 24"
            >
              <path d="M12 15.5A3.5 3.5 0 1 1 15.5 12 3.5 3.5 0 0 1 12 15.5z" />
              <path
                d="M19.14 12.94c-.04-.3-.06-.61-.06-.94s.02-.64.06-.94l2.03-1.58a.49.49 0 0 0 .12-.61l-1.92-3.32a.488.488 0 0 0-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54a.484.484 0 0 0-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.71 8.87c-.14.23-.08.5.12.61l2.03 1.58c.04.3.06.61.06.94s-.02.64-.06.94l-2.03 1.58a.49.49 0 0 0-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.5-.12-.61l-2.01-1.58z"
              />
            </svg>
          </div>
          <div class="card-title">
            {{ btn.title }}
          </div>
        </div>

        <div class="card-description">
          <template v-for="(text, index) in btn.description" :key="index">
            {{ text }}<br v-if="index !== btn.description.length - 1" />
          </template>
        </div>
      </div>
      <div class="service-tips" v-if="!trainAble">服务器已有进程，请等待进程结束后开启新训练！</div>
    </div>
    <TrainLogModal ref="refTrainLogModal" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import TrainLogModal from './modules/trainLogModal.vue'
import { GetProcesses } from '@/api/train-common'

const trainAble = ref(true)
const refTrainLogModal = ref()
const loading = ref(true)
const loadingText = ref('查询服务器进程使用状态中...请稍后！')

async function fnCheckServiceTrainStatus() {
  try {
    // 显示全屏加载状态
    loading.value = true

    // 调用 GetProcesses 接口查询服务器状态
    const serverStatus = await GetProcesses()
    if (serverStatus.data && serverStatus.data[0] && serverStatus.data[0].length) {
      trainAble.value = false
    } else {
      trainAble.value = true
    }
    loading.value = false
  } catch (error) {
    loadingText.value = '查询服务器状态失败，请重试或联系管理员！'
  }
}
fnCheckServiceTrainStatus()
const handleLogClick = () => {
  refTrainLogModal.value.openDialog()
}
// 定义数据源卡片配置
const dataSource = [
  {
    title: '快速训练',
    type: 'simpleness',
    icon: 'lightning',
    description: [
      '一键开启模型训练，系统将自动配置最优默认参数，仅需设置关键参数即可快速启动。',
      '适合新手用户或追求高效训练或小体量的开发者。',
      '500~10000条左右数据'
    ]
  },
  {
    title: '高级训练',
    type: 'major',
    icon: 'gear',
    description: [
      '进入全参数配置页面，自由调整模型训练的每一项细节参数，满足个性化需求。',
      '适合专业开发者或需要精细化调优或大体量的开发者。',
      '10000条以上数据'
    ]
  }
]

const hoverIndex = ref(-1)
const router = useRouter()

function handleCardClick(type: string) {
  if (type == 'major') {
    router.push('/model-control-desk/model-training/major')
  } else {
    router.push('/model-control-desk/model-training/simpleness')
  }
}
</script>

<style lang="scss" scoped>
.source-container {
  height: calc(100vh - 56px);
  display: flex;
  align-items: center;
  flex-direction: column;
  background: url('@/assets/model-control-desk/banner-background.png') no-repeat;
  background-size: cover;
  box-sizing: border-box;
  padding-top: 10%;

  .page-title {
    margin-bottom: 50px;
    font-weight: 700;
    font-size: 30px;
    color: rgb(71, 85, 105);
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  .btn-log {
    position: absolute;
    right: 44px;
    top: 144px;
    cursor: pointer;
    padding: 8px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
    background: rgba(255, 255, 255, 0.8);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

    &:hover {
      background: white;
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);

      svg path {
        stroke: #2a4df0;
      }
    }

    &:active {
      transform: translateY(0);
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    }
  }
  .addBox-container {
    max-width: 100%;
    display: flex;
    gap: 30px;
    position: relative;
    flex-wrap: wrap;
    justify-content: center;
    .service-tips {
      font-size: 16px;
      text-align: center;
      width: 100%;
    }
    .btn-card {
      width: 450px;
      border-radius: 16px;
      box-shadow:
        0 0 0 1px #f1f5f9,
        0 4px 8px rgba(0, 0, 0, 0.05),
        0 16px 32px rgba(0, 0, 0, 0.1);
      border: 2px solid transparent;
      background-color: hsla(0, 0%, 100%, 0.85);
      padding: 25px;
      cursor: pointer;
      box-sizing: border-box;
      user-select: none;
      transition: all 0.3s ease;
      text-align: center;
      &.disabled {
        filter: saturate(0); // 饱和度降为0
        cursor: not-allowed; // 禁止光标
        pointer-events: none; // 禁用所有鼠标事件
        // 移除所有交互效果
        &:hover,
        &:active {
          transform: none !important;
          box-shadow:
            0 0 0 1px #f1f5f9,
            0 4px 8px rgba(0, 0, 0, 0.05),
            0 16px 32px rgba(0, 0, 0, 0.1) !important;
          background-color: hsla(0, 0%, 100%, 0.85) !important;
          border: 2px solid transparent !important;
        }

        // 禁用状态下的图标和文字样式
        .card-icon {
          fill: #cbd5e1 !important; // 灰色图标
          transform: none !important;
        }

        .card-title {
          color: #94a3b8 !important; // 灰色标题
        }

        .card-description {
          color: #cbd5e1 !important; // 灰色描述
        }
      }
      &:hover {
        transform: translateY(-5px);
        box-shadow:
          0 0 0 2px rgba(77, 107, 254, 0.3),
          0 6px 12px rgba(77, 107, 254, 0.1),
          0 20px 40px rgba(0, 0, 0, 0.15);
        background-color: white;
      }

      &:active {
        transform: translateY(0);
        border: rgba(77, 107, 254, 0.5) 2px solid;
      }

      .icon-container {
        margin-bottom: 20px;
        display: flex;
        justify-content: center;
      }

      .card-icon {
        width: 60px;
        height: 60px;
        fill: #4d6bfe;
        transition: all 0.3s ease;

        &.hover {
          fill: #2a4df0;
          transform: scale(1.1);
        }
      }

      .card-title {
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 15px;
        color: rgb(77 107 254);
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 6px;
        transition: color 0.3s ease;
      }

      .card-description {
        font-size: 15px;
        line-height: 1.6;
        color: rgb(100 116 139);
        transition: color 0.3s ease;
      }

      &:hover .card-title {
        color: #2a4df0;
      }

      &:hover .card-description {
        color: #64748b;
      }
    }
  }
}
.fullscreen-loading {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(5px);

  .loading-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 30px 40px;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 12px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    animation: pulse 1.5s infinite;

    .loading-icon {
      color: #4d6bfe;
      margin-bottom: 20px;
      animation: spin 1.5s linear infinite;
    }

    .loading-text {
      font-size: 18px;
      color: #333;
      font-weight: 500;
      text-align: center;
      max-width: 300px;
    }
  }
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.02);
  }
  100% {
    transform: scale(1);
  }
}
</style>
