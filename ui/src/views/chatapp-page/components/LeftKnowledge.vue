<template>
  <div class="knowledge-list">
    <div>
      <div class="p-24 pb-0 mb-16">
        <el-button class="add-button w-full" type="primary" @click="newChat">
          <el-icon style="font-size: 16px">
            <CirclePlus />
          </el-icon>
          <span class="ml-4 add-text">新建对话</span>
        </el-button>
      </div>

      <div v-if="hasKnowledgeBase">
        <div v-for="(item, index) in knowledgeBases" :key="index" class="p-24 pb-0">
          <el-button
            class="add-button w-full"
            :class="{ active: selectedIndex === index }"
            color="#dcedfd"
            @click="selectKnowledgeBase(item.application_id, index)"
          >
            <span class="ml-4 add-text storehouse-color">{{ item.name }}</span>
          </el-button>
        </div>
      </div>
    </div>
    <!-- 历史记录 -->
    <div class="p-16">
      <div class="gradient-divider lighter mt-8">
        <span>历史记录对话</span>
      </div>
      <el-scrollbar>
        <div class="p-8 pt-0">
          <common-list
            :data="chatLogeData.slice(0, 5)"
            class="mt-8"
            v-loading="left_loading"
            :defaultActive="currentChatId"
            @click="clickListHandle"
            @mouseenter="mouseenter"
            @mouseleave="mouseId = ''"
          >
            <template #default="{ row }">
              <div class="flex-between">
                <auto-tooltip :content="row.abstract">
                  {{ row.abstract }}
                </auto-tooltip>
                <div @click.stop v-if="mouseId === row.id">
                  <el-button style="padding: 0" link @click.stop="deleteLog(row)">
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </div>
              </div>
            </template>

            <template #empty>
              <div class="text-center">
                <el-text type="info">暂无历史记录</el-text>
              </div>
            </template>
          </common-list>
        </div>
        <div v-if="chatLogeData.length" class="gradient-divider lighter mt-8">
          <span>仅显示最近 5 条对话</span>
        </div>
      </el-scrollbar>
    </div>
  </div>
</template>
<script setup lang="ts">
import useStore from '@/stores';
import { nextTick, onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute()
const { name } = useRoute()
const emit = defineEmits([
  'selectKnowledgeAppId',
  'setScrollBottom',
  'update:currentChatId',
  'update:currentRecordList'
])
const selectedIndex = ref(-1)
const knowledgeBases = [
  { name: '合同知识库', application_id: 'f80d2778-ac6c-11ef-8794-0242ac110003' },
  { name: '财务知识库', application_id: '3e203d72-ac6d-11ef-9182-0242ac110003' },
  { name: '项目知识库', application_id: '631b7bd2-ac6d-11ef-8108-0242ac110003' }
]

const selectKnowledgeBase = (application_id: string, index: number) => {
  selectedIndex.value = index
  emit('selectKnowledgeAppId', application_id)
}
const hasKnowledgeBase = ref(true)
// 新建对话
const currentChatId = ref('new') // 当前历史记录Id 默认为'new'
const currentRecordList = ref<any>([])

watch(currentChatId, (newVal) => {
  emit('update:currentChatId', newVal)
})
watch(currentRecordList, (newVal) => {
  emit('update:currentRecordList', newVal)
})

const props = defineProps({
  applicationForm: {
    type: Object,
    default: () => {}
  }
})
const paginationConfig = ref({
  current_page: 1,
  page_size: 20,
  total: 0
})
const newObj = {
  id: 'new',
  abstract: '新建对话'
}
const currentChatName = ref('新建对话')
const { application, user, log, common } = useStore()
const isCollapse = ref(false)
const left_loading = ref(false)

function newChat() {
  console.log(chatLogeData.value, 'chatLogeData.value')

  if (!chatLogeData.value.some((v: any) => v.id === 'new')) {
    paginationConfig.value.current_page = 1
    paginationConfig.value.total = 0
    currentRecordList.value = []
    chatLogeData.value.unshift(newObj)
  } else {
    paginationConfig.value.current_page = 1
    paginationConfig.value.total = 0
    currentRecordList.value = []
  }
  currentChatId.value = 'new'
  currentChatName.value = '新建对话'
  if (common.isMobile()) {
    isCollapse.value = false
  }
}
const clickListHandle = (item: any) => {
  if (item.id !== currentChatId.value) {
    paginationConfig.value.current_page = 1
    paginationConfig.value.total = 0
    currentRecordList.value = []
    currentChatId.value = item.id
    currentChatName.value = item.abstract
    if (currentChatId.value !== 'new') {
      getChatRecord()
    }
  }
  if (common.isMobile()) {
    isCollapse.value = false
  }
}
const mouseId = ref('')
function mouseenter(row: any) {
  mouseId.value = row.id
}
function deleteLog(row: any) {
  console.log(props.applicationForm.id, row, 'props.applicationForm.id')
  log.asyncDelChatClientLog(props.applicationForm.id, row.id, left_loading).then(() => {
    if (currentChatId.value === row.id) {
      currentChatId.value = 'new'
      currentChatName.value = '新建对话'
      paginationConfig.value.current_page = 1
      paginationConfig.value.total = 0
      currentRecordList.value = []
    }
    getChatLog(props.applicationForm.id)
  })
}
const chatLogeData = ref<any[]>([])

function getChatLog(id: string, refresh?: boolean) {
  const page = {
    current_page: 1,
    page_size: 20
  }
  log.asyncGetChatLogClient(id, page, left_loading).then((res: any) => {
    chatLogeData.value = res.data.records
    if (refresh) {
      currentChatName.value = chatLogeData.value[0].abstract
    }
  })
}
function getChatRecord() {
  // leftLoading -> loading
  return log
    .asyncChatRecordLog(
      props.applicationForm.id,
      currentChatId.value,
      paginationConfig.value,
      left_loading,
      false
    )
    .then((res: any) => {
      console.log(res,'res');
      
      paginationConfig.value.total = res.data.total
      const list = res.data.records
      list.map((v: any) => {
        v['write_ed'] = true
        v['record_id'] = v.id
      })
      currentRecordList.value = [...list, ...currentRecordList.value].sort((a, b) =>
        a.create_time.localeCompare(b.create_time)
      )
      if (paginationConfig.value.current_page === 1) {
        nextTick(() => {
          // 将滚动条滚动到最下面
          // AiChatRef.value.setScrollBottom()
          emit('setScrollBottom')
        })
      }
    })
}
function handleScroll(event: any) {
  if (
    currentChatId.value !== 'new' &&
    event.scrollTop === 0 &&
    paginationConfig.value.total > currentRecordList.value.length
  ) {
    const history_height = event.dialogScrollbar.offsetHeight
    paginationConfig.value.current_page += 1
    getChatRecord().then(() => {
      event.scrollDiv.setScrollTop(event.dialogScrollbar.offsetHeight - history_height)
    })
  }
}
defineExpose({ getChatLog, handleScroll })

// 新建对话 end

onMounted(() => {
  if (name === 'industryTalk') {
    // 行业对话
    hasKnowledgeBase.value = false
    // 对话应用id,选择要使用的应用
    selectKnowledgeBase('4dad4271-1e32-11ef-8c6e-009337917002', 0)
  } else if (name === 'smartQuery') {
    // 智能查询 默认选中“合同知识库”
    const defaultIndex = 0 // 合同知识库的索引
    const defaultAppId = knowledgeBases[defaultIndex].application_id
    selectKnowledgeBase(defaultAppId, defaultIndex)
  } else if (name === 'documentRead') {
    hasKnowledgeBase.value = false
    selectKnowledgeBase('b873e5bf-c205-11ef-8e84-28565a277758', 0)
  }
})
</script>
<style scoped lang="scss">
.add-button.active,
.add-button:hover {
  background-color: #409eff !important;
}

.add-button.active .add-text,
.add-button:hover .add-text {
  color: #ffffff !important;
}
.knowledge-list {
  width: 300px;
  height: calc(100% - 20px); // 减去父元素底部padding
  background-color: #edf7fd;
  border-radius: 18px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  .add-button {
    // border: 1px solid var(--el-color-primary);
    height: 44px;
    .add-text {
      font-size: 16px;
    }
    .storehouse-color {
      color: #329cff;
    }
  }
  :deep(.el-divider__text) {
    color: #a9a7a7;
    padding: 0px 18px;
    background-color: #edf7fd;
  }
  :deep(.el-divider--horizontal) {
    border-top: 1px #a9a7a7 solid;
  }
  .gradient-divider {
    position: relative;
    text-align: center;
    color: var(--el-color-info);

    ::before {
      content: '';
      width: 17%;
      height: 1px;
      background: linear-gradient(90deg, rgba(222, 224, 227, 0) 0%, #dee0e3 100%);
      position: absolute;
      left: 16px;
      top: 50%;
    }

    ::after {
      content: '';
      width: 17%;
      height: 1px;
      background: linear-gradient(90deg, #dee0e3 0%, rgba(222, 224, 227, 0) 100%);
      position: absolute;
      right: 16px;
      top: 50%;
    }
  }
}
</style>
