<template>
  <div class="audio-player" v-loading="!isPlaying">
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
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps<{
  audioUrl?: string;  // 音频URL
  autoPlay?: boolean; // 是否自动播放
}>();

const emit = defineEmits<{
  (e: 'playEnd'): void;    // 播放结束事件
  (e: 'playStart'): void;  // 播放开始事件
}>();

const audioPlayer = ref<HTMLAudioElement | null>(null);
const showPlayer = ref(false);
const isPlaying = ref(true);

// 监听音频URL变化
watch(() => props.audioUrl, (newUrl) => {
  if (newUrl) {
    showPlayer.value = true;
    if (audioPlayer.value) {
      audioPlayer.value.src = newUrl;
      if (props.autoPlay) {
        audioPlayer.value.play();
      }
    }
  } else {
    showPlayer.value = false;
  }
});

// 播放结束处理
const handleAudioEnded = () => {
  showPlayer.value = false;
  emit('playEnd');
};

// 开始播放处理
const handlePlay = () => {
  isPlaying.value = true;
  emit('playStart');
};

// 过渡动画结束处理
const afterEnter = () => {
  isPlaying.value = true;
};

const afterLeave = () => {
  isPlaying.value = false;
};

// 提供给父组件的方法
defineExpose({
  play: () => audioPlayer.value?.play(),
  pause: () => audioPlayer.value?.pause(),
  stop: () => {
    if (audioPlayer.value) {
      audioPlayer.value.pause();
      audioPlayer.value.currentTime = 0;
    }
  }
});
</script>

<style scoped lang="scss">
.audio-player {
  position: fixed;
  left: 50%;
  transform: translateX(-50%);
  z-index: 100;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style> 