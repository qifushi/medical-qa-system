<template>
  <el-dialog title="创建数据源" v-model="dialogVisible">
    <el-form
      ref="dataFormRef"
      :model="dataForm"
      :rules="rules"
      label-position="top"
      require-asterisk-position="right"
      @submit.prevent
    >
      <el-form-item prop="name" label="数据源名称">
        <el-input
          v-model="dataForm.name"
          placeholder="请输入数据源名称"
          maxlength="70"
          show-word-limit
        >
        </el-input>
      </el-form-item>
      <el-form-item prop="selectedTag" label="数据源标签">
        <SelectTags v-model="dataForm.selectedTag" @change="onTagChange"></SelectTags>
      </el-form-item>
      <el-form-item prop="describe" label="数据源描述">
        <el-input
          v-model="dataForm.describe"
          placeholder="描述该数据源的用途和内容"
          type="textarea"
          :rows="3"
          maxlength="200"
          show-word-limit
        >
        </el-input>
      </el-form-item>
      <el-form-item label="数据源类型" prop="type">
        <el-radio-group v-model="dataForm.type">
          <el-radio value="0">文件型</el-radio>
          <el-radio value="1">数据库</el-radio>
          <el-radio value="2" disabled>知识图谱</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item v-if="dataForm.type === '0'" label="上传文件" prop="fileList">
        <el-upload
          :webkitdirectory="false"
          class="w-full"
          drag
          multiple
          v-model:file-list="dataForm.fileList"
          action="#"
          :auto-upload="false"
          :show-file-list="false"
          accept=".txt, .md, .docx, .pdf"
          :limit="50"
          :on-exceed="onExceed"
          :on-change="fileHandleChange"
          @click.prevent="handlePreview(false)"
        >
          <img src="@/assets/upload-icon.svg" alt="" />
          <div class="el-upload__text">
            <p>
              拖拽文件至此上传或
              <em class="hover" @click.prevent="handlePreview(false)"> 选择文件 </em>
              <!-- <em class="hover" @click.prevent="handlePreview(true)"> 选择文件夹 </em> -->
            </p>
            <div class="upload__decoration">
              <p>
                支持格式：TXT、Markdown、PDF、DOCX、HTML 每次最多上传50个文件，每个文件不超过 100MB
              </p>
            </div>
          </div>
        </el-upload>
      </el-form-item>
      <!-- 数据库类型数据源 -->
      <template v-if="dataForm.type === '1'">
        <el-form-item label="数据库地址" prop="dataUrl">
          <el-input v-model="dataForm.dataUrl" placeholder="请输入数据库地址"> </el-input>
        </el-form-item>
        <el-form-item label="数据库账号" prop="dataAccount">
          <el-input v-model="dataForm.dataAccount" placeholder="请输入数据源账号"> </el-input>
        </el-form-item>
        <el-form-item label="数据库密码" prop="DataPassword">
          <el-input
            v-model="dataForm.DataPassword"
            placeholder="请输入数据库密码"
            type="password"
            show-password
          >
          </el-input>
        </el-form-item>
        <el-form-item label="拉取类型" prop="pullType">
          <el-radio-group v-model="dataForm.pullType">
            <el-radio value="1">手动</el-radio>
            <el-radio value="2">自动</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="dataForm.pullType === '2'" label="拉取频率" prop="pullFrequency">
          <el-radio-group v-model="dataForm.pullFrequency">
            <el-radio value="1">一天</el-radio>
            <el-radio value="2">三天</el-radio>
            <el-radio value="3">七天</el-radio>
          </el-radio-group>
        </el-form-item>
      </template>
    </el-form>
    <el-row :gutter="8" v-if="dataForm.fileList?.length && dataForm.type === '0'">
      <template v-for="(item, index) in dataForm.fileList" :key="index">
        <el-col :span="12" class="mb-8">
          <el-card shadow="never" class="file-List-card">
            <div class="flex-between">
              <div class="flex file-info">
                <img :src="getImgUrl(item && item?.name)" alt="" width="40" />
                <div class="ml-8 file-name-container">
                  <div class="file-name">
                    <auto-tooltip :content="item.name">
                      {{ item?.name }}
                    </auto-tooltip>
                  </div>
                  <el-text type="info" size="small">{{ filesize(item && item?.size) }}</el-text>
                </div>
              </div>
              <div class="file-actions">
                <el-button text @click="deleteFile(index)">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
            </div>
          </el-card>
        </el-col>
      </template>
    </el-row>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click.prevent="dialogVisible = false"> 取消 </el-button>
        <el-button type="primary" @click="submit(dataFormRef)" :loading="loading"> 创建 </el-button>
      </span>
    </template>
  </el-dialog>
</template>
<script setup lang="ts">
import trainSourceApi from '@/api/train-source'
import { MsgSuccess } from '@/utils/message'
import type { FormInstance } from 'element-plus'
import { reactive, ref, watch, nextTick } from 'vue'
import { MsgError } from '@/utils/message'
import { filesize, getImgUrl } from '@/utils/utils'
import type { UploadFiles } from 'element-plus'
import SelectTags from './SelectTags.vue'

const emit = defineEmits(['refresh'])

const dataFormRef = ref()
const dataForm = ref<any>({
  name: '',
  type: '1',
  fileList: '',
  dataUrl: '',
  dataAccount: '',
  pullType: '1',
  pullFrequency: '',
  selectedTag: {
    tags: [],
    custom_tags: []
  },
  user_id: ''
})

const rules = reactive({
  name: [
    { required: true, message: '请输入数据源名称', trigger: 'blur' },
    { max: 30, message: '长度最多 70 个字符', trigger: 'blur' }
  ],
  type: [{ required: true, message: '请选择数据源类型', trigger: 'change' }],
  selectedTag: [
    {
      required: true,
      message: '请选择数据源标签',
      trigger: 'change',
      validator: (rule: any, value: any) => {
        // 检查是否至少选择了一个标签（预定义或自定义）
        if (
          !value ||
          ((!value.tags || value.tags.length === 0) &&
            (!value.custom_tags || value.custom_tags.length === 0))
        ) {
          return new Error('请选择至少一个数据源标签')
        }
        return true
      }
    }
  ],
  fileList: [
    {
      required: true,
      message: '请上传文件',
      trigger: 'change',
      validator: (rule: any, value: string) => {
        if (dataForm.value.type === '0' && !value) {
          return new Error('请上传文件')
        }
        return true
      }
    }
  ],
  dataUrl: [
    {
      required: true,
      message: '请输入数据库地址',
      trigger: 'blur',
      validator: (rule: any, value: string) => {
        if (dataForm.value.type === '2' && !value) {
          return new Error('请输入数据库地址')
        }
        return true
      }
    },
    {
      pattern: /^[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})*(:([0-9]{1,5}))?$/,
      message: '请输入正确的数据库地址',
      trigger: 'blur'
    }
  ],
  dataAccount: [
    {
      required: true,
      message: '请输入数据库账号',
      trigger: 'blur',
      validator: (rule: any, value: string) => {
        if (dataForm.value.type === '2' && !value) {
          return new Error('请输入数据库账号')
        }
        return true
      }
    }
  ],
  DataPassword: [{ required: true, message: '请输入数据源密码', trigger: 'blur' }],
  pullType: [
    {
      required: true,
      message: '请选择拉取类型',
      trigger: 'change',
      validator: (rule: any, value: string) => {
        if (dataForm.value.type === '2' && !value) {
          return new Error('请选择拉取类型')
        }
        return true
      }
    }
  ],
  pullFrequency: [
    {
      required: true,
      message: '请选择拉取频率',
      trigger: 'change',
      validator: (rule: any, value: string) => {
        if (dataForm.value.type === '2' && dataForm.value.pullType === '2' && !value) {
          return new Error('请选择拉取频率')
        }
        return true
      }
    }
  ]
})

const dialogVisible = ref<boolean>(false)
const loading = ref(false)
const isEdit = ref(false)
interface TagOutput {
  tags: { key: string; value: string }[]
  custom_tags: { value: string }[]
}
watch(dialogVisible, (bool) => {
  if (!bool) {
    dataForm.value = {
      name: '',
      type: '0'
    }
    isEdit.value = false
    dataFormRef.value?.clearValidate()
  }
})

const open = (data: any) => {
  if (data) {
    dataForm.value.name = data.name
    dataForm.value.type = data.type
    dataForm.value.fileList = data.fileList
    dataForm.value.dataUrl = data.dataUrl
    dataForm.value.dataAccount = data.dataAccount
    dataForm.value.pullType = data.pullType
    dataForm.value.pullFrequency = data.pullFrequency
    isEdit.value = true
  }
  dialogVisible.value = true
}

const submit = async (formEl: FormInstance | undefined) => {
  console.log('[ dataForm.value ] >', dataForm.value)
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      // 准备提交的数据
      const submitData = {
        ...dataForm.value,
        // 将标签数据转换为API需要的格式
        tags: dataForm.value.selectedTag.tags,
        custom_tags: dataForm.value.selectedTag.custom_tags
      }
      console.log(
        '%c [ submitData ]-297',
        'font-size:13px; background:pink; color:#bf2c9f;',
        submitData
      )
      if (dataForm.value.type === '0') {
        trainSourceApi
          .postTrainSource(submitData, loading)
          .then((res) => {
            console.log('%c [ res ]-304', 'font-size:13px; background:pink; color:#bf2c9f;', res)
            if (res.data.id) {
              // 如果有文件列表且不为空
              if (dataForm.value.fileList && dataForm.value.fileList.length > 0) {
                // 创建上传进度计数器
                let uploadedCount = 0
                const totalFiles = dataForm.value.fileList.length

                // 遍历文件列表，逐个上传
                dataForm.value.fileList.forEach((file: any) => {
                  // 为每个文件创建一个FormData对象
                  const formData = new FormData()
                  formData.append('file', file.raw) // 添加文件原始数据
                  formData.append('type', dataForm.value.type)
                  formData.append('name', file.name)
                  console.log('[ formData ] >', formData.get('file'), file)
                  // 上传单个文件
                  trainSourceApi
                    .uploadTrainSource(res.data.id, formData, loading)
                    .then(() => {
                      uploadedCount++
                      // 当所有文件都上传完成时，显示成功消息并关闭对话框
                      if (uploadedCount === totalFiles) {
                        emit('refresh')
                        MsgSuccess('新增成功')
                        dialogVisible.value = false
                      }
                    })
                    .catch((error) => {
                      console.error('文件上传失败:', error)
                      MsgError(`文件 ${file.name} 上传失败`)
                      uploadedCount++
                    })
                })
              } else {
                // 没有文件需要上传，直接完成
                emit('refresh')
                MsgSuccess('新增成功')
                dialogVisible.value = false
              }
            }
          })
          .catch((error) => {
            console.error('创建数据源失败:', error)
            MsgError('创建数据源失败')
          })
      }
    }
  })
}
const onExceed = () => {
  MsgError('每次最多上传50个文件')
}
// 上传on-change事件
const fileHandleChange = (file: any, fileList: UploadFiles) => {
  console.log('[ dataForm.fileList ] >', dataForm.value.fileList, fileList)
  //1、判断文件大小是否合法，文件限制不能大于100M
  const isLimit = file?.size / 1024 / 1024 < 100
  if (!isLimit) {
    MsgError('文件大小超过 100MB')
    fileList.splice(-1, 1) //移除当前超出大小的文件
    return false
  }
}
const handlePreview = (bool: boolean) => {
  let inputDom: any = null
  nextTick(() => {
    if (document.querySelector('.el-upload__input') != null) {
      inputDom = document.querySelector('.el-upload__input')
      inputDom.webkitdirectory = bool
    }
  })
}
function deleteFile(index: number) {
  dataForm.value.fileList.splice(index, 1)
}

function onTagChange(val: TagOutput) {
  console.log('选中的标签:', val)
}
defineExpose({ open })
</script>
<style lang="scss" scope>
.upload__decoration {
  font-size: 12px;
  line-height: 20px;
  color: var(--el-text-color-secondary);
}
.el-upload__text {
  .hover:hover {
    color: var(--el-color-primary-light-5);
  }
}
.file-info {
  flex: 1;
  min-width: 0; /* 关键：允许flex子项收缩 */
  overflow: hidden;
}
.file-name-container {
  flex: 1;
  min-width: 0;
  overflow: hidden;
}
.file-name {
  width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.file-actions {
  display: flex;
  justify-content: end;
  align-items: center;
  min-width: 40px; /* 确保按钮区域有最小宽度 */
  flex-shrink: 0; /* 防止按钮区域被压缩 */
}
</style>
