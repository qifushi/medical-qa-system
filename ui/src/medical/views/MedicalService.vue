<template>
  <div class="medical-service">
    <!-- 头部 -->
    <div class="header">
      <div class="header-left">
        <button class="btn-back" @click="goBack">
          ←
        </button>
        <h1>就医助手</h1>
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
        <!-- 功能卡片作为对话的一部分 -->
        <div class="medicine-manager-container">
          <!-- 统计文案 -->
          <p class="user-count">累计服务用户超过2700万人</p>

          <!-- 数据统计区 -->
          <div class="stats-section">
            <div class="stat-item">
              <div class="stat-value">90万</div>
              <div class="stat-label">正规执业医师</div>
            </div>
            <div class="divider"></div>
            <div class="stat-item">
              <div class="stat-value">3000+</div>
              <div class="stat-label">公立三甲医院</div>
            </div>
            <div class="divider"></div>
            <div class="stat-item">
              <div class="stat-value">600万</div>
              <div class="stat-label">患者真实评价</div>
            </div>
          </div>

          <!-- 功能列表 -->
          <div class="function-list">
            <!-- AI问诊 -->
            <div class="function-item">
              <div class="function-left">
                <div class="icon-wrapper ai-doctor">
                  <img 
                    src="/medical/img/img15.png" 
                    alt="AI问诊" 
                    class="function-icon"
                  >
                </div>
                <div class="function-text">
                  <div class="function-title">AI问诊</div>
                  <div class="function-desc">智能分析病情，推荐科室</div>
                </div>
              </div>
              <span class="arrow">→</span>
            </div>

            <!-- 在线问诊 -->
            <div class="function-item">
              <div class="function-left">
                <div class="icon-wrapper online-consult">
                  <img 
                    src="/medical/img/img16.png" 
                    alt="在线问诊" 
                    class="function-icon"
                  >
                </div>
                <div class="function-text">
                  <div class="function-title">在线问诊</div>
                  <div class="function-desc">专业医生一对一解答</div>
                </div>
              </div>
              <span class="arrow">→</span>
            </div>

            <!-- 预约挂号 -->
            <div class="function-item">
              <div class="function-left">
                <div class="icon-wrapper register">
                  <img 
                    src="/medical/img/img17.png" 
                    alt="预约挂号" 
                    class="function-icon"
                  >
                </div>
                <div class="function-text">
                  <div class="function-title">预约挂号</div>
                  <div class="function-desc">覆盖全国三甲医院</div>
                </div>
              </div>
              <span class="arrow">→</span>
            </div>
          </div>
        </div>

        <!-- 消息列表 -->
        <div v-for="(message, index) in messages" :key="index" :class="['message', message.role]">
          <!-- 助手消息 -->
          <template v-if="message.role === 'assistant'">
            <!-- 助手头像 -->
            <div class="message-avatar">
              <img src="/medical/img/img4.png" alt="AI医生" />
            </div>
            
            <div class="message-content">
              <div class="assistant-message">
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
            </div>
          </template>
          
          <!-- 用户消息 -->
          <template v-else>
            <div class="message-content">
              {{ message.content }}
            </div>
            
            <!-- 用户头像 -->
            <div class="message-avatar">
              <img src="/medical/img/img5.png" alt="用户" />
            </div>
          </template>
        </div>
        <div v-if="loading" class="loading">
          <span>AI 正在思考...</span>
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
        <textarea class="input-field" v-model="inputValue" placeholder="请输入您的就医需求" @keyup.enter="sendMessage"></textarea>
        
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
            <button class="send-btn" @click="sendMessage">发送</button>
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

// 发送消息（带问题）
const sendMessageWithQuestion = async (content: string) => {
  // 添加用户消息
  messages.value = [...messages.value, { role: 'user', content }]
  scrollToBottom()
  
  loading.value = true
  try {
    console.log('✅ 发送消息:', content)
    console.log('✅ 智能搜索状态:', smartSearchActive.value, '深度思考状态:', deepThinkActive.value)
    const response = await medicalApi.chat(content, smartSearchActive.value, deepThinkActive.value, 'medical_service')
    console.log('✅ API 返回成功:', response)
    console.log('✅ response.data:', response.data)
    
    // 添加 AI 回复，默认折叠思考过程和网页地址
    const assistantMessage = {
      role: 'assistant' as const,
      content: response.data || '抱歉，暂时无法获取回复',
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
  router.back()
}

const sendMessage = async () => {
  const content = inputValue.value.trim()
  if (!content && uploadedFiles.value.length === 0) return
  
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
    const response = await medicalApi.chat(messageContent, smartSearchActive.value, deepThinkActive.value, 'medical_service')
    console.log('✅ API 返回成功:', response)
    console.log('✅ response.data:', response.data)
    
    // 这里直接显示，不用打字效果
    const assistantMessage = {
      role: 'assistant' as const,
      content: response.data || '抱歉，暂时无法获取回复',
      sources: response.sources || [],
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
  const message = messages.value[index]
  if (!message || message.role !== 'assistant') return
  
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
    currentText = actualContent.substring(0, i + 1)
    displayMessages.value[index] = currentText
    
    // 每打一个句子就朗读一次，避免频繁触发语音合成
    if (i === actualContent.length - 1 || currentText.endsWith('。') || currentText.endsWith('！') || currentText.endsWith('？')) {
      speakText(currentText)
    }
    
    await new Promise(resolve => setTimeout(resolve, 30))
  }
  
  // 打字完成后，显示完整内容（包括标签）
  setTimeout(() => {
    displayMessages.value[index] = content
  }, 100)
  
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

onMounted(() => {
  console.log('mainContentRef:', mainContentRef.value) // 应该能看到 DOM 元素
  console.log('chatAreaRef:', chatAreaRef.value)       // 应该能看到 DOM 元素
  
  // 初始消息
  const initialMessage = {
    role: 'assistant' as const,
    content: '您好，我是就医助手，有什么可以帮助您的吗？',
    thoughtExpanded: false
  }
  messages.value.push(initialMessage)
  displayMessages.value.push(initialMessage.content)
  scrollToBottom()
})

onUnmounted(() => {
  // 离开页面时重置对话历史
  medicalApi.resetHistory().catch(error => {
    console.error('重置对话历史失败:', error)
  })
})
</script>

<style scoped lang="scss">
.medical-service {
    min-height: 100%;
    background-image: url('/medical/img/body_bg.jpg');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
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
    justify-content: space-between;
    align-items: center;
    padding: 8px 16px;
    background: linear-gradient(180deg, #f0f4ff 0%, #e8e8ff 100%);
    z-index: 100;
    margin-bottom: 16px;

    .header-left {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .header-right {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .btn-back {
      background: none;
      border: none;
      font-size: 18px;
      color: #333;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      transition: all 0.3s ease;
      font-weight: bold;

      &:hover {
        background: rgba(0, 0, 0, 0.05);
      }

      &:active {
        transform: scale(0.95);
      }
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

    h1 {
      font-size: 20px;
      font-weight: 600;
      color: #333;
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
    margin-bottom: 16px;
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

  /* 药管家容器 */
  .medicine-manager-container {
    max-width: 375px;
    margin: 0 auto;
    padding: 20px 15px;
    background-color: #fff;
    border-radius: 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  }

  /* 用户统计文案 */
  .user-count {
    padding: 10px 20px;
    font-size: 14px;
    color: #666;
    background-color: #f8f9fa;
    margin: 0;
    border-radius: 12px;
    margin-bottom: 16px;
  }

  /* 数据统计区 */
  .stats-section {
    display: flex;
    padding: 20px;
    justify-content: space-between;
    border-bottom: 1px solid #eee;
    margin-bottom: 16px;
  }

  .stat-item {
    text-align: center;
    flex: 1;
  }

  .stat-value {
    font-size: 24px;
    font-weight: 700;
    color: #409eff;
    margin-bottom: 5px;
  }

  .stat-label {
    font-size: 14px;
    color: #666;
  }

  .divider {
    width: 1px;
    background-color: #eee;
    margin: 0 10px;
  }

  /* 功能列表 */
  .function-list {
    padding: 10px 0;
  }

  .function-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
    border-bottom: 1px solid #f5f5f5;
  }

  .function-left {
    display: flex;
    align-items: center;
    gap: 15px;
  }

  .icon-wrapper {
    width: 50px;
    height: 50px;
    border-radius: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .ai-doctor {
    background-color: #e8f4fd;
  }

  .online-consult {
    background-color: #f0f9ff;
  }

  .register {
    background-color: #fdf2f8;
  }

  .function-icon {
    width: 30px;
    height: 30px;
    object-fit: contain;
  }

  .function-text {
    flex: 1;
  }

  .function-title {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 3px;
  }

  .function-desc {
    font-size: 12px;
    color: #999;
  }

  .arrow {
    color: #ccc;
    font-size: 16px;
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
      &:nth-child(3) { background: #e0e7ff; color: #3730a3; }
      &:nth-child(4) { background: #f3e8ff; color: #6b21a8; }

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
    flex: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding: 0;
    background: transparent;
    margin: 0;
    border-radius: 0;

    /* 功能卡片容器 */
    .medicine-manager-container {
      margin-bottom: 8px;
    }

    .message {
      display: flex;
      margin-bottom: 8px;
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
          background-color: #f5f7fa;
          color: #303133;
          border-bottom-left-radius: 4px;
          margin-right: 8px;
        }
      }

      .message-avatar {
        width: 32px;
        height: 32px;
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
        padding: 10px 14px;
        border-radius: 16px;
        word-wrap: break-word;
        line-height: 1.5;
        max-width: calc(100% - 40px);
      }

      /* 网页地址折叠栏样式 */
      .urls-section {
        margin-top: 8px;
        border: 1px solid #e4e7ed;
        border-radius: 8px;
        overflow: hidden;

        .urls-header {
          background-color: #f0f4ff;
          padding: 8px 12px;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 8px;

          .urls-icon {
            font-size: 12px;
            color: #6366f1;
          }

          .urls-label {
            font-size: 13px;
            font-weight: 500;
            color: #6366f1;
          }
        }

        .urls-content {
          padding: 10px;
          background-color: #f8f9ff;
          font-size: 13px;
          line-height: 1.5;
          color: #333;
          word-break: break-all;
        }
      }

      /* 思考过程样式 */
      .thought-section {
        margin-top: 8px;
        border: 1px solid #e4e7ed;
        border-radius: 8px;
        overflow: hidden;

        .thought-header {
          background-color: #f5f5f5;
          padding: 8px 12px;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 8px;

          .thought-icon {
            font-size: 12px;
            color: #666;
          }

          .thought-label {
            font-size: 13px;
            font-weight: 500;
            color: #333;
          }
        }

        .thought-content {
          padding: 10px;
          background-color: #fafafa;
          font-size: 13px;
          line-height: 1.5;
          color: #666;
        }
      }

      /* 实际回复样式 */
      .actual-response {
        font-size: 15px;
        line-height: 1.5;
        color: #333;
      }

      .sources-box {
        margin-top: 12px;
        padding-top: 10px;
        border-top: 1px dashed #e2e8ea;
        .sources-title { font-size: 12px; color: #8a9399; margin-bottom: 8px; }
        .sources-list { display: flex; flex-wrap: wrap; gap: 8px; }
        .source-chip {
          display: inline-flex; align-items: baseline; gap: 6px;
          padding: 4px 10px; border-radius: 12px;
          background: #eef7f6; border: 1px solid #cfe8e5;
          font-size: 12px; color: #0a6b60;
          em { font-style: normal; font-size: 11px; color: #7fa8a4; }
        }
      }
    }

    .loading {
      align-self: flex-start;
      display: flex;
      align-items: center;
      gap: 8px;
      color: #909399;
      font-size: 13px;
    }
  }
}
</style>
