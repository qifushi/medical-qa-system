<template>
  <el-select 
    v-model="innerValue" 
    multiple 
    placeholder="添加标签" 
    @remove-tag="handleRemoveTag"
  >
    <el-option-group v-for="group in selectTagsList" :key="group.parentKey" :label="group.parentValue">
      <div class="p-8">
        <el-option
          class="productGroupSelector-option"
          v-for="item in group.childs"
          :key="item.key"
          :label="item.value"
          :value="item.value"
        ></el-option>
      </div>
    </el-option-group>
    <template #footer>
      <div style="display: flex; align-items: center; gap: 6px; padding: 10px; flex-wrap: wrap;">
        <span v-if="innerValue.length">已选标签：</span>
        <el-tag
          v-for="tag in displayTags"
          :key="tag.value"
          closable
          disable-transitions
          @close="handleClose(tag)"
        >
          {{ tag.value }}
        </el-tag>
        <el-input
          v-if="inputVisible"
          style="width: 100px"
          ref="InputRef"
          v-model="inputValue"
          size="small"
          @keyup.enter="handleInputConfirm"
          @blur="handleInputConfirm"
        />
        <el-button 
          v-else 
          class="button-new-tag" 
          size="small" 
          @click="showInput"
        >
          + 自定义标签
        </el-button>
      </div>
    </template>
  </el-select>
</template>

<script setup lang="ts">
import { ref, watch, nextTick, computed } from 'vue'
import type { InputInstance } from 'element-plus'
import { ElMessage } from 'element-plus'
import {type Tag, selectTagsList} from '../type/tag'

// 定义输出格式
interface TagOutput {
  tags: { key: string, value: string }[];
  custom_tags: { value: string }[];
}

const props = defineProps({
  modelValue: {
    type: Object as () => TagOutput,
    default: () => ({ tags: [], custom_tags: [] })
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

// 内部值存储选中标签的value
const innerValue = ref<string[]>([])

// 初始化innerValue
const initInnerValue = () => {
  const predefinedValues = props.modelValue.tags.map(t => t.value)
  const customValues = props.modelValue.custom_tags.map(t => t.value)
  innerValue.value = [...predefinedValues, ...customValues]
}

// 初始化
initInnerValue()

// 输入框相关状态
const inputValue = ref('')
const inputVisible = ref(false)
const InputRef = ref<InputInstance>()

// 获取所有预定义标签
const allPredefinedTags = computed(() => {
  return selectTagsList.flatMap(g => g.childs)
})

// 获取所有标签值（预定义+自定义）用于去重检查
const allTagValues = computed(() => {
  // 获取预定义标签的所有值
  const predefined = allPredefinedTags.value.map(t => t.value)
  // 获取当前选中的自定义标签值（innerValue中不属于预定义标签的部分）
  const custom = innerValue.value.filter(v => !predefined.includes(v))
  return [...predefined, ...custom]
})

// 显示标签（包含自定义标签和预定义标签）
const displayTags = computed<Tag[]>(() => {
  const tags: Tag[] = []
  
  // 1. 添加预定义标签
  innerValue.value.forEach(value => {
    const found = allPredefinedTags.value.find(t => t.value === value)
    if (found) {
      tags.push(found)
    }
  })
  
  // 2. 添加自定义标签
  innerValue.value.forEach(value => {
    if (!tags.some(t => t.value === value)) {
      tags.push({
        key: value,
        value: value
      })
    }
  })
  
  return tags
})

// 生成输出格式
const generateOutput = (): TagOutput => {
  const predefinedTags = []
  const customTags = []
  
  // 遍历所有选中的值
  for (const value of innerValue.value) {
    // 查找是否是预定义标签
    const predefined = allPredefinedTags.value.find(t => t.value === value)
    if (predefined) {
      predefinedTags.push({ key: predefined.key, value: predefined.value })
    } else {
      customTags.push({ value })
    }
  }
  
  return {
    tags: predefinedTags,
    custom_tags: customTags
  }
}

// 监听父组件传入的值变化
watch(() => props.modelValue, (newVal, oldVal) => {
  // 检查值是否真的变化了
  const newTags = newVal.tags.map(t => t.value).sort().join(',')
  const newCustomTags = newVal.custom_tags.map(t => t.value).sort().join(',')
  
  const oldTags = oldVal ? oldVal.tags.map(t => t.value).sort().join(',') : ''
  const oldCustomTags = oldVal ? oldVal.custom_tags.map(t => t.value).sort().join(',') : ''
  
  // 只有当值真正变化时才初始化
  if (newTags !== oldTags || newCustomTags !== oldCustomTags) {
    initInnerValue()
  }
}, { deep: true })

// 监听内部值变化
watch(innerValue, (newVal) => {
  // 检查标签数量是否超过限制
  // if (newVal.length > 6) {
  //   innerValue.value = newVal.slice(0, 6) // 只保留前6个标签
  //   ElMessage.warning('最多只能添加6个标签')
  //   return
  // }
  
  const output = generateOutput()
  
  // 检查输出是否真的变化了
  const currentTags = props.modelValue.tags.map(t => t.value).sort().join(',')
  const currentCustomTags = props.modelValue.custom_tags.map(t => t.value).sort().join(',')
  
  const newTags = output.tags.map(t => t.value).sort().join(',')
  const newCustomTags = output.custom_tags.map(t => t.value).sort().join(',')
  
  // 只有当值真正变化时才触发更新
  if (currentTags !== newTags || currentCustomTags !== newCustomTags) {
    emit('update:modelValue', output)
    emit('change', output)
  }
}, { deep: true })

// 处理标签关闭
const handleClose = (tag: Tag) => {
  const index = innerValue.value.indexOf(tag.value)
  if (index > -1) {
    innerValue.value.splice(index, 1)
  }
}

// 处理选择器移除标签
const handleRemoveTag = (tagValue: string) => {
  const index = innerValue.value.indexOf(tagValue)
  if (index > -1) {
    innerValue.value.splice(index, 1)
  }
}

// 显示自定义标签输入框
const showInput = () => {
  // 检查是否达到上限
  // if (innerValue.value.length >= 6) {
  //   ElMessage.warning('最多只能添加6个标签')
  //   return
  // }
  
  inputVisible.value = true
  nextTick(() => {
    InputRef.value?.input?.focus()
  })
}


// 确认添加自定义标签
const handleInputConfirm = () => {
  const trimmedValue = inputValue.value.trim()
  
  if (trimmedValue) {
    // 检查是否达到上限
    if (innerValue.value.length >= 6) {
      ElMessage.warning('最多只能添加6个标签')
      inputVisible.value = false
      inputValue.value = ''
      return
    }
    
    // 查找是否与预定义标签匹配
    const matchedTag = allPredefinedTags.value.find(
      tag => tag.value.toLowerCase() === trimmedValue.toLowerCase()
    )
    
    // 检查是否已经选中
    if (innerValue.value.some(v => v.toLowerCase() === trimmedValue.toLowerCase())) {
      ElMessage.warning('此标签已添加过啦')
    } 
    // 如果匹配到预定义标签且未选中
    else if (matchedTag) {
      // 选中匹配的预定义标签
      if (!innerValue.value.includes(matchedTag.value)) {
        innerValue.value = [...innerValue.value, matchedTag.value]
      }
    } 
    // 如果是新的自定义标签
    else {
      // 检查是否重复（不区分大小写）
      const isDuplicate = allTagValues.value.some(
        v => v.toLowerCase() === trimmedValue.toLowerCase()
      )
      
      if (isDuplicate) {
        ElMessage.warning('此标签已添加过啦')
      } else {
        // 添加自定义标签
        innerValue.value = [...innerValue.value, trimmedValue]
      }
    }
  }
  
  inputVisible.value = false
  inputValue.value = ''
}
</script>

<style scoped>
.productGroupSelector-option {
  display: inline-flex;
  align-items: center;
  flex-wrap: wrap;
}
</style>
