<template>
  <LayoutContainer class="create-application">
    <template #header>
      <div class="flex-between w-full">
        <h3>创建任务</h3>
        <!-- <el-button type="primary" @click="submit(applicationFormRef)" :disabled="loading">
          保存并发布
        </el-button> -->
      </div>
    </template>
    <el-row v-loading="loading">
      <!-- 配置栏 -->
      <el-col :span="8">
        <div class="p-24 mb-16" style="padding-bottom: 0">
          <h4 class="title-decoration-1">
            {{ applicationForm.name }}
          </h4>
        </div>
        <div class="scrollbar-height-left">
          <el-scrollbar>
            <el-form
              hide-required-asterisk
              ref="applicationFormRef"
              :model="applicationForm"
              :rules="rules"
              label-position="top"
              require-asterisk-position="right"
              class="p-24"
              style="padding-top: 0"
            >
              <el-form-item prop="name">
                <template #label>
                  <div class="flex-between mt-12">
                    <span>文章标题 <span class="danger">*</span></span>
                  </div>
                </template>
                <el-input
                  maxlength="64"
                  placeholder="请输入文章标题"
                  show-word-limit
                  v-model="articleTitle"
                />
              </el-form-item>
              <el-form-item>
                <template #label>
                  <div class="flex-between mt-12">
                    <span>选择模板 <span class="danger">*</span></span>
                  </div>
                </template>
                <el-select
                  v-model="selectTemplate"
                  placeholder="请选择模板"
                  class="w-full"
                  popper-class="select-model"
                  :clearable="true"
                >
                  <el-option
                    v-for="item in selectTemplateOptions"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  />
                </el-select>
              </el-form-item>
              <!-- ai模型 -->
              <el-form-item
                :label="$t('views.application.applicationForm.form.aiModel.label')"
                prop="model_id"
              >
                <template #label>
                  <div class="flex-between">
                    <span>{{ $t('views.application.applicationForm.form.aiModel.label') }}</span>
                  </div>
                </template>
                <el-select
                  v-model="applicationForm.model_id"
                  :placeholder="$t('views.application.applicationForm.form.aiModel.placeholder')"
                  class="w-full"
                  popper-class="select-model"
                  :clearable="true"
                >
                  <el-option-group
                    v-for="(value, label) in modelOptions"
                    :key="value"
                    :label="relatedObject(providerOptions, label, 'provider')?.name"
                  >
                    <el-option
                      v-for="item in value.filter((v: any) => v.status === 'SUCCESS')"
                      :key="item.id"
                      :label="item.name"
                      :value="item.id"
                      class="flex-between"
                    >
                      <div class="flex">
                        <span
                          v-html="relatedObject(providerOptions, label, 'provider')?.icon"
                          class="model-icon mr-8"
                        ></span>
                        <span>{{ item.name }}</span>
                      </div>
                      <el-icon class="check-icon" v-if="item.id === applicationForm.model_id">
                        <Check />
                      </el-icon>
                    </el-option>
                    <!-- 不可用 -->
                    <el-option
                      v-for="item in value.filter((v: any) => v.status !== 'SUCCESS')"
                      :key="item.id"
                      :label="item.name"
                      :value="item.id"
                      class="flex-between"
                      disabled
                    >
                      <div class="flex">
                        <span
                          v-html="relatedObject(providerOptions, label, 'provider')?.icon"
                          class="model-icon mr-8"
                        ></span>
                        <span>{{ item.name }}</span>
                        <span class="danger">{{
                          $t('views.application.applicationForm.form.aiModel.unavailable')
                        }}</span>
                      </div>
                      <el-icon class="check-icon" v-if="item.id === applicationForm.model_id">
                        <Check />
                      </el-icon>
                    </el-option>
                  </el-option-group>
                  <template #footer>
                    <div class="w-full text-left cursor" @click="openCreateModel()">
                      <el-button type="primary" link>
                        <el-icon class="mr-4">
                          <Plus />
                        </el-icon>
                        {{ $t('views.application.applicationForm.form.addModel') }}
                      </el-button>
                    </div>
                  </template>
                </el-select>
              </el-form-item>
              <!-- 提示词 -->
              <!-- <el-form-item
                :label="$t('views.application.applicationForm.form.prompt.label')"
                prop="model_setting.prompt"
              >
                <template #label>
                  <div class="flex align-center">
                    <div class="flex-between mr-4">
                      <span
                        >{{ $t('views.application.applicationForm.form.prompt.label') }}
                        <span class="danger">*</span></span
                      >
                    </div>
                    <el-tooltip effect="dark" placement="right">
                      <template #content>{{
                        $t('views.application.applicationForm.form.prompt.tooltip', {
                          data: '{data}',
                          question: '{question}'
                        })
                      }}</template>
                      <AppIcon iconName="app-warning" class="app-warning-icon"></AppIcon>
                    </el-tooltip>
                  </div>
                </template>
                <el-input
                  v-model="applicationForm.model_setting.prompt"
                  :rows="6"
                  type="textarea"
                  maxlength="2048"
                  :placeholder="defaultPrompt"
                />
              </el-form-item>
           -->
              <!-- 多轮对话 -->
              <!-- <el-form-item
                :label="$t('views.application.applicationForm.form.multipleRoundsDialogue')"
                @click.prevent
              >
                <el-switch
                  size="small"
                  v-model="applicationForm.multiple_rounds_dialogue"
                ></el-switch>
              </el-form-item> -->
              <!-- 关联知识库 -->
              <el-form-item
                label="$t('views.application.applicationForm.form.relatedKnowledgeBase')"
              >
                <template #label>
                  <div class="flex-between">
                    <span>{{
                      $t('views.application.applicationForm.form.relatedKnowledgeBase')
                    }}</span>
                    <div>
                      <el-button type="primary" link @click="openParamSettingDialog">
                        <AppIcon iconName="app-operation" class="mr-4"></AppIcon
                        >{{ $t('views.application.applicationForm.form.paramSetting') }}
                      </el-button>
                      <el-button type="primary" link @click="openDatasetDialog">
                        <el-icon class="mr-4"> <Plus /> </el-icon
                        >{{ $t('views.application.applicationForm.form.add') }}
                      </el-button>
                    </div>
                  </div>
                </template>
                <div class="w-full">
                  <el-text type="info" v-if="applicationForm.dataset_id_list?.length === 0">{{
                    $t('views.application.applicationForm.form.relatedKnowledgeBaseWhere')
                  }}</el-text>
                  <el-row :gutter="12" v-else>
                    <el-col
                      :xs="24"
                      :sm="24"
                      :md="24"
                      :lg="12"
                      :xl="12"
                      class="mb-8"
                      v-for="(item, index) in applicationForm.dataset_id_list"
                      :key="index"
                    >
                      <el-card class="relate-dataset-card border-r-4" shadow="never">
                        <div class="flex-between">
                          <div class="flex align-center">
                            <AppAvatar
                              v-if="relatedObject(datasetList, item, 'id')?.type === '1'"
                              class="mr-8 avatar-purple"
                              shape="square"
                              :size="32"
                            >
                              <img src="@/assets/icon_web.svg" style="width: 58%" alt="" />
                            </AppAvatar>

                            <AppAvatar v-else class="mr-8" shape="square" :size="32">
                              <img src="@/assets/icon_document.svg" style="width: 58%" alt="" />
                            </AppAvatar>
                            <div class="ellipsis">
                              {{ relatedObject(datasetList, item, 'id')?.name }}
                            </div>
                          </div>
                          <el-button text @click="removeDataset(item)">
                            <el-icon>
                              <Close />
                            </el-icon>
                          </el-button>
                        </div>
                      </el-card>
                    </el-col>
                  </el-row>
                </div>
              </el-form-item>
              <!-- 开场白 -->
              <!-- <el-form-item :label="$t('views.application.applicationForm.form.prologue')">
                <MdEditor
                  class="prologue-md-editor"
                  v-model="applicationForm.prologue"
                  :preview="false"
                  :toolbars="[]"
                  :footers="[]"
                />
              </el-form-item> -->
              <!-- 问题优化 -->
              <!-- <el-form-item @click.prevent>
                <template #label>
                  <div class="flex align-center">
                    <span class="mr-4">{{
                      $t('views.application.applicationForm.form.problemOptimization.label')
                    }}</span>
                    <el-tooltip
                      effect="dark"
                      :content="
                        $t('views.application.applicationForm.form.problemOptimization.tooltip')
                      "
                      placement="right"
                    >
                      <AppIcon iconName="app-warning" class="app-warning-icon"></AppIcon>
                    </el-tooltip>
                  </div>
                </template>
                <el-switch size="small" v-model="applicationForm.problem_optimization"></el-switch>
              </el-form-item> -->
              <el-form-item
                :label="$t('views.application.applicationForm.form.prompt.label')"
                prop="model_setting.prompt"
              >
                <template #label>
                  <div class="align-center flex-between">
                    <div class="flex-between mr-4">
                      <span>撰写思路 <span class="danger">*</span></span>
                    </div>
                    <el-button type="primary" text @click="generateIdeas(applicationFormRef)"
                      >生成思路</el-button
                    >
                  </div>
                </template>
                <MdEditor
                  class="prologue-md-editor"
                  v-model="chatContent"
                  :preview="false"
                  :toolbars="[]"
                  :footers="[]"
                  v-loading="ideasLoading"
                  element-loading-text="思路生成中..."
                  model="editable"
                />
                <!-- <el-input
                  v-model="chatContent"
                  :rows="15"
                  type="textarea"
                  v-loading="ideasLoading"
                  element-loading-text="思路生成中..."
                /> -->
              </el-form-item>
              <el-col :span="24">
                <el-button type="primary" style="width: 100%" @click="generatOutline"
                  >生成大纲</el-button
                >
              </el-col>
            </el-form>
          </el-scrollbar>
        </div>
      </el-col>
      <!-- 显示栏 -->
      <el-col :span="16" class="p-24 border-l" v-loading="outlineLoading">
        <!-- 大纲 -->
        <h4 class="title-decoration-1">{{ isShowOutline ? '大纲' : '文章' }}</h4>

        <div class="dialog-bg">
          <h1 class="p-24">{{ outlineData.title }}</h1>
          <div class="scrollbar-height">
            <el-scrollbar noresize>
              <GenerateOutline
                v-if="isShowOutline"
                :outlineData="outlineData"
                @deleteOutline="deleteOutline"
                @editOutline="editOutline"
                @addOutline="addOutline"
              />
              <div v-else style="font-size: 16px">
                <MdRenderer :source="articleContent"></MdRenderer>
              </div>
            </el-scrollbar>
          </div>
        </div>

        <!-- 大纲按钮 -->
        <template v-if="outlineData.title">
          <template v-if="isShowOutline">
            <div class="text-right">
              <!-- <el-button>保存大纲</el-button> -->
              <el-button @click="generateArticle">生成文章</el-button>
            </div>
          </template>

          <!-- 文章按钮 -->
          <template v-else>
            <div class="flex-between">
              <el-button type="primary" icon="ArrowLeft" text @click="showOutline">
                查看大纲
              </el-button>
              <div>
                <el-button @click="generateArticle(true)">重新生成</el-button>
                <el-button>导出文章</el-button>
              </div>
            </div>
          </template>
        </template>
      </el-col>
    </el-row>

    <ParamSettingDialog ref="ParamSettingDialogRef" @refresh="refreshParam" />
    <AddDatasetDialog
      ref="AddDatasetDialogRef"
      @addData="addDataset"
      :data="datasetList"
      @refresh="refresh"
      :loading="datasetLoading"
    />

    <!-- 添加模版 -->
    <CreateModelDialog
      ref="createModelRef"
      @submit="getModel"
      @change="openCreateModel($event)"
    ></CreateModelDialog>
    <SelectProviderDialog ref="selectProviderRef" @change="openCreateModel($event)" />
  </LayoutContainer>
</template>
<script setup lang="ts">
import applicationApi from '@/api/application'
import type { ApplicationFormType } from '@/api/type/application'
import type { Provider } from '@/api/type/model'
import MdRenderer from '@/components/markdown/MdRenderer.vue'
import { t } from '@/locales'
import useStore from '@/stores'
import { MsgSuccess } from '@/utils/message'
import { relatedObject } from '@/utils/utils'
import CreateModelDialog from '@/views/template/component/CreateModelDialog.vue'
import SelectProviderDialog from '@/views/template/component/SelectProviderDialog.vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import { groupBy } from 'lodash'
import { onMounted, reactive, ref } from 'vue'
import { useRoute } from 'vue-router'
import AddDatasetDialog from '../.././component/AddDatasetDialog.vue'
import ParamSettingDialog from '../.././component/ParamSettingDialog.vue'
import GenerateOutline from './generateOutline.vue'

const { model, application } = useStore()

const isShowOutline = ref(true)
const route = useRoute()
const {
  params: { id }
} = route as any
// @ts-ignore
const defaultPrompt = t('views.application.prompt.defaultPrompt', {
  data: '{data}',
  question: '{question}'
})

const ParamSettingDialogRef = ref<InstanceType<typeof ParamSettingDialog>>()
const createModelRef = ref<InstanceType<typeof CreateModelDialog>>()
const selectProviderRef = ref<InstanceType<typeof SelectProviderDialog>>()

const applicationFormRef = ref<FormInstance>()
const AddDatasetDialogRef = ref()

const ideasLoading = ref(false)
const loading = ref(false)
const datasetLoading = ref(false)
const applicationForm = ref<ApplicationFormType>({
  // title: '',
  reasoning: '',
  name: '',
  desc: '',
  model_id: '',
  multiple_rounds_dialogue: false,
  // prologue: t('views.application.prompt.defaultPrologue'),
  dataset_id_list: [],
  dataset_setting: {
    top_n: 3,
    similarity: 0.6,
    max_paragraph_char_number: 5000,
    search_mode: 'embedding',
    no_references_setting: {
      status: 'ai_questioning',
      value: '{question}'
    }
  },
  model_setting: {
    prompt: defaultPrompt
  },
  problem_optimization: false,
  type: 'SIMPLE'
})
const selectTemplate = ref('通用文章')
const selectTemplateOptions = [
  {
    value: '通用文章',
    label: '通用文章'
  },
  {
    value: '项目申报书',
    label: '项目申报书'
  },
  {
    value: '立项任务书',
    label: '立项任务书'
  },
  {
    value: '年度报告',
    label: '年度报告'
  }
]
async function generateArticle(isRefresh: boolean) {
  console.log(
    applicationForm.value.model_id,
    applicationForm.value.dataset_id_list,
    applicationForm,
    '11'
  )
  outlineLoading.value = true
  articleContent.value = ''
  isShowOutline.value = false
  let generateArticleParamsObj = {
    model_id: applicationForm.value.model_id,
    dataset_id_list: applicationForm.value.dataset_id_list,
    multiple_rounds_dialogue: true,
    dataset_setting: {
      top_n: 40,
      similarity: 0.6,
      max_paragraph_char_number: 100000,
      search_mode: 'embedding',
      no_references_setting: {
        status: 'ai_questioning',
        value: '{question}'
      }
    },
    model_setting: {
      prompt:
        '请根据以下论文提纲生成一篇完整的学术论文。请详细扩展提纲中的每个要点，确保内容逻辑严谨、论证充分，并符合学术写作规范。特别注意使用学术语言、准确引用文献，并保证整体结构的连贯性。提纲内容如下：\n{question}'
    },
    problem_optimization: false
  }
  const TempChatRes = await applicationApi.postChatOpen(generateArticleParamsObj)
  const TempChatId = TempChatRes.data
  const getArticleParams = {
    message: JSON.stringify(outlineData.value),
    re_chat: isRefresh ? true : false
  }
  const chatRes = await applicationApi.postChatMessage(TempChatId, getArticleParams)
  console.log(chatRes, 'sss')
  if (!chatRes.body) {
    outlineLoading.value = false
    throw new Error('对话网络错误，请重试')
  }
  const reader = chatRes.body.getReader()
  outlineLoading.value = false

  const write = getWrite(reader, 'article')
  reader.read().then((res: any) => {
    // this.isAnswering = false;
    if (res.done) {
      console.log('Stream is done!')
    } else {
      // 确保 write 函数接收正确的参数
      write({ done: res.done, value: res.value })
      console.log(res, 'mmm')
    }
  })
}
function showOutline() {
  isShowOutline.value = true
}

// 操作大纲--start
interface addOutlineForm {
  oneTitle: string
  oneContent: string
  twoTitle: string
  twoContent: string
  node: 'after' | 'before'
}

// 辅助函数，用于计算插入位置
function calculatePosition(index: number, node: string, arrayLength: number) {
  let position = 0
  if (node === 'before') {
    position = index > 0 ? index : 0
  } else if (node === 'after') {
    position = index === arrayLength - 1 ? arrayLength : index + 1
  }
  console.log(position, 'Math.max(0, Math.min(position, arrayLength))')

  return position // 确保位置在数组范围内
}
// 创建一级目录数据
function createOneOutlineData(form: any) {
  return {
    outline_one: form.oneTitle,
    outline_one_content: form.oneContent,
    outline_two: [
      {
        outline_two_title: form.twoTitle,
        outline_two_content: form.twoContent
      }
    ]
  }
}

// 创建二级目录数据
function createTwoOutlineData(form: any) {
  return {
    outline_two_title: form.twoTitle,
    outline_two_content: form.twoContent
  }
}
function addOutline(
  addOutlineForm: addOutlineForm,
  isOneOutline: boolean,
  addOneOutlineIndex: number,
  addTwoOutlineIndex?: number
) {
  let outlineArr = outlineData.value.outline
  // 二级目录的数组
  let outlineTwoArr = outlineData.value.outline[addOneOutlineIndex].outline_two

  const addOutlineIndex = isOneOutline ? addOneOutlineIndex : addTwoOutlineIndex
  // 根据 isOneOutline 决定是添加一级目录还是二级目录
  let dataToAdd = isOneOutline
    ? createOneOutlineData(addOutlineForm)
    : createTwoOutlineData(addOutlineForm)

  // 计算插入位置
  const position = calculatePosition(
    addOutlineIndex as number,
    addOutlineForm.node,
    outlineArr.length
  )

  // 插入数据
  if (isOneOutline) {
    outlineArr.splice(position, 0, dataToAdd)
  } else {
    outlineTwoArr.splice(position, 0, dataToAdd)
  }
}

interface editOutlineForm {
  title: string
  content: string
}

function editOutline(
  editOutlineForm: editOutlineForm,
  outline_one_index: number,
  outline_two_index?: number
) {
  let outlineArr = outlineData.value.outline
  console.log(outline_two_index, 'outline_two_indexs')

  if (!outline_two_index && outline_two_index !== 0) {
    // 修改一级大纲
    outlineArr[outline_one_index].outline_one = editOutlineForm.title
    outlineArr[outline_one_index].outline_one_content = editOutlineForm.content
  } else {
    // 修改二级大纲
    let outlineTwoObj = outlineArr[outline_one_index].outline_two[outline_two_index]
    console.log(outlineTwoObj, '2222')
    outlineTwoObj.outline_two_content = editOutlineForm.content
    outlineTwoObj.outline_two_title = editOutlineForm.title
    console.log(outlineArr, 'aaaa')
  }
}

function deleteOutline(outline_one_index: number, outline_two_index?: number) {
  let outlineArr = outlineData.value.outline
  if (outline_two_index !== undefined && outline_two_index !== null) {
    // 删除二级标题
    outlineArr[outline_one_index].outline_two.splice(outline_two_index, 1)
  } else {
    // 删除一级标题
    outlineArr.splice(outline_one_index, 1)
    console.log(outlineArr, 'outlineArr')
  }
}
// 操作大纲--end

const articleTitle = ref('')
const rules = reactive<FormRules<ApplicationFormType>>({
  name: [
    {
      required: true,
      message: '请输入文章标题',
      trigger: 'blur'
    }
  ],
  model_id: [
    {
      required: false,
      message: t('views.application.applicationForm.form.aiModel.placeholder'),
      trigger: 'change'
    }
  ],
  'model_setting.prompt': [
    {
      required: true,
      message: t('views.application.applicationForm.form.prompt.placeholder'),
      trigger: 'blur'
    }
  ]
})
const modelOptions = ref<any>(null)
const providerOptions = ref<Array<Provider>>([])
const datasetList = ref([])

const submit = async (formEl: FormInstance | undefined) => {
  console.log(id, applicationForm.value, 'applicationForm.value')

  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      application.asyncPutApplication(id, applicationForm.value, loading).then((res) => {
        MsgSuccess(t('views.application.applicationForm.buttons.saveSuccess'))
      })
    }
  })
}

const generateIdeas = async (formEl: FormInstance | undefined) => {
  if (!articleTitle.value) {
    return ElMessage({
      message: '请输入文章标题',
      type: 'warning'
    })
  }
  ideasLoading.value = true
  console.log(id, applicationForm.value, formEl, 'applicationForm.value')
  try {
    // 修改应用设置
    let ResSaveApplicationSetting = await application.asyncPutApplication(id, applicationForm.value)
    console.log(ResSaveApplicationSetting, 'ResSaveApplicationSetting')

    if (!ResSaveApplicationSetting) {
      throw new Error('保存应用设置失败，请重试')
    }

    // 点击生成赋空值
    chatContent.value && (chatContent.value = '')
    let ideasAppId = '06e6fab8-433f-11ef-90d2-92ef9389d40c'
    // 根据应用id生成对话id
    let chatOpenRes = await applicationApi.getChatOpen(ideasAppId)
    let chatOpenId = chatOpenRes.data
    if (!chatOpenId) {
      throw new Error('获取对话ID失败，请重试')
    }
    let obj = {
      message: articleTitle.value,
      re_chat: false
      // stream: false
    }
    // 对话
    let chatRes = await applicationApi.postChatMessage(chatOpenId, obj)
    // 有输出则取消loading
    // ideasLoading.value = false
    console.log(chatRes, 'chatRes')
    if (!chatRes.body) {
      throw new Error('对话网络错误，请重试')
    }
    const reader = chatRes.body.getReader()
    const write = getWrite(reader, 'ideas')
    console.log(write, 'q1111qq')

    // reader.read().then(write)
    reader.read().then((res: any) => {
      // this.isAnswering = false;
      if (res.done) {
        console.log('Stream is done!')
      } else {
        // 确保 write 函数接收正确的参数
        write({ done: res.done, value: res.value })
        console.log(res, 'mmm')
      }
    })
  } catch (error: any) {
    // 显示错误消息
    ElMessage({
      message: error.message || '网络错误，请重试',
      type: 'error'
    })
  } finally {
    // 无论成功或失败，都关闭加载状态
    ideasLoading.value = false
  }
  // if (!formEl) return
  // await formEl.validate((valid, fields) => {
  //   if (valid) {
  //     application.asyncPutApplication(id, applicationForm.value, loading).then((res) => {
  //       MsgSuccess(t('views.application.applicationForm.buttons.saveSuccess'))
  //     })
  //   }
  // })
}
let chatContent = ref('')
let articleContent = ref('')
function getWrite(reader: any, dataBox: string, stream = 'true') {
  console.log('getWrite')
  let tempResult = ''
  /**
   *
   * @param done  是否结束
   * @param value 值
   */
  const write_stream = ({ done, value }: { done: boolean; value: any }) => {
    console.log(done, value, 'done')
    try {
      if (done) {
        console.log(' i am done', done)
        return
      }

      const decoder = new TextDecoder('utf-8')
      let str = decoder.decode(value, { stream: true })
      // 这里解释一下 start 因为数据流返回流并不是按照后端chunk返回 我们希望得到的chunk是data:{xxx}\n\n 但是它获取到的可能是 data:{ -> xxx}\n\n 总而言之就是 fetch不能保证每个chunk都说以data:开始 \n\n结束
      tempResult += str
      const split = tempResult.match(/data:.*}\n\n/g)
      console.log(split, 'split111')
      if (split) {
        str = split.join('')
        tempResult = tempResult.replace(str, '')
        console.log(tempResult, 'tempResult')
      } else {
        return reader.read().then(write_stream)
      }

      // 这里解释一下 end
      if (str && str.startsWith('data:')) {
        if (split) {
          for (const index in split) {
            const chunk = JSON?.parse(split[index].replace('data:', ''))
            const content = chunk?.content
            // 赋值显示
            if (dataBox === 'ideas') {
              // chatContent.value += content.replace(/\n\s*\n/g, '\n')
              chatContent.value += content.replace(/\n\s*\n/g, '\n').replace(/[*#-]/g, '')
              console.log(content, chunk.is_end, 'content', chatContent.value)
            } else if (dataBox === 'article') {
              articleContent.value += content.replace(/\n\s*\n/g, '\n')
            }
            if (chunk.is_end) {
              // 流处理成功 返回成功回调
              return Promise.resolve()
            }
          }
        }
      }
    } catch (e) {
      console.log('catch')
      return Promise.reject(e)
    }
    return reader.read().then(write_stream)
  }

  /**
   * 处理 json 响应
   * @param param0
   */
  const write_json = ({ done, value }: { done: boolean; value: any }) => {
    console.log(done, value, 'wo zai zhe')
    if (done) {
      const result_block = JSON.parse(tempResult)
      if (result_block.code === 500) {
        return Promise.reject(result_block.message)
      } else {
        if (result_block.content) {
          console.log('wo zai zhe li ', result_block.content)
          // 拼接/记录内容
        }
      }
      return
    }
    if (value) {
      const decoder = new TextDecoder('utf-8')
      tempResult += decoder.decode(value)
      console.log(tempResult, 'tempResult')
    }
    return reader.read().then(write_json)
  }
  console.log(stream ? write_stream : write_json, 'qqq')
  return stream ? write_stream : write_json
}
const outlineData = ref<any>({})
const outlineLoading = ref(false)
async function generatOutline() {
  if (!chatContent.value) {
    return ElMessage({
      message: '请先生成撰写思路',
      type: 'warning'
    })
  }
  if (!articleTitle.value) {
    return ElMessage({
      message: '请输入文章标题',
      type: 'warning'
    })
  }
  // 根据应用id生成对话id
  let chatOpenRes = await applicationApi.getChatOpen(id)
  let chatOpenId = chatOpenRes.data

  let obj = {
    chat_model: applicationForm.value.model_id,
    theme: articleTitle.value,
    abstract: chatContent.value
  }
  // 生成大纲
  try {
    outlineLoading.value = true
    let outlineRes = await applicationApi.postGeneratOutline(id, chatOpenId, obj)
    console.log(outlineRes, 'outlineRes')
    outlineData.value = outlineRes.data
  } catch {
    ElMessage.error(' 网络异常，请重新生成大纲')
  } finally {
    outlineLoading.value = false
  }
}

const openParamSettingDialog = () => {
  ParamSettingDialogRef.value?.open(applicationForm.value.dataset_setting)
}

function refreshParam(data: any) {
  applicationForm.value.dataset_setting = data
}

const openCreateModel = (provider?: Provider) => {
  if (provider && provider.provider) {
    createModelRef.value?.open(provider)
  } else {
    selectProviderRef.value?.open()
  }
}

function removeDataset(id: any) {
  if (applicationForm.value.dataset_id_list) {
    applicationForm.value.dataset_id_list.splice(
      applicationForm.value.dataset_id_list.indexOf(id),
      1
    )
  }
}
function addDataset(val: Array<string>) {
  applicationForm.value.dataset_id_list = val
}
function openDatasetDialog() {
  AddDatasetDialogRef.value.open(applicationForm.value.dataset_id_list)
}

function getDetail() {
  application.asyncGetApplicationDetail(id, loading).then((res: any) => {
    applicationForm.value = res.data
    applicationForm.value.model_id = res.data.model
  })
}

function getDataset() {
  application.asyncGetApplicationDataset(id, datasetLoading).then((res: any) => {
    datasetList.value = res.data
  })
}

function getModel() {
  loading.value = true
  applicationApi
    .getApplicationModel(id)
    .then((res: any) => {
      modelOptions.value = groupBy(res?.data, 'provider')
      loading.value = false
    })
    .catch(() => {
      loading.value = false
    })
}

function getProvider() {
  loading.value = true
  model
    .asyncGetProvider()
    .then((res: any) => {
      providerOptions.value = res?.data
      loading.value = false
    })
    .catch(() => {
      loading.value = false
    })
}

function refresh() {
  getDataset()
}

onMounted(() => {
  console.log(id, 'id')

  getProvider()
  getModel()
  getDataset()
  getDetail()
})
</script>
<style lang="scss" scoped>
.create-application {
  .relate-dataset-card {
    color: var(--app-text-color);
  }

  .scrollbar-height-left {
    height: calc(var(--app-main-height) - 64px);
  }

  .scrollbar-height {
    height: calc(var(--app-main-height) - 160px);
  }
}

.prologue-md-editor {
  height: 350px;
}
</style>
