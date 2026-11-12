<template>
  <v-scale-screen ref="xlDigitalRef" width="1920" height="1080" :autoScale="true" :delay="100">
    <!-- <div style="position: relative;"> -->
    <!-- <div v-if="showHuman" class="iframe-wrapper" :class='digitalBg'> -->
    <div v-show="showHuman" class="iframe-wrapper" id="iframe-wrapper">
      <div style="width: 100%; height: 100%">
        <video
          v-show="isVideo"
          ref="videoDigitalRef"
          style="width: 100%; height: 100%; position: absolute"
          :src="currentVideoSource"
          @ended="handleVideoEnded"
        ></video>
        <div
          v-show="!isVideo"
          style="width: 100%; height: 100%; position: absolute"
          :class="digitalBg"
        ></div>
      </div>
      <!-- <iframe
        id="digital-human-iframe"
        src="https://open.xiling.baidu.com/cloud/client/ar?platform=paas&licenseKey=XUNIREN-20250422_0249&licenseUrl=https://brain.jrsoft.com.cn/ui/xuniren-20250422_0249.license"
        allow="autoplay"
        style="position: absolute; bottom: 0px; right: 15%"
        :style="[
          {
            width: '800px',
            height: '800px',
            border: 'none'
          },
          { transition: 'all 1.5s ease-in-out' }
        ]"
      /> -->
    </div>

    <!-- 控制按钮 -->
    <div class="control-wrapper">
      <div class="control-row">
        <div class="control-line">
          <div class="selet-item">
            <span style="font-size: 12px">人物：</span>
            <el-select
              v-model="activeFigure"
              placeholder="Select"
              size="small"
              style="width: 80px"
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
            <span style="font-size: 12px">服装：</span>
            <el-select
              v-model="activeAccessory"
              placeholder="Select"
              size="small"
              @change="handleAccessoryChange"
              :teleported="false"
              style="width: 80px"
            >
              <el-option
                v-for="item in accessoryOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>
          <div>
            <span style="font-size: 12px">背景：</span>
            <el-select
              v-model="selectedBackground"
              placeholder="Select"
              size="small"
              style="width: 80px"
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
          <el-button text @click="togglePointer">
            <el-icon>
              <Pointer />
            </el-icon>
            <span style="font-size: 12px">动作</span>
          </el-button>
          <el-button text @click="toggleFullScreen">
            <el-icon>
              <FullScreen v-if="!isFullscreen" />
              <Aim v-else />
            </el-icon>
            <span style="font-size: 12px">{{ isFullscreen ? '退出全屏' : '全屏' }}</span>
          </el-button>
        </div>
        <div class="control-btns">
          <!-- <el-button text @click="handleceshi">
            <el-icon>
              <Pointer />
            </el-icon>
            <span style="font-size: 12px">ceshi</span>
          </el-button> -->
        </div>
      </div>
      <!-- <div class="input-row">
        <el-input 
          type="textarea" 
          class="input-box" 
          :rows="2" 
          v-model="textarea"
          placeholder="请输入要驱动的文本"
        ></el-input>
        <el-button type="primary" @click="handleRender">驱动</el-button>
      </div>
      <div>
          <h4>切换相机位，参考人像包config.json文件，部分人像不支持如下机位</h4>
          <div style="display: flex; gap: 10px;">   <button type="button" @click="changeCamera('h_full_cam')" class="btn">全身</button>
          <button type="button" @click="changeCamera('h_half_cam')" class="btn">半身</button>
          <button type="button" @click="changeCamera('h_face_cam')" class="btn">人脸</button>
          <button type="button" @click="changeCamera('h_shoulder_cam')" class="btn">肩位</button></div>
      </div> -->
      <div
        class="pointer-wrap"
        v-if="animojis && animojis.length"
        :style="{ height: `${pointerDisplayFlag ? 275 : 0}px` }"
      >
        <button
          v-for="animoji in animojis"
          :key="animoji"
          type="button"
          @click="handleAddAnimoji(animoji)"
          style="margin-right: 10px"
        >
          {{ animoji }}
        </button>
      </div>
    </div>
    <!-- 聊天框 -->
    <AiChatDigitalLocal
      v-if="isLoaded"
      style="position: absolute; bottom: 50px; left: 30px; opacity: 0.85"
      :data="applicationForm"
      :appId="applicationForm?.id"
      :xlchatObj="{ dhIframe, commandId, iframeToken }"
      @inputValue="handleInputValue"
    ></AiChatDigitalLocal>

    <!-- </div> -->
  </v-scale-screen>
</template>

<script setup lang="ts">
import type { ApplicationFormType } from '@/api/type/application'
import vidioBg from '@/assets/videoBg.mp4'
import AiChatDigitalLocal from '@/components/ai-chatDigital-local/index.vue'
import { t } from '@/locales'
import useStore from '@/stores'
import { DHIframeV2 } from '@bddh/starling-dhiframe'
import { useFullscreen } from '@vueuse/core'
import CryptoJS from 'crypto-js'
import { v4 as uuidV4 } from 'uuid'
import VScaleScreen from 'v-scale-screen'
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
type AccessoryOption = {
  label: string
  value: string
  body?: string
  [key: string]: any // 允许有其他扩展字段
}

let dhIframe: any = undefined
const showHuman = ref(true)
const commandId = ref(uuidV4())
const iframeToken = ref('')
const modelUrl = ref('https://sdk-demo.bj.bcebos.com/Judy_h5_250212.zip')

const activeFigure = ref('coco')
const figureOptions = ref([
  // {
  //   label: 'judy',
  //   value: 'judy',
  //   url: 'https://meta-human-editor-prd.cdn.bcebos.com/open-api/Judy_h5_250212.zip',
  //   characterImage: 'AR_RENDER-JUDY',
  //   accessoryList: [
  //     {
  //       label: '雅黑职场套装',
  //       body: 'judy_02_body_out',
  //       value: '1'
  //     }
  //     // {
  //     //   label: '浅蓝结饰套裙',
  //     //   body: 'default',
  //     //   value: '0'
  //     // },
      
  //   ]
  // },
  {
    label: 'charis',
    value: 'charis',
    url: 'https://digital-human-js-cdn.cdn.bcebos.com/paas-demo/charis_h5-20250206.zip',
    characterImage: 'AR_RENDER-Male',
    ttsPer: '7011_vc0038_16k', // 音色
    accessoryList: [
      {
        label: '灰色职场套装',
        body: 'Charis_02_body_out',
        value: '0'
      }
    ]
  },
  {
    label: 'coco',
    value: 'coco',
    url: 'https://meta-human-editor-prd.cdn.bcebos.com/open-api/coco_h5_250305.zip',
    characterImage: 'AR_RENDER-COCO',
    ttsPer: '7011_moxingxiaoxiao_16k', // 音色
    accessoryList: [
      {
        label: '米白职场套装',
        value: '1',
        body: 'coco_02_body_out'
      },
      {
        label: '浅灰职场套装',
        value: '0',
        body: 'default'
      }
    ]
  }
])
const activeAccessory = ref('')

const accessoryOptions = ref<AccessoryOption[]>([])
const handleFigureChange = () => {
  let value = activeFigure.value
  let target = figureOptions.value.find((item: any) => item.value === value)
  if (!target) return
  localStorage.setItem('characterImage', target.characterImage)
  accessoryOptions.value = target.accessoryList
  let accessory = accessoryOptions.value[0]
  if (accessory) {
    activeAccessory.value = accessory.value
  }
  localStorage.setItem('characterImage', target.characterImage)
  modelUrl.value = target.url
  initDynamicIframe()
  handleInterrupt()
}
const handleAccessoryChange = (value: any) => {
  let target = accessoryOptions.value.find((item: any) => item.value === value)
  if (!target) return
  let extraKeys = ['label', 'value']
  let keys = Object.keys(target).filter((key) => !extraKeys.includes(key))
  let partsOptions = keys.map((key) => {
    return {
      type: key,
      id: target?.[key]
    }
  })
  dhIframe?.changeParts(partsOptions)
}
// 切换人物
// const selectedFigure = ref('A2A_V2-fig-rarvdyye4q1ekuum')
// const figureOptions = [
//   {
//     label: '思远(男)',
//     value: 'A2A_V2-3to2_siyuan',
//     ttsPer: '7011_vc0038_16k'
//   },
//   {
//     label: '鑫睿(男)',
//     value: 'A2A_V2-3to2_xinrui',
//     ttsPer: '7011_vc0111_16k'
//   },
//   {
//     label: '美涵-新春(女)',
//     value: 'A2A_V2-fig-rasr44ur7bt7ise1',
//     ttsPer: '7011_moxingkangxi_16k'
//   },
//   {
//     label: '苏瑾-新春(女)',
//     value: 'A2A_V2-fig-rarvdyye4q1ekuum',
//     ttsPer: '7011_vc0019_16k'
//   }
// ]
const backgroundOptions = [
  {
    label: '汇报厅',
    value: '1'
  },
  {
    label: '展示厅',
    value: '2'
  },
  {
    label: '导览厅',
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

const animojis = ref([])
const textarea = ref(null)

const handleRender = (welcome = '空文本测试') => {
  const text = textarea.value || welcome
    // 根据当前选中的人物获取对应的音色
    const currentFigure = figureOptions.value.find(item => item.value === activeFigure.value)
  const ttsPer = currentFigure?.ttsPer || '7011_moxingxiaoxiao_16k' // 默认音色
  
  dhIframe?.textRender?.(
    {
      token: getIframeToken(),
      text,
      tts: {
        per: ttsPer,
        spd: 5,
        pit: 5
      }
    }
    // ({ status, data }) => {}
  )
}
// 获取token
function getIframeToken() {
  const appId = 'i-rertk1rvqftq0'
  const appKey = 'jucsn7xwimgdua2kr3sn'
  const time = new Date(new Date().getTime() + 60 * 60 * 1000).toISOString()

  const algorithm = CryptoJS.algo.SHA256
  const hmac = CryptoJS.algo.HMAC.create(algorithm, appKey)
  hmac.update(appId + time)
  return `${appId}/${hmac.finalize().toString()}/${time}`
}
const config = ref(false)

const changeCamera = (cameraId: any) => {
  dhIframe.changeCamera(cameraId)
}
const handleAddAnimoji = (id: any) => {
  dhIframe.animojiRender(id)
}

// 打断播报
const handleInterrupt = () => {
  dhIframe?.sendMessage('INTERRUPT', {})
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
  return application
    .asyncGetApplicationDetail(applicationId.value, loading)
    .then((res: any) => {
      applicationForm.value = res.data
      applicationForm.value.model_id = res.data.model
      isLoaded.value = true
    })
    .finally(() => {
      loading.value = false
    })
}
// 全屏
const { isFullscreen, toggle } = useFullscreen(xlDigitalRef)
// 使用 toggle 方法切换全屏
const toggleFullScreen = () => {
  toggle()
}

// 根据聊天框关键字切换背景(背景图片 -> 视频)
const { digitalVideo } = useStore()
const isVideo = ref(false)
const videoDigitalRef = ref<HTMLVideoElement | null>(null)

// 计算当前要使用的视频源
const currentVideoSource = computed(() => {
  return digitalVideo.currentVideoSrc || vidioBg
})
// 处理视频播放结束事件
function handleVideoEnded() {
  console.log('视频播放结束')
  isVideo.value = false
  digitalVideo.stopVideo()
}

function handleInputValue(inputValue: string) {
  console.log('handleInputValue', inputValue)
  digitalVideo.checkInputTrigger(inputValue)
}

// 监听视频播放状态变化
watch(
  () => digitalVideo.isVideoPlaying,
  (newValue) => {
    console.log('视频播放状态变化:', newValue)
    isVideo.value = newValue

    if (newValue) {
      // 播放视频
      if (videoDigitalRef.value) {
        videoDigitalRef.value.src = currentVideoSource.value
        videoDigitalRef.value.play()
      }
    } else {
      // 停止视频
      if (videoDigitalRef.value) {
        videoDigitalRef.value.pause()
        videoDigitalRef.value.currentTime = 0
      }
    }
  }
)

const handleKeyDown = (event: KeyboardEvent) => {
  // 现代浏览器推荐使用 event.key 判断
  if (event.key === 'F11' || event.keyCode === 122) {
    // 122是F11的历史keyCode
    event.preventDefault()
    event.stopPropagation()

    // 如果需要替代全屏功能可以调用自定义逻辑
    toggleFullScreen() // 调用你的全屏切换方法
  }
}

const initDynamicIframe = () => {
  // 获取容器元素（注意原代码中使用的是 class 而非 id）
  const container = document.getElementById('iframe-wrapper') as HTMLDivElement
  if (!container) return
  const existingIframe = document.getElementById('digital-human-iframe')
  if (existingIframe) {
    // 销毁DHIframe实例
    dhIframe?.destroy()
    dhIframe?.removeMessageReceived()
    // 移除DOM元素
    existingIframe.remove()
  }

  // 创建iframe元素
  const iframe = document.createElement('iframe')
  iframe.id = 'digital-human-iframe'
  iframe.src =
    'https://open.xiling.baidu.com/cloud/client/ar?platform=paas&licenseKey=XUNIREN-20250519_0259&licenseUrl=https://brain.jrsoft.com.cn/ui/xuniren-20250519_0259.license'
    // 'https://open.xiling.baidu.com/cloud/client/ar?platform=paas&licenseKey=XUNIREN-20250519_0259&licenseUrl=http://localhost:5173/ui/xuniren-20250519_0259.license'
  iframe.allow = 'autoplay'

  // 设置样式（保持与原始样式一致）
  Object.assign(iframe.style, {
    position: 'absolute',
    bottom: '0px',
    right: '15%',
    width: '800px',
    height: '800px',
    border: 'none',
    transition: 'all 1.5s ease-in-out'
  })

  // 插入到容器中
  container.appendChild(iframe)

  // 重新初始化DHIframe（重要！）
  dhIframe = new DHIframeV2('digital-human-iframe')
  loadDhiframe() // 调用已有的初始化方法

  return iframe
}
const loadDhiframe = () => {
  dhIframe.registerMessageReceived((data: any) => {
    if (data.type === 'state') {
      if (data.content.status === 'INIT') {
        dhIframe.load({
          backgroundImageUrl: '',
          modelUrl: modelUrl.value,
          cameraId: 'h_half_cam'
        })
      }
      if (data.content.status === 'AVATAR_LOAD') {
        animojis.value = data.content?.message?.config?.animationList.map(
          (item: any) => item.animationName
        )
        handleAddAnimoji('Vis_Female_youshoubaibai')
        handleRender('您好，我是smart brain数字人，很高兴认识您')
        handleAccessoryChange(activeAccessory.value)
      }
      // if (data.content.status === 'USER_ACTIVE') {
      // }
      // if (data.content.status === 'AUTHENTICATION') {
      // }
      if (data.content.status === 'CLOSE') {
        showHuman.value = false
      }
    }
  })
}
onMounted(() => {
  iframeToken.value = getIframeToken()
  document.addEventListener('keydown', handleKeyDown)
  getDetail().then((res) => {
    handleFigureChange()
    showHuman.value = true
  })
  // loadDhiframe()
  // handleFigureChange(selectedFigure.value)
})
const handleceshi = () => {
  modelUrl.value = 'https://meta-human-editor-prd.cdn.bcebos.com/open-api/coco_h5_250305.zip'
  initDynamicIframe()
  // loadDhiframe()
}
const pointerDisplayFlag = ref(false)
const togglePointer = () => {
  pointerDisplayFlag.value = !pointerDisplayFlag.value
}
onBeforeUnmount(() => {
  dhIframe.removeMessageReceived()
  document.removeEventListener('keydown', handleKeyDown)
})
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

<style lang="scss" scoped>
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

.control-wrapper {
  position: absolute;
  top: 10px;
  left: 10px;
  // display: flex;
  // flex-direction: column;
  /* gap: 12px; */
  padding: 4px 12px;
  background: #fff;
  border-radius: 10px;
  width: 500px;
}

.control-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  .control-line {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
  }
  .control-btns {
    width: 100%;
    display: flex;
    justify-content: flex-end;
  }
}

.input-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  width: 100%;
}

.input-box {
  flex: 1;
  min-width: 100px;
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

/* 添加图片通用样式 */
.img-responsive {
  width: 100%;
  height: auto;
  object-fit: contain;
}

.img-fixed {
  width: 100px;
  height: 100px;
  object-fit: cover;
}

.img-icon {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

/* 可以根据需要添加更多尺寸 */
.img-sm {
  width: 32px;
  height: 32px;
}

.img-md {
  width: 64px;
  height: 64px;
}

.img-lg {
  width: 128px;
  height: 128px;
}
.pointer-wrap {
  display: flex;
  flex-wrap: wrap;
  /* height: 0; */
  transition: height 0.5s;
  overflow: hidden;
  background-color: #fff;
  button {
    margin-bottom: 4px;
    padding: 1px;
    margin-right: 4px;
  }
}
</style>
