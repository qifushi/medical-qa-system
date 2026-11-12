<template>
  <router-view v-slot="{ Component }">
    <transition appear name="fade-transform" mode="out-in">
      <keep-alive :include="cachedViews">
        <component :is="Component" :key="route.fullPath" />
      </keep-alive>
    </transition>
  </router-view>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const cachedViews = ref<string[]>([])

// 使用 watch 监听路由变化
watch(
  () => route,
  (newRoute) => {
    const { name, meta } = newRoute
    console.log('name', name, meta)
    if (meta?.cache && name && typeof name === 'string') {
      // 添加需要缓存的组件名
      if (!cachedViews.value.includes(name)) {
        cachedViews.value.push(name)
      }
    }
    console.log(' cachedViews.value', cachedViews.value)
  },
  { immediate: true } // 初始化时立即执行
)
</script>
