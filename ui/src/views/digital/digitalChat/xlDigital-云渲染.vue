<template>
  <v-scale-screen ref="xlDigitalRef" width="1920" height="1080" :autoScale="true" :delay="100" >
    <!-- <div style="position: relative;"> -->
    <!-- <div v-if="showHuman" class="iframe-wrapper" :class='digitalBg'> -->
    <div v-show="showHuman" class="iframe-wrapper">
      <div style="width: 100%; height: 100%">
        <video
          v-show="isVideo"
          ref="videoDigital"
          style="width: 100%; height: 100%; position: absolute"
          :src="vidioBg"
        ></video>
        <div
          v-show="!isVideo"
          style="width: 100%; height: 100%; position: absolute"
          :class="digitalBg"
        ></div>
      </div>
      <iframe
        id="digital-human-iframe"
        :src="iframeSrc"
        allow="autoplay"
        style="position: absolute; bottom: 0px; right: 15%"
        :style="[iframeStyle, { transition: 'all 1.5s ease-in-out' }]"
      />
    </div>
    <div v-if="showTimeoutTip" class="tip2" @click="playWelcome">
      长时间无交互，数字人马上消失了，点我一下，进行交互
    </div>
    <!-- 控制按钮 -->
    <div
      class="button-wrapper flex-center flex-around"
      style="background: #fff; padding: 4px; border-radius: 10px"
    >
      <!-- <el-button size="small" @click="playWelcome">文本播报</el-button> -->
      <!-- <el-button size="small" @click="handleInterrupt">停止播报</el-button> -->
      <!-- <el-button size="small" @click="handleMountHuman">重载数字人</el-button> -->
      <div>
        <el-button style="margin-right: 4px" size="small" @click="playWelcome"
          >取消静音,播报开场白</el-button
        >

        <span style="font-size: 12px">切换人物：</span>
        <el-select
          v-model="selectedFigure"
          placeholder="Select"
          size="small"
          style="width: 120px"
          @change="handleFigureChange"
          :teleported="false"
        >
          <el-option
            v-for="item in figureOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </div>
      <div>
        <span style="font-size: 12px">切换背景：</span>
        <el-select
          v-model="selectedBackground"
          placeholder="Select"
          size="small"
          style="width: 120px"
          :teleported="false"
        >
          <el-option
            v-for="bg in backgroundOptions"
            :key="bg.value"
            :label="bg.label"
            :value="bg.value"
          />
        </el-select>
      </div>
      <el-button text @click="toggleFullScreen">
        <el-icon>
          <FullScreen v-if="!isFullscreen" />
          <Aim v-else />
        </el-icon>
        <span style="font-size: 12px">{{ isFullscreen ? '退出全屏' : '全屏' }}</span>
      </el-button>
    </div>
    <!-- 聊天框 -->
    <AiChatDigital
      v-if="isLoaded"
      style="position: absolute; bottom: 50px; left: 30px; opacity: 0.85"
      :data="applicationForm"
      :appId="applicationForm?.id"
      :xlchatObj="{ dhIframe, commandId }"
      @inputValue="handleInputValue"
    ></AiChatDigital>
    <!-- </div> -->
  </v-scale-screen>
</template>

<script setup lang="ts">
import type { ApplicationFormType } from '@/api/type/application'
import vidioBg from '@/assets/videoBg.mp4'
import AiChatDigital from '@/components/ai-chatDigital/index.vue'
import { t } from '@/locales'
import useStore from '@/stores'
import DHIframe from '@bddh/starling-dhiframe'
import { useFullscreen } from '@vueuse/core'
import CryptoJS from 'crypto-js'
import { v4 as uuidV4 } from 'uuid'
import VScaleScreen from 'v-scale-screen'
import { computed, nextTick, onMounted, ref, watch } from 'vue'
const dhIframe = new DHIframe('digital-human-iframe')
const showHuman = ref(true)
const videoIsMuted = ref(false)
const checkOver = ref(false)
const commandId = ref(uuidV4())
const iframeSrc = ref('')

const selectedFigure = ref('A2A_V2-fig-rarvdyye4q1ekuum')
const figureOptions = [
  {
    label: '思远(男)',
    value: 'A2A_V2-3to2_siyuan',
    ttsPer: '7011_vc0038_16k'
  },
  {
    label: '鑫睿(男)',
    value: 'A2A_V2-3to2_xinrui',
    ttsPer: '7011_vc0111_16k'
  },
  {
    label: '美涵-新春(女)',
    value: 'A2A_V2-fig-rasr44ur7bt7ise1',
    ttsPer: '7011_moxingkangxi_16k'
  },
  {
    label: '苏瑾-新春(女)',
    value: 'A2A_V2-fig-rarvdyye4q1ekuum',
    ttsPer: '7011_vc0019_16k'
  }
]
const backgroundOptions = [
  {
    label: '场景1',
    value: '1'
  },
  {
    label: '场景2',
    value: '2'
  },
  {
    label: '场景3',
    value: '3'
  }
]
const selectedBackground = ref(backgroundOptions[0].value)
const digitalBg = computed(() => ({
  digitalBg: true,
  'digitalBg-1': selectedBackground.value === '1',
  'digitalBg-2': selectedBackground.value === '2',
  'digitalBg-3': selectedBackground.value === '3'
}))
const xlDigitalRef = ref(null)

const handleFigureChange = (value: string) => {
  // 获取选中人物的ttsPer
  const selectedFigureTtsPer = figureOptions.find((item) => item.value === value)
  const ttsPer = selectedFigureTtsPer?.ttsPer ? `&ttsPer=${selectedFigureTtsPer.ttsPer}` : ''

  handleInterrupt()
  showHuman.value = false
  const token = getIframeToken()

  // 更新iframe src中的figureId参数
  iframeSrc.value = `https://open.xiling.baidu.com/cloud/realtime?token=${token}&initMode=noAudio&cameraId=0&figureId=${value}&resolutionWidth=1920&resolutionHeight=1080&cameraId=0&ttsPer=${ttsPer}&autoChromaKey=true&ttsSpeed=4`

  // 重新加载数字人
  nextTick(() => {
    showHuman.value = true
  })
}
// 获取token
function getIframeToken() {
  const appId = 'i-rc1puqfbkee2y'
  const appKey = 'tkaxgd7593bvb41g2hk7'
  const time = new Date(new Date().getTime() + 60 * 60 * 1000).toISOString()

  const algorithm = CryptoJS.algo.SHA256
  const hmac = CryptoJS.algo.HMAC.create(algorithm, appKey)
  hmac.update(appId + time)
  return `${appId}/${hmac.finalize().toString()}/${time}`
}
const config = ref(false)
const realTimeVideoReady = ref(false)
const wsConnected = ref(false)
const showTimeoutTip = ref(false)

const ReadyState = {
  UNINSTANTIATED: -1,
  CONNECTING: 0,
  OPEN: 1,
  CLOSING: 2,
  CLOSED: 3
}
// 消息处理
const onMessage = (msg: any) => {
  console.log('收到消息:', msg)
  if (msg.origin === 'https://open.xiling.baidu.com') {
    const { type, content } = msg.data
    console.log('消息类型:', type, '内容:', content)
    const { action, requestId } = content

    switch (type) {
      case 'rtcState':
        console.log('type1-rs', content.action)

        if (content.action === 'remoteVideoConnected') {
          realTimeVideoReady.value = true
        }
        if (content.action === 'localVideoMuted' && content.body) {
          videoIsMuted.value = true
        }
        break
      case 'wsState':
        console.log('type2-ws', content.readyState)

        if (content.readyState === ReadyState.OPEN) {
          wsConnected.value = true
        } else if (
          content.readyState === ReadyState.CLOSED ||
          content.readyState === ReadyState.CLOSING
        ) {
          wsConnected.value = false
        }
        break
      case 'msg':
      console.log('type3-msg', content.action)


        if (videoDigital.value && content.action === 'RENDER_START') {
          console.log('切换背景', config.value)

          if (config.value) {
            iframeStyle.value = {
              width: '400px',
              height: '400px',
              border: 'none'
            }

            isVideo.value = true
            videoDigital.value.muted = true
            videoDigital.value.play()
          }
          config.value = false
        }
        if (requestId === commandId.value &&  (content.action === 'FINISHED' || content.action === 'RENDER_END')) {
          console.info(`数字人驱动完成, 驱动id为${requestId}`)
          iframeStyle.value = {
            width: '800px',
            height: '800px',
            border: 'none'
          }
          isVideo.value = false
          videoDigital.value?.pause()
          const newCommandId = uuidV4()
          // 解开注释可以进行持续播报
          // commandId.value = newCommandId;
        } else if (action === 'DISCONNECT_ALERT') {
          showTimeoutTip.value = true
        }
        // else if (action === 'TIMEOUT_EXIT') {
        //     const iframeDom = document.getElementById('digital-human-iframe');
        //     iframeDom?.remove();
        // }
        break
      default:
        break
    }
  }
}

// 播放欢迎语
const playWelcome = () => {
  videoIsMuted.value = false
  dhIframe.sendCommand({
    subType: 'muteAudio',
    subContent: false
  })
  dhIframe.sendMessage({
    action: 'TEXT_RENDER',
    body: '你好,我是smart brain数字人助手',
    requestId: commandId.value
  })
}

// 打断播报
const handleInterrupt = () => {
  dhIframe.sendMessage({
    action: 'TEXT_RENDER',
    body: '<interrupt></interrupt>',
    requestId: commandId.value
  })
  // 清空音频队列
  dhIframe.sendCommand({
    subType: 'clearAudioQueue',
    subContent: true
  })

  // 重置命令ID
  commandId.value = uuidV4()
}

// 重载数字人
const handleMountHuman = () => {
  showHuman.value = true
}

// 聊天
const { application } = useStore()
const loading = ref(false)
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
const applicationId = ref('01eafd71-5ddb-11ef-871a-dc7196811e7d')
const isLoaded = ref(false)

function getDetail() {
  loading.value = true
  return application.asyncGetApplicationDetail(applicationId.value, loading).then((res: any) => {
    console.log(res,'res11')
    applicationForm.value = res.data
    applicationForm.value.model_id = res.data.model
    isLoaded.value = true
  }).finally(() => {
    loading.value = false
  })
}
// 全屏
const { isFullscreen, toggle } = useFullscreen(xlDigitalRef)
// 使用 toggle 方法切换全屏
const toggleFullScreen = () => {
  toggle()
}

// 切换背景(背景图片 -> 视频)
const isVideo = ref(false)
const videoDigital = ref<HTMLVideoElement | null>(null)
const currentInputValue = ref('')
function handleInputValue(inputValue: string) {
  // if (inputValue.includes('你') && inputValue.includes('好')) {
  //   currentInputValue.value = inputValue
  // }
  if (inputValue.includes('smart brain ai大模型') && inputValue.includes('介绍')) {
    config.value = true
  } else {
    config.value = false
  }
}
// 可以有声播放则返回true,否则返回false

// 检测浏览器是否允许自动播放非静音内容
async function checkPlayUnMute(): Promise<boolean> {
  if (
    typeof navigator.userActivation !== 'undefined' &&
    typeof navigator.userActivation.hasBeenActive !== 'undefined'
  ) {
    return navigator.userActivation.hasBeenActive
  }

  return new Promise((resolve) => {
    const audioElem = document.createElement('audio')
    audioElem.src =
      'data:audio/wav;base64,UklGRigAAABXQVZFZm10IBAAAAABAAEAESsAACJWAAACABAAZGF0YQAAAAA='
    audioElem.muted = false

    const playPromise = audioElem.play()

    if (playPromise !== undefined) {
      playPromise
        .then(() => {
          resolve(true)
        })
        .catch((error: Error) => {
          if (error.name === 'NotAllowedError' || error.name === 'AbortError') {
            resolve(false)
          } else {
            resolve(false)
          }
        })
      audioElem.remove()
    } else {
      audioElem.remove()
      resolve(false)
    }
  })
}

onMounted(async () => {
  getDetail()
  handleFigureChange(selectedFigure.value)
  // 检测自动播放能力
  const result = await checkPlayUnMute()
  videoIsMuted.value = !result
  checkOver.value = true
  // 初始化数字人
  dhIframe.registerMessageReceived(onMessage)
  return () => {
    dhIframe.removeMessageReceived(onMessage)
  }
})
watch(
  [realTimeVideoReady, wsConnected, checkOver, videoIsMuted],
  ([newRealTimeVideoReady, newWsConnected, newCheckOver, newVideoIsMuted]) => {
    if (newRealTimeVideoReady && newWsConnected && newCheckOver && !newVideoIsMuted) {
      dhIframe.sendMessage({
        action: 'TEXT_RENDER',
        body: '您好，我是smart brain数字人助手',
        requestId: commandId.value
      })
    }
  }
)
defineExpose({
  dhIframe
})
// iframeStyle 需要使用设计稿尺寸
let iframeStyle = ref({
  width: '800px',
  height: '800px',
  border: 'none'
})
</script>

<style scoped>
.iframe-wrapper {
  position: absolute;
  /* width: 100vw;
  height: 100vh; */
  width: 1920px;
  height: 1080px;
  top: 0;
  left: 0;
  overflow: hidden;
}

.button-wrapper {
  position: absolute;
  top: 10px;
  left: 10px;
  display: flex;
  gap: 10px;
}

.tip {
  position: absolute;
  left: 50%;
  top: 20%;
  transform: translateX(-50%);
  cursor: pointer;
}
.flex-center {
  display: flex;
  justify-content: center;
  align-items: center;
}
.flex-around {
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.digitalBg {
  background-size: cover;
}
.digitalBg-1 {
  background: url('@/assets/studio1.jpg') no-repeat;
  background-size: cover;
}
.digitalBg-2 {
  background: url('@/assets/studio2.jpg') no-repeat;
  background-size: cover;
}
.digitalBg-3 {
  background: url('@/assets/studio3.jpg') no-repeat;
  background-size: cover;
}
</style>
