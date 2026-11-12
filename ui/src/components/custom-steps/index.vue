// file: e:/project-jr/smartbrain/v3.4.9/ui/src/components/custom-steps/index.vue

<template>
  <div class="custom-steps">
    <div
      v-for="(step, index) in steps"
      :key="index"
      class="step-item"
      :class="{
        completed: index < modelValue,
        active: index === modelValue,
        incomplete: index > modelValue
      }"
      @click="goToStep(index)"
    >
      <div class="step-indicator">
        <div v-if="index < modelValue" class="completed-icon">✓</div>
        <div v-else class="step-number">{{ index + 1 }}</div>
      </div>
      <div class="step-title">{{ step.title }}</div>

      <!-- 虚线连接器（除最后一个节点） -->
      <div
        v-if="index < steps.length - 1"
        class="step-connector"
        :class="{ completed: index < modelValue }"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

// 定义props接收外部传入的值
const props = defineProps({
  modelValue: {
    type: Number,
    required: true
  },
  disabled: {
    type: Boolean,
    default: false
  },
  steps: {
    type: Array,
    default: () => []
  }
})

// 定义emit事件
const emit = defineEmits(['update:modelValue'])

// 跳转到指定步骤
const goToStep = (index) => {
  if (props.disabled) return
  if (index <= props.modelValue && index !== props.modelValue.length - 1) {
    emit('update:modelValue', index)
  }
}
</script>

<style scoped>
.custom-steps {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.step-item {
  flex: 1;
  display: flex;
  align-items: center;
  position: relative;
  justify-content: center;
  padding: 10px 0;
}

.step-item:not(:last-child)::after {
  content: '';
  position: absolute;
  left: 50%;
  height: 80%;
  top: 60%;
  bottom: -10px;
  margin-left: -1px;
  width: 2px;
  background: linear-gradient(to bottom, #c0c4cc 50%, transparent 50%);
  background-size: 2px 10px;
  background-repeat: repeat-y;
}

.step-item.completed:not(:last-child)::after {
  background: linear-gradient(to bottom, #409eff 50%, transparent 50%);
  background-size: 2px 10px;
  background-repeat: repeat-y;
}

.step-indicator {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
  z-index: 1;
  flex-shrink: 0;
}

.step-item.completed .step-indicator {
  background-color: #409eff;
  color: white;
}

.step-item.active .step-indicator {
  border: 2px solid #409eff;
  color: #409eff;
}

.step-item.incomplete .step-indicator {
  border: 2px solid #c0c4cc;
  color: #c0c4cc;
}

.completed-icon,
.step-number {
  font-size: 12px;
  font-weight: bold;
}

.step-title {
  font-size: 14px;
}

.step-item.completed .step-title {
  color: #409eff;
  font-weight: bold;
}

.step-item.active .step-title {
  color: #409eff;
  font-weight: bold;
}

.step-item.incomplete .step-title {
  color: #909399;
}

.step-connector {
  position: absolute;
  left: 50%;
  height: 80%;
  top: 60%;
  bottom: -10px;
  margin-left: -1px;
  width: 2px;
  background: linear-gradient(to bottom, #c0c4cc 50%, transparent 50%);
  background-size: 2px 10px;
  background-repeat: repeat-y;
}

.step-connector.completed {
  background: linear-gradient(to bottom, #409eff 50%, transparent 50%);
  background-size: 2px 10px;
  background-repeat: repeat-y;
}
</style>
