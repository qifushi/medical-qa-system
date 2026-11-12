<template>
  <div class="cmp-banner">
    <img src="@/assets/model-control-desk/banner.jpg" alt="" class="banner-video" />
    <!-- <video ref="videoPlayer" :src="videoSrc" autoplay muted loop playsinline class="banner-video" /> -->
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
// import videoSrc from '@/assets/model-control-desk/banner.mp4'

const videoPlayer = ref<HTMLVideoElement | null>(null)

onMounted(() => {
  if (videoPlayer.value) {
    videoPlayer.value.play().catch((error) => {
      console.error('视频自动播放失败:', error)
      videoPlayer.value!.muted = true
      videoPlayer.value!.play()
    })
  }
})
</script>
<style lang="scss" scoped>
.cmp-banner {
  position: relative;
  width: 100%;
  overflow: hidden;

  // 关键修改：添加最大高度限制
  max-height: 500px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #000; // 添加黑色背景以防视频加载前的空隙

  .banner-video {
    width: 100%;
    height: auto;
    display: block;
    transition: max-height 0.5s ease;
    // 保持16:9宽高比
    aspect-ratio: 16 / 9;

    // 设置最大高度为50vh
    max-height: 500px;

    // 确保视频在容器内正确显示
    object-fit: cover;

    // 对于不支持aspect-ratio的浏览器
    @supports not (aspect-ratio: 16 / 9) {
      position: relative;
      height: 0;
      padding-top: 56.25%; // 16:9比例的计算值

      & > video {
        position: absolute;
        top: 0;
        left: ​0;
        width: 100%;
        height: 100%;
      }
    }
  }

  // 移动设备优化
  @media (max-width: 768px) {
    max-height: 300px; // 移动设备上设置更小的高度

    .banner-video {
      aspect-ratio: 9 / 16;
      max-height: 300px;

      @supports not (aspect-ratio: 9 / 16) {
        padding-top: 177.78%; // 9:16比例
      }
    }
  }

  // 超大屏幕优化
  @media (min-width: 1920px) {
    max-height: 500px; // 容器高度限制

    .banner-video {
      // 在大屏幕上保持比例但限制高度
      width: 100%;
      max-height: 500px; // 设置最大高度为700px
      height: auto;

      // 确保视频居中显示
      margin: 0 auto;
      display: block;
    }
  }
}
</style>
