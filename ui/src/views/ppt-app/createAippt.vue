<template>
  <div class="flex-center ppt-container">
    <div class="btn-log" title="历史记录" @click="handleLogClick">
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
       <!-- <div class="btn-log" title="模板编辑" style="right: 94px" @click="handleTemplateClick">
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
      <path d="M7 12H10" stroke="#4d6bfe" stroke-width="1.5" stroke-linecap="round" />
      <path d="M7 16H14" stroke="#4d6bfe" stroke-width="1.5" stroke-linecap="round" />
      <path d="M14 12L17 15L20 12" stroke="#4d6bfe" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
      <path d="M17 15V9" stroke="#4d6bfe" stroke-width="1.5" stroke-linecap="round" />
    </svg>
    </div> -->
    <div
      class="aippt-dialog"
      :class="{ aipptWidth: step !== 'template', templateStyle: step === 'template' }"
    >
      <div class="header">
        <span class="title">智能PPT</span>
        <span class="subtite" v-if="step === 'template'">从下方挑选合适的模板，开始生成PPT</span>
        <span class="subtite" v-else-if="step === 'outline'"
          >确认下方内容大纲（点击编辑内容，右键添加/删除大纲项），开始选择模板</span
        >
        <span class="subtite" v-else
          >在下方输入您的PPT主题，并适当补充信息，如行业、岗位、学科、用途等</span
        >
      </div>

      <template v-if="step === 'setup'">
        <div class="generate-entry">
          <div class="tabs">
            <div
              class="tab"
              :class="{ active: activeTab === 'manual' }"
              @click="activeTab = 'manual'"
            >
              <img src="@pptApp/assets/imgs/input.svg" alt="" width="20px" class="mr-8" />
              输入主题
            </div>
            <div class="tab" :class="{ active: activeTab === 'file' }" @click="activeTab = 'file'">
              <img src="@pptApp/assets/imgs/upload.svg" alt="" width="20px" class="mr-8" />
              导入文档生成PPT
            </div>
          </div>
          <transition name="tab-fade" mode="out-in">
            <div
              v-if="activeTab === 'manual'"
              key="manual"
              class="generate-entry-content input input--right"
            >
              <div class="filter">
                <div class="configs">
                  <div class="config-item">
                    <div class="label">语言：</div>
                    <el-select
                      class="config-content"
                      v-model="language"
                      placeholder="请选择语言"
                      style="width: 80px"
                    >
                      <el-option
                        v-for="item in [
                          { label: '中文', value: '中文' },
                          { label: '英语', value: '英语' },
                          { label: '韩语', value: '韩语' },
                          { label: '日语', value: '日语' }
                        ]"
                        :key="item.label"
                        :label="item.label"
                        :value="item.value"
                      />
                    </el-select>
                  </div>
                  <div class="config-item">
                    <div class="label">风格：</div>
                    <el-select
                      class="config-content"
                      v-model="style"
                      placeholder="请选择风格"
                      style="width: 100px"
                    >
                      <el-option
                        v-for="item in [
                          { label: '通用', value: '通用' },
                          { label: '学术风', value: '学术风' },
                          { label: '职场风', value: '职场风' },
                          { label: '教育风', value: '教育风' },
                          { label: '营销风', value: '营销风' }
                        ]"
                        :key="item.label"
                        :label="item.label"
                        :value="item.value"
                      />
                    </el-select>
                    <!-- <Select 
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
                  /> -->
                  </div>
                  <div class="config-item">
                    <div class="label">关联知识库：</div>
                    <el-select
                      class="config-content"
                      v-model="applicationInfo.dataset_id_list"
                      multiple
                      collapse-tags
                      placeholder="请选择关联知识库"
                      style="width: 180px"
                    >
                      <el-option
                        v-for="item in datasetList"
                        :key="item.id"
                        :label="item.name"
                        :value="item.id"
                      />
                    </el-select>
                  </div>
                </div>
              </div>
              <div class="title-box">
                <el-input
                  ref="inputRef"
                  v-model="keyword"
                  @keydown.enter="sendChatHandle($event)"
                  type="textarea"
                  :autosize="{ minRows: 1, maxRows: 2 }"
                  :placeholder="placeholderText"
                ></el-input>
                <div class="title-box__footer-container">
                  <el-button type="primary" @click="createOutline()">AI 生成</el-button>
                </div>
              </div>
              <!-- 更多生成要求按钮 -->
              <el-button
                class="more-requirements"
                @click="toggleMoreRequirements"
                link
                type="primary"
                >更多生成要求
                <el-icon class="el-icon--right" :class="{ expanded: showMoreRequirements }">
                  <ArrowDown />
                </el-icon>
              </el-button>
              <!-- 更多生成要求输入框  -->
              <transition name="slide-fade" appear>
                <div class="more-requirements-input" v-show="showMoreRequirements">
                  <el-input
                    v-model="moreRequirements"
                    placeholder="请输入更多生成要求，如：内容结构、重点内容等"
                    :autosize="{ minRows: 4, maxRows: 4 }"
                    type="textarea"
                    class="requirements-textarea"
                  >
                  </el-input>
                </div>
              </transition>

              <div class="recommends">
                <div
                  class="recommend"
                  v-for="(item, index) in recommends"
                  :key="index"
                  @click="setKeyword(item)"
                >
                  {{ item }}
                </div>
              </div>
            </div>
            <div v-else key="file" class="generate-entry-content input input--left">
              <div class="tab-placeholder">
                <div class="placeholder-title">导入文档生成PPT</div>
                <div class="placeholder-desc">
                  敬请期待：上传 PDF/Docx/Markdown，自动抽取大纲并生成 PPT
                </div>
              </div>
            </div>
          </transition>
        </div>
      </template>
      <div class="preview" v-if="step === 'outline'">
        <pre ref="outlineRef" v-if="outlineCreating">{{ outline }}</pre>
        <div class="outline-view" v-else>
          <OutlineEditor v-model:value="outline" />
        </div>
        <div class="btns" v-if="!outlineCreating">
          <Button class="btn" type="primary" @click="step = 'template'">选择模板</Button>
          <Button class="btn" @click="handleRest">返回重新生成</Button>
        </div>
      </div>
      <div class="select-template" v-if="step === 'template'">
        <!-- <div class="templates">
          <div
            class="template"
            :class="{ selected: selectedTemplate === template.id }"
            v-for="template in templates"
            :key="template.id"
            @click="selectedTemplate = template.id"
          >
            <img :src="getImageUrl(template.cover)" :alt="template.name" />
          </div>
        </div> -->
        <TemplateSelector :templates="templates" v-model:selectedTemplate="selectedTemplate" />
        <div class="btns">
          <Button class="btn" type="primary" @click="createPPT()">生成</Button>
          <Button class="btn" @click="step = 'outline'">返回大纲</Button>
        </div>
      </div>
    </div>
    <FullscreenSpin :loading="loading" tip="AI生成中，请耐心等待 ..." />
    <PPTLogModal ref="refPPTLogModal" />
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, onBeforeUnmount, computed, useTemplateRef } from 'vue'
import { storeToRefs } from 'pinia'
import api from '@pptApp/services'
import useAIPPT from '@pptApp/hooks/useAIPPT'
// import type { AIPPTSlide } from '@pptApp/types/AIPPT'
// import type { Slide, SlideTheme } from '@pptApp/types/slides'
import message from '@pptApp/utils/message'
import { useMainStore, useSlidesStore, useOutLineStore } from '@pptApp/store'
import Input from '@pptApp/components/Input.vue'
import Button from '@pptApp/components/Button.vue'
import FullscreenSpin from '@pptApp/components/FullscreenSpin.vue'
import OutlineEditor from '@pptApp/components/OutlineEditor.vue'
import { useSSEWriter } from '@pptApp/hooks/useSSEWriter'
import { useRouter, useRoute } from 'vue-router'
import applicationApi from '@/api/application'
import type { ApplicationFormType } from '@/api/type/application'
import useStore from '@/stores'
import PPTLogModal from '@pptApp/components/PPTLogModal.vue'
import TemplateSelector from '@pptApp/views/components/templateSelector/index.vue'
const { application } = useStore()

const outLineStore = useOutLineStore()
const router = useRouter()
const route = useRoute()
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
const activeTab = ref<'manual' | 'file'>('manual')

const recommends = ref([
  // '2025科技前沿动态',
  // '大数据如何改变世界',
  // '餐饮市场调查与研究',
  // 'AIGC在教育领域的应用',
  // '社交媒体与品牌营销',
  // '5G技术如何改变我们的生活',
  // '年度工作总结与展望',
  // '区块链技术及其应用',
  // '大学生职业生涯规划',
  // '公司年会策划方案',
])
// 打字机占位符：基于 recommends 循环输出
const placeholderText = ref<string>()
const defaultRecommends = ['大学生职业生涯规划', 'AIGC在教育领域的应用', '年度工作总结与展望']
const typingWords = computed<string[]>(() =>
  recommends.value && recommends.value.length > 0 ? recommends.value : defaultRecommends
)

const typingTimer = ref<number | null>(null)
const startTypewriter = () => {
  const words = typingWords.value
  if (!words.length) return
  let wordIndex = 0
  let charIndex = 0
  let deleting = false

  const step = () => {
    const current = words[wordIndex]
    if (!deleting) {
      charIndex = Math.min(charIndex + 1, current.length)
    } else {
      charIndex = Math.max(charIndex - 1, 0)
    }
    placeholderText.value = current.slice(0, charIndex)

    let delay = deleting ? 40 : 80

    if (!deleting && charIndex === current.length) {
      deleting = true
      delay = 1200
    } else if (deleting && charIndex === 0) {
      deleting = false
      wordIndex = (wordIndex + 1) % words.length
      delay = 300
    }

    typingTimer.value = window.setTimeout(step, delay)
  }
  step()
}
interface DatasetItem {
  id: string
  name: string
  type: '0' | '1'
  category: string
  desc?: string
  user_id: string
  create_time: string
  update_time: string
  meta?: string
}
const showMoreRequirements = ref(false)
const moreRequirements = ref('')
const applicationInfo = ref<ApplicationFormType>({})
const applicationId = '23ac74e8-7741-11f0-80dd-0242ac110005' // 应用ID

const toggleMoreRequirements = () => {
  showMoreRequirements.value = !showMoreRequirements.value
}
const getApplicationInfo = async () => {
  const res = await applicationApi.getApplicationDetail(applicationId) // 通过应用id获取应用详情
  applicationInfo.value = res.data
  applicationInfo.value.model_id = res.data.model
}
const datasetList = ref<DatasetItem[]>([])

const getDatasetIdList = () => {
  application.asyncGetApplicationDataset(applicationId).then((res: any) => {
    datasetList.value = res.data
  })
}

// 预加载 mocks/img 目录下所有 png 图片
// 定义图片模块的接口类型
interface ImageModule {
  default: string
}
// 使用类型断言指定images对象的类型
const images: Record<string, ImageModule> = import.meta.glob(
  '/src/views/ppt-app/mocks/imgs/*.jpg',
  {
    eager: true
  }
) as Record<string, ImageModule>

const getImageUrl = (name: string): string => {
  // 构建完整的图片路径
  const path = `/src/views/ppt-app/mocks/imgs/${name}`
  // 返回图片的实际URL
  return images[path].default
}

const setKeyword = (value: string) => {
  keyword.value = value
  inputRef.value!.focus()
}
function sendChatHandle(event: any) {
  if (event.shiftKey) {
    // Shift+Enter：手动插入换行
    keyword.value += '\n'
    event.preventDefault()
  } else if (!event.ctrlKey) {
    // 仅 Enter：发送消息
    event.preventDefault()
    if (keyword.value.trim()) {
      createOutline()
    }
  } else {
    // Ctrl+Enter：也换行
    keyword.value += '\n'
  }
}
const createOutline = async () => {
  if (!keyword.value) return message.error('请先输入PPT主题')

  loading.value = true
  outlineCreating.value = true

  // 构建完整的内容，包含主题、语言、风格、更多要求
  const obj = {
    message: `${keyword.value}\n语言：${language.value}\n风格：${style.value}\n更多要求：${moreRequirements.value}`,
    re_chat: false
  }
  let res = await applicationApi.postChatOpen(applicationInfo.value) // 获得临时回话Id
  let stream = await applicationApi.postChatMessage(res.data, obj) // 对话
  console.log('%c [ stream ]-185', 'font-size:13px; background:pink; color:#bf2c9f;', stream)

  loading.value = false
  step.value = 'outline'

  const reader = stream.body.getReader()

  writeStream({
    reader,
    onContent: (content, chunk) => {
      // chunk 包含后端 SSE 流返回的所有字段
      outline.value += content.replace(/\n\s*\n/g, '\n')
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
  slideStore.setTitle(keyword.value) // 设置默认ppt title
  slideStore.setIsTemplateEdit(false) // 设置页面类型为编辑页还是模板创建页
  outLineStore.setSelectedTemplate(selectedTemplate.value) // 模版
  outLineStore.setOutline(outline.value) // 大纲内容
  outLineStore.setStyle(style.value) // 风格
  outLineStore.setPPTThem(keyword.value) // ppt主题
  outLineStore.setLang(language.value) // 语言
  outLineStore.setDescription(moreRequirements.value) // 更多要求
  outLineStore.setDatasetIdList(applicationInfo.value?.dataset_id_list as string[]) // 关联知识库
  router.push({ name: 'pptAppEdit' })

  if (img.value === 'test') {
    const imgs = await api.getMockData('imgs')
    presetImgPool(imgs)
  }
}
const handleBackOutline = () => {
  step.value = 'outline'
  outline.value = outLineStore.outline
}
onMounted(() => {
  // 回到大纲逻辑
  const route = useRoute()
  if (route.query.step === 'outline') {
    handleBackOutline()
  } else {
    setTimeout(() => {
      inputRef.value!.focus()
    }, 500)
  }
  getApplicationInfo()
  getDatasetIdList()
  startTypewriter()
})
onBeforeUnmount(() => {
  if (typingTimer.value) clearTimeout(typingTimer.value)
})

const handleRest = () => {
  outline.value = ''
  step.value = 'setup'
}
const refPPTLogModal = ref()
const handleLogClick = () => {
  refPPTLogModal.value.openDialog()
}
const handleTemplateClick=()=>{
    slideStore.setIsTemplateEdit(true) 
  router.push({ name: 'pptAppEdit' })
}
</script>

<style lang="scss" scoped>
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
.ppt-container {
  width: 100%;
  height: 100%;
}
.aipptWidth {
  width: 900px;
}
.templateStyle {
  width: 80%;
  height: 80%;
}
.aippt-dialog {
  margin: 0 auto;
  padding: 30px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  min-height: 420px;
}
.header {
  margin-bottom: 20px;

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
    font-size: 13px;
  }
}
.preview {
  pre {
    max-height: 450px;
    padding: 10px;
    margin-bottom: 15px;
    background-color: #fff;
    overflow: auto;
  }
  .outline-view {
    max-height: 450px;
    padding: 10px;
    margin-bottom: 15px;
    background-color: #fff;
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
  display: flex;
  flex-direction: column; /* 垂直排列 */
  height: 100%; /* 让它占满父容器高度 */
  .templates {
    display: flex;
    justify-content: left;
    margin-bottom: 10px;
    gap: 12px;
    @include flex-grid-layout();
    .template {
      border: 2px solid $borderColor;
      border-radius: $borderRadius;
      width: 324px;
      height: 184px;
      // margin-bottom: 12px;

      // &:not(:nth-child(2n)) {
      //   margin-right: 12px;
      // }

      &.selected {
        border-color: $themeColor;
      }

      img {
        width: 100%;
        -webkit-user-drag: none; /* 禁止 WebKit 浏览器拖动 */
      }
    }
  }
  .btns {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: auto;
    margin-bottom: 30px;
    margin-top: 10px;
    .btn {
      width: 120px;
      margin: 0 5px;
    }
  }
}
.recommends {
  display: flex;
  flex-wrap: wrap;
  // margin-top: 10px;

  .recommend {
    font-size: 12px;
    background-color: #ffffff;
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
  margin-top: 10px;
  display: flex;
  // justify-content: space-between;
  gap: 8px;

  .config-item {
    // font-size: 13px;
    font-size: 14px;
    display: flex;
    align-items: center;
    // min-width: 154px;
    .label {
      flex-shrink: 0;
    }
    .config-content {
      // width: 160px !important;
      :deep(.el-select__wrapper) {
        border-radius: 2px !important;
      }
    }
  }
}

.tab-placeholder {
  background: #fff;
  border: 1px dashed #e5e7eb;
  border-radius: 6px;
  padding: 16px;
  color: #6b7280;
  .placeholder-title {
    font-weight: 600;
    margin-bottom: 6px;
    color: #374151;
  }
  .placeholder-desc {
    font-size: 13px;
  }
}
.count {
  font-size: 14px;
  color: #999;
  margin-right: 10px;
}
.submit {
  height: 20px;
  font-size: 14px;
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

.more-requirements {
  margin-top: 16px;
  .expanded {
    transform: rotate(180deg);
  }
  &.el-button:focus {
    border: 1px solid transparent !important;
  }
}

.more-requirements-input {
  margin-top: 8px;
  overflow: hidden;
  :deep(.el-textarea__inner) {
    resize: none;
    border-radius: 12px;
  }
}

// 添加过渡动画样式
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateY(-10px) scale(0.98);
  max-height: 0;
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.98);
  max-height: 0;
}

.slide-fade-enter-to,
.slide-fade-leave-from {
  opacity: 1;
  transform: translateY(0) scale(1);
  max-height: 200px;
}

// 选项卡内容切换淡入淡出
.tab-fade-enter-active,
.tab-fade-leave-active {
  transition:
    opacity 0.25s ease,
    transform 0.25s ease;
}
.tab-fade-enter-from,
.tab-fade-leave-to {
  opacity: 0;
  transform: translateY(4px);
}

@media screen and (width <= 800px) {
  .configs {
    margin-top: 10px;
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

        // & + .template {
        //   margin-top: 20px;
        // }
      }
    }
  }
}
.generate-entry {
  position: relative;
  width: 820px;
  box-shadow: 0 16px 36px #542fb814;
  border-radius: 24px;
  border: 2px solid #ffffff;
  overflow: hidden;
  .tabs {
    display: flex;
    border-radius: 24px 24px 0 0;
    flex-direction: row;
    height: 60px;
    flex-shrink: 0;
    overflow: hidden;
    position: relative;
    z-index: 1;
    user-select: none;
    .tab {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family:
        PingFangSC,
        PingFang SC;
      font-weight: 500;
      font-size: 18px;
      color: #141414;
      position: relative;
      cursor: pointer;
      &:first-of-type.active {
        border-radius: 0 30px 0 0;
        &::after {
          content: '';
          pointer-events: none;
          position: absolute;
          width: 60px;
          height: 60px;
          right: -30px;
          bottom: 0;
          background: radial-gradient(circle at 100% 0, transparent 30px, #fff 31px);
          transform: translateY(50%);
        }
      }
      &:last-of-type.active {
        border-radius: 30px 0 0 0;
        &::before {
          content: '';
          pointer-events: none;
          position: absolute;
          width: 60px;
          height: 60px;
          left: -30px;
          bottom: 0;
          background: radial-gradient(circle at 0 0, transparent 30px, #fff 31px);
          transform: translateY(50%);
        }
      }
      &.active {
        background: #fff;
      }
    }
  }
  .generate-entry-content {
    background-color: #fff;

    &.input {
      border-radius: 0 24px 0 0;
      padding: 6px 22px 10px 22px;
    }

    &.input--right {
      border-radius: 0 24px 0 0;
    }

    &.input--left {
      border-radius: 24px 0 0 0;
    }

    .filter {
      // margin: 16px 0;
      margin-bottom: 16px;
      display: flex;
      gap: 8px;
      align-items: center;
      flex-direction: row;
    }

    .title-box {
      height: 80px;
      border: 4px solid transparent;
      border-radius: 18px;
      background-clip: padding-box, border-box;
      background-origin: padding-box, border-box;
      // background-image: linear-gradient(to right, #fff, #fff), linear-gradient(270deg, #79BBFF, #409EFF, #337ECC);
      // background-image: linear-gradient(to right, #fff, #fff), linear-gradient(270deg,#337ECC, #79BBFF, #409EFF, );
      background-image:
        linear-gradient(to right, #fff, #fff), linear-gradient(270deg, #d897fd, #33bcfc);
      padding: 8px 20px 0 10px;

      :deep(.el-textarea__inner) {
        border-radius: 8px !important;
        box-shadow: none;
        resize: none;
        box-sizing: border-box;
        padding: 0 2px 0px 12px;
        height: 40px !important;
      }

      .title-box__footer-container {
        display: flex;
        justify-content: flex-end;
      }
    }
  }
}
</style>
