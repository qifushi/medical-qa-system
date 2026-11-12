<template>
  <el-dialog title="新增指令" v-model="dialogVisible">
    <el-form
      ref="newOrderRef"
      :model="newOrderForm"
      :rules="rules"
      label-position="top"
      require-asterisk-position="right"
      @submit.prevent
    >
      <el-form-item label="指令标题" prop="name">
        <el-input v-model="newOrderForm.name" placeholder="请输入指令标题"> </el-input>
      </el-form-item>
      <el-form-item label="指令分类" prop="type">
        <el-select v-model="newOrderForm.type" placeholder="请选择指令分类">
          <el-option
            v-for="item in type"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="指令内容" prop="content">
        <el-input
          v-model="newOrderForm.content"
          placeholder="请输入指令内容，例如：帮我提炼这篇文档的中心思想"
          type="textarea"
          maxlength="1000"
          show-word-limit
          :rows="12"
          :autosize="false"
          class="fixed-textarea"
        >
        </el-input>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click.prevent="dialogVisible = false"> 取消 </el-button>
        <el-button type="primary" @click="submit(newOrderRef)" :loading="loading"> 保存 </el-button>
      </span>
    </template>
  </el-dialog>
</template>
<script setup lang="ts">
import customApi from '@/api/custom'
import type { CustomFormType } from '@/api/type/custom'
import { MsgSuccess } from '@/utils/message'
import type { FormInstance, FormRules } from 'element-plus'
import { reactive, ref, watch } from 'vue'

const emit = defineEmits(['refresh'])

const newOrderRef = ref()
const newOrderForm = ref<any>({
  name: '',
  type: '',
  content: ''
})

const rules = reactive<FormRules<CustomFormType>>({
  name: [
    {
      required: true,
      message: '请输入指令标题',
      trigger: 'blur'
    }
  ],
  type: [
    {
      required: true,
      message: '请选择指令分类',
      trigger: 'blur'
    }
  ],
  content: [
    {
      required: true,
      message: '请输入指令内容',
      trigger: 'blur'
    }
  ]
})
const dialogVisible = ref<boolean>(false)
const loading = ref(false)
const userId = ref('')

watch(dialogVisible, (bool) => {
  if (!bool) {
    newOrderForm.value = {
      name: '',
      type: '',
      content: ''
    }
  }
})
const type = [
  {
    value: 'finance',
    label: '财务'
  },
  {
    value: 'contract',
    label: '合同'
  },
  {
    value: '"project"',
    label: '项目'
  },
  {
    value: '"fund"',
    label: '经费'
  }
]
const open = () => {
  dialogVisible.value = true
  newOrderRef.value?.clearValidate()
}

const submit = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      customApi.postCustom(newOrderForm.value).then((res) => {
        MsgSuccess('新增成功')
        emit('refresh')
        dialogVisible.value = false
      })
    }
  })
}

defineExpose({ open })
</script>
<style lang="scss" scope>
.fixed-textarea textarea {
  resize: none; /* 禁用调整大小 */
}
</style>
