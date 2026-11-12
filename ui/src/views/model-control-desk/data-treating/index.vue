<template>
  <div class="data-treating">
    <iframe src="https://brain.jrsoft.com.cn/dpft/" style="width: 100%; flex: 1;" frameborder="0"></iframe>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import useStore from '@/stores'
const { user } = useStore()
const token = user.getToken()
let timer = undefined
let count = 0

const messageHandler = (event) => {
  if (event.data === 'MSG_RECEIVED') {
    clearInterval(timer)
    window.removeEventListener('message', messageHandler) // 收到响应后移除监听
  }
}

onMounted(() => {
  window.addEventListener('message', messageHandler) // 只在组件挂载时添加监听
})

onUnmounted(() => {
  clearInterval(timer)
  window.removeEventListener('message', messageHandler) // 组件卸载时确保移除监听
})
const sendDataToPlugin = () => {
  const iframe = document.querySelector('iframe')
  try {
    iframe.contentWindow.postMessage(
      {
        token: token,
        type: 'receivedMessage'
      },
      '*'
    )
  } catch (err) {
    if (count > 14) {
      clearInterval(timer)
    }
    console.error('消息发送失败:', err)
  }
}
const initMessage = () => {
  count = 0
  timer = setInterval(() => {
    count++
    sendDataToPlugin()
  }, 200)
}
initMessage()
</script>

<style lang="scss" scoped>
.data-treating {
  height: calc(100vh - 56px);
  display: flex;
  flex-direction: column;
}
</style>
