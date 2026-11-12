<template>
  <div class="l-container">
    <div class="flex-end">
      <el-button text icon="Setting"></el-button>
    </div>
    <div v-for="(tagGroup, index) in tagsList" :key="index">
      <div style="margin: 20px 0">{{ tagGroup.parentValue }}</div>
      <div class="tag-selector">
        <button
          v-for="(tag, index) in tagGroup.childs"
          :key="index"
          :class="['custom-tag', { 'is-selected': isTagSelected(tag) }]"
          :disabled="tag.disabled"
          @click="handleTagClick(tag)"
        >
          {{ tag.value }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { type Tag, tagsList } from '../type/tag'
const emit = defineEmits(['update:modelValue'])
// 定义modelValue的类型接口
interface SelectedTags {
  type: string;
  tags: Tag[]; // 明确指定tags数组中的元素类型为Tag
}
const props = defineProps({
  modelValue: {
    type: Object as () => SelectedTags,
    default: () => ({ type: '', tags: [] })
  }
})

// 计算属性，用于检查标签是否被选中
const selectedTags = computed({
  get() {
    return props.modelValue
  },
  set(value) {
    emit('update:modelValue', value)
  }
})

// 检查标签是否被选中
const isTagSelected = (tag: Tag) => {
  // 如果是数据源类型标签（parentKey为'100'）
  const group = tagsList.find(g => g.childs.some(c => c.value === tag.value))
  if (group && group.parentKey === '100') {
    return selectedTags.value?.type === tag.key
  } else {
    
    // 其他标签
    return  Array.isArray(selectedTags.value?.tags) && 
    selectedTags.value.tags.some(item => item.value === tag.value)
  }
}

// 处理标签点击事件
const handleTagClick = (tag: Tag) => {
  const newSelectedTags = { ...selectedTags.value }
  console.log('%c [ newSelectedTags ]-64', 'font-size:13px; background:pink; color:#bf2c9f;', newSelectedTags)
  
  // 查找标签所属的分组
  const group = tagsList.find(g => g.childs.some(c => c.value === tag.value))
  console.log('%c [ group ]-67', 'font-size:13px; background:pink; color:#bf2c9f;', group)
  
  // 如果是数据源类型标签（parentKey为'100'）
  if (group && group.parentKey === '100') {
    // 如果已选中，则取消选中
    if (newSelectedTags.type === tag.key) {
      newSelectedTags.type = ''
    } else {
      // 否则选中新标签
      newSelectedTags.type = tag.key
    }
  } else {
    // 其他标签
    const index = newSelectedTags.tags.findIndex(item => item.value === tag.value)
    if (index > -1) {
      // 如果已选中，则取消选中
      newSelectedTags.tags.splice(index, 1)
    } else {
      // 否则添加新标签
      newSelectedTags.tags.push(tag)
    }
  }
  
  selectedTags.value = newSelectedTags
}
</script>

<style scoped>
.l-container {
  width: var(--sidebar-width);
  min-width: var(--sidebar-width);
  background-color: var(--sidebar-bg-color);
  /* height: 100%; */
  padding: 20px;
}
.tag-selector {
  /* display: flex;
  flex-wrap: wrap;
  gap: 8px; */
  display: grid;
  flex-wrap: wrap;
  gap: 8px;
  grid-template-columns: repeat(2, minmax(120px, 1fr));
}

.custom-tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 32px;
  padding: 0 10px;
  font-size: 14px;
  border-radius: 4px;
  border: 1px solid #cad5ee;
  background-color: #fff;
  color: #606266;
  cursor: pointer;
  transition: all 0.3s ease;
}

.custom-tag:not(:disabled):hover {
  color: #409eff;
  border-color: #c6e2ff;
  background-color: #ecf5ff;
}

.custom-tag.is-selected {
  color: #409eff;
  border-color: #409eff;
  background-color: #ecf5ff;
  font-weight: 500;
}

/* 点击动效 */
.custom-tag:not(:disabled):active {
  transform: scale(0.98);
}
/* 禁用状态样式 */
.custom-tag:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.flex-end {
  display: flex;
  justify-content: flex-end;
}
</style>
