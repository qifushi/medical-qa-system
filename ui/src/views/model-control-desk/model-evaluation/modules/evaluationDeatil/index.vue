<template>
  <div class="evaluation-detail">
    <div class="line-card-wrap">
      <div class="card-wrap-left">
        <div class="model-card">
          <h5 class="model-name-title">
            <auto-tooltip>{{ trainInfo?.model_name }}</auto-tooltip>
          </h5>
          <el-row :gutter="24">
            <el-col :span="14">
              <div class="model-info-section">
                <el-descriptions :column="1" border class="compact-descriptions">
                  <el-descriptions-item label="基座模型">{{
                    trainInfo?.base_model
                  }}</el-descriptions-item>
                  <el-descriptions-item label="训练数据集">{{
                    trainInfo?.train_dataset
                  }}</el-descriptions-item>
                  <el-descriptions-item label="训练阶段">{{
                    trainInfo?.train_info.training_stage
                  }}</el-descriptions-item>
                  <el-descriptions-item label="量化等级">{{
                    trainInfo?.train_info.quantization_bit
                  }}</el-descriptions-item>
                </el-descriptions>
              </div>
            </el-col>
            <el-col :span="10">
              <div class="chart-section">
                <div class="chart-container">
                  <div ref="refChartDom" style="width: 100%; height: 140px"></div>
                </div>
              </div>
            </el-col>
          </el-row>
        </div>
        <div class="model-card params-form">
          <h4 class="title-decoration-1 mb-8">评测参数</h4>
          <div class="card-contet">
            <el-form :model="formData" label-position="top">
              <el-row :gutter="36">
                <el-col :span="12">
                  <el-form-item>
                    <template #label>
                      <div class="form-label required">输出目录</div>
                      <div class="form-des">保存结果的路径。</div>
                    </template>
                    <el-input
                      v-model="formData.output_dir"
                      style="width: 100%"
                      placeholder="请输入"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item>
                    <template #label>
                      <div class="form-label">数据路径</div>
                      <div class="form-des">数据文件夹的路径。</div>
                    </template>
                    <el-input
                      v-model="formData.dataset_dir"
                      @change="fnUpdateDatesets"
                      style="width: 100%"
                      placeholder="请输入"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item>
                    <template #label>
                      <div class="form-label required">数据集</div>
                      <div class="form-des">训练使用的数据集</div>
                    </template>
                    <el-select
                      v-model="formData.dataset"
                      placeholder="请选择"
                      style="width: 100%"
                      multiple
                      clearable
                    >
                      <el-option
                        v-for="item in datasetOptions"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                      />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item>
                    <template #label>
                      <div class="form-label">截断长度</div>
                      <div class="form-des">输入序列分词后的最大长度。</div>
                      <div class="input-draggable-progress">
                        <InputDraggableProgress
                          v-model="formData.cutoff_len"
                          :min="4"
                          :max="131072"
                          :defaultValue="1024"
                        />
                      </div>
                    </template>
                    <DraggableProgress v-model="formData.cutoff_len" :min="4" :max="131072" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item>
                    <template #label>
                      <div class="form-label">最大样本数</div>
                      <div class="form-des">每个数据集的最大样本数。</div>
                    </template>
                    <el-input
                      v-model="formData.max_samples"
                      style="width: 100%"
                      placeholder="请输入"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item>
                    <template #label>
                      <div class="form-label">批处理大小</div>
                      <div class="form-des">每个 GPU 处理的样本数量。</div>
                      <div class="input-draggable-progress">
                        <InputDraggableProgress
                          v-model="formData.batch_size"
                          :min="1"
                          :max="1024"
                          :defaultValue="2"
                        />
                      </div>
                    </template>
                    <DraggableProgress v-model="formData.batch_size" :min="1" :max="1024" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item>
                    <template #label>
                      <div class="form-label">最大生成长度</div>
                      <div class="form-des"></div>
                      <div class="input-draggable-progress">
                        <InputDraggableProgress
                          v-model="formData.max_new_tokens"
                          :min="8"
                          :max="4096"
                          :defaultValue="512"
                        />
                      </div>
                    </template>
                    <DraggableProgress v-model="formData.max_new_tokens" :min="8" :max="4096" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item>
                    <template #label>
                      <div class="form-label">Top-p 采样值</div>
                      <div class="form-des"></div>
                      <div class="input-draggable-progress">
                        <InputDraggableProgress
                          v-model="formData.top_p"
                          :min="0.01"
                          :max="1"
                          :step="0.01"
                          :defaultValue="0.7"
                        />
                      </div>
                    </template>
                    <DraggableProgress v-model="formData.top_p" :min="0.01" :step="0.01" :max="1" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item>
                    <template #label>
                      <div class="form-label">温度系数</div>
                      <div class="form-des"></div>
                      <div class="input-draggable-progress">
                        <InputDraggableProgress
                          v-model="formData.temperature"
                          :min="0.01"
                          :max="1.5"
                          :step="0.01"
                          :defaultValue="0.95"
                        />
                      </div>
                    </template>
                    <DraggableProgress
                      v-model="formData.temperature"
                      :step="0.01"
                      :min="0.01"
                      :max="1.5"
                    />
                  </el-form-item>
                </el-col>
              </el-row>
            </el-form>
          </div>
        </div>
      </div>
      <div class="card-wrap-right">
        <div class="model-card">
          <div class="card-contet eval-result-content">
            <div class="eval-content-left">
              <h4 class="title-decoration-1 mb-8">评测进度{{ evalProgress }}%</h4>
              <div style="padding: 12px 0">
                <el-progress :text-inside="true" :stroke-width="16" :percentage="evalProgress" />
              </div>
            </div>
          </div>
        </div>
        <div class="model-card eval-analyse">
          <h4 class="title-decoration-1 mb-8">评测建议及分析</h4>
          <div style="height: calc(100% - 30px)">
            <div class="no-data" v-loading="llmLoading" v-if="!evalLog?.llm_suggestion">
              <span v-if="evalingLoading">
                模型评测中，评测结束后自动生成评测建议及分析。。。请稍后！
              </span>
              <span v-else-if="llmLoading"> 评测建议及分析生成中。。。请稍后！ </span>
              <span v-else> 暂无模型评测结果，评测结束后自动生成评测建议及分析！ </span>
            </div>
            <div class="Md-content" v-if="evalLog?.llm_suggestion">
              <MdPreview
                noIconfont
                editorId="preview-only"
                :modelValue="evalLog?.llm_suggestion"
                class="maxkb-md"
                :codeFoldable="false"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="model-card" style="margin-top: 12px" v-if="evalLog.eval_status == 2">
      <h4 class="title-decoration-1 mb-8">导出参数</h4>
      <div class="card-contet">
        <el-form :model="formExportData" label-position="top">
          <el-row :gutter="36">
            <el-col :span="12">
              <el-form-item>
                <template #label>
                  <div class="form-label">最大分块大小（GB）</div>
                  <div class="form-des">单个模型文件的最大大小。</div>
                  <div class="input-draggable-progress">
                    <InputDraggableProgress
                      v-model="formExportData.export_size"
                      :min="1"
                      :max="100"
                      :defaultValue="5"
                    />
                  </div>
                </template>
                <DraggableProgress v-model="formExportData.export_size" :min="1" :max="100" />
              </el-form-item>
            </el-col>
            <el-col :sm="12" :md="16" :lg="6" :xl="4">
              <el-form-item>
                <template #label>
                  <div class="form-label">导出量化数据集</div>
                  <div class="form-des">量化过程中使用的校准数据集。</div>
                </template>
                <el-input
                  v-model="formExportData.export_quantization_dataset"
                  style="width: 100%"
                  placeholder="请输入"
                />
              </el-form-item>
            </el-col>
            <el-col :sm="12" :md="16" :lg="6" :xl="4">
              <el-form-item>
                <template #label>
                  <div class="form-label">导出设备</div>
                  <div class="form-des">导出模型使用的设备类型。</div>
                </template>
                <el-radio-group v-model="formExportData.export_device">
                  <el-radio value="cpu">cpu</el-radio>
                  <el-radio value="auto">auto</el-radio>
                </el-radio-group>
              </el-form-item>
            </el-col>
            <el-col :sm="12" :md="16" :lg="6" :xl="4">
              <el-form-item>
                <template #label>
                  <div class="form-label">额外参数</div>
                  <div class="form-des">以 JSON 格式传递给训练器的额外参数。</div>
                </template>
                <el-input
                  v-model="formExportData.extra_args"
                  style="width: 100%"
                  placeholder="请输入"
                />
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>
    </div>
    <div class="model-card" style="margin-top: 12px">
      <h4 class="title-decoration-1 mb-8">评测日志</h4>
      <div class="Md-content" style="height: 200px">
        <MdPreviewBlack
          noIconfont
          ref="refMdPreviewBlack"
          editorId="preview-only"
          :modelValue="evalLogObject"
          class="maxkb-md"
          :codeFoldable="false"
        />
      </div>
    </div>
    <div class="btn-wrap">
      <div class="button-group">
        <el-button
          v-if="!evalingLoading && (!evalLog.eval_status || evalLog.eval_status == 0)"
          class="action-btn next-btn primary-btn"
          @click="handleStartEval"
          :disabled="!evalAble"
        >
          开始评测
        </el-button>
        <el-button
          v-if="evalingLoading && evalLog.eval_status == 1"
          class="action-btn interrupt-btn danger-btn"
          @click="handleInterrupt"
        >
          中断
        </el-button>
        <el-button
          v-if="evalLog.eval_status == 2"
          class="action-btn next-btn primary-btn"
          @click="handleExportEval"
        >
          导出模型
        </el-button>
        <el-button class="action-btn prev-btn" @click="handleBack"> 返回 </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import MdPreviewBlack from '@/components/markdown/MdPreviewBlack.vue'
import MdPreview from '@/components/markdown/MdPreview.vue'
import { ref, onMounted, watch, nextTick, onUnmounted } from 'vue'
import { EvaluationTrainFileDict } from '@/views/model-control-desk/utils/config'
import InputDraggableProgress from '@/components/input-draggable-progress/index.vue'
import DraggableProgress from '@/components/draggable-progress/index.vue'
import {
  GetCheckpoints,
  FnMonitor,
  GetDatasets,
  RunEval,
  GetProcesses,
  FnBreakOff,
  SaveModel
} from '@/api/train-common'
import { GetTrainLogDetail } from '@/api/train-training'
import { ElMessage, ElLoading } from 'element-plus'
import evaluationApi from '@/api/train-evaluation'
import { useRoute, useRouter } from 'vue-router'
import { EvalFieldMapping, ExportFieldMapping } from '@/views/model-control-desk/utils/config'
import * as echarts from 'echarts'
interface TrainInfo {
  [key: string]: any
  base_model: string
  create_time: string
  finetuning_type: string
  id: string
  lang: string
  model_name: string
  train_category: number
  train_dataset: string
  train_info: Record<string, any>
  train_log: string
  train_output_dir: string
  train_status: number
  update_time: string
  user_id: string
  username: string
}

interface EvaluationFormData {
  output_dir?: string
  dataset_dir?: string
  dataset?: string[]
  model_path?: string
  cutoff_len?: number
  max_samples?: string
  batch_size?: number
  max_new_tokens?: number
  top_p?: number
  temperature?: number
  predict: boolean
  [key: string]: any
}

interface AnyData {
  [key: string]: any
}
const formExportData = ref({
  lang: 'zh',
  model_name: '',
  model_path: '',
  finetuning_type: '',
  checkpoint_path: [] as string[],
  template: '',
  export_size: 5,
  export_device: 'cpu',
  export_quantization_bit: '',
  export_quantization_dataset: 'data/c4_demo.jsonl',
  export_legacy_format: false,
  export_dir: '',
  export_hub_model_id: '',
  extra_args: '{}'
})

// 创建响应式变量存储 trainLogId
const trainLogId = ref<string>('')
const route = useRoute()
const router = useRouter()
// 当前训练任务详情
const trainInfo = ref<TrainInfo>()
// 定时器
const evalLogTimer = ref()
// 当前是否在评测
const evalingLoading = ref<boolean>(false)
// 当前是否获取分析中
const llmLoading = ref<boolean>(false)
// 当前训练记录对应的评测记录
const evalLog = ref({
  llm_suggestion: '',
  export_status: 0,
  eval_status: 0,
  eval_result: {} as Record<string, number>,
  eval_info: {},
  eval_output_dir: '',
  eval_dataset_name: '',
  eval_dataset_path: '',
  checkpoint_path: '',
  train_id: '',
  id: ''
})
// 评测日志的md格式内容
const evalLogObject = ref()
//
const refElLoading = ref()
// 评测进度
const evalProgress = ref(0)
const evalAble = ref<boolean>(true)
// 当前服务器进程list
const processesInstance = ref<string[]>([])
const isStop = ref<boolean>(false)
const resizeHandler = ref()
const mainChart = ref()
const isFirst = ref(false)
const logInstance = ref()
// GetCheckpoints({})
// FnMonitor({
//   do_train: false,
//   output_dir: 'eval_2025-07-22-15-29-41',
//   finetuning_type: 'lora',
//   lang: 'zh',
//   model_name: 'Qwen3-0.6B-Instruct'
// }).then((res: any) => {
// })

async function fnCheckServiceTrainStatus() {
  // 显示全屏加载状态
  const loading = ElLoading.service({
    lock: true,
    text: '查询服务器进程状态，请稍后！',
    background: 'rgba(0, 0, 0, 0.7)'
  })

  // 调用 GetProcesses 接口查询服务器状态
  return GetProcesses().then((serverStatus: any) => {
    if (serverStatus.data && serverStatus.data[0] && serverStatus.data[0].length) {
      processesInstance.value = serverStatus.data[0]
        .filter((item: any) => item.name === 'llamafactory-cl')
        .map((item: any) => item.cmdline[item.cmdline.length - 1])
      evalAble.value = false
      // let url = `saves/${target.base_model}/${target.finetuning_type}/${target.train_output_dir}/training_args.yaml`
    } else {
      evalAble.value = true
    }
    loading.close()
    return serverStatus
  })
}
const refChartDom = ref()
const updateChart = () => {
  let options = mainChart.value.getOption()
  options.series[0].name = trainInfo.value?.model_name
  options.series[0].data = [
    [
      evalLog.value.eval_result['predict_rouge-1'] || 0,
      evalLog.value.eval_result['predict_bleu-4'] || 0,
      evalLog.value.eval_result['predict_rouge-2'] || 0,
      evalLog.value.eval_result['predict_rouge-l'] || 0
    ]
  ]
  mainChart.value.setOption(options)
}
const initChart = () => {
  if (refChartDom.value && !mainChart.value) {
    mainChart.value = echarts.init(refChartDom.value)
    mainChart.value.setOption({
      tooltip: {
        trigger: 'item',
        formatter: function (params: any) {
          const data = params.data
          return `
          ${trainInfo.value?.model_name}<br/>
          BLEU-4分数: ${data[0]}<br/>
          ROUGE-1分数: ${data[1]}<br/>
          ROUGE-2分数: ${data[2]}<br/>
          ROUGE-L分数: ${data[3]}
        `
        }
      },
      radar: {
        indicator: [
          { name: 'BLEU-4', max: 100 },
          { name: 'ROUGE-1', max: 100 },
          { name: 'ROUGE-2', max: 100 },
          { name: 'ROUGE-L', max: 100 }
        ],
        center: ['50%', '50%'],
        radius: '50%',
        axisName: {
          fontSize: 10,
          color: '#666'
          // padding: [3, 5] // 为文字添加内边距
        },
        splitArea: {
          areaStyle: {
            color: ['rgba(64, 158, 255, 0.1)', 'rgba(64, 158, 255, 0.05)']
          }
        }
      },
      series: [
        {
          name: '',
          type: 'radar',
          data: [
            {
              value: [0, 0, 0, 0],
              areaStyle: {
                opacity: 0.3
              }
            }
          ]
        }
      ]
    })
    // 添加 resize 事件监听
    resizeHandler.value = () => {
      if (mainChart.value) {
        mainChart.value.resize()
      }
    }
    window.addEventListener('resize', resizeHandler.value)
  }
}

const formatTimestamp = (timestamp: any) => {
  const date = new Date(timestamp)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')
  return `${year}-${month}-${day}-${hours}-${minutes}-${seconds}`
}
onMounted(() => {
  // 从路由参数中获取 trainLogId
  trainLogId.value = (route.params.trainLogId as string) || (route.query.trainLogId as string) || ''
  fnCheckServiceTrainStatus().then((a) => {
    if (trainLogId.value) {
      // 这里可以调用加载数据的函数
      loadTrainData()
    }
  })
  nextTick(() => {
    initChart()
  })
  window.addEventListener('resize', resizeHandler.value)
  let time = new Date().getTime()
  formData.value.output_dir = 'eval_' + formatTimestamp(time)
})
onUnmounted(() => {
  // 清除训练日志定时器
  if (evalLogTimer.value) {
    clearInterval(evalLogTimer.value)
    evalLogTimer.value = null
  }
  // 关闭加载状态（如果存在）
  if (refElLoading.value) {
    refElLoading.value.close()
    refElLoading.value = null
  }
  // 销毁图表实例
  if (mainChart.value) {
    mainChart.value.dispose()
    mainChart.value = null
  }
  // 新增：移除 resize 事件监听
  if (resizeHandler.value) {
    window.removeEventListener('resize', resizeHandler.value)
    resizeHandler.value = null
  }
})
// 根据训练记录获取训练数据
const loadTrainData = () => {
  const loading = ElLoading.service({
    lock: true,
    text: '评测初始化中...请稍后！',
    background: 'rgba(0, 0, 0, 0.7)'
  })
  Promise.all([
    GetTrainLogDetail(trainLogId.value),
    evaluationApi.GetEvalInfoByTrainId(trainLogId.value)
  ])
    .then((res) => {
      if (res[0].code == 200) {
        trainInfo.value = res[0].data
        const keys = [
          'lang',
          'model_name',
          'model_path',
          'finetuning_type',
          'quantization_bit',
          'quantization_method',
          'rope_scaling',
          'booster',
          'template'
        ]
        keys.forEach((key) => {
          formData.value[key] = trainInfo.value?.train_info?.[key] || ''
        })
        formData.value.checkpoint_path = [trainInfo.value?.train_output_dir]
      }
      if (res[1].code == 200) {
        let evalFinish = res[1].data.find((item: any) => item.eval_status == 2)
        if (evalFinish) {
          evalLog.value = evalFinish
          formData.value = evalFinish.eval_info
          loadCurrentLog().finally(() => {
            loading.close()
          })
        } else {
          let target = res[1].data.find((item: any) => item.eval_status == 1)
          if (target) {
            evalLog.value = target
            formData.value = target.eval_info
            let url = `saves/${target.eval_info.model_name}/${target.eval_info.finetuning_type}/${target.eval_info.output_dir}/training_args.yaml`
            if (processesInstance.value.includes(url)) {
              evalingLoading.value = true
              getEvalLog()
            } else {
              let params = Object.assign({}, target)
              params.eval_status = 3
              evaluationApi.UpdateEvalInfo(target.id, params).then((res) => {})
            }
            loading.close()
          } else {
            loading.close()
          }
        }
      }
      fnUpdateDatesets()
    })
    .catch(() => {
      loading.close()
    })
}
const refMdPreviewBlack = ref()
const updateScroll = () => {
  const logContentDom = refMdPreviewBlack?.value
  if (logContentDom) {
    logContentDom.scrollTo({
      top: logContentDom.scrollHeight,
      behavior: 'smooth'
    })
  }
}
watch(
  evalLogObject,
  () => {
    nextTick(() => {
      // updateScroll()
    })
  },
  { deep: true }
)
const formData = ref<EvaluationFormData>({
  lang: 'zh',
  model_name: '',
  model_path: '',
  finetuning_type: '',
  checkpoint_path: [],
  quantization_bit: '',
  quantization_method: '',
  template: '',
  rope_scaling: '',
  booster: '',
  dataset_dir: '/opt/workspace/LLaMA-Factory/data/ceH9MOpIrX-9',
  dataset: [],
  cutoff_len: 1024,
  max_samples: '10000',
  batch_size: 2,
  predict: true,
  max_new_tokens: 512,
  top_p: 0.7,
  temperature: 0.95,
  output_dir: ''
})
const datasetOptions = ref<Array<{ label: string; value: string }>>([])
const fnUpdateDatesets = () => {
  if (!formData.value.dataset_dir || !trainInfo.value?.train_info?.training_stage) return
  datasetOptions.value = []
  formData.value.dataset = []
  GetDatasets({
    dataset_dir: formData.value.dataset_dir,
    training_stage: trainInfo.value?.train_info?.training_stage
  }).then((res: any) => {
    let sourceList = (res.data[0] && res.data[0].choices) || []
    sourceList.forEach((item: any) => {
      datasetOptions.value.push({
        label: item[0],
        value: item[0]
      })
    })
  })
}
const addEvalLog = (eval_status = 0) => {
  let params = {
    lang: formData.value.lang,
    train_id: trainInfo.value?.id,
    checkpoint_path: trainInfo.value?.train_output_dir,
    eval_dataset_path: formData.value.dataset_dir,
    eval_dataset_name: formData.value.dataset?.join(),
    eval_output_dir: formData.value.output_dir,
    eval_info: formData.value,
    eval_result: {},
    llm_suggestion: '',
    eval_status,
    model_name: trainInfo.value?.model_name
    // export_path: ''
    // export_time: ''
  }

  evaluationApi.AddEvalInfo(params).then((res) => {
    if (res.code == 200) {
      evalLog.value = res.data
    }
  })
}

const setEvalResult = () => {
  let finishInfoObj = {}
  try {
    const finishInfoStr = logInstance.value.finish_info // 假设这是从接口获取的原始字符串
    finishInfoObj = JSON.parse(finishInfoStr.replace(/```json\s*|\s*```/g, '')) // 去除 ```json 和 ``` 标记后解析为对象
  } catch (error) {
    finishInfoObj = {}
  }
  let obj = Object.assign({}, evalLog.value, {
    eval_log: logInstance.value.running_log,
    eval_result: finishInfoObj,
    eval_status: 2,
    export_status: 0
  })
  return evaluationApi.UpdateEvalInfo(evalLog.value?.id, obj).then((res) => {
    if (res.code == 200) {
      evalLog.value = res.data
      if (!evalLog.value?.llm_suggestion) {
        fnGetEvalAnalyse()
      }
    }
  })
}
const FnCalculationProgress = (data: any) => {
  let target = data[data.length - 1]
  evalProgress.value = Math.floor((target.current_steps / target.total_steps) * 10000) / 100
}
const loadCurrentLog = () => {
  let obj = {
    do_train: false,
    output_dir: formData.value.output_dir,
    finetuning_type: trainInfo.value?.finetuning_type,
    lang: formData.value.lang,
    model_name: trainInfo.value?.base_model
  }
  return FnMonitor(obj).then((res: any) => {
    let logTarget = res.data && res.data[0]
    if (logTarget) {
      logInstance.value = logTarget
      // md显示日志内容
      evalLogObject.value = logTarget.running_log
      // 关闭全屏loading
      refElLoading.value && logTarget.running_log && refElLoading.value.close()

      if (logTarget.running_log && evalingLoading.value && isFirst) {
        isFirst.value = false
        updateEvalStatus(1)
      }

      if (logTarget.finish_info == '训练出错。') {
        // 更新进度以及echart损失函数图
        let running_info = logTarget.running_info || []
        if (running_info.length) {
          FnCalculationProgress(running_info)
        }
      } else {
        let finishInfoObj = {}
        try {
          const finishInfoStr = logInstance.value.finish_info // 假设这是从接口获取的原始字符串
          finishInfoObj = JSON.parse(finishInfoStr.replace(/```json\s*|\s*```/g, '')) // 去除 ```json 和 ``` 标记后解析为对象
        } catch (error) {
          finishInfoObj = {}
        }
        if (Object.keys(finishInfoObj).length != 0) {
          setEvalResult().then(() => {
            updateChart()
          })
          evalProgress.value = 100
          evalingLoading.value = false
          evalLogTimer.value && clearInterval(evalLogTimer.value)
        }
      }
    }
  })
}
const updateEvalStatus = (eval_status: any) => {
  let obj = Object.assign({}, evalLog.value, {
    eval_status: eval_status
  })
  return evaluationApi.UpdateEvalInfo(evalLog.value?.id, obj).then((res) => {
    if (res.code == 200) {
      evalLog.value = res.data
    }
  })
}
const getEvalLog = () => {
  evalLogTimer.value = setInterval(() => {
    if (evalingLoading.value) {
      loadCurrentLog()
    } else {
      clearInterval(evalLogTimer.value)
    }
  }, 4000)
}
const processChartData = (data: any) => {
  // 如果数据长度小于等于10，直接返回原数组
  if (data.length <= 10) {
    return data
  }

  // 获取第一条和最后一条数据
  const firstItem = data[0]
  const lastItem = data[data.length - 1]

  // 中间部分的数据（除去第一条和最后一条）
  const middleData = data.slice(1, data.length - 1)

  // 需要从中间数据中选取8条
  const middleResult = []
  const middleDataLength = middleData.length

  // 计算间隔，尽量均匀分布
  const step = middleDataLength / 8

  for (let i = 0; i < 8; i++) {
    // 计算索引位置
    const index = Math.min(Math.floor(i * step), middleDataLength - 1)
    middleResult.push(middleData[index])
  }

  // 返回结果：第一条 + 中间8条 + 最后一条
  return [firstItem, ...middleResult, lastItem]
}
const fnGetEvalAnalyse = () => {
  const key = 'application-ac2dc70a8019b9041dc0f15d92bd8fbc'
  let train_log = trainInfo.value?.train_log || []
  llmLoading.value = true
  evaluationApi
    .callApiWithApiKey(key, {
      train_log: processChartData(train_log),
      train_results: trainInfo.value?.train_result,
      predict_results: evalLog.value?.eval_result
    })
    .then((res) => {
      llmLoading.value = false
      if (res.code == 200) {
        let obj = Object.assign({}, evalLog.value, {
          llm_suggestion: res.data.content
        })
        evaluationApi.UpdateEvalInfo(evalLog.value?.id, obj).then((res) => {
          if (res.code == 200) {
            evalLog.value = res.data
          }
        })
      }
    })
}
const handleExportEval = () => {
  formExportData.value.model_name = trainInfo.value?.base_model ?? ''
  formExportData.value.model_path = trainInfo.value?.train_info.model_path
  formExportData.value.finetuning_type = trainInfo.value?.finetuning_type ?? ''
  formExportData.value.checkpoint_path = [trainInfo.value?.train_output_dir ?? '']
  formExportData.value.template = trainInfo.value?.train_info.template
  formExportData.value.export_quantization_bit = trainInfo.value?.train_info.quantization_bit
  formExportData.value.export_dir = `/root/autodl-tmp/workspace/export_models/${evalLog.value?.id}`

  let logParams = Object.assign({}, evalLog.value, {
    export_status: 1,
    export_path: formExportData.value.export_dir
  })
  SaveModel(formExportData.value).then(() => {})
  evaluationApi.UpdateEvalInfo(evalLog.value?.id, logParams).then((res) => {
    if (res.code == 200) {
      evalLog.value = res.data
      ElMessage({
        message: '导出成功',
        type: 'success'
      })
    }
  })
}
const handleInterrupt = () => {
  isStop.value = true
  const loading = ElLoading.service({
    lock: true,
    text: '评测中断中...请稍后！'
  })
  FnBreakOff().finally(() => {
    loading.close()
  })
}
// 开始训练前部分内容初始化
const initEval = () => {
  evalLogObject.value = ''
  evalingLoading.value = false
  isStop.value = false
  evalLog.value = {
    llm_suggestion: '',
    export_status: 0,
    eval_status: 0,
    eval_result: {},
    eval_info: {},
    eval_output_dir: '',
    eval_dataset_name: '',
    eval_dataset_path: '',
    checkpoint_path: '',
    train_id: '',
    id: ''
  }
  evalLogTimer.value && clearInterval(evalLogTimer.value)
}
const handleStartEval = () => {
  if (!formData.value.dataset || !formData.value.dataset.length) {
    ElMessage({
      message: '请选择评测数据集！',
      type: 'warning'
    })
    return
  }
  if (!formData.value.output_dir) {
    ElMessage({
      message: '请配置评测输出目录！',
      type: 'warning'
    })
    return
  }

  addEvalLog()
  const params: Record<string, any> = {}
  for (let i in EvalFieldMapping) {
    params[i] = formData.value[EvalFieldMapping[i]]
  }
  evalingLoading.value = true
  refElLoading.value = ElLoading.service({
    lock: true,
    text: '模型评测准备中',
    background: 'rgba(0, 0, 0, 0.7)'
  })
  RunEval(params).then((res: any) => {
    refElLoading.value && refElLoading.value.close()
    evalingLoading.value = false
    if (isStop.value) {
      ElMessage.error('评测已中断')
      initEval()
    }
    if (res.data && res.data[0] === '任务已存在，请先中断训练。') {
      const loading = ElLoading.service({
        lock: true,
        text: '当前服务器已有进程使用，请先稍后再试！',
        background: 'rgba(0, 0, 0, 0.7)'
      })
      setTimeout(() => {
        loading.close()
      }, 5000)
      return
    } else if (res.data && res.data[0].indexOf('训练出错。 Exit code:') > -1) {
      ElMessage.error('评测出错，请修改配置重新评测')
      updateEvalStatus(3)
      initEval()
    }
    loadCurrentLog()
  })
  getEvalLog()
}

const handleBack = () => {
  router.back()
}
</script>
<style lang="scss">
.evaluation-detail {
  .el-form-item__label {
    margin-bottom: 4px !important;
    position: relative !important;
    width: 100% !important;
  }
}
</style>

<style lang="scss" scoped>
::v-deep {
  .el-col-12,
  .el-col-12.is-guttered {
    margin-bottom: 24px;
  }
}
.input-draggable-progress {
  position: absolute;
  right: 0;
  width: 115px;
  top: 50%;
  margin-top: -16px;
}
// 保留原有表单样式
.form-label {
  font-size: 14px;
  color: #1f2329;
  position: relative;
  width: 100%;

  &.required {
    padding-left: 12px;
  }

  &.required::after {
    content: '*';
    position: absolute;
    left: 0;
    height: 12px;
    margin-top: -6px;
    top: 50%;
    font-size: 24px;
    color: red;
  }
}

.evaluation-detail {
  padding: 24px;
  box-sizing: border-box;
  height: calc(100vh - 56px - 65px);
  overflow-y: auto;
}
.detail-container {
  padding: 0 15px;
  max-height: 200px;
  overflow-y: auto;
  width: 100%;
  box-sizing: border-box;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(220px, 1fr)); /* 宽屏4列 */
  gap: 16px;
  max-height: 200px;
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 8px;
  /* 响应式调整列数 */
  @media (max-width: 1400px) {
    grid-template-columns: repeat(3, minmax(220px, 1fr)); /* 中等屏幕3列 */
  }

  @media (max-width: 1100px) {
    grid-template-columns: repeat(2, minmax(220px, 1fr)); /* 小屏幕2列 */
  }

  @media (max-width: 768px) {
    grid-template-columns: 1fr; /* 移动端1列 */
  }

  &::-webkit-scrollbar {
    width: 6px;
    height: 6px;
  }

  &::-webkit-scrollbar-thumb {
    background-color: #c0c4cc;
    border-radius: 3px;
    &:hover {
      background-color: #a0a4ac;
    }
  }
}
.form-des {
  color: #bbbbc2;
  font-size: 12px;
  height: 22px;
  line-height: 22px;
}
.model-card {
  background: #fff;
  border-radius: 12px;
  border: 1px solid #e4e7ed;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  margin-bottom: 12px;
  &.eval-analyse {
    height: calc(100% - 112px - 12px);
    box-sizing: border-box;
  }
  &:last-child {
    margin-bottom: 0;
  }

  // &:hover {
  //   box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  //   border-color: #409eff;
  // }

  .model-name-title {
    font-size: 18px;
    font-weight: 600;
    color: #303133;
    margin: 0 0 16px 0;
    padding: 12px 16px;
    background: linear-gradient(135deg, #f0f7ff 0%, #e8f4ff 100%);
    border-radius: 8px;
    border-left: 4px solid #409eff;
  }
}
.no-data {
  height: 100%;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-size: 14px;
}
::v-deep {
  .Md-content {
    height: 100%;
    .md-editor {
      height: 100%;
    }
  }
}
.btn-wrap {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  box-sizing: border-box;
  padding: 0 24px;
  background: white;
  border-top: 1px solid #ebeef5;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
  z-index: 10;
  /* 确保按钮在最上层 */

  .button-group {
    display: flex;
    justify-content: center;
    gap: 16px;
    padding: 16px 0;
    flex-wrap: wrap;
    /* 允许按钮换行 */
  }

  .action-btn {
    padding: 12px 28px;
    font-size: 15px;
    border-radius: 6px;
    transition: all 0.3s;
    font-weight: 600;
    min-width: 120px;
    display: flex;
    align-items: center;
    justify-content: center;

    /* 普通按钮样式 */
    background-color: #f5f7fa;
    border: 1px solid #dcdfe6;
    color: #606266;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* 禁用状态样式 */
    &:disabled,
    &.is-disabled {
      opacity: 0.6;
      cursor: not-allowed;
      transform: none;
      box-shadow: none;

      &:hover {
        transform: none;
        box-shadow: none;
      }
    }

    /* 主要按钮样式 */
    &.primary-btn {
      background-color: #409eff;
      color: white;
      border: none;
      box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4);

      &:hover {
        background-color: #66b1ff;
        box-shadow: 0 6px 14px rgba(64, 158, 255, 0.5);
      }

      /* 主要按钮禁用状态 */
      &:disabled,
      &.is-disabled {
        background-color: #a0cfff;
        box-shadow: none;
      }
    }

    /* 危险按钮样式 */
    &.danger-btn {
      background-color: #f56c6c;
      color: white;
      border: none;
      box-shadow: 0 4px 12px rgba(245, 108, 108, 0.4);

      &:hover {
        background-color: #f78989;
        box-shadow: 0 6px 14px rgba(245, 108, 108, 0.5);
      }

      /* 危险按钮禁用状态 */
      &:disabled,
      &.is-disabled {
        background-color: #fab6b6;
        box-shadow: none;
      }
    }
  }
}
.line-card-wrap {
  display: flex;
  flex-wrap: wrap;
  .card-wrap-left {
    width: 560px;
    margin-right: 12px;
  }
  .card-wrap-right {
    width: calc(100% - 560px - 12px);
    height: 953px;
  }
}
.chart-container {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  background: #fafafa;
  padding: 10px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
}
</style>
