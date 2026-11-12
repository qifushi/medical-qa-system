<!-- src/components/TooltipList.vue -->
<template>
  <el-tooltip popper-class="tooltip-style" placement="top">
    <template #content>
      <ul>
        <li v-for="(item, index) in list" :key="index">
          {{ item }}
        </li>
      </ul>
    </template>
    <slot>
      <el-icon><QuestionFilled /></el-icon>
    </slot>
  </el-tooltip>
</template>

<script setup>
import { QuestionFilled } from '@element-plus/icons-vue'

defineProps({
  list: {
    type: Array,
    required: true
  }
})
</script>
