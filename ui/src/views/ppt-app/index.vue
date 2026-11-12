<template>
  <div v-if="slides.length" class="pptApp-wrapper">
    <Screen v-if="screening" class="pptApp-fullscreen" />
    <Editor v-else-if="_isPC" />
    <Mobile v-else />
    <FullscreenSpin tip="数据加载中，请稍等 ..." v-if="loading" loading :mask="true" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import {
  useScreenStore,
  useMainStore,
  useSnapshotStore,
  useSlidesStore,
  useOutLineStore,
  usePPTLogStore
} from '@pptApp/store'
import { LOCALSTORAGE_KEY_DISCARDED_DB } from '@pptApp/configs/storage'
import { deleteDiscardedDB } from '@pptApp/utils/database'
import { isPC } from '@pptApp/utils/common'
import api from '@pptApp/services'
import modelApi from '@pptApp/api/aippt'
import type { AIPPTSlide } from '@pptApp/types/AIPPT'
import type { Slide, SlideTheme } from '@pptApp/types/slides'
import useAIPPT from '@pptApp/hooks/useAIPPT'
import useSlideHandler from '@pptApp/hooks/useSlideHandler'
const { resetSlides } = useSlideHandler()
const { AIPPT } = useAIPPT()

import Editor from './views/Editor/index.vue'
import Screen from './views/Screen/index.vue'
import Mobile from './views/Mobile/index.vue'
import FullscreenSpin from '@pptApp/components/FullscreenSpin.vue'
import applicationApi from '@/api/application'
import type { ApplicationFormType } from '@/api/type/application'

const _isPC = isPC()

const outLineStore = useOutLineStore()
const PPTLogStore = usePPTLogStore()
const mainStore = useMainStore()
const slidesStore = useSlidesStore()
const snapshotStore = useSnapshotStore()
const { databaseId } = storeToRefs(mainStore)
const { slides } = storeToRefs(slidesStore)
const { screening } = storeToRefs(useScreenStore())
const { outline, selectedTemplate, datasetIdList, style, lang, description } =
  storeToRefs(outLineStore)

const loading = ref(false)
const applicationInfo = ref<ApplicationFormType>({})

if (import.meta.env.MODE !== 'development') {
  window.onbeforeunload = () => false
}

async function getAipptContent() {
  const templateData = await api.getMockData(selectedTemplate.value)
  const templateSlides: Slide[] = templateData.slides
  const templateTheme: SlideTheme = templateData.theme

  let obj = {
    message: `${outline.value}\n语言：${lang.value}\n风格：${style.value}\n更多要求：${description.value}`,
    re_chat: false
  }
  console.log(applicationInfo.value, 'applicationInfo.value', obj)

  let res = await applicationApi.postChatOpen(applicationInfo.value) // 获得临时回话Id
  let stream = await applicationApi.postChatMessage(res.data, obj) // 对话

  // 缓存区用于拼接流式数据
  let buffer = ''
  // 页边界标识
  const PAGE_START = '[START_PAGE]'
  const PAGE_END = '[END_PAGE]'

  const reader = stream.body.getReader()
  const decoder = new TextDecoder('utf-8')
  const contentSlides: AIPPTSlide[] = []

  const readStream = async () => {
    const { done, value } = await reader.read()
    if (done) {
      loading.value = false
      slidesStore.setTheme(templateTheme)
      slidesStore.setContentSlides(contentSlides) // 新增：保存内容真源(ai生成的幻灯片原始数据)
      console.log('流式传输结束')
      slidesStore.setAICreateLoading(false)
      PPTLogStore.updateLog()
      // 触发动画提示显示
      setTimeout(() => {
        mainStore.setShowTemplateTooltip(true)
        // 4秒后自动隐藏
        setTimeout(() => {
          mainStore.setShowTemplateTooltip(false)
        }, 4000)
      }, 800)
      return
    }

    // 1. 解码当前片段
    const decodedChunk = decoder.decode(value, { stream: true })

    // 2. 处理SSE格式的data字段（可能包含多行data:）
    const dataLines = decodedChunk
      .split('\n')
      .map((line) => line.trim())
      .filter((line) => line.startsWith('data:')) // 过滤非data行
      .map((line) => line.replace(/^data:\s*/, '')) // 去除data:前缀

    // 3. 解析每个data块的JSON并提取content
    const contentChunks = []
    for (const dataStr of dataLines) {
      if (!dataStr) continue
      try {
        const dataObj = JSON.parse(dataStr)
        if (dataObj.content) {
          contentChunks.push(dataObj.content)
        }
      } catch (e) {
        console.error('解析data字段失败:', e, dataStr)
      }
    }

    // 4. 将提取的content拼接后存入缓存区
    buffer += contentChunks.join('')
    console.log('处理后的缓存区:', buffer)

    // 解析
    // eslint-disable-next-line no-constant-condition
    while (true) {
      const startIndex = buffer.indexOf(PAGE_START)
      const endIndex = buffer.indexOf(PAGE_END)

      if (startIndex !== -1 && endIndex !== -1 && endIndex > startIndex) {
        const pageContent = buffer.substring(startIndex + PAGE_START.length, endIndex)
        buffer = buffer.substring(endIndex + PAGE_END.length)

        try {
          const slide: AIPPTSlide = JSON.parse(pageContent)
          console.log('解析到完整页:', slide)
          AIPPT(templateSlides, [slide])
          contentSlides.push(slide) // 新增：保存内容真源(ai生成的幻灯片原始数据)
        } catch (e) {
          console.error('单页解析失败:', e, pageContent)
        }
      } else {
        break
      }
    }

    readStream()
  }

  readStream()
}
const getApplicationInfo = async () => {
  const applicationId = '7cb16946-77f9-11f0-b98a-0242ac110005'
  const res = await applicationApi.getApplicationDetail(applicationId) // 通过应用id获取应用详情
  applicationInfo.value = res.data
  applicationInfo.value.model_id = res.data.model // 设置模型id
  applicationInfo.value.dataset_id_list = datasetIdList.value // 设置数据集id列表
}
onMounted(async () => {
  // const slides = await api.getFileData('slides')
  // const slides = await api.getMockData('slides')
  // slidesStore.setSlides(slides)
  loading.value = true
  await getApplicationInfo() // 获取应用详情

  if (selectedTemplate.value && outline.value) {
    // 1. 先重置幻灯片
    resetSlides()
    // 2. 再进行后续初始化和数据获取
    slidesStore.setAICreateLoading(true)
    getAipptContent()
  } else {
    // const slides = await api.getFileData('slides')
    const slides = await api.getMockData('slides')
    slidesStore.setSlides(slides)
    loading.value = false
  }

  await deleteDiscardedDB()
  snapshotStore.initSnapshotDatabase()
})
// 应用注销时向 localStorage 中记录下本次 indexedDB 的数据库ID，用于之后清除数据库
window.addEventListener('beforeunload', () => {
  const discardedDB = localStorage.getItem(LOCALSTORAGE_KEY_DISCARDED_DB)
  const discardedDBList: string[] = discardedDB ? JSON.parse(discardedDB) : []

  discardedDBList.push(databaseId.value)

  const newDiscardedDB = JSON.stringify(discardedDBList)
  localStorage.setItem(LOCALSTORAGE_KEY_DISCARDED_DB, newDiscardedDB)
})
</script>

<style lang="scss">
.pptApp-fullscreen {
  position: fixed;
  z-index: 9999;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background: #fff;
}
.pptApp-wrapper {
  height: 100%;
  @import '@pptApp/assets/styles/prosemirror.scss';
  @import '@pptApp/assets/styles/global.scss';
  @import '@pptApp/assets/styles/font.scss';
}
</style>
