<template>
  <div v-if="showChatappPage" class="chatapp-container">
    <div class="chat-app">
      <!-- 只在非知贝页面显示侧边栏 -->
      <chatappSidebar v-if="!isMedicalPage"></chatappSidebar>
      <div class="chat-app-container" :class="{ 'no-sidebar': isMedicalPage }">
        <AppMain />
      </div>
    </div>
  </div>
  <div v-else class="main-layout h-full flex">
    <div class="sidebar-container">
      <Sidebar />
    </div>
    <div class="view-container">
      <AppMain />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { AppMain, Sidebar } from '../components'
import chatappSidebar from '../components/chatappSidebar/index.vue'
const route = useRoute()

const showChatappPage = computed(() => {
  const { meta, name } = route as any
  console.log(meta, 'man-layout-meta')
  console.log(name, 'current route name')
  // 检查当前路由是否是知贝页面
  if (['graphAssistant', 'medicalConsult', 'reportAnalysis', 'medicalService', 'medicineAnalysis', 'doctorMain'].includes(name)) {
    return true
  }
  // 检查当前路由或其父路由是否是chatapp-page类型
  return meta.type === 'chatapp-page'
})

const isMedicalPage = computed(() => {
  const { name } = route as any
  // 检查当前路由是否是医疗相关页面
  return ['graphAssistant', 'medicalConsult', 'reportAnalysis', 'medicalService', 'medicineAnalysis', 'doctorMain'].includes(name)
})
</script>
<style lang="scss">
.sidebar-container {
  box-sizing: border-box;
  transition: width 0.28s;
  width: var(--sidebar-width);
  min-width: var(--sidebar-width);
  background-color: var(--sidebar-bg-color);
}
.view-container {
  width: calc(100% - var(--sidebar-width));
}
</style>
<style scoped lang="scss">
.chatapp-container {
  height: 100%;
  transition: all 0.4s ease;
  box-sizing: border-box;
  overflow: hidden;
  .chat-app {
      width: 100%;
      height: 100%;
      position: relative;
      display: flex;
      flex-direction: row;
      background: url('@/assets/chatapp-page/bg.jpg') no-repeat center center;
      background-size: cover; /* 确保背景图片覆盖整个屏幕 */
      padding: 10px 5px 0px 0px;
      
      /* 当路由是知贝时，不显示侧边栏空间 */
      &:has(.chat-app-container.no-sidebar) {
        padding-left: 10px;
        
        &::before {
          right: 10px;
        }
      }
      
      &::before {
        background: url(/ui/src/assets/chatapp-page/aijpg.jpg) no-repeat;
        background-size: cover;
        content: '';
        position: absolute;
        width: 700px;
        bottom: 0px;
        right: 261px;
        height: 700px;
      }
    .chat-app-container {
      height: 100%;
      width: 100%;
      overflow: auto;
      display: flex;
      flex-direction: column;
    }
    .chat-app-container.no-sidebar {
      margin-left: 0 !important;
    }
  }
}
</style>
