<template>
  <div class="audio-recorder" :class="{ 'is-recording': isRecording }">
    <!-- 开始录音按钮 -->
    <el-tooltip
      v-if="!isRecording"
      :content="isAnswerComplete ? '开始录音' : 'AI正在回答中...'"
      placement="bottom"
      effect="dark"
      :show-after="500"
    >
      <el-button 
        :loading="isInitializing" 
        @click="startRecord" 
        style="height: 45px; width: 45px"
        :disabled="!isAnswerComplete"
      >
        <AppIcon v-if="!isInitializing" iconName="Microphone" size="22px"></AppIcon>
      </el-button>
    </el-tooltip>

    <!-- 录音中的布局 -->
    <div v-show="isRecording" class="recording-container">
      <el-tooltip content="停止录音" placement="bottom" effect="dark" :show-after="500">
        <el-button @click="stopRecord" style="height: 45px; width: 45px">
          <AppIcon iconName="Mute" style="color: red" size="22px"></AppIcon>
        </el-button>
      </el-tooltip>

      <!-- 波形显示容器 -->
      <div ref="waveContainer" class="wave-container"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { MicVAD, utils } from '@ricky0123/vad-web';
import { ElMessage } from 'element-plus';
import { defineProps, nextTick, onUnmounted, ref, watch } from 'vue';
import { WaveView } from './WaveView';

const ws = ref<WebSocket | null>(null)
const audioUrl = ref('')
const vad = ref<MicVAD | null>(null)
const waveContainer = ref<HTMLElement | null>(null)
const waveView = ref<WaveView | null>(null)
const isRecording = ref(false)
const isInitializing = ref(false)

// 定义接收的 props
const props = defineProps({
  chatMessage: {
    type: Function,
    required: true
  },
  isAnswerComplete: {
    type: Boolean,
    default: false
  }
})
const emit = defineEmits<{
  (e: 'recording-state-change', recording: boolean): void
}>()

// WebSocket连接初始化
const setupWebSocket = async () => {
  return new Promise<void>((resolve, reject) => {
    try {
      ws.value = new WebSocket('wss://brain.jrsoft.com.cn/ws/chat/')

      ws.value.onopen = () => {
        console.log('WebSocket已连接')
        resolve()
      }

      ws.value.onerror = (error) => {
        console.error('WebSocket连接失败:', error)
        stopRecord()
        ElMessage.warning('语音连接失败，请重试')
        reject(error)
      }

      ws.value.onclose = () => {
        console.log('WebSocket已断开')
        stopRecord()
        ElMessage.warning('语音连接已断开，请重试')
      }

      ws.value.onmessage = (event) => {
        try {
          const response = JSON.parse(event.data)
          console.log(response, 'response')
          if (response.type === 'recognition') {
            handleRecognitionResult(response.text)
          }
        } catch (e) {
          console.log('收到文本消息:', event.data)
          handleRecognitionResult(event.data)
        }
      }
    } catch (error) {
      reject(error)
    }
  })
}

// 监听 AI 回答状态
watch(
  () => props.isAnswerComplete,
  (newVal) => {
    console.log(newVal, 'newVal')

    if (newVal && vad.value) {
      vad.value.start()
    }
  }
)

const handleRecognitionResult = (text: string) => {
  props.chatMessage(null, text)
  vad.value?.pause()
  // 重置波形图到静默状态
  // if (waveView.value) {
  //   // 发送一个空的或者很小的值来让波形图显示为静默状态
  //   waveView.value.input(new Float32Array(1024), 0, 16000)
  // }
  console.log(vad.value, '语音识别结果:', text)
}

const startRecord = async () => {
  try {
    isInitializing.value = true

    // 如果存在旧的 VAD 实例，先销毁它
    if (vad.value) {
      await vad.value.destroy()
      vad.value = null
    }

    // 清理之前的状态
    // if (audioUrl.value) {
    //   URL.revokeObjectURL(audioUrl.value)
    //   audioUrl.value = ''
    // }

    if (waveView.value) {
      waveView.value.destroy()
      waveView.value = null
      if (waveContainer.value) {
        waveContainer.value.innerHTML = ''
      }
    }

    // 初始化 WebSocket 和 VAD
    await setupWebSocket()
    await initVAD()

    isRecording.value = true
    emit('recording-state-change', true)

    // 使用 nextTick 确保 DOM 更新后再初始化波形显示
    await nextTick()
    if (waveContainer.value && !waveView.value) {
      waveView.value = new WaveView({
        elem: waveContainer.value,
        width: waveContainer.value.offsetWidth,
        height: 46,
        scale: 2,
        speed: 9,
        phase: 21.8,
        fps: 20,
        keep: false,
        lineWidth: 3,
        linear1: [0, 'rgba(150,96,238,1)', 0.2, 'rgba(170,79,249,1)', 1, 'rgba(53,199,253,1)'],
        linear2: [0, 'rgba(209,130,255,0.6)', 1, 'rgba(53,199,255,0.6)'],
        linearBg: [0, 'rgba(255,255,255,0.2)', 1, 'rgba(54,197,252,0.2)']
      })
    }
  } catch (error) {
    console.error('初始化失败:', error)
    ElMessage.error('初始化失败，请重试')
  } finally {
    isInitializing.value = false
  }
}

const stopRecord = async () => {
  if (vad.value) {
    await vad.value.pause()
    // 销毁当前的 VAD 实例
    await vad.value.destroy()
    vad.value = null
    console.log('停止录音')

    // 清理波形显示
    if (waveView.value) {
      waveView.value.destroy()
      waveView.value = null
      if (waveContainer.value) {
        waveContainer.value.innerHTML = ''
      }
    }

    isRecording.value = false
    emit('recording-state-change', false)
  }
}

const initVAD = async () => {
  try {
    vad.value = await MicVAD.new({
      additionalAudioConstraints: {
        sampleRate: 16000
      },
      // 配置本地文件路径
      baseAssetPath: '/vad/',
      onnxWASMBasePath: '/vad/',
      onSpeechStart: () => {
        console.log('检测到说话')
      },
      onFrameProcessed: (probabilities, frame) => {
        if (waveView.value) {
          let sum = 0
          for (let i = 0; i < frame.length; i++) {
            sum += Math.abs(frame[i])
          }
          const powerLevel = Math.min(100, Math.max(0, Math.sqrt(sum / frame.length) * 100))
          waveView.value.input(frame, powerLevel, 16000)
        }
      },
      onSpeechEnd: (audio) => {
        console.log('📢 用户停止讲话，开始处理音频...')

        const wavBuffer = utils.encodeWAV(audio)

        const wavBlob = new Blob([wavBuffer], { type: 'audio/wav' })
        // 上传音频文件（本地预览）
        // const base64 = utils.arrayBufferToBase64(wavBuffer);
        // audioUrl.value = `data:audio/wav;base64,${base64}`;
        // if (audioUrl.value) {
        //   URL.revokeObjectURL(audioUrl.value);
        // }

        // audioUrl.value = URL.createObjectURL(wavBlob);
        // console.log("🎧 录音文件已保存");

        if (ws.value && ws.value.readyState === WebSocket.OPEN) {
          ws.value.send(wavBlob)
          console.log('🎧 录音文件已通过WebSocket上传')
        }
      },
      onVADMisfire: () => {
        console.log('VAD误触发')
        // stopRecord();
      }
    })

    await vad.value.start()
  } catch (e) {
    console.error('VAD初始化失败:', e)
    throw e
  }
}

// 组件卸载时清理资源
onUnmounted(() => {
  if (vad.value) {
    vad.value.destroy()
  }
  // if (audioUrl.value) {
  //   URL.revokeObjectURL(audioUrl.value);
  // }
  if (ws.value) {
    ws.value.close()
  }
  if (waveView.value) {
    waveView.value.destroy()
  }
})
</script>

<style scoped lang="scss">
.audio-recorder {
  display: flex;
  width: auto; // 默认宽度自适应

  &.is-recording {
    width: 100%; // 录音状态时占满宽度
  }
}

.recording-container {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;

  .wave-container {
    flex: 1;
    height: 46px;
    background-color: #f5f5f5;
    border-radius: 4px;
  }
}
</style>
