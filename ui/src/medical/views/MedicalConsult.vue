<template>
  <div class="medical-consult">
    <!-- 头部 -->
    <div class="header">
      <div class="header-left">
        <button class="btn-back" @click="goBack" title="返回">
          <span class="back-arrow">←</span>
        </button>
        <h1>知贝</h1>
      </div>
      <div class="header-right">
        <button class="btn-voice-reading" :class="{ active: voiceReadingActive }" @click="toggleVoiceReading" title="语音阅读">
          <img src="/medical/img/语音阅读.png" alt="语音阅读" />
        </button>
        <button class="btn-archive" @click="openArchive"><img src="/medical/img/pic1.png" alt="" />我的档案</button>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="main-content" ref="mainContentRef">
      <!-- 对话区域 -->
      <div class="chat-area" ref="chatAreaRef">
        <!-- 医生头像 -->
        <div class="doctor-avatar">
          <img src="/medical/img/person.png" alt="AI医生">
        </div>

        <!-- AI诊室卡片 -->
        <div class="ai-clinic-card">
          <div class="card-header">
            <div class="card-title">AI诊室</div>
            <div class="status-tag">问诊中</div>
          </div>
          <div class="card-content">
            <div class="steps">01.选咨询人 >> 02.描述症状 >> 03.诊疗建议</div>
            <div class="divider"></div>
            <p>你好~我是你的AI医生，我将通过深度问诊了解你的健康状况，并提供明确的诊疗意见。</p>
          </div>
        </div>

        <!-- 咨询人卡片 -->
        <div class="consultant-card">
          <div class="consultant-name">本次咨询人 (刘**)</div>
          <div class="consultant-desc">好的，现在请描述病情，你输入的信息越详细，我的回答越精准。</div>
          <div class="divider"></div>
          <div class="upload-area">
            <span><img src="/medical/img/pic9.png" alt="" />如有相关报告，可点击上传</span>
            <button class="upload-btn">上传</button>
          </div>
        </div>

        <div v-for="(message, index) in messages" :key="index" :class="['message', message.role]">
          <!-- 助手头像 -->
          <div v-if="message.role === 'assistant'" class="message-avatar">
            <img src="/medical/img/img4.png" alt="AI医生" />
          </div>
          
          <div class="message-content">
            <!-- 助手消息 -->
            <div v-if="message.role === 'assistant'" class="assistant-message">
              <!-- 分割实际回复、网页地址和思考过程 -->
              <!-- 实际回复 -->
              <div class="actual-response" v-html="getActualContent(displayMessages[index] || message.content)"></div>

              <!-- 参考知识库来源 -->
              <div v-if="message.sources && message.sources.length" class="sources-box">
                <div class="sources-title">参考知识库条目</div>
                <div class="sources-list">
                  <span v-for="(src, si) in message.sources" :key="si" class="source-chip">
                    {{ src.name }}
                    <em>{{ src.kb }} · {{ Number(src.score).toFixed(3) }}</em>
                  </span>
                </div>
              </div>
              
              <!-- 网页地址折叠栏 -->
              <div v-if="displayMessages[index] && message.content.includes('<urls>')" class="urls-section">
                <div class="urls-header" @click="toggleUrls(index)">
                  <span class="urls-icon">{{ message.urlsExpanded ? '▼' : '▶' }}</span>
                  <span class="urls-label">参考网页地址</span>
                </div>
                <div v-if="message.urlsExpanded" class="urls-content" v-html="getUrlsContent(message.content)"></div>
              </div>
              
              <!-- 思考过程 -->
              <div v-if="displayMessages[index] && message.content.includes('<think>')" class="thought-section">
                <div class="thought-header" @click="toggleThought(index)">
                  <span class="thought-icon">{{ message.thoughtExpanded ? '▼' : '▶' }}</span>
                  <span class="thought-label">思考过程</span>
                </div>
                <div v-if="message.thoughtExpanded" class="thought-content" v-html="getThinkContent(message.content)"></div>
              </div>
            </div>
            <!-- 用户消息 -->
            <template v-else>
              {{ message.content }}
            </template>
          </div>
          
          <!-- 用户头像 -->
          <div v-if="message.role === 'user'" class="message-avatar">
            <img src="/medical/img/img5.png" alt="用户" />
          </div>
        </div>
        <div v-if="loading" class="loading">
          <div class="loading-avatar">
            <img src="/medical/img/img4.png" alt="AI医生" />
          </div>
          <span>AI 正在思考...</span>
        </div>
        
        <!-- 引导问题区域 -->
        <div class="guide-questions" v-if="showGuideQuestions">
          <div class="questions-container">
            <div v-for="(question, index) in guideQuestions" :key="index" class="guide-question-wrapper">
              <div class="guide-question" @click="selectGuideQuestion(question)">
                <span class="question-text">{{ question }}</span>
              </div>
              <button v-if="index === guideQuestions.length - 1" class="refresh-btn" @click.stop="refreshGuideQuestions">
                <img src="/medical/img/refresh.png" alt="刷新" />
              </button>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- 功能按钮区 -->
    <div class="func-buttons">
      <button class="func-btn" @click="navigateTo('reportAnalysis')">
        <img src="/medical/img/pic2.png" alt="" />
        报告分析
      </button>
      <button class="func-btn" @click="navigateTo('medicineAnalysis')">
        <img src="/medical/img/pic3.png" alt="" />
        药品分析
      </button>
      <button class="func-btn" @click="navigateTo('medicalService')">
        <img src="/medical/img/pic4.png" alt="" />
        就医助手
      </button>
      <button class="func-btn" @click="openDoctorConsult">
        <img src="/medical/img/pic5.png" alt="" />
        真人医生
      </button>
      <button class="func-btn" @click="openMedicalHistory">
        <img src="/medical/img/pic6.png" alt="" />
        就医史
      </button>
    </div>

    <!-- 底部输入区 -->
    <div class="input-bar">
      <div class="input-area">
        <!-- 输入框 -->
        <textarea class="input-field" v-model="inputValue" placeholder="请输入您要咨询的问题" @keyup.enter="sendMessage"></textarea>
        
        <!-- 按钮区域 -->
        <div class="button-row">
          <div class="button-row-left">
            <button class="action-btn smart-search" :class="{ active: smartSearchActive }" @click="toggleSmartSearch">
              <img src="/medical/img/搜索.png" alt="智能搜索" />
              <span>智能搜索</span>
            </button>
            <button class="action-btn deep-think" :class="{ active: deepThinkActive }" @click="toggleDeepThink">
              <img src="/medical/img/思考.png" alt="深度思考" />
              <span>深度思考</span>
            </button>
          </div>
          <div class="button-row-right">
            <button class="voice-btn" :class="{ active: voiceInputActive }" @click="toggleVoiceInput" title="语音输入">
              <img src="/medical/img/pic7.png" alt="语音" />
            </button>
            <button class="plus-btn" @click="toggleUploadMenu" title="上传">
              <span>{{ uploadMenuVisible ? '✕' : '+' }}</span>
            </button>
            <button class="send-btn" @click="sendMessage" :disabled="loading">
              {{ loading ? '发送中…' : '发送' }}
            </button>
          </div>
          
          <div v-if="uploadMenuVisible" class="upload-options">
            <div class="upload-option" @click="selectImage">
              <img src="/medical/img/pic8.png" alt="上传图片" />
              <span>上传图片</span>
            </div>
            <div class="upload-option" @click="selectFile">
              <span>📄</span>
              <span>上传文件</span>
            </div>
          </div>
        </div>
        <input type="file" ref="imageInput" accept="image/*" @change="uploadImage" style="display: none;" />
        <input type="file" ref="fileInput" @change="uploadFile" style="display: none;" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import medicalApi from '../api/medical'

// 为window对象添加语音识别相关的类型声明
declare global {
  interface Window {
    SpeechRecognition?: any
    webkitSpeechRecognition?: any
  }
}

const router = useRouter()
const chatAreaRef = ref<HTMLElement>()
const mainContentRef = ref<HTMLElement>()
const messages = ref<Array<{ role: string; content: string; thoughtExpanded?: boolean; urlsExpanded?: boolean }>>([])
const displayMessages = ref<Array<string>>([])
const inputValue = ref('')
const loading = ref(false)
const typing = ref(false)
let typingTimeout: number | null = null

// 上传相关
const uploadMenuVisible = ref(false)
const imageInput = ref<HTMLInputElement>()
const fileInput = ref<HTMLInputElement>()

// 智能搜索和深度思考方法
const smartSearchActive = ref(false)
const deepThinkActive = ref(false)

// 语音输入相关
const voiceInputActive = ref(false)

// 语音阅读相关
const voiceReadingActive = ref(false)
let speechSynthesisUtterance: SpeechSynthesisUtterance | null = null

// 上传文件信息
const uploadedFiles = ref<Array<{ type: string; url: string; name: string }>>([])

// 上传相关方法
const toggleUploadMenu = () => {
  uploadMenuVisible.value = !uploadMenuVisible.value
}

const toggleSmartSearch = () => {
  smartSearchActive.value = !smartSearchActive.value
  console.log('智能搜索:', smartSearchActive.value ? '已启动' : '已关闭')
  // TODO: 实现智能搜索功能
}

const toggleDeepThink = () => {
  deepThinkActive.value = !deepThinkActive.value
  console.log('深度思考:', deepThinkActive.value ? '已启动' : '已关闭')
  // TODO: 实现深度思考功能
}

// 语音输入相关
const toggleVoiceInput = () => {
  voiceInputActive.value = !voiceInputActive.value
  console.log('语音输入:', voiceInputActive.value ? '已启动' : '已关闭')
  
  if (voiceInputActive.value) {
    // 启动语音输入
    startVoiceRecognition()
  } else {
    // 停止语音输入
    stopVoiceRecognition()
  }
}

let recognition: any = null

const startVoiceRecognition = () => {
  // 检查浏览器是否支持语音识别
  if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition
    recognition = new SpeechRecognition()
    
    // 设置为中文
    recognition.lang = 'zh-CN'
    // 连续识别
    recognition.continuous = true
    
    // 开始识别
    recognition.start()
    
    // 识别结果回调
    recognition.onresult = (event: any) => {
      let transcript = ''
      for (let i = 0; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript
      }
      inputValue.value = transcript
    }
    
    // 错误回调
    recognition.onerror = (event: any) => {
      console.error('语音识别错误:', event.error)
      voiceInputActive.value = false
    }
    
    // 结束回调
    recognition.onend = () => {
      if (voiceInputActive.value) {
        // 如果还需要继续识别，重新启动
        recognition.start()
      }
    }
  } else {
    console.error('浏览器不支持语音识别')
    voiceInputActive.value = false
  }
}

const stopVoiceRecognition = () => {
  if (recognition) {
    recognition.stop()
    recognition = null
  }
}

// 语音阅读相关方法
const toggleVoiceReading = () => {
  voiceReadingActive.value = !voiceReadingActive.value
  console.log('语音阅读:', voiceReadingActive.value ? '已启动' : '已关闭')
  
  if (!voiceReadingActive.value) {
    // 停止当前正在播放的语音
    window.speechSynthesis.cancel()
  }
}

const speakText = (text: string) => {
  if (!voiceReadingActive.value) return
  
  // 停止当前正在播放的语音
  window.speechSynthesis.cancel()
  
  // 创建新的语音合成实例
  speechSynthesisUtterance = new SpeechSynthesisUtterance(text)
  
  // 设置语音属性
  speechSynthesisUtterance.lang = 'zh-CN'
  speechSynthesisUtterance.rate = 1.0
  speechSynthesisUtterance.pitch = 1.0
  speechSynthesisUtterance.volume = 1.0
  
  // 开始播放语音
  window.speechSynthesis.speak(speechSynthesisUtterance)
}

// 把 messages 挂到 window 上，方便调试
;(window as any).debugMessages = messages

// 引导问题相关
const showGuideQuestions = ref(true)
const guideQuestions = ref<string[]>([])

// 热门医疗问题列表
const hotMedicalQuestions = [
  '孩子发烧了怎么办？',
  '感冒了应该吃什么药？',
  '如何缓解头痛？',
  '腹泻应该注意什么？',
  '过敏性鼻炎怎么治疗？',
  '如何改善失眠？',
  '血压高怎么办？',
  '如何预防感冒？',
  '皮肤过敏怎么处理？',
  '胃痛怎么办？',
  '如何缓解疲劳？',
  '眼睛干涩怎么缓解？'
]

// 随机选择3个问题
const generateGuideQuestions = () => {
  // 打乱数组
  const shuffled = [...hotMedicalQuestions].sort(() => 0.5 - Math.random())
  // 取前3个
  guideQuestions.value = shuffled.slice(0, 3)
}

// 刷新引导问题
const refreshGuideQuestions = () => {
  generateGuideQuestions()
}

// 选择引导问题
const selectGuideQuestion = async (question: string) => {
  // 隐藏引导问题
  showGuideQuestions.value = false
  
  // 调用发送消息函数
  await sendMessageWithQuestion(question)
}

// 发送消息（带问题）
const sendMessageWithQuestion = async (content: string) => {
  // 添加用户消息
  messages.value = [...messages.value, { role: 'user', content }]
  scrollToBottom()
  
  loading.value = true
  try {
    console.log('✅ 发送消息:', content)
    console.log('✅ 智能搜索状态:', smartSearchActive.value, '深度思考状态:', deepThinkActive.value)
    
    // 只发送一次请求，后端会查询所有知识库并总结
    const response = await medicalApi.chat(content, smartSearchActive.value, deepThinkActive.value)
    console.log('✅ API 返回成功:', response)
    console.log('✅ response.data:', response.data)
    
    // 直接使用API返回的回复
    const finalResponse = response.data
    console.log('✅ 最终响应:', finalResponse)
    
    // 添加 AI 回复，默认折叠思考过程和网页地址
    const assistantMessage = {
      role: 'assistant' as const,
      content: finalResponse,
      sources: response.sources || [],
      thoughtExpanded: false,
      urlsExpanded: false
    }
    // 关键修复：用展开运算符创建新数组
    messages.value = [...messages.value, assistantMessage]
    // 同样用展开运算符更新 displayMessages，确保 Vue 能检测到变化
    // 初始化为空字符串，让打字效果从空白开始
    displayMessages.value = [...displayMessages.value, '']
    console.log('✅ 消息已推送到 messages，长度:', messages.value.length)
    
    // 关闭 loading 状态
    loading.value = false
    
    // 强制 Vue 更新 DOM
    await nextTick()
    
    // 实现打字效果
    await typeWriterEffect(messages.value.length - 1)
  } catch (error) {
    console.error('❌ 对话失败:', error)
    loading.value = false
  } finally {
    scrollToBottom()
  }
}

// 跳转到功能页面
const navigateTo = (pageName: string) => {
  router.push(`/chatapp/${pageName}`)
}

// 打开我的档案
const openArchive = () => {
  console.log('打开我的档案')
  // TODO: 实现我的档案功能
}

// 打开真人医生咨询
const openDoctorConsult = () => {
  console.log('打开真人医生咨询')
  // TODO: 实现真人医生咨询功能
}

// 打开就医史
const openMedicalHistory = () => {
  console.log('打开就医史')
  // TODO: 实现就医史功能
}

// 返回上一页
const goBack = () => {
  router.push('/chatapp/graphAssistant')
}

const sendMessage = async () => {
  const content = inputValue.value.trim()
  if (!content && uploadedFiles.value.length === 0) return
  if (loading.value) return
  // 上一条回复还在打字动画中时点发送，先终止动画再发新问题
  pauseTyping()
  
  // 隐藏引导问题
  showGuideQuestions.value = false
  
  // 构建消息内容
  let messageContent = content
  if (uploadedFiles.value.length > 0) {
    messageContent += '\n\n上传的文件：\n'
    uploadedFiles.value.forEach(file => {
      if (file.type === 'pdf') {
        messageContent += `- PDF文件: ${file.name} (${file.url}) [VL分析]\n`
      } else {
        messageContent += `- ${file.type === 'image' ? '图片' : '文件'}: ${file.name} (${file.url})\n`
      }
    })
  }
  
  // 添加用户消息
  messages.value.push({ role: 'user', content: messageContent })
  inputValue.value = ''
  uploadedFiles.value = []
  scrollToBottom()
  
  loading.value = true
  try {
    console.log('✅ 发送消息:', messageContent)
    console.log('✅ 智能搜索状态:', smartSearchActive.value, '深度思考状态:', deepThinkActive.value)
    
    // 只发送一次请求，后端会查询所有知识库并总结
    const response = await medicalApi.chat(messageContent, smartSearchActive.value, deepThinkActive.value)
    console.log('✅ API 返回成功:', response)
    console.log('✅ response.data:', response.data)
    
    // 直接使用API返回的回复
    const finalResponse = response.data
    console.log('✅ 最终响应:', finalResponse)
    
    // 这里直接显示，不用打字效果
    const assistantMessage = {
      role: 'assistant' as const,
      content: finalResponse,
      thoughtExpanded: false,
      urlsExpanded: false
    }
    messages.value = [...messages.value, assistantMessage]
    // 同样用展开运算符更新 displayMessages，确保 Vue 能检测到变化
    // 初始化为空字符串，让打字效果从空白开始
    displayMessages.value = [...displayMessages.value, '']
    console.log('✅ 消息已推送到 messages，长度:', messages.value.length)
    
    loading.value = false
    
    // 强制 Vue 更新 DOM
    await nextTick()
    
    // 实现打字效果
    await typeWriterEffect(messages.value.length - 1)
    
    scrollToBottom()
  } catch (error) {
    console.error('❌ 对话失败:', error)
    loading.value = false
  } finally {
    scrollToBottom()
  }
}

const typeWriterEffect = async (index: number) => {
  typing.value = true
  const message = messages.value[index]
  if (!message || message.role !== 'assistant') {
    typing.value = false
    return
  }
  
  // 实现打字效果
  const content = message.content
  // 提取实际内容（去掉 think 和 urls 标签）
  let actualContent = content
  const thinkStartIndex = actualContent.indexOf('<think>')
  const thinkEndIndex = actualContent.indexOf('</think>')
  if (thinkStartIndex > -1 && thinkEndIndex > thinkStartIndex) {
    actualContent = actualContent.substring(0, thinkStartIndex) + actualContent.substring(thinkEndIndex + 8)
  }
  if (actualContent.includes('<urls>')) {
    actualContent = actualContent.split('<urls>')[0]
  }
  actualContent = actualContent.trim()
  
  displayMessages.value[index] = ''
  
  // 边打字边朗读
  let currentText = ''
  for (let i = 0; i < actualContent.length; i++) {
    // 检查是否应该暂停
    if (!typing.value) break
    
    currentText = actualContent.substring(0, i + 1)
    displayMessages.value[index] = currentText
    
    // 每打一个句子就朗读一次，避免频繁触发语音合成
    if (i === actualContent.length - 1 || currentText.endsWith('。') || currentText.endsWith('！') || currentText.endsWith('？')) {
      speakText(currentText)
    }
    
    // 使用 Promise 实现延迟，以便可以中断
    await new Promise(resolve => {
      typingTimeout = window.setTimeout(resolve, 8)
    })
  }
  
  // 打字完成后，显示完整内容（包括标签）
  if (typing.value) {
    setTimeout(() => {
      displayMessages.value[index] = content
    }, 100)
  }
  
  typing.value = false
  scrollToBottom()
}

const toggleThought = (index: number) => {
  if (messages.value[index]) {
    messages.value[index].thoughtExpanded = !messages.value[index].thoughtExpanded
  }
}

const toggleUrls = (index: number) => {
  if (messages.value[index]) {
    messages.value[index].urlsExpanded = !messages.value[index].urlsExpanded
  }
}

const pauseTyping = () => {
  typing.value = false
  if (typingTimeout) {
    clearTimeout(typingTimeout)
    typingTimeout = null
  }
  // 停止语音朗读
  window.speechSynthesis.cancel()
}

const getActualContent = (content: string) => {
  console.log('原始内容:', content)
  let actualContent = content
  // 处理 tool_call 标签
  const toolCallStartIndex = actualContent.indexOf('<tool_call>')
  const toolCallEndIndex = actualContent.indexOf('</tool_call>')
  console.log('toolCallStartIndex:', toolCallStartIndex)
  console.log('toolCallEndIndex:', toolCallEndIndex)
  if (toolCallStartIndex > -1 && toolCallEndIndex > toolCallStartIndex) {
    // 如果内容以 <tool_call> 开头，返回 </tool_call> 之后的内容
    if (toolCallStartIndex === 0) {
      actualContent = actualContent.substring(toolCallEndIndex + 11)
      console.log('处理 tool_call 标签后:', actualContent)
    } else {
      // 否则返回 <tool_call> 之前的内容
      actualContent = actualContent.substring(0, toolCallStartIndex)
      console.log('处理 tool_call 标签后:', actualContent)
    }
  }
  // 处理 think 标签
  const thinkStartIndex = actualContent.indexOf('<think>')
  const thinkEndIndex = actualContent.indexOf('</think>')
  console.log('thinkStartIndex:', thinkStartIndex)
  console.log('thinkEndIndex:', thinkEndIndex)
  if (thinkStartIndex > -1 && thinkEndIndex > thinkStartIndex) {
    // 如果内容以 <think> 开头，返回 </think> 之后的内容
    if (thinkStartIndex === 0) {
      actualContent = actualContent.substring(thinkEndIndex + 8)
      console.log('处理 think 标签后:', actualContent)
    } else {
      // 否则返回 <think> 之前的内容
      actualContent = actualContent.substring(0, thinkStartIndex)
      console.log('处理 think 标签后:', actualContent)
    }
  }
  // 处理 urls 标签
  if (actualContent.includes('<urls>')) {
    actualContent = actualContent.split('<urls>')[0]
    console.log('处理 urls 标签后:', actualContent)
  }
  // 清理多余的空白和换行
  actualContent = actualContent.trim()
  // 把模型残留的 Markdown 标记转成 HTML，避免 #### 原样显示
  actualContent = actualContent
    .replace(/^\s*#{1,6}\s*(.+)$/gm, '<strong>$1</strong>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/^\s*[-*]\s+(.+)$/gm, '· $1')
  // 纯文本换行在 v-html 里会被压缩成空格，必须先转成 <br> 才能分段
  actualContent = actualContent
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/\r\n/g, '\n')
    .replace(/\n/g, '<br>')
  console.log('最终内容:', actualContent)
  console.log('getActualContent 返回长度:', actualContent.length)
  return actualContent || content
}

const getThinkContent = (content: string) => {
  // 尝试匹配标准格式
  let match = content.match(/<think>(.*?)<\/think>/s)
  if (match) {
    return match[1]
  }
  
  // 尝试匹配非标准格式，处理可能的格式问题
  match = content.match(/<\/think>(.*?)<\/think>/s)
  if (match) {
    return match[1]
  }
  
  return ''
}

const getUrlsContent = (content: string) => {
  const match = content.match(/<urls>(.*?)<\/urls>/s)
  return match ? match[1] : ''
}

const scrollToBottom = () => {
  nextTick(() => {
    // 这里应该用 mainContentRef，因为滚动区域是 main-content
    if (mainContentRef.value) {
      mainContentRef.value.scrollTop = mainContentRef.value.scrollHeight
    }
  })
}

onMounted(() => {
  console.log('mainContentRef:', mainContentRef.value) // 应该能看到 DOM 元素
  console.log('chatAreaRef:', chatAreaRef.value)       // 应该能看到 DOM 元素
  
  // 生成引导问题
  generateGuideQuestions()
  
  // 初始欢迎消息
  const welcomeMessage = {
    role: 'assistant' as const,
    content: '您好，我是知贝医疗助手，有什么可以帮助您的吗？',
    thoughtExpanded: false
  }
  messages.value.push(welcomeMessage)
  displayMessages.value.push(welcomeMessage.content)
  scrollToBottom()
})

const selectImage = () => {
  imageInput.value?.click()
  uploadMenuVisible.value = false
}

const selectFile = () => {
  fileInput.value?.click()
  uploadMenuVisible.value = false
}

const uploadImage = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  // 显示上传中状态
  messages.value.push({ role: 'user', content: '正在上传图片...' })
  scrollToBottom()

  try {
    // 创建FormData对象
    const formData = new FormData()
    formData.append('image', file)

    // 调用上传API
    const response = await fetch('/api/medical/upload/image/', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      throw new Error('上传失败')
    }

    const result = await response.json()
    const imageUrl = result.data

    // 存储上传的图片信息
    uploadedFiles.value.push({ type: 'image', url: imageUrl, name: file.name })

    // 显示上传成功的消息
    messages.value.push({ role: 'user', content: `上传图片: ${file.name}` })
    scrollToBottom()

    // 提示用户输入文字介绍
    messages.value.push({ role: 'assistant', content: '请输入图片的文字介绍，然后点击发送按钮' })
    scrollToBottom()
  } catch (error) {
    console.error('上传失败:', error)
    messages.value.push({ role: 'user', content: '图片上传失败，请重试' })
    scrollToBottom()
  } finally {
    // 清空input
    target.value = ''
  }
}

const uploadFile = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  // 检查文件类型
  const isPDF = file.type === 'application/pdf'

  // 显示上传中状态
  messages.value.push({ role: 'user', content: `正在上传${isPDF ? 'PDF文件' : '文件'}: ${file.name}` })
  scrollToBottom()

  try {
    // 创建FormData对象
    const formData = new FormData()
    formData.append('file', file)
    // 添加文件类型信息
    formData.append('fileType', isPDF ? 'pdf' : 'other')

    // 调用上传API
    const response = await fetch('/api/medical/upload/file/', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      throw new Error('上传失败')
    }

    const result = await response.json()
    const fileUrl = result.data

    // 存储上传的文件信息
    uploadedFiles.value.push({ 
      type: isPDF ? 'pdf' : 'file', 
      url: fileUrl, 
      name: file.name 
    })

    // 显示上传成功的消息
    messages.value.push({ role: 'user', content: `上传${isPDF ? 'PDF文件' : '文件'}: ${file.name}` })
    scrollToBottom()

    // 提示用户输入文字介绍
    if (isPDF) {
      messages.value.push({ role: 'assistant', content: 'PDF文件已上传，VL模型将自动分析文件内容。请输入您的问题，然后点击发送按钮' })
    } else {
      messages.value.push({ role: 'assistant', content: '请输入文件的文字介绍，然后点击发送按钮' })
    }
    scrollToBottom()
  } catch (error) {
    console.error('上传失败:', error)
    messages.value.push({ role: 'user', content: '文件上传失败，请重试' })
    scrollToBottom()
  } finally {
    // 清空input
    target.value = ''
  }
}

onUnmounted(() => {
  // 离开页面时重置对话历史
  medicalApi.resetHistory().catch(error => {
    console.error('重置对话历史失败:', error)
  })
})
</script>

<style lang="scss">
.medical-consult {
  min-height: 100%;
  background: linear-gradient(180deg, #f0f4ff 0%, #e8e8ff 100%);
  color: #333;
  height: 100%;
  position: relative;
  display: flex;
  flex-direction: column;

  /* 通用图标样式 - 解决垂直居中核心 */
  button img {
    vertical-align: middle; /* 图标与文字垂直居中 */
    display: inline-block;
    margin-right: 4px; /* 图标和文字之间留一点间距 */
    width: 16px; /* 统一图标大小，可根据实际需求调整 */
    height: 16px;
  }

  /* 纯图标按钮（无文字）特殊处理 */
  .voice-btn img,
  .camera-btn img {
    margin-right: 0; /* 纯图标按钮去掉右边距 */
    width: 20px; /* 底部语音/相机图标稍大一点 */
    height: 20px;
  }

  /* 头部 */
    .header {
        display: flex;
        align-items: center;
        padding: 8px 16px;
        background: linear-gradient(180deg, #f0f4ff 0%, #e8e8ff 100%);
        z-index: 100;

        .header-left {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .header-right {
            margin-left: auto;
        }

        h1 {
            margin: 0;
            font-size: 20px;
            font-weight: 600;
            color: #333;
        }

        .header-right {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .btn-voice-reading {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: #fff;
            border: none;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;

            &:hover {
                background: #e5e7eb;
            }

            &.active {
                background: #6366f1;
            }

            img {
                width: 16px;
                height: 16px;
                margin-right: 0;
            }
        }

        .btn-back {
            background: transparent;
            border: none;
            padding: 8px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;

            &:hover {
                background: rgba(0, 0, 0, 0.05);
            }

            .back-arrow {
                font-size: 20px;
                color: #333;
                font-weight: bold;
            }
        }

        .btn-archive {
            background: #6366f1;
            color: #fff;
            border: none;
            padding: 6px 12px;
            border-radius: 16px;
            font-size: 12px;
            font-weight: 500;
            display: flex; /* 确保按钮内元素居中 */
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;
            transform: scale(1);

            &:hover {
                background: #4f46e5;
                transform: scale(1.05);
            }

            &:active {
                transform: scale(0.95);
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }
        }
    }

  /* 主内容区 */
  .main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    padding: 0 16px 4px;
    margin-bottom: 0;
    scrollbar-width: thin;
    scrollbar-color: #6366f1 #f0f4ff;
    
    &::-webkit-scrollbar {
      width: 8px;
    }
    
    &::-webkit-scrollbar-track {
      background: #f0f4ff;
      border-radius: 4px;
    }
    
    &::-webkit-scrollbar-thumb {
      background: #6366f1;
      border-radius: 4px;
    }
    
    &::-webkit-scrollbar-thumb:hover {
      background: #4f46e5;
    }
  }

  /* 医生头像 */
  .doctor-avatar {
    text-align: center;

    img {
      width: 100px;
      height: auto;
      margin-right: 0; /* 去掉通用样式的右边距 */
    }
  }

  /* AI诊室卡片 */
  .ai-clinic-card {
    margin: 0 0 8px;
    background: #fff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border: 1px solid #6366f1;
    min-height: 120px;

    .card-header {
      display: flex;
      align-items: center;
      background: #6366f1;
      color: #fff;
      padding: 8px 12px;

      .card-title {
        font-size: 16px;
        font-weight: 600;
        margin-right: 8px;
      }

      .status-tag {
        background: rgba(255,255,255,0.2);
        padding: 4px 8px;
        border-radius: 10px;
        font-size: 10px;
      }
    }

    .card-content {
      padding: 12px 12px;
      font-size: 14px;
      line-height: 1.4;

      .steps {
        color: #666;
        margin-bottom: 8px;
        font-size: 12px;
      }

      .divider {
        border-bottom: 1px dashed #ddd;
        margin: 8px 0;
      }
    }
  }

  /* 咨询人卡片 */
  .consultant-card {
    margin: 0 0 8px;
    background: #fff;
    border-radius: 12px;
    padding: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);

    .consultant-name {
      color: #6366f1;
      font-size: 14px;
      margin-bottom: 8px;
    }

    .consultant-desc {
      font-size: 16px;
      line-height: 1.4;
      margin-bottom: 12px;
    }

    .divider {
      border-bottom: 1px dashed #ddd;
      margin: 8px 0;
    }

    .upload-area {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px;
      background: #f8f9ff;
      border-radius: 6px;
      font-size: 12px;
      color: #666;

      span img {
        vertical-align: middle;
        margin-right: 4px;
        width: 14px;
        height: 14px;
      }

      .upload-btn {
        background: #e8e8ff;
        color: #6366f1;
        border: none;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
      }
    }
  }

  /* 引导问题区域 */
    .guide-questions {
      margin: 0 0 8px 44px;
      
      .questions-container {
        display: flex;
        flex-direction: column;
        gap: 4px;
        align-items: flex-start;
      }
      
      .guide-question-wrapper {
        display: flex;
        align-items: center;
        gap: 4px;
      }
      
      .guide-question {
        background: #fff;
        border: 1px solid #e0e7ff;
        border-radius: 16px;
        padding: 6px 12px;
        font-size: 11px;
        color: #333;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        
        &:hover {
          background: #f0f4ff;
          border-color: #6366f1;
        }
        
        .question-text {
          flex: 1;
        }
      }
      
      .refresh-btn {
        background: #f0f4ff;
        border: 1px solid #e0e7ff;
        cursor: pointer;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        
        &:hover {
          background: #e0e7ff;
          border-color: #6366f1;
        }
        
        img {
          width: 8px;
          height: 8px;
          margin-right: 0;
        }
      }
    }

  /* 功能按钮区 */
  .func-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    padding: 4px 10px;
    background: linear-gradient(180deg, rgba(240, 244, 255, 0.95), rgba(232, 232, 255, 0.95));
    border-radius: 12px;
    margin: 2px 0;

    .func-btn {
      flex: 1;
      min-width: 70px;
      padding: 4px 8px;
      border-radius: 16px;
      font-size: 11px;
      border: none;
      color: #333;
      background: #f0f4ff;
      white-space: nowrap;
      display: flex; /* 确保按钮内图标文字居中 */
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.3s ease;
      transform: scale(1);

      &:nth-child(1) { background: #fef3c7; color: #92400e; }
      &:nth-child(2) { background: #d1fae5; color: #065f46; }
      &:nth-child(3) { background: #dbeafe; color: #1e40af; }
      &:nth-child(4) { background: #e0e7ff; color: #3730a3; }
      &:nth-child(5) { background: #f3e8ff; color: #6b21a8; }

      &:hover {
        transform: scale(1.05);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      }

      &:active {
        transform: scale(0.95);
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
      }
    }
  }

  /* 底部输入区 */
  .input-bar {
    padding: 6px 12px;
    background: #f0f4ff;
    border-radius: 12px;
    margin: 4px 0;

    /* 输入区域 */
    .input-area {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    /* 第二行：输入框 */
    .input-field {
      width: 100%;
      min-height: 36px;
      border: none;
      padding: 4px 10px;
      font-size: 14px;
      background: transparent;
      outline: none;
      resize: none;
      font-family: inherit;
      color: #333;

      &::placeholder {
        color: #999;
      }
    }

    /* 第三行：按钮区域 */
    .button-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 2px 0;
      position: relative;
    }

    .button-row-left {
      display: flex;
      align-items: center;
      gap: 2px;
    }

    .button-row-right {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .action-btn {
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 4px 8px;
      border-radius: 14px;
      border: none;
      background: transparent;
      font-size: 12px;
      color: #666;
      cursor: pointer;
      transition: all 0.2s;
      white-space: nowrap;

      &:hover {
        background: rgba(0, 0, 0, 0.05);
      }

      img {
        width: 14px;
        height: 14px;
        margin-right: 3px;
      }

      &.deep-think {
        color: #666;
        
        &.active {
          background: #d1d5db;
          color: #1f2937;
          font-weight: 500;
        }
      }

      &.smart-search {
        color: #6366f1;
        
        &.active {
          background: #c7d2fe;
          color: #4338ca;
          font-weight: 500;
        }
      }
    }

    .voice-btn {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: #ffffff;
      border: none;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      flex-shrink: 0;
      transition: all 0.2s;

      &:hover {
        background: #e5e7eb;
      }

      &.active {
        background: #6366f1;
      }

      img {
        width: 18px;
        height: 18px;
        margin-right: 0;
      }
    }

    .plus-btn {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: #ffffff;
      border: none;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      color: #6366f1;
      font-size: 20px;
      font-weight: 300;
      flex-shrink: 0;
      transition: all 0.2s;

      &:hover {
        background: #e5e7eb;
      }
    }

    .send-btn {
      padding: 6px 20px;
      border-radius: 16px;
      background: #6366f1;
      border: none;
      color: #fff;
      font-size: 12px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s;
      white-space: nowrap;

      &:hover {
        background: #4f46e5;
      }

      &.pause-btn {
        background: #ef4444;

        &:hover {
          background: #dc2626;
        }
      }
    }

    .upload-options {
      position: absolute;
      right: 70px;
      bottom: 45px;
      background: #ffffff;
      border-radius: 6px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.15);
      padding: 6px;
      z-index: 1000;
      min-width: 100px;

      .upload-option {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 6px 10px;
        border-radius: 3px;
        cursor: pointer;
        transition: all 0.3s ease;

        &:hover {
          background: #f0f4ff;
        }

        img {
          width: 14px;
          height: 14px;
          margin-right: 0;
        }

        span:first-child {
          font-size: 14px;
        }

        span:last-child {
          font-size: 12px;
          color: #333;
        }
      }
    }
  }

  /* 对话区域 */
  .chat-area {
    margin: 0 0 8px;
    padding: 8px;
    background: transparent;
    border-radius: 12px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 8px;
    min-height: 300px;

    .message {
      display: flex;
      margin-bottom: 4px;
      max-width: 80%;

      &.user {
        align-self: flex-end;

        .message-content {
          background-color: #409eff;
          color: white;
          border-bottom-right-radius: 4px;
          margin-right: 8px;
        }
      }

      &.assistant {
        align-self: flex-start;
        flex-direction: row;

        .message-content {
          background-color: rgba(245, 247, 250, 0.8);
          color: #303133;
          border-bottom-left-radius: 4px;
          margin-right: 8px;
        }
      }

      .message-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        overflow: hidden;
        flex-shrink: 0;

        img {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }
      }

      .message-content {
        padding: 8px 12px;
        border-radius: 16px;
        word-wrap: break-word;
        line-height: 1.4;
        max-width: calc(100% - 44px);
      }

      /* 网页地址折叠栏样式 */
      .urls-section {
        margin-bottom: 8px;
        border: 1px solid rgba(224, 224, 224, 0.6);
        border-radius: 6px;
        overflow: hidden;

        .urls-header {
          background-color: rgba(240, 244, 255, 0.8);
          padding: 6px 10px;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 6px;

          .urls-icon {
            font-size: 10px;
            color: #6366f1;
          }

          .urls-label {
            font-size: 12px;
            font-weight: 500;
            color: #6366f1;
          }
        }

        .urls-content {
          padding: 8px;
          background-color: rgba(248, 249, 255, 0.8);
          font-size: 12px;
          line-height: 1.4;
          color: #333;
          word-break: break-all;
        }
      }

      /* 思考过程样式 */
      .thought-section {
        margin-bottom: 8px;
        border: 1px solid rgba(224, 224, 224, 0.6);
        border-radius: 6px;
        overflow: hidden;

        .thought-header {
          background-color: rgba(245, 245, 245, 0.8);
          padding: 6px 10px;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 6px;

          .thought-icon {
            font-size: 10px;
            color: #666;
          }

          .thought-label {
            font-size: 12px;
            font-weight: 500;
            color: #333;
          }
        }

        .thought-content {
          padding: 8px;
          background-color: rgba(250, 250, 250, 0.8);
          font-size: 12px;
          line-height: 1.4;
          color: #666;
        }
      }

      /* 实际回复样式 */
      .actual-response {
        font-size: 14px;
        line-height: 1.5;
        color: #333;
      }

      .sources-box {
        margin-top: 12px;
        padding-top: 10px;
        border-top: 1px dashed #e2e8ea;

        .sources-title {
          font-size: 12px;
          color: #8a9399;
          margin-bottom: 8px;
        }

        .sources-list {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
        }

        .source-chip {
          display: inline-flex;
          align-items: baseline;
          gap: 6px;
          padding: 4px 10px;
          border-radius: 12px;
          background: #eef7f6;
          border: 1px solid #cfe8e5;
          font-size: 12px;
          color: #0a6b60;

          em {
            font-style: normal;
            font-size: 11px;
            color: #7fa8a4;
          }
        }
      }
    }

    .loading {
      align-self: flex-start;
      display: flex;
      align-items: center;
      gap: 6px;
      color: #909399;
      font-size: 12px;

      .loading-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        overflow: hidden;
        flex-shrink: 0;

        img {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }
      }
    }
  }
}
</style>