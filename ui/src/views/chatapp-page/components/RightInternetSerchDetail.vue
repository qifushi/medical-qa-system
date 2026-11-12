<template>
  <div class="right-order-container">
    <div class="title" style="font-size: 20px">网页搜索</div>
    <el-scrollbar ref="scrollbarRef" style="padding: 0 16px 12px; height: calc(100% - 80px)">
      <div class="content-box" v-for="(item, index) of webSearchList">
        <div class="flex align-center mb-8" style="font-size: 12px">
          <el-avatar style="background-color: #fff" :src="item.siteIcon" :size="20" />
          <div style="white-space: nowrap; margin-left: 10px">{{ item.siteName }}</div>
          <div>・</div>
          <div style="color: #5e6772">{{ dateFormat(item.dateLastCrawled) }}</div>
        </div>
        <a class="title-link primary" :href="item.url">{{ item.name }}</a>
        <div class="mt-8 network-detail ellipsis-4">
          {{ item.summary }}
        </div>
      </div>
    </el-scrollbar>

    <el-button text class="closeBtn" @click="handleClose">
      <el-icon><Close /></el-icon>
    </el-button>
  </div>
</template>

<script setup lang="ts">
import { dateFormat } from '@/utils/time'
import { ref, watch } from 'vue'
interface webSearchListType {
  dateLastCrawled: string
  id: string
  name: string
  siteIcon: string
  siteName: string
  summary: string
  url: string
}
const props = defineProps<{
  webSearchList: webSearchListType[]
}>()
// 监听webSearchList的变化
const scrollbarRef = ref()
watch(
  () => props.webSearchList,
  () => {
    smoothScrollToTop()
  },
  { deep: true }
)
// 平滑滚动到顶部的方法
const smoothScrollToTop = () => {
  const scrollbar = scrollbarRef.value?.wrapRef
  if (scrollbar) {
    scrollbar.scrollTo({
      top: 0,
      behavior: 'smooth' // 使用平滑滚动
    })
  }
}
const emit = defineEmits(['close'])
const handleClose = () => {
  emit('close')
}
</script>

<style scoped lang="scss">
.right-order-container {
  position: relative;
  height: calc(100% - 20px); // 减去父元素底部padding
  background-color: #fff;
  border-radius: 18px;
  margin-right: 10px;
  box-sizing: border-box;
  .closeBtn {
    position: absolute;
    right: 20px;
    top: 16px;
  }
  .title {
    padding: 12px 16px 20px;
  }
  .content-box {
    padding: 12px 0;
    &:not(:last-child) {
      box-shadow: 0 -1px 0 0 #e5e5e5 inset;
    }
    &:first-child {
      padding: 0 0 12px;
    }

    .title-link {
      font-size: 16px;
      &:hover {
        // 添加下划线
        color: #2f99ff;
        text-decoration: underline;
      }
      &:visited {
        color: #7214af;
      }
    }
    .network-detail {
      color: #5e6772;
    }
  }
}
.ellipsis-4 {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 4;
  overflow: hidden;
}
</style>
