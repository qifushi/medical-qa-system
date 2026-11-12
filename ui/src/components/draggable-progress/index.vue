<template>
  <div class="draggable-progress-wrapper">
    <div class="progress-container">
      <span class="min-label">{{ formatLabel(min) }}</span>
      <div class="draggable-progress-container" ref="container">
        <div class="progress-track" @click="handleTrackClick">
          <div class="progress-fill" :style="{ width: thumbPosition + '%' }"></div>
        </div>
        <div
          class="progress-thumb"
          ref="thumb"
          :style="{ left: thumbPosition + '%' }"
          @mousedown="startDrag"
        >
          <div class="progress-tooltip">{{ formatDisplayValue(actualValue) }}</div>
        </div>
      </div>
      <span class="max-label">{{ formatLabel(max) }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'

interface Props {
  modelValue: number | string | undefined
  min: number // 必填项
  max: number // 必填项
  step?: number // 新增步长属性
}

const props = withDefaults(defineProps<Props>(), {
  step: 1, // 默认步长为1
  modelValue: 0 // 添加默认值
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: number): void
  (e: 'change', value: number): void
}>()

const container = ref<HTMLElement | null>(null)
const thumb = ref<HTMLElement | null>(null)
const isDragging = ref(false)
const containerWidth = ref(0)
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
  // 按步长对齐值
  return snapToStep(rawValue)
})

// 计算滑块位置百分比
const thumbPosition = computed(() => {
  return Math.min(100, Math.max(0, value.value * 100))
})

// 按步长对齐值（优化精度处理）
function snapToStep(val: number): number {
  // 计算步数并四舍五入
  const steps = Math.round((val - props.min) / props.step)
  let result = props.min + steps * props.step

  // 确保值在[min, max]范围内
  result = Math.max(props.min, Math.min(props.max, result))

  // 根据步长精度返回适当格式的值
  if (props.step >= 1) {
    return Math.round(result) // 步长为整数时返回整数
  } else if (props.step >= 0.1) {
    return parseFloat(result.toFixed(1)) // 步长0.1时保留1位小数
  } else if (props.step >= 0.01) {
    return parseFloat(result.toFixed(2)) // 步长0.01时保留2位小数
  } else {
    return parseFloat(result.toFixed(3)) // 其他情况保留3位小数
  }
}

// 获取小数位数
function getDecimalPlaces(num: number): number {
  const decimalPart = num.toString().split('.')[1]
  return decimalPart ? decimalPart.length : 0
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

// 格式化显示值（优化精度处理）
function formatDisplayValue(val: number): string {
  if (props.step >= 1) {
    return Math.round(val).toString() // 步长为整数时显示整数
  } else if (props.step >= 0.1) {
    return val.toFixed(1) // 步长0.1时显示1位小数
  } else if (props.step >= 0.01) {
    return val.toFixed(2) // 步长0.01时显示2位小数
  } else {
    return val.toFixed(3) // 其他情况显示3位小数
  }
}

// 格式化标签值（与显示值一致）
function formatLabel(val: number): string {
  return formatDisplayValue(val)
}

// 更新容器宽度
function updateContainerWidth() {
  if (container.value) {
    containerWidth.value = container.value.offsetWidth
  }
}

// 处理轨道点击
function handleTrackClick(e: MouseEvent) {
  if (isDragging.value) return
  if (!container.value) return

  const rect = container.value.getBoundingClientRect()
  const clickX = e.clientX - rect.left
  const percentage = Math.min(1, Math.max(0, clickX / containerWidth.value))

  // 计算实际值
  const rawValue = percentage * (props.max - props.min) + props.min
  // 按步长对齐
  const snappedValue = snapToStep(rawValue)
  // 映射回百分比
  const snappedPercentage = (snappedValue - props.min) / (props.max - props.min)

  if (snappedPercentage !== value.value) {
    value.value = snappedPercentage
    emit('change', actualValue.value)
  }
}

// 开始拖拽
function startDrag(e: MouseEvent) {
  e.preventDefault()
  isDragging.value = true
  window.addEventListener('mousemove', handleDrag)
  window.addEventListener('mouseup', stopDrag)
}

// 处理拖拽
function handleDrag(e: MouseEvent) {
  if (!isDragging.value || !container.value) return

  const rect = container.value.getBoundingClientRect()
  const dragX = e.clientX - rect.left
  const percentage = Math.min(1, Math.max(0, dragX / containerWidth.value))

  // 计算实际值
  const rawValue = percentage * (props.max - props.min) + props.min
  // 按步长对齐
  const snappedValue = snapToStep(rawValue)
  // 映射回百分比
  const snappedPercentage = (snappedValue - props.min) / (props.max - props.min)

  if (snappedPercentage !== value.value) {
    value.value = snappedPercentage
    emit('change', actualValue.value)
  }
}

// 停止拖拽
function stopDrag() {
  isDragging.value = false
  window.removeEventListener('mousemove', handleDrag)
  window.removeEventListener('mouseup', stopDrag)
}

// 监听外部值变化
watch(
  () => props.modelValue,
  (newVal) => {
    value.value = parseValue(newVal)
  }
)

// 监听内部值变化
watch(value, (newVal) => {
  // 将0-1范围的值映射回实际范围
  const mappedValue = newVal * (props.max - props.min) + props.min
  const snappedValue = snapToStep(mappedValue)
  emit('update:modelValue', snappedValue)
})

// 监听min/max变化
watch([() => props.min, () => props.max], () => {
  // 当范围变化时重新映射当前值
  value.value = parseValue(actualValue.value)
})

// 生命周期钩子
onMounted(() => {
  updateContainerWidth()
  window.addEventListener('resize', updateContainerWidth)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateContainerWidth)
  window.removeEventListener('mousemove', handleDrag)
  window.removeEventListener('mouseup', stopDrag)
})
</script>

<style lang="scss" scoped>
.draggable-progress-wrapper {
  width: 100%;
  padding: 0;
  height: 32px;
  display: flex;
  align-items: center;
}

.progress-container {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  height: 100%;
}

.min-label,
.max-label {
  font-size: 12px;
  color: #606266;
  min-width: 40px;
  text-align: center;
}

.draggable-progress-container {
  flex: 1;
  cursor: pointer;
  height: 100%;
  display: flex;
  align-items: center;
  position: relative;
}

.progress-track {
  position: relative;
  width: 100%;
  height: 6px;
  background-color: #ebeef5;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  position: absolute;
  height: 100%;
  background-color: #409eff;
  border-radius: 3px;
}

.progress-thumb {
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 13px;
  height: 13px;
  background-color: white;
  border: 2px solid #409eff;
  border-radius: 50%;
  box-shadow:
    0 0 3px rgba(64, 158, 255, 0.8),
    0 2px 4px rgba(0, 0, 0, 0.3);
  cursor: pointer;
  z-index: 10;
  transition: transform 0.1s;

  &:hover,
  &:active {
    transform: translate(-50%, -50%) scale(1.2);
    box-shadow:
      0 0 8px rgba(64, 158, 255, 1),
      0 3px 10px rgba(0, 0, 0, 0.4);
  }
}

.progress-tooltip {
  position: absolute;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  padding: 0 10px;
  background-color: #303133;
  color: white;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.2s;
  pointer-events: none;

  &::after {
    content: '';
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    border-width: 5px;
    border-style: solid;
    border-color: #303133 transparent transparent transparent;
  }
}

.progress-thumb:hover .progress-tooltip {
  opacity: 1;
}
</style>
