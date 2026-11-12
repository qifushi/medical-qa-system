<template>
  <div style="position: relative; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08)">
    <div ref="playerBox" style="height: 600px; cursor: pointer"></div>
    <div class="play-status" @click.stop="togglePlayPause" v-if="showBtn">
      <!-- 播放图标 -->
      <svg
        v-if="!isPlaying"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path d="M8 5V19L19 12L8 5Z" fill="white" />
      </svg>

      <!-- 暂停图标 -->
      <svg
        v-else
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <rect x="6" y="5" width="4" height="14" rx="1" fill="white" />
        <rect x="14" y="5" width="4" height="14" rx="1" fill="white" />
      </svg>
    </div>
  </div>
</template>

<script setup lang="ts">
import ICraftPlayer from '@icraft/player'
import { ref, onMounted, onBeforeUnmount } from 'vue'

const playerBox = ref<HTMLDivElement>()
const player = ref<any>(null) // 存储播放器实例
const isPlaying = ref(false) // 播放状态
const showBtn = ref(false)
// 切换播放/暂停
const togglePlayPause = () => {
  if (!player.value) return
  if (isPlaying.value) {
    player.value.reset()
    player.value.changeCustomCamera(0)
    isPlaying.value = false
  } else {
    player.value.tooglePlay()
    isPlaying.value = true
  }
}

onMounted(() => {
  player.value = new ICraftPlayer({
    src: 'https://cdn.jrsoft.com.cn/ModelTrainingSystemArchitecture.iplayer',
    container: playerBox.value as HTMLDivElement,
    autoPlay: false,
    defaultLoop: true,
    onReady: () => {
      player.value.changeCustomCamera(0)
      showBtn.value = true
    }
  })
})

// 组件卸载时清理资源
onBeforeUnmount(() => {
  if (player.value && player.value.destroy) {
    player.value.destroy()
  }
})
</script>

<style scoped>
.play-status {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 14px;
  z-index: 10;
  transition: opacity 0.3s;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.play-status:hover {
  background: rgba(0, 0, 0, 0.9);
  transform: scale(1.05);
}
</style>
