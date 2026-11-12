<template>
  <div class="aippt-dialog">
    <div class="header">
      <span class="title">AIPPT</span>
      <span class="subtite" v-if="step === 'template'">从下方挑选合适的模板，开始生成PPT</span>
      <span class="subtite" v-else-if="step === 'outline'">确认下方内容大纲（点击编辑内容，右键添加/删除大纲项），开始选择模板</span>
      <span class="subtite" v-else>在下方输入您的PPT主题，并适当补充信息，如行业、岗位、学科、用途等</span>
    </div>
    
    <template v-if="step === 'setup'">
      <Input class="input" 
        ref="inputRef"
        v-model:value="keyword" 
        :maxlength="50" 
        placeholder="请输入PPT主题，如：大学生职业生涯规划" 
        @enter="createOutline()"
      >
        <template #suffix>
          <span class="count">{{ keyword.length }} / 50</span>
          <div class="submit" type="primary" @click="createOutline()"><IconSend class="icon" /> AI 生成</div>
        </template>
      </Input>
      <div class="recommends">
        <div class="recommend" v-for="(item, index) in recommends" :key="index" @click="setKeyword(item)">{{ item }}</div>
      </div>
      <div class="configs">
        <div class="config-item">
          <div class="label">语言：</div>
          <Select 
            class="config-content"
            style="width: 80px;"
            v-model:value="language"
            :options="[
              { label: '中文', value: '中文' },
              { label: '英文', value: 'English' },
              { label: '日文', value: '日本語' },
            ]"
          />
        </div>
        <div class="config-item">
          <div class="label">风格：</div>
          <Select 
            class="config-content"
            style="width: 80px;"
            v-model:value="style"
            :options="[
              { label: '通用', value: '通用' },
              { label: '学术风', value: '学术风' },
              { label: '职场风', value: '职场风' },
              { label: '教育风', value: '教育风' },
              { label: '营销风', value: '营销风' },
            ]"
          />
        </div>
        <!-- <div class="config-item">
          <div class="label">模型：</div>
          <Select 
            class="config-content"
            style="width: 190px;"
            v-model:value="model"
            :options="[
              { label: 'GLM-4.5-Air', value: 'GLM-4.5-Air' },
              { label: 'GLM-4.5-Flash', value: 'GLM-4.5-Flash' },
              { label: 'Doubao-Seed-1.6-flash', value: 'ark-doubao-seed-1.6-flash' },
              { label: 'Doubao-Seed-1.6', value: 'ark-doubao-seed-1.6' },
            ]"
          />
        </div> -->
        <!-- <div class="config-item">
          <div class="label">配图：</div>
          <Select 
            class="config-content"
            style="width: 100px;"
            v-model:value="img"
            :options="[
              { label: '无', value: '' },
              { label: '模拟测试', value: 'test' },
              { label: 'AI搜图', value: 'ai-search', disabled: true },
              { label: 'AI生图', value: 'ai-create', disabled: true },
            ]"
          />
        </div> -->
      </div>
    </template>
    <div class="preview" v-if="step === 'outline'">
      <pre ref="outlineRef" v-if="outlineCreating">{{ outline }}</pre>
       <div class="outline-view" v-else>
         <OutlineEditor v-model:value="outline" />
       </div>
      <div class="btns" v-if="!outlineCreating">
        <Button class="btn" type="primary" @click="step = 'template'">选择模板</Button>
        <Button class="btn" @click="outline = ''; step = 'setup'">返回重新生成</Button>
      </div>
    </div>
    <div class="select-template" v-if="step === 'template'">
      <div class="templates">
        <div class="template" 
          :class="{ 'selected': selectedTemplate === template.id }" 
          v-for="template in templates" 
          :key="template.id" 
          @click="selectedTemplate = template.id"
        >
          <img :src="template.cover" :alt="template.name">
        </div>
      </div>
      <div class="btns">
        <Button class="btn" type="primary" @click="createPPT()">生成</Button>
        <Button class="btn" @click="step = 'outline'">返回大纲</Button>
      </div>
    </div>

    <FullscreenSpin :loading="loading" tip="AI生成中，请耐心等待 ..." />
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, useTemplateRef } from 'vue'
import { storeToRefs } from 'pinia'
import api from '@pptApp/services'
import useAIPPT from '@pptApp/hooks/useAIPPT'
import type { AIPPTSlide } from '@pptApp/types/AIPPT'
import type { Slide, SlideTheme } from '@pptApp/types/slides'
import message from '@pptApp/utils/message'
import { useMainStore, useSlidesStore } from '@pptApp/store'
import Input from '@pptApp/components/Input.vue'
import Button from '@pptApp/components/Button.vue'
import Select from '@pptApp/components/Select.vue'
import FullscreenSpin from '@pptApp/components/FullscreenSpin.vue'
import OutlineEditor from '@pptApp/components/OutlineEditor.vue'
import { useSSEWriter } from '@pptApp/hooks/useSSEWriter'
import modelApi from '@pptApp/api/aippt'

const { writeStream } = useSSEWriter()
const mainStore = useMainStore()
const slideStore = useSlidesStore()
const { templates } = storeToRefs(slideStore)
const { AIPPT, presetImgPool, getMdContent } = useAIPPT()

const language = ref('中文')
const style = ref('通用')
const img = ref('')
const keyword = ref('')
const outline = ref('')
const selectedTemplate = ref('template_1')
const loading = ref(false)
const outlineCreating = ref(false)
const step = ref<'setup' | 'outline' | 'template'>('setup')
const model = ref('GLM-4.5-Air')
const outlineRef = useTemplateRef<HTMLElement>('outlineRef')
const inputRef = useTemplateRef<InstanceType<typeof Input>>('inputRef')

const recommends = ref([
  '2025科技前沿动态',
  '大数据如何改变世界',
  '餐饮市场调查与研究',
  'AIGC在教育领域的应用',
  '社交媒体与品牌营销',
  '5G技术如何改变我们的生活',
  '年度工作总结与展望',
  '区块链技术及其应用',
  '大学生职业生涯规划',
  '公司年会策划方案',
]) 

onMounted(() => {
  setTimeout(() => {
    inputRef.value!.focus()
  }, 500)
})

const setKeyword = (value: string) => {
  keyword.value = value
  inputRef.value!.focus()
}

const createOutline = async () => {
  if (!keyword.value) return message.error('请先输入PPT主题')

  loading.value = true
  outlineCreating.value = true
  
  // const stream = await api.AIPPT_Outline({
  //   content: keyword.value,
  //   language: language.value,
  //   model: model.value,
  // })
  const stream = await modelApi.callApiWithApiKey('application-6dd3de2c39953bf9a44208652a0b033a', {
    content: keyword.value,
    // language: language.value,
    // model: model.value,
  },true)
    console.log('%c [ stream ]-185', 'font-size:13px; background:pink; color:#bf2c9f;', stream)

  loading.value = false
  step.value = 'outline'


   const reader = stream.body.getReader()

  writeStream({
    reader,
    onContent: (content, chunk) => {
      // chunk 包含后端 SSE 流返回的所有字段
      outline.value += content.replace(/\n\s*\n/g, '\n')
      console.log('%c [ outline.value ]-243', 'font-size:13px; background:pink; color:#bf2c9f;', outline.value)

      // 其它处理逻辑
          if (outlineRef.value) {
          outlineRef.value.scrollTop = outlineRef.value.scrollHeight + 20
        }
    },
    onEnd: () => {
      console.log('Stream is done!')
        outlineCreating.value = false
    },
    onError: (err) => {
      console.error('SSE解析错误', err)
    }
  })
}

const createPPT = async () => {
  loading.value = true

  // const stream = await api.AIPPT({
  //   content: outline.value,
  //   language: language.value,
  //   style: style.value,
  //   model: model.value,
  // })
  const stream = await modelApi.callApiWithApiKey('application-2d206ab5e77001742fb4ef50b4315acb', {
    content: outline.value,
  },true)
  
  if (img.value === 'test') {
    const imgs = await api.getMockData('imgs')
    presetImgPool(imgs)
  }

  // const templateData = await api.getFileData(selectedTemplate.value)
  const templateData = await api.getMockData(selectedTemplate.value)
  const templateSlides: Slide[] = templateData.slides
  const templateTheme: SlideTheme = templateData.theme

  // const reader: ReadableStreamDefaultReader = stream.body.getReader()
  // const decoder = new TextDecoder('utf-8')
  
  // const readStream = () => {
  //   reader.read().then(({ done, value }) => {
  //     if (done) {
  //       loading.value = false
  //       mainStore.setAIPPTDialogState(false)
  //       slideStore.setTheme(templateTheme)
  //       return
  //     }
  
  //     const chunk = decoder.decode(value, { stream: true })
  //     try {
  //       const text = chunk.replace('```json', '').replace('```', '').trim()
  //       if (text) {
  //         const slide: AIPPTSlide = JSON.parse(chunk)
  //         AIPPT(templateSlides, [slide])
  //       }
  //     }
  //     catch (err) {
  //       // eslint-disable-next-line
  //       console.error(err)
  //     }

  //     readStream()
  //   })
  // }
  // readStream()

  // 缓存区用于拼接流式数据
  let buffer = ''
  // 页边界标识
  const PAGE_START = '[START_PAGE]'
  const PAGE_END = '[END_PAGE]'

  const reader = stream.body.getReader()
  const decoder = new TextDecoder('utf-8')

  const readStream = async () => {
    const { done, value } = await reader.read()
    if (done) {
      console.log('流式传输结束')
      loading.value = false
        mainStore.setAIPPTDialogState(false)
      slideStore.setTheme(templateTheme)
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

</script>

<style lang="scss" scoped>
.aippt-dialog {
  margin: -20px;
  padding: 30px;
}
.header {
  margin-bottom: 12px;

  .title {
    font-weight: 700;
    font-size: 20px;
    margin-right: 8px;
    background: linear-gradient(270deg, #d897fd, #33bcfc);
    background-clip: text;
    color: transparent;
    vertical-align: text-bottom;
    line-height: 1.1;
  }
  .subtite {
    color: #888;
    font-size: 12px;
  }
}
.preview {
  pre {
    max-height: 450px;
    padding: 10px;
    margin-bottom: 15px;
    background-color: #f1f1f1;
    overflow: auto;
  }
  .outline-view {
    max-height: 450px;
    padding: 10px;
    margin-bottom: 15px;
    background-color: #f1f1f1;
    overflow: auto;
  }
  .btns {
    display: flex;
    justify-content: center;
    align-items: center;

    .btn {
      width: 120px;
      margin: 0 5px;
    }
  }
}
.select-template {
  .templates {
    display: flex;
    margin-bottom: 10px;
    @include flex-grid-layout();
  
    .template {
      border: 2px solid $borderColor;
      border-radius: $borderRadius;
      width: 324px;
      height: 184px;
      margin-bottom: 12px;

      &:not(:nth-child(2n)) {
        margin-right: 12px;
      }

      &.selected {
        border-color: $themeColor;
      }
  
      img {
        width: 100%;
      }
    }
  }
  .btns {
    display: flex;
    justify-content: center;
    align-items: center;

    .btn {
      width: 120px;
      margin: 0 5px;
    }
  }
}
.recommends {
  display: flex;
  flex-wrap: wrap;
  margin-top: 10px;

  .recommend {
    font-size: 12px;
    background-color: #FFFFFF;
    border-radius: $borderRadius;
    padding: 3px 5px;
    margin-right: 5px;
    margin-top: 5px;
    cursor: pointer;

    &:hover {
      color: $themeColor;
    }
  }
}
.configs {
  margin-top: 15px;
  display: flex;
  // justify-content: space-between;

  .config-item {
    font-size: 13px;
    display: flex;
    align-items: center;
    min-width: 154px;
  .label {
    flex-shrink: 0;
  }
  .config-content {
    width: 80px !important;
  }
  }
}
.count {
  font-size: 12px;
  color: #999;
  margin-right: 10px;
}
.submit {
  height: 20px;
  font-size: 12px;
  background-color: $themeColor;
  color: #fff;
  display: flex;
  align-items: center;
  padding: 0 8px 0 6px;
  border-radius: $borderRadius;
  cursor: pointer;

  &:hover {
    background-color: $themeHoverColor;
  }

  .icon {
    font-size: 15px;
    margin-right: 3px;
  }
}

@media screen and (width <= 800px) {
  .configs {
    margin-top: 15px;
    display: flex;
    flex-direction: column;

    .config-item {
      margin-top: 8px;

      .label {
        flex-shrink: 0;
      }

      .config-content {
        width: 100% !important;
      }
    }
  }
  .select-template {
    .templates {
      max-height: 450px;
      display: block;
      overflow: auto;
    
      .template {
        width: 100%;
        height: unset;
        margin-bottom: 0 !important;
        margin-right: 0 !important;

        & + .template {
          margin-top: 20px;
        }
      }
    }
  }
}
</style>