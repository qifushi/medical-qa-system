<template>
  <el-dialog :title="title" v-model="dialogVisible">
    <el-form
      ref="dataFormRef"
      :model="dataForm"
      :rules="rules"
      label-position="top"
      require-asterisk-position="right"
      @submit.prevent
    >
      <el-row :gutter="20">
        <el-col :span="24">
          <el-form-item prop="model_name" label="模型名称">
            <el-select
              v-model="dataForm.model_name"
              @change="handleModelNameChange"
              placeholder="请选择模型名称"
              filterable
              clearable
              style="width: 100%;"
               popper-class="custom-model-select-dropdown"
              :loading="modelOptionsLoading"
            >
              <el-option
                v-for="item in modelOptions"
                :key="item.value"
                :label="item.label"
                :value="item.label"
              />
              
              <template #footer v-if="paginationConfig.total > paginationConfig.page_size">
                <div class="select-pagination p-2">
                  <el-pagination
                    v-model:current-page="paginationConfig.current_page"
                    :page-size="paginationConfig.page_size"
                    :total="paginationConfig.total"
                    layout="prev, pager, next,total"
                   size="small"
                    @current-change="handleModelPageChange"
                    hide-on-single-page
                  />
                </div>
              </template>
              <template #empty >
              <div v-loading="modelOptionsLoading" style="height: 254px;" class="flex-center">
                <el-empty v-if="modelOptions.length === 0"></el-empty>
              </div>
                </template>
            </el-select> 
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="推理框架" prop="infer_framework">
            <el-radio-group v-model="dataForm.infer_framework">
              <el-radio value="vllm">vllm</el-radio>
              <el-radio value="sglang" disabled>sglang</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item prop="model_path" label="模型路径">
            <template #label>
              <span class="form-label-flex">
                模型路径
                <el-tooltip
                  content="模型路径是指模型文件所在的目录或文件路径，通常用于加载和使用模型。"
                  placement="top"
                >
                  <span class="icon-flex">
                    <AppIcon iconName="InfoFilled"></AppIcon>
                  </span>
                </el-tooltip>
              </span>
            </template>
            <div class="input-button-group">
              <el-input
                v-model="dataForm.model_path"
                placeholder="选择模型后自动填充"
                disabled
              ></el-input>
              <!-- <el-button type="primary" class="export-button">导出</el-button> -->
            </div>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item prop="model_code" label="模型编码">
            <el-input
              v-model="dataForm.model_code"
              placeholder="首字母为字母，包含字母、数字、下划线和 - 号，长度不超过8个字符"
              maxlength="8"
              show-word-limit
            >
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item prop="api_key" label="API Key">
            <el-input
              v-model="dataForm.api_key"
              placeholder="以  sk-  开头，包含字母、数字、下划线和 - 号，长度不超过32个字符"
            >
              <template #prepend>sk-</template>
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item
            prop="gpu_memory_utilization"
            label="GPU内存利用率"
            placeholder="请输入0-1之间的数字"
          >
            <template #label>
              <span class="form-label-flex">
                GPU内存利用率
                <el-tooltip
                  content="GPU 内存使用率是指当前 GPU 显卡的显存（Video Memory）被占用的百分比，可取0-1。"
                  placement="top"
                >
                  <span class="icon-flex">
                    <AppIcon iconName="InfoFilled"></AppIcon>
                  </span>
                </el-tooltip>
              </span>
            </template>
            <el-input v-model="dataForm.gpu_memory_utilization"> </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item prop="context_length" label="最大上下文长度">
            <template #label>
              <span class="form-label-flex">
                最大上下文长度
                <el-tooltip
                  content="最大上下文长度指的是 模型一次输入可以处理的最大 token（词元）数。"
                  placement="top"
                >
                  <span class="icon-flex">
                    <AppIcon iconName="InfoFilled"></AppIcon>
                  </span>
                </el-tooltip>
              </span>
            </template>
            <el-input v-model.number="dataForm.context_length" placeholder="默认可不填写">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item prop="publish_ip" label="发布IP">
            <el-input v-model="dataForm.publish_ip" disabled> </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item prop="publish_port" label="发布端口">
            <el-input
              v-model.number="dataForm.publish_port"
              placeholder="请输入发布端口，范围8000-8087，不能重复"
            >
            </el-input>
          </el-form-item>
        </el-col>

        <el-col :span="24">
          <el-form-item prop="model_desc" label="模型描述">
            <el-input
              v-model="dataForm.model_desc"
              placeholder="描述该模型的用途和内容"
              type="textarea"
              :rows="3"
              maxlength="256"
              show-word-limit
            >
            </el-input>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click.prevent="dialogVisible = false"> 取消 </el-button>
        <el-button type="primary" @click="submit(dataFormRef)" :loading="loading"> 保存 </el-button>
      </span>
    </template>
  </el-dialog>
</template>
<script setup lang="ts">
import modelReleaseApi from '@/api/train-release'
import modelEvalApi from '@/api/train-evaluation'
import { MsgSuccess } from '@/utils/message'
import type { FormInstance } from 'element-plus'
import { reactive, ref } from 'vue'
import AppIcon from '@/components/icons/AppIcon.vue'
import { type ModelReleaseType } from '@/api/type/model-release'

const emit = defineEmits(['refresh'])

const dataFormRef = ref()
const dataForm = ref<ModelReleaseType>({
  model_path: '',
  infer_framework: 'vllm',
  model_name: '',
  model_code: '',
  publish_port: null,
  publish_ip: import.meta.env.VITE_MODEL_PUBLISH_IP,
  api_key: '',
  context_length: 4096,
  model_desc: '',
  publish_status: 0,
  health_check_url: '',
  username: '',
  gpu_memory_utilization: 0.2
})

const rules = reactive({
  model_name: [
    { required: true, message: '请输入数据源名称', trigger: 'blur' },
    { max: 30, message: '长度最多 30 个字符', trigger: 'blur' }
  ],
  infer_framework: [{ required: true, message: '请选择推理框架', trigger: 'change' }],

  model_path: [{ required: true, message: '请输入模型路径', trigger: 'blur' }],

  model_code: [
    { required: true, message: '请输入模型编码', trigger: 'blur' },
    {
      pattern: /^[a-zA-Z][a-zA-Z0-9_-]{7}$/,
      message: '首字母为字母，包含字母、数字、下划线和 - 号，长度为8个字符',
      trigger: 'blur'
    }
  ],

  publish_port: [
    { required: true, message: '请输入发布端口', trigger: 'blur' },
    {
      pattern: /^(800[0-9]|80[1-7][0-9]|808[0-7])$/,
      message: '请输入有效的端口号(8000-8087)',
      trigger: 'blur'
    }
  ],
  api_key: [
    { required: true, message: '请输入API Key', trigger: 'blur' },
    {
      pattern: /^[a-zA-Z0-9_-]{1,32}$/,
      message: '包含字母、数字、下划线和 - 号，长度不超过32个字符',
      trigger: 'blur'
    }
  ],
  gpu_memory_utilization: [
    { required: true, message: '请输入GPU内存利用率', trigger: 'blur' },
    {
      validator: (rule: any, value: any, callback: any) => {
        if (value === null || value === undefined || value === '') {
          callback(new Error('请输入GPU内存利用率'))
          return
        }
        const num = Number(value)
        if (isNaN(num)) {
          callback(new Error('请输入有效的数字'))
          return
        }
        if (num < 0 || num > 1) {
          callback(new Error('GPU内存利用率取值在0-1之间'))
          return
        }
        callback()
      },
      trigger: 'blur'
    }
  ]
})

const dialogVisible = ref<boolean>(false)
const loading = ref(false)
const isEdit = ref(false)
const title = ref('')
// watch(dialogVisible, (bool) => {
//   if (!bool) {
//     dataForm.value = {
//       model_path: '',
//       infer_framework: 'vllm',
//       model_name: '',
//       model_code: '',
//       publish_port: null,
//       publish_ip: import.meta.env.VITE_MODEL_PUBLISH_IP,
//       api_key: '',
//       context_length: null,
//       model_desc: '',
//       publish_status: 0,
//       health_check_url: '',
//       username: ''
//     }
//     isEdit.value = false
//     dataFormRef.value?.clearValidate()
//   }
// })
// 生成随机字符串的工具函数
const generateRandomString = (length: number, includeNumbers = true, includeSpecial = false) => {
  const letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
  const numbers = '0123456789'
  const special = '_-'

  let chars = letters
  if (includeNumbers) chars += numbers
  if (includeSpecial) chars += special

  let result = ''
  // 确保首字母是字母
  result += letters[Math.floor(Math.random() * letters.length)]

  // 生成剩余字符
  for (let i = 1; i < length; i++) {
    result += chars[Math.floor(Math.random() * chars.length)]
  }

  return result
}

// 生成符合条件的模型编码
const generateModelCode = () => {
  return generateRandomString(8, true, true) // 8位，包含数字和特殊字符
}

// 生成符合条件的API Key（不包含sk-前缀）
const generateApiKey = () => {
  return generateRandomString(32, true, true) // 29位，包含数字和特殊字符
}
const open = (data: any) => {
  isEdit.value = true
  dataFormRef.value?.clearValidate()
  // 获取模型选项数据
  initModelOptions()

  if (data?.id) {
    title.value = '编辑模型发布'
    dataForm.value = {
      ...data,
      api_key:
        data.api_key && data.api_key.startsWith('sk-') ? data.api_key.substring(3) : data.api_key
    }
  } else {
    title.value = '创建模型发布'
    dataForm.value = {
      model_path: '',
      infer_framework: 'vllm',
      model_name: '',
      model_code: generateModelCode(),
      publish_port: null,
      publish_ip: import.meta.env.VITE_MODEL_PUBLISH_IP,
      api_key: generateApiKey(),
      context_length: 4096,
      model_desc: '',
      publish_status: 0,
      health_check_url: '',
      username: '',
      gpu_memory_utilization: 0.2
    }
  }

  dialogVisible.value = true
}

const submit = async (formEl: FormInstance | undefined) => {
  console.log('[ dataForm.value ] >', dataForm.value)
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      let data = {
        ...dataForm.value,
        api_key: `sk-${dataForm.value.api_key}`
      }
      if (dataForm.value.id) {
        console.log(
          '%c [ dataForm.value.id ]-251',
          'font-size:13px; background:pink; color:#bf2c9f;',
          data
        )
        // 编辑模式
        modelReleaseApi.putModelRelease(dataForm.value.id, data, loading).then((res) => {
          console.log('%c [ res ]-247', 'font-size:13px; background:pink; color:#bf2c9f;', res)
          emit('refresh')
          MsgSuccess('修改成功')
          dialogVisible.value = false
        })
      } else {
        // 新增模式
        modelReleaseApi.addModelRelease(data, loading).then((res) => {
          console.log('%c [ res ]-253', 'font-size:13px; background:pink; color:#bf2c9f;', res)

          emit('refresh')
          MsgSuccess('创建成功')
          dialogVisible.value = false
        })
      }
    }
  })
}
const modelOptions = ref<Array<{ label: string; value: string; model_path: '' }>>([])
const modelOptionsLoading = ref(false)

const paginationConfig = reactive({
  current_page: 1,
  page_size: 10,
  total: 0
})
// 获取模型选项数据
const getModelOptions = async (page = 1) => {
  console.log('wochufale',page)

  try {
    modelOptionsLoading.value = true
    paginationConfig.current_page = page
    const res = await modelEvalApi.postModelEvaList(paginationConfig, { export_status: 1 })
    if (res.code === 200 && res.data?.records) {
      paginationConfig.total = res.data.total

      console.log(
        '%c [  modelOptions.value  ]-393',
        'font-size:13px; background:pink; color:#bf2c9f;',
        modelOptions.value
      )
      modelOptions.value = res.data.records.map((item: any) => ({
        label: item.model_name,
        value: item.model_name,
        model_path: item.export_path || item.model_path || '',
        id: item.id
      }))

      console.log('加载完成，总数据:', modelOptions.value.length)
    }
  } catch (error) {
    console.error('获取模型列表失败:', error)
  } finally {
    modelOptionsLoading.value = false
  }
}
// 处理分页变化
const handleModelPageChange = (page: number) => {
  getModelOptions(page)
}
// 初始化加载第一页数据
const initModelOptions = async () => {
  paginationConfig.current_page = 1
  paginationConfig.total = 0
  modelOptions.value = []
  await getModelOptions(1)
}
// 处理模型名称选择变化
const handleModelNameChange = (value: string) => {
  console.log('%c [ value ]-410', 'font-size:13px; background:pink; color:#bf2c9f;', value)
  if (value) {
    // 根据选中的值找到对应的模型选项
    const selectedModel = modelOptions.value.find((item) => item.value === value)
    if (selectedModel && selectedModel.model_path) {
      // 自动填充模型路径
      dataForm.value.model_path = selectedModel.model_path
    }
  } else {
    // 清空选择时，也清空模型路径
    dataForm.value.model_path = ''
  }
}
// onMounted(() => {
//   initModelOptions()
// })
defineExpose({ open })
</script>
<style lang="scss" scope>
.form-label-flex {
  display: inline-flex;
  align-items: center;
  min-width: 0;
  .icon-flex {
    display: flex;
    align-items: center;
    margin-left: 4px;
  }
}
.input-button-group {
  display: flex;
  gap: 8px;
  width: 100%;

  .flex-input {
    flex: 1;
    min-width: 0;
  }

  .export-button {
    flex-shrink: 0;
    width: 60px;
  }
}

</style>
<style lang="scss">
.custom-model-select-dropdown {
  .el-select-dropdown__wrap {
    min-height: 274px !important;
  }
}
</style>