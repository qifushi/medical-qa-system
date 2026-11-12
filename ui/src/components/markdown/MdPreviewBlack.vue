<template>
  <MdPreview noIconfont noPrettier v-bind="$attrs" class="command-line-theme" />
</template>

<script setup lang="ts">
import { MdPreview } from 'md-editor-v3'
defineOptions({ name: 'MdPreview' })
</script>
<style scoped>
.command-line-theme {
  /* 命令行黑色主题 */
  --md-bk-color: #000; /* 背景色 */
  --md-color: #fff; /* 文字色（绿色模拟命令行） */
  --md-hover-color: #fff; /* 悬停色 */
  min-height: 100%;
}

/* 深度选择器穿透子组件 */
.command-line-theme :deep(.md-editor-preview) {
  background-color: var(--md-bk-color);
  color: var(--md-color);
  font-family: monospace; /* 等宽字体 */
  padding: 12px;
  border-radius: 4px;
}

/* 代码块样式 */
.command-line-theme :deep(pre) {
  background-color: #111 !important;
  border: 1px solid #333;
}
/* 添加终端光标闪烁效果 */
@keyframes blink {
  50% {
    opacity: 0;
  }
}
.command-line-theme::after {
  content: '▋';
  animation: blink 1s infinite;
}
</style>
