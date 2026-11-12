<template>
  <div class="flex-center" style="background-color: white" v-loading="loading">
    <div class="p-24" style="width: 80%">
      <!-- 页面标识 -->
      <div class="page-header-section mb-24">
        <div class="page-title-area">
          <div class="title-content">
            <el-icon class="title-icon">
              <TrendCharts />
            </el-icon>
            <h2 class="main-title">模型横向对比</h2>
          </div>
          <p class="page-description">对比分析多个模型的性能指标，为模型选择提供数据支撑</p>
        </div>
      </div>

      <h4 class="title-decoration-1 mb-8">模型详细信息</h4>
      <el-row :gutter="20">
        <el-col
          :lg="12"
          :md="24"
          :sm="24"
          v-for="(model, modelIndex) in modelData"
          :key="modelIndex"
          class="model-group"
        >
          <div class="model-item mb-24">
            <h5 class="model-name-title">
              <auto-tooltip>{{ model.model_name }}</auto-tooltip>
            </h5>
            <el-row :gutter="24">
              <el-col :span="14">
                <div class="model-info-section">
                  <el-descriptions :column="1" border class="compact-descriptions">
                    <el-descriptions-item label="基座模型">{{
                      model.base_model
                    }}</el-descriptions-item>
                    <el-descriptions-item label="训练数据集">{{
                      model.train_dataset
                    }}</el-descriptions-item>
                    <el-descriptions-item label="训练阶段">{{
                      model.train_info.training_stage
                    }}</el-descriptions-item>
                    <el-descriptions-item label="训练步数">{{
                     model.train_log?.[0]?.total_steps || '暂无数据'
                    }}</el-descriptions-item>
                  </el-descriptions>
                </div>
              </el-col>
              <el-col :span="10">
                <div class="chart-section">
                  <div class="chart-container">
                    <div :id="`chart-${modelIndex}`" style="width: 100%; height: 140px"></div>
                  </div>
                </div>
              </el-col>
            </el-row>
          </div>
        </el-col>
      </el-row>
      <h4 class="title-decoration-1 mb-8">模型对比</h4>
      <el-row :gutter="20" class="mb-16">
        <el-col :span="12">
          <div class="table-container">
            <el-table :data="comparisonTableData" border style="width: 100%" :height="450">
              <el-table-column
                label="模型名称"
                prop="model_name"
                align="left"
                show-overflow-tooltip
                min-width="220"
              >
                <template #default="scope">
                  {{ scope.row.model_name }}
                </template>
              </el-table-column>
              <el-table-column prop="bleu4" width="140" align="center">
                <template #header>
                  <div>
                    <el-tooltip placement="top">
                      <template #content
                        ><div class="w-200">{{ fieldExplanation['samples_per_second'] }}</div>
                      </template>
                      <div class="flex-center" style="gap: 2px">
                        每秒处理样本数 <el-icon><QuestionFilled /></el-icon>
                      </div>
                    </el-tooltip>
                  </div>
                </template>
                <template #default="{row}"> {{extractNumber(row.predict_samples_per_second,2)}} </template>
              </el-table-column>
              <el-table-column prop="bleu4" width="100" align="center">
                <template #header>
                  <div>
                    <el-tooltip placement="top">
                      <template #content
                        ><div class="w-200">{{ fieldExplanation['blue4'] }}</div>
                      </template>
                      <div class="flex-center" style="gap: 2px">
                        BLEU-4 <el-icon><QuestionFilled /></el-icon>
                      </div>
                    </el-tooltip>
                  </div>
                </template>
                <template #default="scope"> {{ extractNumber(scope.row.bleu4,2) }} </template>
              </el-table-column>
              <el-table-column label="ROUGE-1" prop="rouge1" width="120" align="center">
                <template #header>
                  <div>
                    <el-tooltip :content="fieldExplanation['rouge1']" placement="top">
                      <template #content
                        ><div class="w-200">{{ fieldExplanation['rouge1'] }}</div>
                      </template>
                      <div class="flex-center" style="gap: 2px">
                        ROUGE-1 <el-icon><QuestionFilled /></el-icon>
                      </div>
                    </el-tooltip>
                  </div>
                </template>
                <template #default="scope"> {{ extractNumber(scope.row.rouge1,2) }}</template>
              </el-table-column>
              <el-table-column label="ROUGE-2" prop="rouge2" width="120" align="center">
                <template #header>
                  <div>
                    <el-tooltip :content="fieldExplanation['rouge2']" placement="top">
                      <template #content
                        ><div class="w-200">{{ fieldExplanation['rouge2'] }}</div>
                      </template>
                      <div class="flex-center" style="gap: 2px">
                        ROUGE-2 <el-icon><QuestionFilled /></el-icon>
                      </div>
                    </el-tooltip>
                  </div>
                </template>
                <template #default="scope"> {{ extractNumber(scope.row.rouge2,2) }}</template>
              </el-table-column>
              <el-table-column label="ROUGE-L" prop="rougel" width="120" align="center">
                <template #header>
                  <div>
                    <el-tooltip :content="fieldExplanation['rougel']" placement="top">
                      <template #content
                        ><div class="w-200">{{ fieldExplanation['rougel'] }}</div>
                      </template>
                      <div class="flex-center" style="gap: 2px">
                        ROUGE-L <el-icon><QuestionFilled /></el-icon>
                      </div>
                    </el-tooltip>
                  </div>
                </template>
                <template #default="scope"> {{ extractNumber(scope.row.rougel,2) }} </template>
              </el-table-column>
              <el-table-column label="图例" width="80" align="center" fixed="right">
                <template #default="scope">
                  <div
                    class="legend-item"
                    :class="{ 'legend-disabled': hiddenSeries.includes(scope.row.id) }"
                    @click="toggleSeries(scope.row.id)"
                  >
                    <div class="legend-color" :style="{ backgroundColor: scope.row.color }"></div>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="comparison-chart-section">
            <div class="comparison-chart-container">
              <div id="comparison-chart" style="width: 100%; height: 100%"></div>
            </div>
          </div>
        </el-col>
      </el-row>

      <h4 class="title-decoration-1 mb-8">对比分析及建议</h4>
      <div class="evaluation-suggestions-simple">
        <el-card shadow="never" v-if="analysisContent">
          <MdPreview
            noIconfont
            editorId="preview-only"
            :modelValue="analysisContent"
            class="maxkb-md"
            :codeFoldable="false"
          />
        </el-card>
        <el-card
          shadow="never"
          v-else-if="!isViewMode && !analysisGenerated"
          class="analysis-trigger-card"
          :class="{ loading: analysisLoading }"
          @click="generateAnalysis"
        >
          <div class="suggestion-content">
            <div class="trigger-content">
              <el-icon v-if="analysisLoading" class="loading-icon">
                <Loading />
              </el-icon>
              <el-icon v-else class="analysis-icon">
                <Document />
              </el-icon>
              <p class="suggestion-text">
                {{ analysisLoading ? '正在生成对比分析及建议...' : '点击获取对比分析及建议' }}
              </p>
              <div v-if="!analysisLoading" class="click-hint">
                <el-icon class="click-icon">
                  <ArrowRight />
                </el-icon>
              </div>
            </div>
          </div>
        </el-card>
        <el-card v-else shadow="never">
        <el-empty  description="暂无对比分析及建议"></el-empty>
        </el-card>
      </div>
    </div>
    <div class="btn-wrap">
      <div class="button-group">
        <el-button type="primary" v-if="!isViewMode" @click="exportEvaluation" class="action-btn primary-btn"
          >保存横向对比记录</el-button
        >
        <el-button @click="toBack" class="action-btn">关 闭</el-button>
      </div>
    </div>
    <exportEvaluationDialog ref="exportEvaDialogRef"></exportEvaluationDialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import * as echarts from 'echarts'
import { Loading, Document, ArrowRight } from '@element-plus/icons-vue'
import exportEvaluationDialog from './exportEvaluationDialog.vue'
import useStore from '@/stores'
import evaluationApi from '@/api/train-evaluation'

const { evaModelSelected } = useStore()
const router = useRouter()
const route = useRoute()
const isViewMode = ref(false)
let chartInstances: any[] = []
// 简化的数据结构：直接是模型列表，每个模型包含性能指标
const modelData = ref<any[]>([])
const loading = ref(false)
const fieldExplanation = {
  samples_per_second: '代表模型处理速度，值越大越高效',
  blue4:
    '评估机器翻译质量的经典指标，基于生成文本与参考文本的4-gram匹配度。范围 [0, 1]，值越接近1表示质量越高。',
  rouge1:
    '评估文本摘要质量的指标，衡量生成文本与参考文本的‌1-gram（单词）匹配度‌。通常以百分比形式报告，较低值表示质量不佳。',
  rouge2:
    '衡量生成文本与参考文本的‌2-gram（连续两个词）匹配度‌。0.0 表示生成文本中未出现任何正确的连续词组，质量较差。',
  rougel: '基于‌最长公共子序列（LCS）‌的匹配度，考虑句子结构的连贯性。'
}

function extractNumber(value: string, digits: number) {
    const strValue = String(value);
  // 创建正则表达式，允许0到digits位小数
  const regex = new RegExp(`^\\d+(?:\\.\\d{0,${digits}})?`);
  const match = strValue.match(regex);
  return match ? Number(match[0]) : NaN;
}
// 符合系统配色的颜色池
const colorPool = [
  '#409EFF', // Element Plus 主色
  '#67C23A', // 成功色
  '#E6A23C', // 警告色
  '#F56C6C', // 危险色
  '#2b5fd9', // 标签默认色
  '#2ca91f', // 标签成功色
  '#d97400', // 标签警告色
  '#909399', // 信息色
  '#13C2C2' // 青绿色
]

// 动态颜色映射 - 按索引顺序分配
const colorMap = computed(() => {
  const map: Record<string, string> = {}
  modelData.value.forEach((model, index) => {
    // 按照模型在数组中的顺序分配颜色
    const colorIndex = index % colorPool.length
    map[model.id] = colorPool[colorIndex]
  })
  return map
})

// 处理表格数据 - 直接使用模型数据
const comparisonTableData = computed(() => {
  return modelData.value.map((model) => ({
    id: model.id,
    model_name: model.model_name,
    bleu4: model.eval_obj[0].eval_result['predict_bleu-4'],
    rouge1: model.eval_obj[0].eval_result['predict_rouge-1'],
    rouge2: model.eval_obj[0].eval_result['predict_rouge-2'],
    rougel: model.eval_obj[0].eval_result['predict_rouge-l'],
    predict_samples_per_second:model.eval_obj[0].eval_result.predict_samples_per_second,
    color: colorMap.value[model.id]
  }))
})

// 初始化单个模型的雷达图
const initSingleChart = (modelIndex: number) => {
  const chartElement = document.getElementById(`chart-${modelIndex}`)
  if (!chartElement) return

  // 检查是否已经存在实例，如果存在则先销毁
  let chartInstance = echarts.getInstanceByDom(chartElement)
  if (chartInstance) {
    chartInstance.dispose()
  }

  chartInstance = echarts.init(chartElement)
  chartInstances.push(chartInstance)

  const model = modelData.value[modelIndex]

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: function (params: any) {
        const data = params.data.value
        return `
          ${model.model_name}<br/>
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
        color: '#666',
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
        name: model.id,
        type: 'radar',
        data: [
          {
            value: [
              model.eval_obj[0].eval_result['predict_bleu-4'],
              model.eval_obj[0].eval_result['predict_rouge-1'],
              model.eval_obj[0].eval_result['predict_rouge-2'],
              model.eval_obj[0].eval_result['predict_rouge-l']
            ],
            name: model.id,
            itemStyle: {
              color: colorMap.value[model.id]
            },
            areaStyle: {
              opacity: 0.3
            }
          }
        ]
      }
    ]
  }

  chartInstance.setOption(option)
}

let comparisonChartInstance: any = null

// 初始化对比柱状图
const initComparisonChart = () => {
  const chartElement = document.getElementById('comparison-chart')
  if (!chartElement) return

  comparisonChartInstance = echarts.init(chartElement)

  const categories = ['BLEU-4', 'ROUGE-1', 'ROUGE-2', 'ROUGE-L']
  const series: any[] = []

  // 为每个模型创建一个系列
  modelData.value.forEach((model) => {
    const baseColor = colorMap.value[model.id]

    series.push({
      name: model.id,
      type: 'bar',
      data: [
        model.eval_obj[0].eval_result['predict_bleu-4'],
        model.eval_obj[0].eval_result['predict_rouge-1'],
        model.eval_obj[0].eval_result['predict_rouge-2'],
        model.eval_obj[0].eval_result['predict_rouge-l']
      ],
      itemStyle: {
        color: baseColor
      }
    })
  })

  const option = {
    title: {
      text: '模型性能对比',
      left: 'center',
      top: 10,
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: function (params: any) {
        let result = `<strong>${params[0].axisValue}</strong><br/>`
        params.forEach((param: any) => {
          const model = modelData.value.find((m: any) => m.id === param.seriesName)
          const name = model ? model.model_name : param.seriesName
          result += `<span style="color:${param.color}">${name}</span>: ${param.value}<br/>`
        })
        return result
      }
    },
    // 图例设置
    legend: {
      type: 'scroll', // 添加滚动功能
      data: series.map((s) => s.name),
      top: '10%',
      orient: 'horizontal', // 水平排列
      width: '80%', // 控制图例区域宽度
      left: 'center', // 居中显示
      pageButtonPosition: 'end', // 翻页按钮位置
      pageButtonGap: 5, // 翻页按钮与图例的间隔
      pageButtonItemGap: 5, // 翻页按钮之间的间隔
      pageIconColor: '#409EFF', // 翻页按钮颜色
      pageIconInactiveColor: '#C0C4CC', // 不可用翻页按钮颜色
      pageIconSize: 12, // 翻页按钮大小
      textStyle: {
        fontSize: 12,
        color: '#606266'
      },
      itemWidth: 15, // 图例标记的宽度
      itemHeight: 10, // 图例标记的高度
      itemGap: 20, // 图例项之间的间隔
      formatter: function (id: any) {
        // 通过 id 查找 model_name
        const model = modelData.value.find((m) => m.id === id)
        if (model) {
          // 名称过长可截断
          return model.model_name.length > 15
            ? model.model_name.slice(0, 15) + '...'
            : model.model_name
        }
        return id
      },
      tooltip: {
        show: true // 当图例名称被截断时，鼠标悬停可以显示完整名称
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '5%',
      top: '20%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: categories,
      axisLabel: {
        fontSize: 12,
        fontWeight: 'bold'
      },
      axisTick: {
        alignWithLabel: true
      }
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        formatter: '{value}'
      },
      splitLine: {
        lineStyle: {
          type: 'dashed',
          opacity: 0.5
        }
      }
    },
    series: series
  }

  comparisonChartInstance.setOption(option)

  // 添加图例点击事件监听
  comparisonChartInstance.on('legendselectchanged', (params: any) => {
    // 同步更新表格的 hiddenSeries 状态
    const seriesId = params.name
    const isSelected = params.selected[seriesId]

    const index = hiddenSeries.value.indexOf(seriesId)
    if (isSelected && index > -1) {
      // 图例被选中，从隐藏列表中移除
      hiddenSeries.value.splice(index, 1)
    } else if (!isSelected && index === -1) {
      // 图例被取消选中，添加到隐藏列表
      hiddenSeries.value.push(seriesId)
    }
  })
}

// 初始化所有图表
const initAllCharts = async () => {
  await nextTick()

  // 初始化每个模型的雷达图
  modelData.value.forEach((model, modelIndex) => {
    initSingleChart(modelIndex)
  })

  // 初始化对比图表
  initComparisonChart()

  // 监听窗口大小变化
  window.addEventListener('resize', handleResize)
}

// 处理窗口大小变化
const handleResize = () => {
  chartInstances.forEach((instance) => {
    if (instance) {
      instance.resize()
    }
  })

  if (comparisonChartInstance) {
    comparisonChartInstance.resize()
  }
}
// 保存弹窗
const exportEvaDialogRef = ref()
const exportEvaluation = () => {
  console.log(typeof modelData.value, 'modelData.value')
  const completeData = {
    modelData: modelData.value,
    analysisContent: analysisContent.value
  }
  exportEvaDialogRef.value.open(completeData)
}

// 添加隐藏系列的状态管理 （控制柱状图的图例）
const hiddenSeries = ref<string[]>([])

// 切换系列显示/隐藏
const toggleSeries = (seriesId: string) => {
  const index = hiddenSeries.value.indexOf(seriesId)
  if (index > -1) {
    // 如果已隐藏，则显示
    hiddenSeries.value.splice(index, 1)
  } else {
    // 如果显示中，则隐藏
    hiddenSeries.value.push(seriesId)
  }

  // 更新图表
  updateChartLegend()
}

// 更新图表图例状态
const updateChartLegend = () => {
  if (!comparisonChartInstance) return

  // 使用 ECharts 的 dispatchAction 来控制图例
  modelData.value.forEach((model) => {
    const isHidden = hiddenSeries.value.includes(model.id)

    comparisonChartInstance.dispatchAction({
      type: isHidden ? 'legendUnSelect' : 'legendSelect',
      name: model.id
    })
  })
}

// 添加分析相关的状态
const analysisLoading = ref(false)
const analysisContent = ref('')
const analysisGenerated = ref(false)

// 生成分析报告
const generateAnalysis = async () => {
  if (analysisLoading.value) return

  analysisLoading.value = true
  try {
    // 构建请求参数
    const key = 'application-98c2e0bc69b9538b6493449d3ad4d427'

    const analysisData = modelData.value.map((model) => {
      const evalResult = model?.eval_obj[0]?.eval_result
      return {
        [model.model_name]: evalResult
      }
    })
    console.log(
      '%c [ analysisData ]-570',
      'font-size:13px; background:pink; color:#bf2c9f;',
      analysisData
    )

    const res = await evaluationApi.callApiWithApiKey(key, analysisData)

    if (res.code !== 200) return
    analysisContent.value = res.data.content

    analysisGenerated.value = true
  } catch (error) {
    console.error('生成分析报告失败:', error)
    // 可以添加错误提示
  } finally {
    analysisLoading.value = false
  }
}
const toBack = () => {
  router.push({name:'ModelEvaluation'})
}

function getList() {
  const contrast_id = route.query.contrast_id

  if (contrast_id) {
    console.log('我是查看')

    // 查看模式：从API获取保存的记录
    isViewMode.value = true
    loadContrastRecord(contrast_id as string)
  } else {
    // 新建模式：从store获取选中的模型
    isViewMode.value = false
    console.log('selectedModels =>', evaModelSelected.selectedModels)
    modelData.value = evaModelSelected.selectedModels
  }
}

// 加载保存的对比记录
const loadContrastRecord = async (contrast_id: string) => {
  loading.value = true
  try {
    const res = await evaluationApi.getEvalContrastRecordById(contrast_id)
    if (res.code !== 200) return
    modelData.value = res.data.eval_contrast_data.modelData
    analysisContent.value = res.data.eval_contrast_data.analysisContent

    // 数据加载完成后初始化图表
    await nextTick()
    initAllCharts()
  } catch (error) {
    console.error('加载对比记录失败:', error)
  } finally {
  loading.value = false

  }
}

onMounted(() => {
  getList()
  console.log('组件挂载，开始初始化图表')
  if (!isViewMode.value) {
    initAllCharts()
  }
})

onUnmounted(() => {
  console.log('组件卸载，清理图表')
  chartInstances.forEach((instance) => {
    if (instance) {
      instance.dispose()
    }
  })

  if (comparisonChartInstance) {
    comparisonChartInstance.dispose()
  }

  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped lang="scss">
// 训练记录样式
.model-group {
  .model-item {
    background: #fff;
    border-radius: 12px;
    border: 1px solid #e4e7ed;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    transition: all 0.3s ease;

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
}

// 训练记录样式
.model-info-section {
  .compact-descriptions {
    :deep(.el-descriptions__body) {
      .el-descriptions__table {
        .el-descriptions__cell {
          &.is-bordered-label {
            background-color: #f8f9fa;
            font-weight: 500;
            width: 100px;
            padding: 8px 12px;
          }

          &.is-bordered-content {
            padding: 8px 12px;
          }
        }
      }
    }
  }
}
// 雷达图样式
.chart-section {
  height: 100%;
  display: flex;
  flex-direction: column;

  .chart-container {
    flex: 1;
    border: 1px solid #ebeef5;
    border-radius: 8px;
    background: #fafafa;
    padding: 10px;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
  }
}
// 对比表格样式
.table-container {
  height: 450px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);

  :deep(.el-table) {
    border-radius: 8px;
    .el-table__header-wrapper {
      border-top-left-radius: 8px;
      border-top-right-radius: 8px;
    }
  }
}
.w-200 {
  width: 200px;
}
// 对比柱状图样式
.comparison-chart-section {
  height: 450px;
  display: flex;
  flex-direction: column;

  .comparison-chart-container {
    flex: 1;
    height: 100%;
    border: 1px solid #ebeef5;
    border-radius: 8px;
    background: #fff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }
}

// 对比分析建议样式
.evaluation-suggestions-simple {
  .suggestion-content {
    .suggestion-text {
      margin-bottom: 12px;
      line-height: 1.6;
      color: #303133;
      font-size: 14px;

      &:last-child {
        margin-bottom: 0;
      }

      strong {
        color: #409eff;
        font-weight: 600;
      }
    }
  }
}
// 对比分析建议动效
.analysis-trigger-card {
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px dashed #e4e7ed;
  background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%);

  &:hover {
    border-color: #409eff;
    box-shadow: 0 4px 12px rgba(64, 158, 255, 0.15);
    transform: translateY(-2px);

    .trigger-content {
      .analysis-icon {
        color: #409eff;
        transform: scale(1.1);
      }

      .click-hint {
        opacity: 1;
        transform: translateX(0);
      }
    }
  }

  &.loading {
    cursor: not-allowed;
    border-color: #909399;
    background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);

    &:hover {
      transform: none;
      box-shadow: none;
    }
  }

  .trigger-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    text-align: center;

    .loading-icon {
      font-size: 32px;
      color: #409eff;
      margin-bottom: 16px;
      animation: spin 1s linear infinite;
    }

    .analysis-icon {
      font-size: 32px;
      color: #909399;
      margin-bottom: 16px;
      transition: all 0.3s ease;
    }

    .suggestion-text {
      font-size: 16px;
      color: #606266;
      margin: 0;
      font-weight: 500;
      transition: color 0.3s ease;
    }

    .click-hint {
      margin-top: 12px;
      opacity: 0;
      transform: translateX(-10px);
      transition: all 0.3s ease;

      .click-icon {
        font-size: 18px;
        color: #409eff;
        animation: bounce 2s infinite;
      }
    }
  }
}
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes bounce {
  0%,
  20%,
  50%,
  80%,
  100% {
    transform: translateX(0);
  }
  40% {
    transform: translateX(5px);
  }
  60% {
    transform: translateX(3px);
  }
}
// 图例样式
.legend-item {
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    transform: scale(1.1);
  }

  &.legend-disabled {
    opacity: 0.3;
  }

  .legend-color {
    width: 16px;
    height: 16px;
    border-radius: 3px;
    border: 2px solid #fff;
    box-shadow: 0 0 0 1px #ddd;
    transition: all 0.3s;

    &:hover {
      box-shadow: 0 0 0 2px #409eff;
    }
  }
}

.btn-wrap {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0; 
  box-sizing: border-box;
  padding: 16px 24px;
  background: white;
  border-top: 1px solid #ebeef5;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
  z-index: 10;

  .button-group {
    display: flex;
    justify-content: center;
    gap: 20px;
    // flex-wrap: wrap;
    // margin: 0 auto;
    // max-width: 1200px;
  }
}

/* 为主内容区域添加底部间距，避免被固定按钮遮挡 */
.p-24 {
  padding-bottom: 100px !important;
}

/* 页面标识样式 */
.page-header-section {
  padding: 24px;
  background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%);
  // border: 1px solid #e4e7ed;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);

  .page-title-area {
    .title-content {
      display: flex;
      align-items: center;
      margin-bottom: 8px;

      .title-icon {
        font-size: 28px;
        color: #409eff;
        margin-right: 12px;
      }

      .main-title {
        font-size: 24px;
        font-weight: 700;
        color: #303133;
        margin: 0;
        background: linear-gradient(45deg, #409eff, #67c23a);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
      }
    }

    .page-description {
      font-size: 14px;
      color: #606266;
      margin: 0;
      line-height: 1.5;
      padding-left: 40px; // 与图标对齐
    }
  }
}

.action-btn {
  padding: 12px 28px;
  font-size: 15px;
  border-radius: 6px;
  transition: all 0.3s;
  font-weight: 600;
  min-width: 120px;
  /* 普通按钮样式 */
  background-color: #f5f7fa;
  border: 1px solid #dcdfe6;
  color: #606266;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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

}
</style>
