<template>
  <div class="chat-content" v-loading="loading">
    <!-- 左侧知识库 -->
    <div class="leftBox" :style="{ width: isCollapsed ? '0' : box1Width }">
      <transition name="fade">
        <LeftKnowledge
          v-show="!isCollapsed"
          ref="leftKnowledgeRef"
          @selectKnowledgeAppId="selectKnowledgeAppId"
          @setScrollBottom="setScrollBottom"
          :applicationForm="applicationForm"
          @update:currentChatId="(val) => (currentChatId = val)"
          @update:currentRecordList="(val) => (currentRecordList = val)"
        >
        </LeftKnowledge>
      </transition>
    </div>
    <!-- 展开/收起按钮 -->
    <el-tooltip
      effect="dark"
      placement="right"
      :content="isCollapsed ? '展开对话记录' : '收起对话记录'"
    >
      <div class="expandBtn" @click="toggleLeft" :style="{ left: isCollapsed ? '4px' : box1Width }">
        <!-- {{ isCollapsed ? '展开' : '收起' }} -->
        <el-icon size="25" color="#c3c5cd" v-if="!isCollapsed"><ArrowLeftBold /></el-icon>
        <el-icon size="25" color="#c3c5cd" v-if="isCollapsed"><ArrowRightBold /></el-icon>
      </div>
    </el-tooltip>
    <!-- 对话 -->
    <div class="chatAi-content">
      <ChatApp
        ref="AiChatRef"
        v-model:data="applicationForm"
        :appId="applicationForm?.id"
        :record="currentRecordList"
        :chatId="currentChatId"
        @refresh="refresh"
        @scroll="handleScroll"
        @webSearchList="handleWebSearchList"
      >
      </ChatApp>
    </div>

    <!-- 右侧指令区域 -->
    <RightOrder v-if="showOrder" @clickOrder="clickOrder" />
    <div
      class="rightNetwork-transform"
      :style="{ width: showRightInternetSerchDetail ? '400px' : '0' }"
    >
      <RightInternetSerchDetail
        v-show="showRightInternetSerchDetail"
        :webSearchList="webSearchList"
        @close="
          () => {
            webSearchList = []
          }
        "
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import ChatApp from '@/components/chat-app/index.vue'
import LeftKnowledge from './components/LeftKnowledge.vue'
import RightInternetSerchDetail from './components/RightInternetSerchDetail.vue'
import RightOrder from './components/RightOrder.vue'
// 组件逻辑
import type { ApplicationFormType } from '@/api/type/application'
import { t } from '@/locales'
import useStore from '@/stores'
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
const route = useRoute()

const { application, user, log, common } = useStore()

const defaultPrompt = t('views.application.prompt.defaultPrompt', {
  data: '{data}',
  question: '{question}'
})
const applicationForm = ref<ApplicationFormType & { id: string }>({
  id: '',
  name: '',
  desc: '',
  model_id: '',
  multiple_rounds_dialogue: false,
  prologue: t('views.application.prompt.defaultPrologue'),
  dataset_id_list: [],
  dataset_setting: {
    top_n: 3,
    similarity: 0.6,
    max_paragraph_char_number: 5000,
    search_mode: 'embedding',
    no_references_setting: {
      status: 'ai_questioning',
      value: '{question}'
    }
  },
  model_setting: {
    prompt: defaultPrompt
  },
  problem_optimization: false,
  type: 'SIMPLE',
  show_source: false
})

function getDetail(application_id: string) {
  application.asyncGetApplicationDetail(application_id, loading).then((res: any) => {
    applicationForm.value = res.data
    applicationForm.value.model_id = res.data.model
    leftKnowledgeRef.value.getChatLog(applicationForm.value.id) // 新建对话
  })
}

const loading = ref(false)
const selectKnowledgeAppId = async (application_id: string) => {
  getDetail(application_id)
}

const AiChatRef = ref()
// -- 新建对话 + 历史对话记录 --
const currentChatId = ref('new')
const currentRecordList = ref<any>([])

const leftKnowledgeRef = ref()
function refresh(id: string) {
  leftKnowledgeRef.value.getChatLog(applicationForm.value.id, true)

  leftKnowledgeRef.value.currentChatId = id
}
function setScrollBottom() {
  AiChatRef.value.setScrollBottom()
}
function handleScroll(event: any) {
  leftKnowledgeRef.value.handleScroll(event)
}
const showOrder = computed(() => {
  const { name } = route
  if (name === 'industryTalk' || name === 'documentRead') return false
  return true
})
// --新建对话 end --
// 添加控制变量,智能查询默认展开
const isCollapsed = ref<boolean>(route.name !== 'smartQuery')
const box1Width = computed(() => {
  return isCollapsed.value ? '0' : '300px'
})

// 添加切换方法
const toggleLeft = () => {
  isCollapsed.value = !isCollapsed.value
}
function clickOrder(item: any) {
  AiChatRef.value.inputValue = item.content
}
const webSearchList = ref([])
const isNetwork = ref(false)
const handleWebSearchList = (websearch_list: any, networkStatus: boolean) => {
  webSearchList.value = websearch_list
  isNetwork.value = networkStatus
}
const showRightInternetSerchDetail = computed(() => {
  return webSearchList.value.length > 0 && isNetwork.value
})
onMounted(() => {
  // 根据路由设置默认模型
  if (route.name === 'graphAssistant') {
    // 设置为知贝医疗助手的默认模型
    applicationForm.value.model_id = 'qwen3.5-35b-a3b'
  }
  // user.changeUserType(2) // 设置用户类型为2(用户),历史记录查看、客户端删除权限
})
</script>

<style scoped lang="scss">
.chat-content {
  width: 100%;
  height: 100%;
  display: flex;
  flex: 1 1 0;
  position: relative;
  // height: calc(100% - 20px); // 减去父元素底部padding
  :deep(.el-loading-mask) {
    border-radius: 18px;
  }
  .chatAi-content {
    flex: 1 1 0;
  }
  .expandBtn {
    position: absolute;
    top: 50%; /* 垂直居中 */
    transform: translateY(-50%); /* 确保垂直居中效果 */
    z-index: 10; /* 确保按钮在最上层 */
    transition: left 0.4s ease; /* 跟随 LeftKnowledge 宽度过渡 */
    cursor: pointer;
  }
  .leftBox {
    transition: width 0.4s ease 0s;
    overflow: hidden; // 防止内容溢出
    white-space: nowrap; // 防止内容换行
    flex-shrink: 0; // 防止flex布局下被压缩
    // position: relative; // 建立定位上下文
  }
  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.4s ease; /* 渐变动画 */
  }
  .fade-enter-from,
  .fade-leave-to {
    opacity: 0; /* 隐藏时的透明度 */
  }
}

.rightNetwork-transform {
  transition: width 0.4s ease 0s;
}
</style>
