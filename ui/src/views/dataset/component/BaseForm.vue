<template>
  <h4 class="title-decoration-1 mb-16">基本信息</h4>
  <el-form
    ref="FormRef"
    :model="form"
    :rules="rules"
    label-position="top"
    require-asterisk-position="right"
  >
    <el-form-item label="知识库名称" prop="name">
      <el-input
        v-model="form.name"
        placeholder="请输入知识库名称"
        maxlength="64"
        show-word-limit
        @blur="form.name = form.name.trim()"
      />
    </el-form-item>
    <el-form-item label="知识库描述" prop="desc">
      <el-input
        v-model="form.desc"
        type="textarea"
        placeholder="描述知识库的内容，详尽的描述将帮助AI能深入理解该知识库的内容，能更准确的检索到内容，提高该知识库的命中率。"
        maxlength="256"
        show-word-limit
        :autosize="{ minRows: 3 }"
        @blur="form.desc = form.desc.trim()"
      />
    </el-form-item>
    <el-form-item label="知识库分类" prop="category">
      <el-radio-group v-model="form.category">
      <el-radio v-for="item in categoryOptions" :value="item.value" >{{ item.label }}</el-radio>
    </el-radio-group>
    </el-form-item>
  </el-form>
</template>
<script setup lang="ts">
import type { datasetData } from '@/api/type/dataset'
import useStore from '@/stores'
import { isAllPropertiesEmpty } from '@/utils/utils'
import { computed, onMounted, onUnmounted, reactive, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps({
  data: {
    type: Object,
    default: () => {}
  }
})
const route = useRoute()
const {
  params: { type }
} = route
const isCreate = type === 'create'
const { dataset } = useStore()
const baseInfo = computed(() => dataset.baseInfo)
const form = ref<datasetData>({
  name: '',
  desc: '',
  category:'0'
})

const rules = reactive({
  name: [{ required: true, message: '请输入知识库名称', trigger: 'blur' }],
  desc: [{ required: true, message: '请选择知识库分类', trigger: 'blur' }]
})
const FormRef = ref()

const categoryOptions = [
  {
    value: '0',
    label: '未分类',
  },
  {
    value: '1',
    label: '科研知识',
  },
  {
    value: '2',
    label: '财务知识',
  },
  {
    value: '3',
    label: '人事知识',
  },
]
watch(
  () => props.data,
  (value) => {
    if (value && JSON.stringify(value) !== '{}') {
      form.value.name = value.name
      form.value.desc = value.desc
      form.value.category = value.category
    }
  },
  {
    immediate: true
  }
)

watch(form.value, (value) => {
  if (isAllPropertiesEmpty(value)) {
    dataset.saveBaseInfo(null)
  } else {
    if (isCreate) {
      dataset.saveBaseInfo(value)
    }
  }
})

/*
  表单校验
*/
function validate() {
  if (!FormRef.value) return
  return FormRef.value.validate((valid: any) => {
    return valid
  })
}

onMounted(() => {
  if (baseInfo.value) {
    form.value = baseInfo.value
  }
})
onUnmounted(() => {
  form.value = {
    name: '',
    desc: '',
    category:''
  }
})

defineExpose({
  validate,
  form
})
</script>
<style scoped lang="scss"></style>
