<template>
  <div class="chat-content" v-loading="loading">
    <!-- 左侧知识库 -->
    <LeftKnowledge
      @selectKnowledgeAppId="selectKnowledgeAppId"
      @setScrollBottom="setScrollBottom"
    />
    <!-- 对话 -->
    <div class="chatAi-content">
      <ChatApp ref="AiChatRef" v-model:data="applicationForm" :appId="applicationForm?.id">
      </ChatApp>
    </div>
    <!-- 右侧指令区域 -->
    <RightOrder />
  </div>
</template>

<script setup lang="ts">
import ChatApp from '@/components/chat-app/index.vue'
import LeftKnowledge from './LeftKnowledge.vue'
import RightOrder from './RightOrder.vue'
// 组件逻辑
import type { ApplicationFormType } from '@/api/type/application'
import { t } from '@/locales'
import useStore from '@/stores'
import { onMounted, ref } from 'vue'

const { application } = useStore()

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
  type: 'SIMPLE'
})
const applicationId = ref('')

function getDetail(application_id: string) {
  application.asyncGetApplicationDetail(application_id, loading).then((res: any) => {
    console.log(res, 'red')
    applicationForm.value = res.data
    applicationForm.value.model_id = res.data.model
  })
}
const loading = ref(false)
const selectKnowledgeAppId = (application_id: string) => {
  getDetail(application_id)
  console.log(application_id, 'application_id1111', applicationId.value)
}
const AiChatRef = ref()
const setScrollBottom = () => {
  // 将滚动条滚动到最下面
  AiChatRef.value.setScrollBottom()
}

onMounted(() => {
  // getDetail()
})
</script>

<style scoped lang="scss">
.chat-content {
  width: 100%;
  height: 100%;
  display: flex;
  flex: 1 1 0;

  // height: calc(100% - 20px); // 减去父元素底部padding
  :deep(.el-loading-mask) {
    border-radius: 18px;
  }
  .chatAi-content {
    flex: 1 1 0;
  }
}
</style>
