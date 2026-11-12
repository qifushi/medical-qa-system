<template>
  <el-input
    size="small"
    class="input-draggable-progress-wrapper"
    v-model="displayValue"
    type="number"
    :step="props.step"
    :controls="false"
    @change="handleInputChange"
  >
    <template #append>
      <el-button :icon="Refresh" @click="resetToDefault" class="reset-button" />
    </template>
  </el-input>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { Refresh } from '@element-plus/icons-vue' // 引入重置图标

interface Props {
  modelValue: number | string | undefined
  min: number
  max: number
  step?: number
  defaultValue?: number // 新增默认值属性
}

const props = withDefaults(defineProps<Props>(), {
  step: 1, // 默认步长为1
  modelValue: 0 // 添加默认值
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: number): void
  (e: 'change', value: number): void
}>()

// 显示在输入框的值（字符串格式）
const displayValue = ref('')

// 内部使用的0-1范围值
const value = ref(parseValue(props.modelValue))

// 验证范围配置
if (props.min >= props.max) {
  console.error(
    `[DraggableProgress] min value (${props.min}) must be less than max value (${props.max})`
  )
}

// 计算实际值（根据min/max映射）
const actualValue = computed(() => {
  const rawValue = value.value * (props.max - props.min) + props.min
  return snapToStep(rawValue)
})

// 按步长对齐值
function snapToStep(val: number): number {
  const steps = Math.round((val - props.min) / props.step)
  let result = props.min + steps * props.step
  result = Math.max(props.min, Math.min(props.max, result))

  // 根据步长精度格式化
  if (props.step >= 1) return Math.round(result)
  const decimalPlaces = Math.max(0, Math.ceil(-Math.log10(props.step)))
  return parseFloat(result.toFixed(decimalPlaces))
}

// 解析输入值并映射到0-1范围
function parseValue(val: number | string | undefined): number {
  // 处理 undefined 情况
  if (val === undefined || val === null) return 0

  const num = Number(val)

  if (isNaN(num)) return 0

  // 按步长对齐值
  const snappedValue = snapToStep(num)

  // 将值映射到0-1范围
  const mappedValue = (snappedValue - props.min) / (props.max - props.min)
  return Math.min(1, Math.max(0, mappedValue))
}

// 处理输入框变化
function handleInputChange(val: string) {
  const num = Number(val)
  if (isNaN(num)) {
    // 输入无效时恢复之前的值
    displayValue.value = formatDisplayValue(actualValue.value)
    return
  }

  // 对齐值并更新
  const snappedValue = snapToStep(num)
  value.value = (snappedValue - props.min) / (props.max - props.min)
  displayValue.value = formatDisplayValue(snappedValue)
}

// 重置到默认值
function resetToDefault() {
  const defaultValue = props.defaultValue !== undefined ? props.defaultValue : props.min

  const snappedValue = snapToStep(defaultValue)
  value.value = (snappedValue - props.min) / (props.max - props.min)
  displayValue.value = formatDisplayValue(snappedValue)
  emit('update:modelValue', snappedValue)
  emit('change', snappedValue)
}

// 格式化显示值
function formatDisplayValue(val: number): string {
  if (props.step >= 1) return Math.round(val).toString()

  const decimalPlaces = Math.max(0, Math.ceil(-Math.log10(props.step)))
  return val.toFixed(decimalPlaces)
}

// 初始化显示值
onMounted(() => {
  displayValue.value = formatDisplayValue(actualValue.value)
})

// 监听外部值变化
watch(
  () => props.modelValue,
  (newVal) => {
    value.value = parseValue(newVal)
    displayValue.value = formatDisplayValue(actualValue.value)
  }
)

// 监听内部值变化
watch(value, (newVal) => {
  const mappedValue = newVal * (props.max - props.min) + props.min
  const snappedValue = snapToStep(mappedValue)
  emit('update:modelValue', snappedValue)
  displayValue.value = formatDisplayValue(snappedValue)
})

// 监听min/max变化
watch([() => props.min, () => props.max], () => {
  value.value = parseValue(actualValue.value)
})
</script>

<style lang="scss" scoped>
.input-draggable-progress-wrapper {
  width: 100%;
}
</style>
