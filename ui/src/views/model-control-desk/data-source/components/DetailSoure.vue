<template>
  <div class="source-main-container">
    <LeftTagsList></LeftTagsList>
    <LayoutContainer :header="'数据源详情'" class="main-container detail-container">
      <!-- 返回上一级 -->
      <template #backButton>
        <back-button @click="back"></back-button>
      </template>
      <div class="detail-container__steps flex" style="height: calc(100vh - 112px); overflow: auto">
        <div class="p-24" style="width: 100%">
          <h4 class="title-decoration-1 mb-8">基本信息</h4>
          <div class="baseInfo-container" v-loading="baseLoading">
            <el-row :gutter="20">
              <el-col :span="20" style="font-size: 18px; line-height: 32px">
                <span v-if="!isEditingName">
                  {{ dataForm.name }}
                  <el-button text icon="Edit" @click="startEditing('name')"></el-button>
                </span>
                <div v-else class="flex align-center">
                  <el-input
                    v-model="editingNameValue"
                    @keyup.enter="saveEditing('name')"
                  ></el-input>
                  <el-button type="primary" text @click="saveEditing('name')">
                    <el-icon><Select /></el-icon>
                  </el-button>
                  <el-button text @click="cancelEditing('name')">
                    <el-icon><CloseBold /></el-icon>
                  </el-button>
                </div>
              </el-col>
              <el-col :span="4" class="flex-end">
                <el-tag type="success" effect="plain" style="border-radius: 3px" class="ml-24"
                  >文件型</el-tag
                >
              </el-col>
            </el-row>
            <div class="description-container">
              <span v-if="!isEditingDesc">
                {{ dataForm.describe }}
                <el-button text icon="Edit" @click="startEditing('describe')"></el-button>
              </span>
              <div v-else class="flex align-center">
                <el-input
                  autosize
                  type="textarea"
                  v-model="editingDescValue"
                  @keyup.enter.prevent="handleTextareaEnter('describe')"
                ></el-input>
                <el-button type="primary" text @click="saveEditing('describe')">
                  <el-icon><Select /></el-icon>
                </el-button>
                <el-button text @click="cancelEditing('describe')">
                  <el-icon><CloseBold /></el-icon>
                </el-button>
              </div>
            </div>
            <div style="display: flex; gap: 4px; flex-wrap: wrap">
              <div v-for="tag in dynamicTags" :key="tag" style="margin-bottom: 4px">
                <el-popconfirm
                  title="确定要删除此标签吗?"
                  confirm-button-text="确认"
                  cancel-button-text="取消"
                  @confirm="handleClose(tag)"
                  v-model:visible="tagVisibleMap[tag]"
                >
                  <template #reference>
                    <el-tag class="tootip-tags custom-tag">
                      <span class="tag-content">{{ tag }}</span>
                      <el-icon class="tag-close-icon" @click.stop="showConfirm(tag)">
                        <Close />
                      </el-icon>
                    </el-tag>
                  </template>
                </el-popconfirm>
              </div>
              <!-- 添加新标签 -->
              <div style="margin-bottom: 4px">
                <el-input
                  v-if="inputVisible"
                  ref="InputRef"
                  v-model="inputValue"
                  class="tag-input"
                  size="small"
                  @keyup.enter="handleInputConfirm"
                  @blur="handleInputConfirm"
                />
                <el-button v-else class="button-new-tag" size="small" @click="showInput">
                  + 新增标签
                </el-button>
              </div>
            </div>
          </div>

          <div class="mt-24">
            <div class="flex-between mb-8">
              <h4 class="title-decoration-1 mb-8">文件信息</h4>
              <el-upload
                multiple
                class="upload-button"
                action="#"
                :auto-upload="false"
                :show-file-list="false"
                accept=".txt, .md, .docx, .pdf"
                :on-exceed="onExceed"
                :on-change="handleFileChange"
                :limit="50"
              >
                <el-button type="primary" size="small">上传文件</el-button>
              </el-upload>
            </div>

            <el-row :gutter="8" v-if="fileList?.length" v-loading="fileLoading">
              <template v-for="(item, index) in uploadQueue" :key="index">
                <el-col :span="12" class="mb-8">
                  <el-card
                    shadow="never"
                    class="file-List-card"
                    :style="{
                      border:
                        item.status === 'success'
                          ? '1px #67C23A solid'
                          : item.status === 'error'
                            ? '1px #F56C6C solid'
                            : '1px #409eff solid'
                    }"
                  >
                    <div class="flex-between">
                      <div class="flex file-info">
                        <img :src="getImgUrl(item.name)" alt="" width="40" />
                        <div class="ml-8 file-name-container">
                          <div class="file-name">
                            <auto-tooltip :content="item.name">
                              {{ item.name }}
                            </auto-tooltip>
                          </div>
                          <div class="file-meta">
                            <el-text type="info" size="small">{{ filesize(item.size) }}</el-text>
                            <el-divider direction="vertical" />
                            <el-text
                              :type="
                                item.status === 'success'
                                  ? 'success'
                                  : item.status === 'error'
                                    ? 'danger'
                                    : 'info'
                              "
                              size="small"
                            >
                              {{
                                item.status === 'uploading'
                                  ? '上传中'
                                  : item.status === 'success'
                                    ? '上传成功'
                                    : '上传失败'
                              }}
                            </el-text>
                          </div>
                        </div>
                      </div>
                      <div class="file-actions">
                        <!-- 显示进度条 -->
                        <el-progress
                          v-if="item.status === 'uploading'"
                          :percentage="item.progress"
                          :stroke-width="5"
                          class="mr-2"
                          style="width: 80px"
                        ></el-progress>
                      </div>
                    </div>
                  </el-card>
                </el-col>
              </template>
              <template v-for="(item, index) in fileList" :key="index">
                <el-col :span="12" class="mb-8">
                  <el-card shadow="never" class="file-List-card" style="border: 1px #409eff solid">
                    <div class="flex-between">
                      <div class="flex file-info">
                        <img :src="getImgUrl(item && item?.name)" alt="" width="40" />
                        <div class="ml-8 file-name-container">
                          <div class="file-name">
                            <auto-tooltip :content="item.name">
                              {{ item?.name }}
                            </auto-tooltip>
                          </div>
                          <div class="file-meta">
                            <el-text type="info" size="small">{{
                              filesize(item.file_size)
                            }}</el-text>
                            <el-divider direction="vertical" />
                            <auto-tooltip :content="datetimeFormat(item.create_time)">
                              <el-text type="info" size="small">{{
                                datetimeFormat(item.create_time)
                              }}</el-text>
                            </auto-tooltip>
                          </div>
                        </div>
                      </div>
                      <div class="file-actions">
                        <el-button text @click="downloadFile(item)">
                          <el-icon><Download /></el-icon>
                        </el-button>
                        <el-button
                          text
                          :loading="deleteLoading === item.id"
                          @click="deleteFile(item)"
                        >
                          <el-icon><Delete /></el-icon>
                        </el-button>
                      </div>
                    </div>
                  </el-card>
                </el-col>
              </template>
            </el-row>
            <!-- 没有文件 -->
            <div v-else>
              <el-empty description="暂无数据" />
            </div>
          </div>
        </div>
      </div>
    </LayoutContainer>
  </div>
</template>

<script setup lang="ts">
import LeftTagsList from './LeftTagsList.vue'
import { onMounted, ref, nextTick, computed } from 'vue'
import { MsgSuccess, MsgError } from '@/utils/message'
import { useRouter, useRoute } from 'vue-router'
import { filesize, getImgUrl } from '@/utils/utils'
import trainSourceApi from '@/api/train-source'
import type { InputInstance } from 'element-plus'
import { ElMessage } from 'element-plus'
import { type Tag, selectTagsList } from '../type/tag'
import { datetimeFormat } from '@/utils/time'
import request from '@/request/index'
import type { AxiosResponse } from 'axios'

const router = useRouter()
const route = useRoute()
const {
  params: { id }
} = route

interface uploadItem {
  id: string
  name: string
  file_size: number
  create_time: string
}
const dataForm = ref({
  name: '',
  describe: '',
  tags: [] as Tag[],
  custom_tags: [] as { value: string }[]
})
const deleteLoading = ref('')
const fileList = ref<uploadItem[]>([])
// 获取所有预定义标签
const allPredefinedTags = computed(() => {
  return selectTagsList.flatMap((g) => g.childs)
})

// 显示标签（合并预定义和自定义标签）
const dynamicTags = computed(() => {
  const predefinedValues = dataForm.value.tags.map((t) => t.value)
  const customValues = dataForm.value.custom_tags.map((t) => t.value)
  return [...predefinedValues, ...customValues]
})

const visibleTag = ref<string | null>(null) // 当前要显示确认框的 tag
const inputVisible = ref(false)
const inputValue = ref('')
const InputRef = ref<InputInstance>()

// 显示确认框
// const showConfirm = (tag: string) => {
//   visibleTag.value = tag
// }
// 创建标签可见状态映射
const tagVisibleMap = ref<Record<string, boolean>>({})

// 显示确认框
const showConfirm = (tag: string) => {
  // 先关闭所有其他的 popconfirm
  Object.keys(tagVisibleMap.value).forEach((key) => {
    tagVisibleMap.value[key] = false
  })
  // 显示当前标签的 popconfirm
  tagVisibleMap.value[tag] = true
}
// 显示输入框
const showInput = () => {
  // 检查是否达到上限
  // if (dynamicTags.value.length >= 6) {
  //   ElMessage.warning('最多只能添加6个标签')
  //   return
  // }

  inputVisible.value = true
  nextTick(() => {
    InputRef.value?.input?.focus()
  })
}

// 处理输入确认
const handleInputConfirm = () => {
  const trimmedValue = inputValue.value.trim()

  if (trimmedValue) {
    // 检查是否达到上限
    // if (dynamicTags.value.length >= 6) {
    //   ElMessage.warning('最多只能添加6个标签')
    //   inputVisible.value = false
    //   inputValue.value = ''
    //   return
    // }

    // 检查是否已存在相同标签
    if (dynamicTags.value.includes(trimmedValue)) {
      ElMessage.warning('此标签已添加过啦')
    } else {
      // 查找是否与预定义标签匹配
      const matchedTag = allPredefinedTags.value.find(
        (tag) => tag.value.toLowerCase() === trimmedValue.toLowerCase()
      )

      // 如果匹配到预定义标签
      if (matchedTag) {
        dataForm.value.tags.push({ key: matchedTag.key, value: matchedTag.value })
      } else {
        // 添加为自定义标签
        dataForm.value.custom_tags.push({ value: trimmedValue })
      }

      console.log('[ dataForm.value ] >', dataForm.value)
      // 保存到后端
      trainSourceApi.putTrainSource(id as string, dataForm.value).then((res) => {
        console.log(res, 'res')
      })

      MsgSuccess('标签添加成功')
    }
  }

  inputVisible.value = false
  inputValue.value = ''
}
const fileLoading = ref(false)
function getFileList() {
  fileLoading.value = true
  trainSourceApi
    .getUploadTrainSource(id as string)
    .then((res) => {
      console.log('[ resUpload ] >', res)
      if (res.code === 200) {
        fileList.value = res.data
      }
    })
    .finally(() => {
      fileLoading.value = false
    })
}
const baseLoading = ref(false)
function getList() {
  baseLoading.value = true
  console.log('[ id ] >', id)
  getFileList()
  trainSourceApi
    .getTrainSourceById(id as string)
    .then((res) => {
      console.log(res, 'resbaseInfo')
      if (res.code === 200) {
        dataForm.value = {
          ...res.data
        }
      }
    })
    .finally(() => {
      baseLoading.value = false
    })
}
function deleteFile(item: any) {
  deleteLoading.value = item.id
  trainSourceApi
    .delTrainSourceFile(item.id)
    .then((res) => {
      if (res.code === 200) {
        MsgSuccess('删除成功')
        getFileList()
      }
    })
    .finally(() => {
      deleteLoading.value = ''
    })
}
function downloadFile(item: any) {
  trainSourceApi.getTrainSourceFile(item.name, item.id).then((res) => {
    console.log(res, 'res')
  })
}
function back() {
  router.go(-1)
}

function handleClose(tag: string) {
  // 先检查是否是预定义标签
  const tagIndex = dataForm.value.tags.findIndex((t) => t.value === tag)
  if (tagIndex > -1) {
    // 从预定义标签中删除
    dataForm.value.tags.splice(tagIndex, 1)
  } else {
    // 从自定义标签中删除
    const customIndex = dataForm.value.custom_tags.findIndex((t) => t.value === tag)
    if (customIndex > -1) {
      dataForm.value.custom_tags.splice(customIndex, 1)
    }
  }

  // 保存到后端
  trainSourceApi.putTrainSource(id as string, dataForm.value).then((res) => {
    console.log(res, 'res')
  })

  MsgSuccess('标签删除成功')
}

// 编辑相关状态
const isEditingName = ref(false)
const isEditingDesc = ref(false)
const editingNameValue = ref('')
const editingDescValue = ref('')

// 开始编辑
function startEditing(field: string) {
  if (field === 'name') {
    isEditingName.value = true
    editingNameValue.value = dataForm.value.name || ''
  } else if (field === 'describe') {
    isEditingDesc.value = true
    editingDescValue.value = dataForm.value.describe || ''
  }
}

// 保存编辑
function saveEditing(field: string) {
  if (field === 'name') {
    if (editingNameValue.value.trim()) {
      dataForm.value.name = editingNameValue.value
      isEditingName.value = false
    }
  } else if (field === 'describe') {
    if (editingDescValue.value.trim()) {
      dataForm.value.describe = editingDescValue.value
      isEditingDesc.value = false
    }
  }

  const data = {
    ...dataForm.value
  }
  // 保存到后端
  trainSourceApi.putTrainSource(id as string, data).then((res) => {
    console.log(res, 'res')
  })
  MsgSuccess('修改成功')
}

// 取消编辑
function cancelEditing(field?: string) {
  if (field) {
    if (field === 'name') {
      isEditingName.value = false
    } else if (field === 'describe') {
      isEditingDesc.value = false
    }
  } else {
    // 取消所有编辑
    isEditingName.value = false
    isEditingDesc.value = false
  }
}

// 处理 textarea 的 Enter 键事件
function handleTextareaEnter(field: string) {
  saveEditing(field)
}
// 处理文件上传
const onExceed = () => {
  ElMessage.warning('每次最多上传50个文件')
}
// 添加上传计数器和上传队列
const uploadingCount = ref(0)
const uploadQueue = ref<any[]>([])

function handleFileChange(file: any) {
  // 检查文件大小
  const isLimit = file?.size / 1024 / 1024 < 100
  if (!isLimit) {
    ElMessage.warning('文件大小超过 100MB')
    return false
  }

  // 创建上传文件对象
  const uploadFile = {
    uid: file.uid,
    name: file.name,
    size: file.size,
    status: 'uploading',
    progress: 0
  }

  // 添加到上传队列
  uploadQueue.value.push(uploadFile)

  // 增加上传计数
  uploadingCount.value++

  // 创建FormData对象
  const formData = new FormData()
  formData.append('file', file.raw)
  formData.append('type', '0') // 文件型
  formData.append('name', file.name)

  // 使用request实例以支持进度监控
  request({
    url: `/train/datasource/data/${id}`,
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    onUploadProgress: (progressEvent: any) => {
      if (progressEvent.total) {
        // 计算进度百分比
        const progress = Math.round((progressEvent.loaded / progressEvent.total) * 100)

        // 更新上传队列中的进度
        const fileInQueue = uploadQueue.value.find((item) => item.uid === file.uid)
        if (fileInQueue) {
          fileInQueue.progress = progress
        }
      }
    }
  })
    .then((response: AxiosResponse<any>) => {
      if (response.data.code === 200) {
        // 更新上传队列中的状态
        const fileInQueue = uploadQueue.value.find((item) => item.uid === file.uid)
        if (fileInQueue) {
          fileInQueue.status = 'success'
          fileInQueue.progress = 100
        }

        ElMessage.success({
          message: '文件上传成功',
          type: 'success',
          showClose: true,
          duration: 1500,
          grouping: true
        })
      }
    })
    .catch((error) => {
      console.error('文件上传失败:', error)

      // 更新上传队列中的状态
      const fileInQueue = uploadQueue.value.find((item) => item.uid === file.uid)
      if (fileInQueue) {
        fileInQueue.status = 'error'
      }

      ElMessage.error(`文件 ${file.name} 上传失败`)
    })
    .finally(() => {
      // 减少上传计数
      uploadingCount.value--

      // 只有当所有文件都上传完成后，才刷新文件列表
      if (uploadingCount.value === 0) {
        // 延迟一点时间再刷新，确保服务器处理完成
        setTimeout(() => {
          getFileList()

          // 清空上传队列
          uploadQueue.value = []
        }, 500)
      }
    })

  return false // 阻止默认上传行为
}

onMounted(() => {
  getList()
})
</script>

<style scoped lang="scss">
.flex-end {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}
.source-main-container {
  width: 100%;
  height: calc(100vh - 56px);
  display: flex;
  .main-container {
    flex: 1;
    // padding: 20px;
    .main-container {
      width: 80%;
      margin: 0 auto;
      margin-bottom: 20px;
    }
  }
}
.detail-container {
  &__steps {
    min-width: 450px;
    max-width: 850px;
    width: 80%;
    margin: 0 auto;
    // padding-right: 60px;

    :deep(.el-step__line) {
      left: 64% !important;
      right: -33% !important;
    }
  }

  &__component {
    width: 100%;
    margin: 0 auto;
    overflow: hidden;
  }
  &__footer {
    padding: 16px 24px;
    position: fixed;
    bottom: 0;
    left: 0;
    background: #ffffff;
    width: 100%;
    box-sizing: border-box;
  }
}
.baseInfo-container {
  border-radius: 20px;
  border: 1px #409eff solid;
  padding: 24px;
  :deep(.el-loading-mask) {
    border-radius: 20px;
  }
}
.tag-input {
  width: 100px;
  margin-right: 8px;
  vertical-align: bottom;
}

.button-new-tag {
  height: 24px;
  padding: 0 6px;
  font-size: 12px;
}

// .tootip-tags {

//   padding: 2px 4px 2px 8px;
//   border: rgba(64, 158, 255, 0.4) 1px solid;
//   font-size: 10px;
//   color: #565772;
//   border-radius: 4px;
//   background: #fff;
//   display: flex;
//   align-items: center;
// }
.description-container {
  color: var(--app-text-color-secondary);
  line-height: 32px;
  font-weight: 400;
  margin: 16px 0;
}
.file-List-card {
  .flex-between {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
  }

  .file-info {
    flex: 1;
    min-width: 0; /* 允许flex子项收缩 */
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

  .file-meta {
    display: flex;
    align-items: center;
  }

  .file-actions {
    display: flex;
    align-items: center;
    min-width: 80px; /* 确保按钮区域有最小宽度 */
    flex-shrink: 0; /* 防止按钮区域被压缩 */
  }
}
.custom-tag {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2px 4px 2px 8px;
  border: rgba(64, 158, 255, 0.4) 1px solid;
  font-size: 10px;
  color: #565772;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;

  :deep(.el-tag__content) {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .tag-content {
    margin-right: 4px;
  }

  .tag-close-icon {
    cursor: pointer;
    font-size: 12px;
  }
    &:hover .tag-close-icon {
    color: #f56c6c;
  }
}
</style>
