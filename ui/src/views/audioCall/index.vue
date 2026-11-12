<template>
  <div class="flex-center" style="flex-direction: column; height: 100%">
    <div style="height: 60px"></div>
    <div class="audio-timer">00:35 / 03:00</div>
    <div class="canvas-container flex-center" style="flex: 1">
      <div style="width: 200px; height: 200px; border-radius: 50%; overflow: hidden">
        <cavasColor :color="canvasColor" :speed="speed"></cavasColor>
      </div>
    </div>
    <div class="flex-center" style="margin-bottom: 30px">我正在听</div>

    <div class="flex-center mb-24" style="gap: 40px; width: 100%">
      <el-tooltip
        :show-arrow="false"
        :offset="4"
        effect="dark"
        :content="isRecording ? '关闭麦克风' : '打开麦克风'"
        placement="top"
      >
        <div class="footerBtn-container flex-center" @click="isRecording = !isRecording">
          <el-icon class="fz-24">
            <Microphone v-show="isRecording" />
            <Mute v-show="!isRecording" />
          </el-icon>
        </div>
      </el-tooltip>
      <el-tooltip
        :show-arrow="false"
        :offset="4"
        effect="dark"
        content="选择一个声音"
        placement="top"
      >
        <div class="footerBtn-container flex-center">
          <el-icon class="fz-24"><Operation /></el-icon>
        </div>
      </el-tooltip>

      <el-tooltip :show-arrow="false" :offset="4" effect="dark" content="关闭" placement="top">
        <div class="footerBtn-close-container flex-center" @click="handleBack">
          <el-icon class="fz-24" style="color: rgba(235, 47, 47)"><Close /></el-icon>
        </div>
      </el-tooltip>
    </div>
    <div class="mb-24" style="color: rgb(135 137 159 / 1)">仅支持中文和英文的语音输出。</div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import cavasColor from './components/canvas/index.vue'
import { useRoute, useRouter } from 'vue-router'
const isRecording = ref(false)

const canvasColor = ref([1, 1, 1]) // 颜色数组
const speed = ref(1) // 变化速度
const router = useRouter()
const handleBack = () => {
  router.go(-1)
}
</script>

<style lang="scss" scoped>
.fz-24 {
  font-size: 24px;
}
.canvas-container {
  width: 200px;
  height: 200px;
  margin-bottom: 16px;
  border: none;
}
.audio-timer {
  width: fit-content;
  border-radius: 16px;
  padding: 8px 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  user-select: none;
  line-height: 28px;
  background-color: rgb(247 248 252 / 1);
  margin-bottom: 8px;
}
.footerBtn-container {
  width: 60px;
  height: 60px;
  background-color: rgb(247 248 252 / 1);
  cursor: pointer;
  border-radius: 50%;
}
.footerBtn-close-container {
  width: 60px;
  height: 60px;
  background-color: rgb(255 242 242 / 1);
  cursor: pointer;
  border-radius: 50%;
}
</style>
