<template>
  <div class="medical-chat">
    <div class="chat-header">
      <h3>知贝医疗助手</h3>
    </div>
    <div class="chat-body" ref="chatBodyRef">
      <div v-for="(message, index) in messages" :key="index" :class="['message', message.role]">
        <div class="message-content">
          <!-- 检查是否包含思考过程 -->
          <div v-if="message.role === 'assistant' && message.content.includes('<think>')" class="assistant-message">
            <!-- 分割思考过程和实际回复 -->
            <template v-if="message.content.includes('<think>')">
              <!-- 思考过程 -->
              <div class="thought-section">
                <div class="thought-header" @click="toggleThought(index)">
                  <span class="thought-icon">{{ message.thoughtExpanded ? '▼' : '▶' }}</span>
                  <span class="thought-label">思考过程</span>
                </div>
                <div v-if="message.thoughtExpanded" class="thought-content" v-html="getThoughtContent(message.content)">
                </div>
              </div>
              <!-- 实际回复 -->
              <div class="actual-response" v-html="getActualResponse(message.content)">
              </div>
            </template>
            <template v-else>
              <div v-html="message.content"></div>
            </template>
          </div>
          <template v-else>
            <div v-html="message.content"></div>
          </template>
        </div>
      </div>
      <div v-if="loading" class="loading">
        <el-icon class="is-loading"><Loading /></el-icon>
        <span>AI 正在思考...</span>
      </div>
    </div>
    <div class="chat-footer">
      <el-input
        v-model="inputValue"
        placeholder="请输入您的问题..."
        @keyup.enter="sendMessage"
        type="textarea"
        :rows="2"
      ></el-input>
      <el-button type="primary" @click="sendMessage" :disabled="!inputValue.trim() || loading">
        发送
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'
import medicalApi from '../api/medical'

const chatBodyRef = ref<HTMLElement>()
const messages = ref<Array<{ role: string; content: string; thoughtExpanded?: boolean }>>([])
const inputValue = ref('')
const loading = ref(false)

// 提取思考过程内容
const getThoughtContent = (content: string): string => {
  const start = content.indexOf('<think>')
  const end = content.indexOf('</think>')
  if (start !== -1 && end !== -1) {
    return content.substring(start + 6, end)
  }
  return ''
}

// 提取实际回复内容
const getActualResponse = (content: string): string => {
  const start = content.indexOf('<think>')
  if (start !== -1) {
    return content.substring(0, start)
  }
  return content
}

const sendMessage = async () => {
  const content = inputValue.value.trim()
  if (!content) return

  // 添加用户消息
  messages.value.push({ role: 'user', content })
  inputValue.value = ''
  scrollToBottom()

  loading.value = true
  try {
    const response = await medicalApi.chat(content)
    // 添加AI回复，默认折叠思考过程
    messages.value.push({ role: 'assistant', content: response.data, thoughtExpanded: false })
  } catch (error) {
    ElMessage.error('对话失败，请稍后重试')
    console.error('Chat error:', error)
  } finally {
    loading.value = false
    scrollToBottom()
  }
}

const toggleThought = (index: number) => {
  if (messages.value[index]) {
    messages.value[index].thoughtExpanded = !messages.value[index].thoughtExpanded
  }
}

const scrollToBottom = () => {
  nextTick(() => {
    if (chatBodyRef.value) {
      chatBodyRef.value.scrollTop = chatBodyRef.value.scrollHeight
    }
  })
}

onMounted(() => {
  // 初始欢迎消息
  messages.value.push({
    role: 'assistant',
    content: '您好，我是知贝医疗助手，有什么可以帮助您的吗？',
    thoughtExpanded: false
  })
  scrollToBottom()
})
</script>

<style scoped lang="scss">
.medical-chat {
  height: 100%;
  display: flex;
  flex-direction: column;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  overflow: hidden;

  .chat-header {
    background-color: #f5f7fa;
    padding: 16px;
    border-bottom: 1px solid #e4e7ed;
    h3 {
      margin: 0;
      color: #303133;
      font-size: 16px;
      font-weight: 500;
    }
  }

  .chat-body {
    flex: 1;
    padding: 16px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 12px;

    .message {
      max-width: 80%;
      padding: 10px 14px;
      border-radius: 18px;

      &.user {
        align-self: flex-end;
        background-color: #409eff;
        color: white;
        border-bottom-right-radius: 4px;
      }

      &.assistant {
        align-self: flex-start;
        background-color: #f5f7fa;
        color: #303133;
        border-bottom-left-radius: 4px;
      }

      .message-content {
        word-wrap: break-word;
        line-height: 1.4;
      }

      /* 思考过程样式 */
      .thought-section {
        margin-bottom: 12px;
        border: 1px solid #e0e0e0;
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
            font-size: 14px;
            font-weight: 500;
            color: #333;
          }
        }

        .thought-content {
          padding: 12px;
          background-color: #fafafa;
          font-size: 14px;
          line-height: 1.5;
          color: #666;
        }
      }

      /* 实际回复样式 */
      .actual-response {
        font-size: 15px;
        line-height: 1.6;
        color: #333;
      }
    }

    .loading {
      align-self: flex-start;
      display: flex;
      align-items: center;
      gap: 8px;
      color: #909399;
      font-size: 14px;
    }
  }

  .chat-footer {
    padding: 16px;
    border-top: 1px solid #e4e7ed;
    display: flex;
    gap: 12px;

    .el-input {
      flex: 1;

      textarea {
        resize: none;
      }
    }

    .el-button {
      align-self: flex-end;
    }
  }
}
</style>