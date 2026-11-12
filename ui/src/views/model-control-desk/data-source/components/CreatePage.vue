<template>
  <div class="source-container">
    <div class="page-title">创建数据源</div>
    <div class="addBox-container">
      <div
        v-for="(card, index) in sourceCards"
        :key="index"
        class="btn-card"
        :class="{ 'disabled-card': card.disabled }"
        @mouseover="hoverIndex = card.disabled ? -1 : index"
        @mouseleave="hoverIndex = -1"
        @click="!card.disabled && handleAddSourceDialog(card.type)"
      >
        <div style="display: flex; align-items: center; justify-content: center">
          <div class="icon-container">
            <svg
              v-if="card.icon === 'file'"
              class="card-icon"
              :class="{ hover: hoverIndex === index }"
              viewBox="0 0 24 24"
            >
              <path
                d="M14,2H6C4.9,2,4,2.9,4,4v16c0,1.1,0.9,2,2,2h12c1.1,0,2-0.9,2-2V8L14,2z M13,9V3.5L18.5,9H13z"
              />
              <path d="M8 13h8v2H8zm0 3h8v2H8z" />
            </svg>

            <svg
              v-else-if="card.icon === 'data'"
              class="card-icon"
              :class="{ hover: hoverIndex === index }"
              viewBox="0 0 24 24"
            >
              <path
                d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"
              />
            </svg>

            <svg
              v-else-if="card.icon === 'knowledge'"
              class="card-icon"
              :class="{ hover: hoverIndex === index }"
              viewBox="0 0 24 24"
            >
              <path
                d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"
              />
            </svg>
          </div>
          <div class="card-title">
            {{ card.title }}
          </div>
        </div>

        <div class="card-description">
          <template v-for="(text, index) in card.description" :key="index">
            {{ text }}<br v-if="index !== card.description.length - 1" />
          </template>
        </div>

        <!-- 禁用状态提示 -->
        <div v-if="card.disabled" class="coming-soon-badge">即将上线</div>
      </div>
    </div>
    <AddSourceDialog :title="sourceTitle" ref="AddSourceDialogRef" @refresh="refresh" />
  </div>
</template>

<script setup lang="ts">
import AddSourceDialog from './AddSourceDialog.vue'
import { ref } from 'vue'
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: true
  }
})
const emit = defineEmits(['update:modelValue', 'refresh'])
const hoverIndex = ref(-1)
// 定义数据源类型接口
interface SourceType {
  type: string
  value: string
  title: string
  pullType?: string
}

interface SourceTypes {
  [key: string]: SourceType
}

// 定义数据源类型常量
const SOURCE_TYPES: SourceTypes = {
  DOC: {
    type: 'doc',
    value: '0',
    title: '创建文件型数据源'
  },
  DATA: {
    type: 'data',
    value: '1',
    pullType: '1',
    title: '创建数据型数据源'
  }
}
const sourceTitle = ref('')
const AddSourceDialogRef = ref()

// 处理添加数据源
function handleAddSourceDialog(type: string) {
  const sourceType = SOURCE_TYPES[type.toUpperCase()]
  if (sourceType) {
    sourceTitle.value = sourceType.title
    AddSourceDialogRef.value?.open({ type: sourceType.value, pullType: sourceType.pullType || '1' })
  }
}

// 定义数据源卡片配置
const sourceCards = [
  {
    type: 'doc',
    title: '文件型数据源',
    icon: 'file',
    description: ['支持PDF、Word、TXT等多种格式文件', '自动提取文本内容用于模型训练'],
    disabled: false
  },
  {
    type: 'data',
    title: '数据型数据源',
    icon: 'data',
    description: ['支持MySQL、MongoDB等主流数据库', '结构化数据快速导入训练集'],
    disabled: false
  },
  {
    type: 'graph',
    title: '知识图谱数据源',
    icon: 'knowledge',
    description: ['支持Neo4j、RDF、OWL等知识图谱格式', '构建领域知识关系网络'],
    disabled: true
  }
]
// 关闭创建页面
function closeCreatePage() {
  emit('update:modelValue', false)
}

function refresh() {
  console.log('刷新数据源列表')
    // 通知父组件刷新数据
    emit('refresh')
  // 关闭创建页面
  closeCreatePage()
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

  .addBox-container {
    max-width: 100%;
    display: flex;
    gap: 30px;

    .btn-card {
      width: 320px;
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
      position: relative;
      overflow: hidden;

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

      // 禁用卡片样式
      &.disabled-card {
        opacity: 0.7;
        filter: grayscale(100%);
        cursor: not-allowed;

        &:hover {
          transform: none;
          box-shadow:
            0 0 0 1px #f1f5f9,
            0 4px 8px rgba(0, 0, 0, 0.05),
            0 16px 32px rgba(0, 0, 0, 0.1);
          background-color: hsla(0, 0%, 100%, 0.85);
        }

        .card-icon {
          fill: #94a3b8;

          &.hover {
            fill: #94a3b8;
            transform: none;
          }
        }

        .card-title {
          color: #94a3b8;
        }

        .card-description {
          color: #cbd5e1;
        }

        &:hover .card-title {
          color: #94a3b8;
        }

        &:hover .card-description {
          color: #cbd5e1;
        }
      }
    }

    .coming-soon-badge {
      position: absolute;
      top: 15px;
      right: -35px;
      background-color: #64748b;
      color: white;
      padding: 4px 40px;
      transform: rotate(45deg);
      font-size: 12px;
      font-weight: 500;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
  }
}
</style>
