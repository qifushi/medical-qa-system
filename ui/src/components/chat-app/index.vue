<template>
  <div ref="aiChatRef" class="ai-chat" :class="log ? 'chart-log' : ''">
    <el-scrollbar ref="scrollDiv" @scroll="handleScrollTop">
      <div ref="dialogScrollbar" class="ai-chat__content p-24 chat-width">
        <div class="item-content mb-16" v-if="!props.available || (props.data?.prologue && !log)">
          <div class="avatar">
            <AppAvatar class="avatar-gradient">
              <img src="@/assets/icon_robot.svg" style="width: 75%" alt="" />
            </AppAvatar>
          </div>
          <!-- 开场白 -->
          <div class="content">
            <div style="font-size: 20px; color: #329cff">
              {{ prologueList[0].str }}
            </div>
            <el-card shadow="always" class="dialog-card prologue-card">
              <div class="prologue-zhushou"></div>
              <div class="card-title mb-16">为您推荐</div>
              <el-row :gutter="20">
                <el-col :span="12" v-for="(item, index) in prologueList.slice(1)" :key="index">
                  <div
                    v-if="item.type === 'question'"
                    @click="quickProblemHandle(item)"
                    class="problem-button ellipsis-2 mb-16"
                    :class="log ? 'disabled' : 'cursor'"
                  >
                    <div class="problem-button-icon">
                      <img src="~@/assets/chatapp-page/document.png" alt="" />
                    </div>
                    <!-- <el-icon><EditPen /></el-icon> -->
                    <div class="ellipsis-2 problem-button-text">
                      <div>
                        {{ item.str }}
                      </div>
                      <div style="font-size: 14px; color: #676768">
                        {{ item.strChild }}
                      </div>
                    </div>
                  </div>
                  <MdPreview
                    v-if="item.type === 'md' && !prologueList[0]"
                    class="mb-8"
                    ref="editorRef"
                    editorId="preview-only"
                    :modelValue="item.str"
                    noIconfont
                    no-mermaid
                  />
                </el-col>
              </el-row>
            </el-card>
          </div>
        </div>
        <template v-for="(item, index) in chatList" :key="index">
          <!-- 问题 -->
          <div class="item-content mb-16 lighter">
            <div class="avatar">
              <AppAvatar class="avatar-user">
                <img src="@/assets/user-icon.png" alt="" />
              </AppAvatar>
            </div>
            <div class="content">
              <div class="text break-all">
                {{ item.problem_text }}
              </div>
            </div>
          </div>
          <!-- 回答 -->
          <div class="item-content mb-16 lighter">
            <div class="avatar">
              <AppAvatar class="avatar-gradient">
                <img src="@/assets/icon_robot.svg" style="width: 75%" alt="" />
              </AppAvatar>
            </div>

            <div class="content">
              <div class="flex" v-if="!item.answer_text && !item.think_text">
                <el-card
                  v-if="item.write_ed === undefined || item.write_ed === true"
                  shadow="always"
                  class="dialog-card"
                >
                  <MdRenderer
                    source=" 抱歉，没有查找到相关内容，请重新描述您的问题或提供更多信息。"
                  ></MdRenderer>
                  <!-- 知识来源 -->
                  <div v-if="showSource(item)">
                    <KnowledgeSource :data="item" :type="props.data.type" />
                  </div>
                </el-card>
                <el-card v-else-if="item.is_stop" shadow="always" class="dialog-card">
                  已停止回答
                </el-card>
                <el-card v-else shadow="always" class="dialog-card">
                  回答中 <span class="dotting"></span>
                </el-card>
              </div>

              <el-card v-else shadow="always" class="dialog-card">
                <!-- 思考内容区域 -->
                <div v-if="item.think_text && item.think_text.trim()" class="think-section">
                  <div class="think-button" @click="toggleThink(item)">
                    <img src="@/assets/chatapp-page/chatapp_think.svg" alt="" class="think-icon" />
                    <div
                      v-if="
                        item.think_buffer?.length > 0 ||
                        (item.think_buffer?.length === 0 && item.answer_text == '')
                      "
                    >
                      深度思考中<span class="dotting"></span>
                    </div>
                    <div v-else>已深度思考</div>
                    <el-icon
                      :class="{
                        'is-reverse': item.think_buffer?.length > 0 || item.isThinkExpanded  ||
                        (item.think_buffer?.length === 0 && item.answer_text == '')
                      }"
                      ><ArrowDown
                    /></el-icon>
                  </div>

                  <div
                    v-show="item.think_buffer?.length > 0 || item.isThinkExpanded  ||
                        (item.think_buffer?.length === 0 && item.answer_text == '')"
                    class="think-content"
                  >
                    <MdRenderer :source="item.think_text"></MdRenderer>
                  </div>
                </div>

                <MdRenderer :source="item.answer_text"></MdRenderer>
                <!-- 知识来源 -->
                <div v-if="showSource(item)">
                  <KnowledgeSource :data="item" :type="props.data.type" />
                </div>
              </el-card>
              <div class="flex-between mt-8" v-if="log">
                <LogOperationButton v-model:data="chatList[index]" :applicationId="appId" />
              </div>

              <div class="flex-between mt-8" v-else>
                <div>
                  <el-button
                    type="primary"
                    v-if="item.is_stop && !item.write_ed"
                    @click="startChat(item)"
                    link
                    >继续</el-button
                  >
                  <el-button type="primary" v-else-if="!item.write_ed" @click="stopChat(item)" link
                    >停止回答</el-button
                  >
                </div>
              </div>
              <div v-if="item.write_ed && props.appId && 500 != item.status" class="flex-between">
                <OperationButton
                  :data="item"
                  :applicationId="appId"
                  :chatId="chartOpenId"
                  :chat_loading="loading"
                  @regeneration="regenerationChart(item)"
                  @readAnswer="readAnswer(item)"
                />
              </div>
            </div>
          </div>
        </template>
      </div>
    </el-scrollbar>
    <div class="ai-chat__operate p-24" v-if="!log">
      <slot name="operateBefore" />
      <div class="operate-textarea flex chat-width">
        <div>
          <el-input
            ref="quickInputRef"
            v-model="inputValue"
            placeholder="请输入您想要查询的内容......"
            :autosize="{ minRows: 4, maxRows: isMobile ? 4 : 10 }"
            type="textarea"
            :maxlength="100000"
            @keydown.enter="sendChatHandle($event)"
          />
          <div class="operate">
            <div class="switch-container">
              <div v-if="hasUploadAndNetwork() && route.name !== 'documentRead'">
                <el-switch class="switch" v-model="isNetwork" />
                <span @click="clickNetworkSwt" class="ml-8 switch-text">{{
                  isNetwork ? '联网开启' : '联网关闭'
                }}</span>
              </div>
            </div>
            <div class="sent-button-container flex align-center">
              <span class="flex align-center" v-if="hasUploadAndNetwork()">
                <el-upload
                  action="#"
                  multiple
                  :auto-upload="false"
                  :show-file-list="false"
                  :accept="getAcceptList()"
                  :on-change="(file: any, fileList: any) => uploadFile(file, fileList)"
                >
                  <el-tooltip effect="dark" placement="top" popper-class="upload-tooltip-width">
                    <template #content>
                      <div class="break-all pre-wrap">
                        上传文件：最多50个，每个文件限制 100MB<br />文件类型：pdf、doc、xlsx、ppt、txt、图片等
                      </div>
                    </template>
                    <el-button text :disabled="checkMaxFilesLimit()">
                      <AppIcon
                        iconName="chatapp-upload-file"
                        style="font-size: 26px; color: #5e6772"
                      ></AppIcon>
                    </el-button>
                  </el-tooltip>
                </el-upload>
              </span>
              <el-button
                class="sent-button"
                :disabled="isDisabledChart || loading"
                @click="sendChatHandle"
                type="primary"
              >
                发 送
              </el-button>
              <!-- <el-button
              text
              class="sent-button"
              :disabled="isDisabledChart || loading"
              @click="sendChatHandle"
            >
              <img v-show="isDisabledChart || loading" src="@/assets/icon_send.svg" alt="" />
              <img
                v-show="!isDisabledChart && !loading"
                src="@/assets/icon_send_colorful.svg"
                alt=""
              />
            </el-button> -->
            </div>
          </div>
        </div>
        <el-scrollbar max-height="300px" style="background-color: #f3f5f9; width: 100%">
          <div
            class="p-8-12"
            v-loading="fileLoading"
            v-if="
              uploadDocumentList.length ||
              uploadImageList.length ||
              uploadAudioList.length ||
              uploadVideoList.length
            "
          >
            <el-space wrap>
              <template v-for="(item, index) in uploadDocumentList" :key="index">
                <el-card
                  shadow="never"
                  style="--el-card-padding: 8px; border-radius: 8px"
                  class="file cursor"
                >
                  <div
                    class="flex align-center"
                    style="margin-right: 5px"
                    @mouseenter.stop="mouseenter(item)"
                    @mouseleave.stop="mouseleave()"
                  >
                    <div
                      @click="deleteFile(index, item, 'document')"
                      class="delete-icon color-secondary"
                      v-if="showDelete === item.url"
                    >
                      <el-icon><CircleCloseFilled /></el-icon>
                    </div>
                    <img :src="getImgUrl(item && item?.name)" alt="" width="24" />
                    <div class="ml-4 ellipsis" style="max-width: 160px" :title="item && item?.name">
                      {{ item && item?.name }}
                    </div>
                  </div>
                </el-card>
              </template>
              <template v-for="(item, index) in uploadImageList" :key="index">
                <div
                  class="file cursor border border-r-4"
                  v-if="item.url"
                  @mouseenter.stop="mouseenter(item)"
                  @mouseleave.stop="mouseleave()"
                >
                  <div
                    @click="deleteFile(index, item, 'image')"
                    class="delete-icon color-secondary"
                    v-if="showDelete === item.url"
                  >
                    <el-icon><CircleCloseFilled /></el-icon>
                  </div>
                  <el-image
                    :src="item.url"
                    alt=""
                    fit="cover"
                    style="width: 40px; height: 40px; display: block"
                    class="border-r-4"
                  />
                </div>
              </template>
              <template v-for="(item, index) in uploadAudioList" :key="index">
                <el-card shadow="never" style="--el-card-padding: 8px" class="file cursor">
                  <div
                    class="flex align-center"
                    @mouseenter.stop="mouseenter(item)"
                    @mouseleave.stop="mouseleave()"
                  >
                    <div
                      @click="deleteFile(index, item, 'audio')"
                      class="delete-icon color-secondary"
                      v-if="showDelete === item.url"
                    >
                      <el-icon><CircleCloseFilled /></el-icon>
                    </div>
                    <img :src="getImgUrl(item && item?.name)" alt="" width="24" />
                    <div class="ml-4 ellipsis" style="max-width: 160px" :title="item && item?.name">
                      {{ item && item?.name }}
                    </div>
                  </div>
                </el-card>
              </template>
            </el-space>
          </div>
        </el-scrollbar>
      </div>
    </div>
    <div style="position: fixed; left: 50%" v-loading="!isPlaying">
      <transition :name="'fade'" @after-enter="afterEnter" @after-leave="afterLeave">
        <audio
          v-if="showPlayer"
          ref="audioPlayer"
          controls
          @ended="handleAudioEnded"
          @play="handlePlay"
        ></audio>
      </transition>
    </div>
  </div>
</template>
<script setup lang="ts">
import applicationApi from '@/api/application'
import documentApi from '@/api/document'
import logApi from '@/api/log'
import { ChatManagement, type chatType } from '@/api/type/application'
import MdRenderer from '@/components/markdown/MdRenderer.vue'
import useStore from '@/stores'
import { isWorkFlow } from '@/utils/application'
import { MsgWarning } from '@/utils/message'
import { getImgUrl, randomId } from '@/utils/utils'
import { debounce } from 'lodash'
import { computed, nextTick, onMounted, reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import KnowledgeSource from './KnowledgeSource.vue'
import LogOperationButton from './LogOperationButton.vue'
import OperationButton from './OperationButton.vue'
defineOptions({ name: 'AiChat' })
const router = useRouter()
const route = useRoute()
const {
  params: { accessToken, id },
  query: { mode }
} = route as any
const props = defineProps({
  data: {
    type: Object,
    default: () => {}
  },
  appId: String, // 仅分享链接有
  log: Boolean,
  record: {
    type: Array<chatType>,
    default: () => []
  },
  // 应用是否可用
  available: {
    type: Boolean,
    default: true
  },
  chatId: {
    type: String,
    default: ''
  } // 历史记录Id
})

const emit = defineEmits(['refresh', 'scroll', 'webSearchList'])

const { application, common } = useStore()

const isMobile = computed(() => {
  return common.isMobile() || mode === 'embed'
})

const aiChatRef = ref()
const quickInputRef = ref()
const scrollDiv = ref()
const dialogScrollbar = ref()
const loading = ref(false)
const inputValue = ref('')
const chartOpenId = ref('')
const chatList = ref<any[]>([])
const readPrologue = ref('')

const isDisabledChart = computed(
  () => !(inputValue.value.trim() && (props.appId || props.data?.name))
)
const isMdArray = (val: string) => val.match(/^-\s.*/m)
const isChildMdArray = (val: string) => val.match(/^--\s.*/m)

const prologueList = computed(() => {
  // 新增一级标题逻辑
  const temp =
    readPrologue.value !== ''
      ? readPrologue.value
      : props.available
        ? props.data?.prologue
        : '抱歉，当前正在维护，无法提供服务，请稍后再试！'
  const lines = temp?.split('\n')

  return lines
    .reduce((pre_array: Array<any>, current: string, index: number) => {
      const currentObj = isMdArray(current)
        ? {
            type: 'question',
            str: current.replace(/^-\s+/, ''),
            strChild: '',
            index: index
          }
        : isChildMdArray(current)
          ? {
              type: 'question',
              str: '',
              strChild: current.replace(/^--\s+/, ''),
              index: index
            }
          : {
              type: 'md',
              str: current,
              strChild: '',
              index: index
            }

      if (pre_array.length > 0) {
        const pre = pre_array[pre_array.length - 1]

        if (!isMdArray(current) && !isChildMdArray(current) && pre.type == 'md') {
          // 如果当前是普通文本，合并到上一个 md 类型中
          pre.str = [pre.str, current].join('\n')
          pre.index = index
          return pre_array
        } else if (isChildMdArray(current) && pre.type === 'question' && pre.str) {
          // 如果是 strChild，且前一个是主问题，附加到其 strChild 中
          pre.strChild = current.replace(/^--\s+/, '')
          return pre_array
        } else {
          pre_array.push(currentObj)
        }
      } else {
        pre_array.push(currentObj)
      }
      return pre_array
    }, [])
    .sort((pre: any, next: any) => pre.index - next.index)
})
// const prologueList = computed(() => {
//   const temp = props.available
//     ? props.data?.prologue
//     : '抱歉，当前正在维护，无法提供服务，请稍后再试！'
//   const lines = temp?.split('\n')

//   return lines
//     .reduce((pre_array: Array<any>, current: string, index: number) => {
//       const currentObj = isMdArray(current)
//         ? {
//             type: 'question',
//             str: current.replace(/^-\s+/, ''),
//             index: index
//           }
//         : {
//             type: 'md',
//             str: current,
//             index: index
//           }
//       if (pre_array.length > 0) {
//         const pre = pre_array[pre_array.length - 1]
//         if (!isMdArray(current) && pre.type == 'md') {
//           pre.str = [pre.str, current].join('\n')
//           pre.index = index
//           return pre_array
//         } else {
//           pre_array.push(currentObj)
//         }
//       } else {
//         pre_array.push(currentObj)
//       }
//       return pre_array
//     }, [])
//     .sort((pre: any, next: any) => pre.index - next.index)
// })

watch(
  () => props.chatId,
  (val) => {
    if (val && val !== 'new') {
      chartOpenId.value = val
    } else {
      chartOpenId.value = ''
    }
  },
  { deep: true }
)

watch(
  () => props.data,
  () => {
    chartOpenId.value = ''
  },
  { deep: true }
)

watch(
  () => props.record,
  (value) => {
    // 回显历史数聊天内容
    chatList.value = value.map((item) => {
      // 提取思考内容
      const thinkMatch = item.answer_text.match(/<think>([\s\S]*?)<\/think>/)
      const think_text = thinkMatch ? thinkMatch[1].trim() : ''
      const answer_text = item.answer_text.replace(/<think>[\s\S]*?<\/think>/, '').trim()
      
      return {
        ...item,
        think_text, // 添加思考内容字段
        answer_text, // 清理后的回答内容
        isThinkExpanded: false // 添加展开/收起控制
      }
    })

    // chatList.value = value
  },
  {
    immediate: true
  }
)
const hasUploadAndNetwork = () => {
  if (route.name === 'smartQuery') {
    return false
  } else {
    return true
  }
}

//-----朗读功能----
const audioPlayer = ref()
const showPlayer = ref(false)
const isPlaying = ref(true)
const timer = ref()

function readAnswer(item: chatType) {
  const content = item.answer_text
  showPlayer.value = true
  isPlaying.value = false

  applicationApi
    .postWavVoice(content)
    .then((res: any) => {
      isPlaying.value = true

      // 创建Blob URL
      const audioBlob = new Blob([res], { type: 'audio/wav' })
      const audioUrl = window.URL.createObjectURL(audioBlob)
      // 获取audio元素并设置src
      audioPlayer.value.src = audioUrl
      audioPlayer.value.play()
    })
    .catch((err) => {
      isPlaying.value = false
    })
}
const handlePlay = () => {
  isPlaying.value = true
  // 如果音频播放，则清除定时器
  if (timer.value) {
    clearTimeout(timer.value)
    timer.value = null
  }
}
const handleAudioEnded = () => {
  // 清除之前的定时器
  if (timer.value) {
    clearTimeout(timer.value)
    timer.value = null
  }
  timer.value = setTimeout(() => {
    showPlayer.value = false
  }, 3000) // 播放完毕后等待3秒
}
const afterEnter = () => {
  // 动画进入完成后的回调
}

const afterLeave = () => {
  // 动画离开完成后的回调
  if (audioPlayer.value) {
    audioPlayer.value.src = '' // 重置音频源
    window.URL.revokeObjectURL(audioPlayer.value.src) // 释放URL对象
  }
}
//------- 朗读功能 end -----------
//------- 新增chatapp end -----------
const isNetwork = ref(false)
const clickNetworkSwt = () => {
  isNetwork.value = !isNetwork.value
}

const uploadImageList = ref<Array<any>>([])
const uploadDocumentList = ref<Array<any>>([])
const uploadVideoList = ref<Array<any>>([])
const uploadAudioList = ref<Array<any>>([])
// 上传的文件数（由于uploadfile是并发，无法串行，用此变量控制当文件都上传完毕后，即成功+失败=总数时，再进行文档阅读）
const uploadCount = ref(0)
// 上传成功的文件数
const uploadedSuccessCount = ref(0)
// 上传失败的文件数
const uploadedFaileCount = ref(0)
// 上传成功的文件ID集合，用于后续问答时，只回答ID集合内的文件
const uploadedFileIDList = ref<Array<any>>([])
const file_upload_setting = ref({
  image: true,
  document: true,
  audio: false,
  video: false,
  maxFiles: 50,
  fileLimit: 100
})
const fileLoading = ref(false)
const showDelete = ref('')
const imageExtensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp']
const documentExtensions = ['pdf', 'docx', 'txt', 'xls', 'xlsx', 'md', 'html', 'csv']
const videoExtensions = ['mp4', 'avi', 'mov', 'mkv', 'flv']
const audioExtensions = ['mp3']

const getAcceptList = () => {
  // const { image, document, audio, video } = props.applicationDetails.file_upload_setting

  const { image, document, audio, video } = file_upload_setting.value
  let accepts: any = []
  if (image) {
    accepts = [...imageExtensions]
  }
  if (document) {
    accepts = [...accepts, ...documentExtensions]
  }
  if (audio) {
    accepts = [...accepts, ...audioExtensions]
  }
  if (video) {
    accepts = [...accepts, ...videoExtensions]
  }
  if (accepts.length === 0) {
    // return '.请在文件上传配置中选择文件类型'
    return '上传的文件包含暂未支持的文件格式，请转换文件格式后重试。支持的文件格式：PDF、Word 文档（DOC、DOCX）、Excel 表格（XLSX）、PPT（PPT、PPTX）、图片、CSV、各类纯文本格式等。'
  }
  return accepts.map((ext: any) => '.' + ext).join(',')
}
const uploadFile = (file: any, fileList: any) => {
  // uploadFile是并行，多个文件会多次执行uploadFile，且无延时，因此先记录总共有几个文件上传
  uploadCount.value++
  // const { maxFiles, fileLimit } = props.applicationDetails.file_upload_setting
  const { maxFiles, fileLimit } = file_upload_setting.value
  // 单次上传文件数量限制
  const file_limit_once =
    uploadImageList.value.length +
    uploadDocumentList.value.length +
    uploadAudioList.value.length +
    uploadVideoList.value.length
  if (file_limit_once >= maxFiles) {
    MsgWarning('最多上传' + maxFiles + '个文件')
    fileList.splice(0, fileList.length)
    return
  }
  if (fileList.filter((f: any) => f.size > fileLimit * 1024 * 1024).length > 0) {
    // MB
    MsgWarning('单个文件大小不能超过' + fileLimit + 'MB')
    fileList.splice(0, fileList.length)
    return
  }

  const extension = file.name.split('.').pop().toLowerCase() // 获取文件后缀名并转为小写

  if (imageExtensions.includes(extension)) {
    uploadImageList.value.push(file)
  } else if (documentExtensions.includes(extension)) {
    uploadDocumentList.value.push(file)
  } else if (videoExtensions.includes(extension)) {
    uploadVideoList.value.push(file)
  } else if (audioExtensions.includes(extension)) {
    uploadAudioList.value.push(file)
  } else {
    // 不支持的文件类型
    MsgWarning(
      `上传的文件包含暂未支持的文件格式，请转换文件格式后重试。支持的文件格式：PDF、Word 文档（DOC、DOCX）、Excel 表格（XLSX）、PPT（PPT、PPTX）、图片、CSV、各类纯文本格式等。`
    )
    // fileList.splice(0, fileList.length) // 清空文件列表
    return
  }
  // 上传并解析文件内容
  submitFile(file)
}
const submitFile = async function (file: any) {
  const formData = new FormData()
  formData.append('file', file.raw, file.name)
  loading.value = true
  readPrologue.value = '正在上传文档，请稍后...'
  await documentApi
    .postReadDocument(formData)
    .then(async (res: any) => {
      // 解析成功，成功数+1
      uploadedSuccessCount.value++
      const fileId = res.data
      uploadedFileIDList.value.push({ id: fileId, name: file.name })
      // 成功+失败=总数，再提取问题
      if (uploadedSuccessCount.value + uploadedFaileCount.value != uploadCount.value) {
        readPrologue.value = '' + file.name + '上传完毕，请稍后...'
        return
      }
      readPrologue.value = uploadCount.value + '个文档上传完毕，正在阅读，请稍后...'
      // 都上传完成后，待上传和已上传文件数重置
      uploadCount.value = 0
      uploadedSuccessCount.value = 0
      let chatOpenRes = await applicationApi.getChatOpen(props.appId as string)
      let chatOpenId = chatOpenRes.data
      if (!chatOpenId) {
        loading.value = false
        throw new Error('获取对话ID失败，请重试')
      }
      let obj = {
        message:
          '请对“已知信息”的内容提出三个简短的问题，只提问，不做答，也不做总结。\n输出的格式要求：每个问题一行。',
        re_chat: false,
        stream: false,
        online_search: isNetwork.value,
        doc_content: uploadedFileIDList.value.map((item) => item.id).join(',')
      }
      let tempReadPrologue = '阅读文档完毕，请向我提问吧~~~///(^v^)\\\\~~~'
      // 对话
      await applicationApi.postChatMessageNoStream(chatOpenId, obj).then((response) => {
        let q = response.data?.content
        q = q.replaceAll('<no value>', '')
        try {
          const list = q.split('\n')
          if (list)
            for (const item of list) {
              if (item.trim().length > 0) {
                tempReadPrologue += '\n- ' + item.replace('\n', '')
              }
            }
        } catch (e) {
          readPrologue.value = '阅读有误，重新上传'
        }
      })
      readPrologue.value = tempReadPrologue
      loading.value = false
    })
    .catch(() => {
      // 解析失败，失败数+1
      readPrologue.value = file.name + '上传失败，请稍后...'
      uploadedFaileCount.value++
      loading.value = false
    })
}
const setUrl = (response: any, fileList: any) => {
  fileList.splice(0, fileList.length)

  const allFileLists = [
    uploadImageList.value,
    uploadDocumentList.value,
    uploadAudioList.value,
    uploadVideoList.value
  ]

  // 遍历所有文件列表，将文件的url设置为response.data中的url
  allFileLists.forEach((list) => {
    list.forEach((file: any) => {
      const match = response.data.find((f: any) => f.name === file.name)
      if (match) {
        file.url = match.url
        file.file_id = match.file_id
      }
    })
  })
}
const checkMaxFilesLimit = () => {
  return (
    file_upload_setting.value.maxFiles <=
    uploadImageList.value.length +
      uploadDocumentList.value.length +
      uploadAudioList.value.length +
      uploadVideoList.value.length
  )
}
function mouseenter(row: any) {

  showDelete.value = row.url
}
function mouseleave() {
  showDelete.value = ''
}
function deleteFile(index: number, file: any, val: string) {
  if (val === 'image') {
    uploadImageList.value.splice(index, 1)
  } else if (val === 'document') {
    uploadDocumentList.value.splice(index, 1)
  } else if (val === 'video') {
    uploadVideoList.value.splice(index, 1)
  } else if (val === 'audio') {
    uploadAudioList.value.splice(index, 1)
  }
  // 删除上传的文件ID，避免回答已删除的文件
  uploadedFileIDList.value = uploadedFileIDList.value.filter((item) => item.name !== file.name)
}
//------- 新增chatapp end -----------
const toggleThink = (item: any) => {
  item.isThinkExpanded = !item.isThinkExpanded
}
function showSource(row: any) {
  if (props.log) {
    return true
  } else if (row.write_ed && 500 !== row.status) {
    if (id || props.data?.show_source) {
      return true
    }
  } else {
    return false
  }
}

function quickProblemHandle(val: any) {
  if (!loading.value && props.data?.name) {
    handleDebounceClick(val.children || val.str)
  }
}

const handleDebounceClick = debounce((val) => {
  chatMessage(null, val)
}, 200)

function sendChatHandle(event: any) {
  if (!event.ctrlKey) {
    // 如果没有按下组合键ctrl，则会阻止默认事件
    event.preventDefault()
    if (!isDisabledChart.value && !loading.value && !event.isComposing) {
      if (inputValue.value.trim()) {
        chatMessage()
      }
    }
  } else {
    // 如果同时按下ctrl+回车键，则会换行
    inputValue.value += '\n'
  }
}
const stopChat = (chat: chatType) => {
  ChatManagement.stop(chat.id)
}
const startChat = (chat: chatType) => {
  ChatManagement.write(chat.id)
}
/**
 * 对话
 */
function getChartOpenId(chat?: any) {
  loading.value = true
  const obj = props.data
  if (props.appId) {
    return applicationApi
      .getChatOpen(props.appId)
      .then((res) => {
        chartOpenId.value = res.data
        chatMessage(chat)
      })
      .catch((res) => {
        if (res.response.status === 403) {
          application.asyncAppAuthentication(accessToken).then(() => {
            getChartOpenId(chat)
          })
        } else {
          loading.value = false
          return Promise.reject(res)
        }
      })
  } else {
    if (isWorkFlow(obj.type)) {
      const submitObj = {
        work_flow: obj.work_flow
      }
      return applicationApi
        .postWorkflowChatOpen(submitObj)
        .then((res) => {
          chartOpenId.value = res.data
          chatMessage(chat)
        })
        .catch((res) => {
          loading.value = false
          return Promise.reject(res)
        })
    } else {
      return applicationApi
        .postChatOpen(obj)
        .then((res) => {
          chartOpenId.value = res.data
          chatMessage(chat)
        })
        .catch((res) => {
          loading.value = false
          return Promise.reject(res)
        })
    }
  }
}
/**
 * 获取一个递归函数,处理流式数据
 * @param chat    每一条对话记录
 * @param reader  流数据
 * @param stream  是否是流式数据
 */
const getWrite = (chat: any, reader: any, stream: boolean) => {
  let tempResult = ''
  /**
   *
   * @param done  是否结束
   * @param value 值
   */
  const write_stream = ({ done, value }: { done: boolean; value: any }) => {
    try {
      if (done) {
        ChatManagement.close(chat.id)
        return
      }
      const decoder = new TextDecoder('utf-8')
      let str = decoder.decode(value, { stream: true })
      // 这里解释一下 start 因为数据流返回流并不是按照后端chunk返回 我们希望得到的chunk是data:{xxx}\n\n 但是它获取到的可能是 data:{ -> xxx}\n\n 总而言之就是 fetch不能保证每个chunk都说以data:开始 \n\n结束
      tempResult += str
      const split = tempResult.match(/data:.*}\n\n/g)
      if (split) {
        str = split.join('')
        tempResult = tempResult.replace(str, '')
      } else {
        return reader.read().then(write_stream)
      }
      // 这里解释一下 end
      if (str && str.startsWith('data:')) {
        if (split) {
          for (const index in split) {
            const chunk = JSON?.parse(split[index].replace('data:', ''))
            chat.chat_id = chunk.chat_id
            chat.record_id = chunk.id
            const content = chunk?.content
            if (content) {

              ChatManagement.append(chat.id, content)
            }
            if (chunk.is_end) {
              // 流处理成功 返回成功回调
              return Promise.resolve()
            }
          }
        }
      }
    } catch (e) {
      return Promise.reject(e)
    }
    return reader.read().then(write_stream)
  }
  /**
   * 处理 json 响应
   * @param param0
   */
  const write_json = ({ done, value }: { done: boolean; value: any }) => {
    if (done) {
      const result_block = JSON.parse(tempResult)
      if (result_block.code === 500) {
        return Promise.reject(result_block.message)
      } else {
        if (result_block.content) {
          ChatManagement.append(chat.id, result_block.content)
        }
      }
      ChatManagement.close(chat.id)
      return
    }
    if (value) {
      const decoder = new TextDecoder('utf-8')
      tempResult += decoder.decode(value)
    }
    return reader.read().then(write_json)
  }
  return stream ? write_stream : write_json
}
const errorWrite = (chat: any, message?: string) => {
  ChatManagement.addChatRecord(chat, 50, loading)
  ChatManagement.write(chat.id)
  ChatManagement.append(chat.id, message || '抱歉，当前正在维护，无法提供服务，请稍后再试！')
  ChatManagement.updateStatus(chat.id, 500)
  ChatManagement.close(chat.id)
}
function chatMessage(chat?: any, problem?: string, re_chat?: boolean) {
  loading.value = true

  if (!chat) {
    chat = reactive({
      id: randomId(),
      problem_text: problem ? problem : inputValue.value.trim(),
      answer_text: '',
      buffer: [],
      write_ed: false,
      is_stop: false,
      record_id: '',
      vote_status: '-1',
      status: undefined
    })

    chatList.value.push(chat)
    
    ChatManagement.addChatRecord(chat, 50, loading)
    ChatManagement.write(chat.id)
    inputValue.value = ''
    nextTick(() => {
      // 将滚动条滚动到最下面
      scrollDiv.value.setScrollTop(getMaxHeight())
    })
  }
  if (!chartOpenId.value) {
    getChartOpenId(chat).catch(() => {
      errorWrite(chat)
    })
  } else {
    const obj = {
      message: chat.problem_text,
      re_chat: re_chat || false,
      online_search: isNetwork.value,
      doc_content: uploadedFileIDList.value.map((item) => item.id).join(',')
    }
    // 对话
    applicationApi
      .postChatMessage(chartOpenId.value, obj)
      .then((response) => {
        if (response.status === 401) {
          application
            .asyncAppAuthentication(accessToken)
            .then(() => {
              chatMessage(chat, problem)
            })
            .catch(() => {
              errorWrite(chat)
            })
        } else if (response.status === 460) {
          return Promise.reject('无法识别用户身份')
        } else if (response.status === 461) {
          return Promise.reject('抱歉，您的提问已达到最大限制，请明天再来吧！')
        } else {
          nextTick(() => {
            // 将滚动条滚动到最下面
            scrollDiv.value.setScrollTop(getMaxHeight())
          })
          const reader = response.body.getReader()
          // 处理流数据
          const write = getWrite(
            chat,
            reader,
            response.headers.get('Content-Type') !== 'application/json'
          )
          return reader.read().then(write)
        }
      })
      .then(() => {
        if (props.chatId === 'new') {
          emit('refresh', chartOpenId.value)
        }
        quickInputRef.value.textareaStyle.height = '45px'
        return (id || props.data?.show_source) && getSourceDetail(chat)
      })
      .finally(() => {
        ChatManagement.close(chat.id)
      })
      .catch((e: any) => {
        errorWrite(chat, e + '')
      })
  }
}

function regenerationChart(item: chatType) {
  inputValue.value = item.problem_text
  if (!loading.value) {
    chatMessage(null, '', true)
  }
}
function getSourceDetail(row: any) {
  logApi.getRecordDetail(id || props.appId, row.chat_id, row.record_id, loading).then((res) => {
    const exclude_keys = ['answer_text', 'id']
    Object.keys(res.data).forEach((key) => {
      if (!exclude_keys.includes(key)) {
        row[key] = res.data[key]
      }
    })
    res.data.execution_details.forEach((item: any) => {
      if (item.step_type === 'web_search_step') {
        emit('webSearchList', item.webpage_list, isNetwork.value)
      }
    })
  })
  return true
}

/**
 * 滚动条距离最上面的高度
 */
const scrollTop = ref(0)

const scorll = ref(true)

const getMaxHeight = () => {
  return dialogScrollbar.value!.scrollHeight
}
const handleScrollTop = ($event: any) => {
  scrollTop.value = $event.scrollTop
  if (
    dialogScrollbar.value.scrollHeight - (scrollTop.value + scrollDiv.value.wrapRef.offsetHeight) <=
    30
  ) {
    scorll.value = true
  } else {
    scorll.value = false
  }
  emit('scroll', { ...$event, dialogScrollbar: dialogScrollbar.value, scrollDiv: scrollDiv.value })
}

const handleScroll = () => {
  if (!props.log && scrollDiv.value) {
    // 内部高度小于外部高度 就需要出滚动条
    if (scrollDiv.value.wrapRef.offsetHeight < dialogScrollbar.value.scrollHeight) {
      // 如果当前滚动条距离最下面的距离在 规定距离 滚动条就跟随
      if (scorll.value) {
        scrollDiv.value.setScrollTop(getMaxHeight())
      }
    }
  }
}

function setScrollBottom() {
  // 将滚动条滚动到最下面
  scrollDiv.value.setScrollTop(getMaxHeight())
}

watch(
  chatList,
  (value) => {
    handleScroll()
  },
  { deep: true, immediate: true }
)

onMounted(() => {
  // 从 localStorage 中读取数据(home页面input传来的chat问题)
  const savedMessage = localStorage.getItem('indexMessageContent')
  if (savedMessage) {
    inputValue.value = savedMessage
  }
  setTimeout(() => {
    if (quickInputRef.value) {
      if (savedMessage) {
        chatMessage()
        localStorage.removeItem('indexMessageContent')
      }
      quickInputRef.value.textarea.style.height = '0'
    }
  }, 1500)

  // -old
  // setTimeout(() => {
  //   if (quickInputRef.value) {
  //     quickInputRef.value.textarea.style.height = '0'
  //   }
  // }, 1500)
})

defineExpose({
  setScrollBottom,
  inputValue
})
</script>
<style lang="scss" scoped>
.think-section {
  margin-bottom: 16px;

  .think-button {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    background: #f5f5f5;
    width: fit-content;
    padding: 7px 14px;
    cursor: pointer;
    border-radius: 10px;
    &:hover {
      background: #ececec;
    }
    .think-icon {
      width: 14px;
      height: 14px;
    }
    .is-reverse {
      transform: rotate(180deg);
    }
  }

  .think-content {
    padding: 12px;
    margin-top: 8px;
    background: #f5f5f5;
    border-radius: 4px;
    position: relative;
    box-sizing: border-box;
    &::before {
      // 左边框加个线条
      content: '';
      position: absolute;
      top: 0;
      bottom: 0;
      left: 0px;
      width: 2px;
      background-color: #e4e4e4;
    }
    :deep(.maxkb-md) {
      background-color: #f5f5f5;
    }
  }
}
/* 定义淡入和淡出的动画关键帧 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeOut {
  from {
    opacity: 1;
    transform: translateY(0);
  }
  to {
    opacity: 0;
    transform: translateY(-20px);
  }
}

/* 应用动画到transition的类名 */
.fade-enter-active {
  animation: fadeIn 0.5s ease-out forwards;
}
.fade-leave-active {
  animation: fadeOut 0.5s ease-in forwards;
}
.ai-chat {
  --padding-left: 40px;
  height: 100%;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  position: relative;
  color: var(--app-text-color);
  box-sizing: border-box;

  &__content {
    padding-top: 0;
    box-sizing: border-box;

    .avatar {
      float: left;
      .avatar-gradient {
        background-color: transparent !important;
      }
    }
    .content {
      margin-top: 24px;
      position: relative;
      padding-left: var(--padding-left);
      :deep(ol) {
        margin-left: 16px !important;
      }

      .prologue-card {
        margin-top: 70px;

        .prologue-zhushou {
          position: absolute;
          top: 36px;
          right: 66px;
          width: 100px;
          height: 100px;
          background: url('@/assets/chatapp-page/zhushou.png') no-repeat;
          background-size: contain;
        }
        .card-title {
          font-size: 16px;
          font-weight: 400;
          position: relative;
          z-index: 1;
          &::after {
            content: '';
            position: absolute;
            top: 14px;
            left: 0px;
            width: 50px;
            height: 6px;
            z-index: -1;
            background-image: linear-gradient(
              to right,
              #cef2fe,
              #d8f4fe,
              #e1f7ff,
              #ebf9ff,
              #f4fcff
            );
          }
        }
      }
    }
    .text {
      padding: 6px 0;
      font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei',
        '微软雅黑', Arial, sans-serif;
      color: #3f4a54;
    }
    .problem-button {
      width: 100%;
      border: none;
      border-radius: 8px;
      background: var(--app-layout-bg-color);
      height: 70px;
      padding: 12px 12px;
      line-height: 46px;
      box-sizing: border-box;
      color: var(--el-text-color-regular);
      -webkit-line-clamp: 1;
      word-break: break-all;
      display: flex;
      align-items: center;
      .problem-button-icon {
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #fff;
        margin-right: 12px;
      }
      .problem-button-text {
        line-height: normal;
        font-size: 16px;
      }
      &:hover {
        background: var(--el-color-primary-light-9);
      }
      &.disabled {
        &:hover {
          background: var(--app-layout-bg-color);
        }
      }
      :deep(.el-icon) {
        color: var(--el-color-primary);
      }
    }
  }
  &__operate {
    user-select: none;
    // background: #f3f7f9;
    position: relative;
    width: 100%;
    margin: 0 auto;
    box-sizing: border-box;
    z-index: 10;
    // &::before {
    //   background: url('@/assets/chatapp-page/aijpg.jpg') no-repeat;
    //   background-size: cover;
    //   content: '';
    //   position: absolute;
    //   width: 700px;
    //   top: -400px;
    //   right: -40px;
    //   height: 800px;
    // }
    .operate-textarea {
      box-shadow: 0px 6px 24px 0px rgba(31, 35, 41, 0.08);
      background-color: #ffffff;
      border-radius: 8px;
      // border: 1px solid #ffffff;
      box-sizing: border-box;
      display: flex;
      flex-direction: column;
      // &:has(.el-textarea__inner:focus) {
      //   border: 1px solid var(--el-color-primary);
      // }

      :deep(.el-textarea__inner) {
        border-radius: 8px !important;
        box-shadow: none;
        resize: none;
        padding: 12px 16px;
        box-sizing: border-box;
      }
      .operate {
        padding: 6px 20px;
        display: flex;
        justify-content: space-between;
        .switch-container {
          user-select: none;
          display: flex;
          align-items: center; /* 垂直居中对齐 */
          :deep(.el-switch) {
            .el-switch__core {
              background-color: #fff;
              .el-switch__action {
                background-color: #848199; // 圆球颜色
              }
            }

            &.is-checked {
              .el-switch__core {
                .el-switch__action {
                  background-color: #329cff; // 打开状态圆球颜色
                }
                // background-color: #fff;
              }
            }
          }
          .switch-text {
            color: #999;
            cursor: pointer;
          }
        }
        .sent-button-container {
          .el-button.is-text {
            max-height: none !important;
          }
          .sent-button {
            max-height: none;
            width: 70px;
            margin-left: 8px;
            .el-icon {
              font-size: 24px;
            }
          }
        }

        :deep(.el-loading-spinner) {
          margin-top: -15px;
          .circular {
            width: 31px;
            height: 31px;
          }
        }
      }
    }
  }
  .dialog-card {
    border: none;
    border-radius: 8px;
  }
  .avatar-user {
    background-color: transparent !important;
  }
}
.chat-width {
  max-width: var(--app-chat-width, 860px);
  margin: 0 auto;
}
.cursor {
  cursor: pointer;
}
.file {
  position: relative;
  overflow: inherit;
  .delete-icon {
    position: absolute;
    right: 5px;
    top: 1px;
    z-index: 1;
  }
  .color-secondary {
    color: red;
  }
}
</style>
