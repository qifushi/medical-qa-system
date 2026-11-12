<template>
  <div>
    <el-row>
      <el-col :span="17" class="page-height">
        <div style="padding: 16px 12px 24px 24px">
          <div class="container-title mb-16">
            <h4>模型评测</h4>
            <el-input
              v-model="searchValue"
              @change="searchHandle"
              placeholder="按名称搜索"
              prefix-icon="Search"
              class="w-240"
              clearable
            />
          </div>
          <div v-loading.fullscreen.lock="paginationConfig.current_page === 1 && loading">
            <div v-if="tableData.length > 0">
              <InfiniteScroll
                :size="tableData.length"
                :total="paginationConfig.total"
                :page_size="paginationConfig.page_size"
                v-model:current_page="paginationConfig.current_page"
                @load="getList"
                :loading="loading"
              >
                <el-row :gutter="15">
                  <el-col
                    :xs="24"
                    :sm="12"
                    :md="8"
                    :lg="8"
                    :xl="8"
                    v-for="(item, index) in tableData"
                    :key="index"
                    class="mb-16"
                  >
                    <CardBox
                      :title="item.model_name"
                      @click="handleEvaluation(item)"
                      :description="item.model_desc"
                      :disabled="!canSelect(item)"
                      class="application-card cursor boxShadow"
                      :class="{
                        'comparison-mode': isComparisonMode,
                        'selected-card': isComparisonMode && selectedIds.includes(item.id)
                      }"
                    >
                      <template #icon>
                        <AppIcon iconName="app-smartModel-icon" class="card-icon"></AppIcon>
                      </template>
                      <div class="status-tag">
                        <el-tag
                          :type="getEvalStatusType(item)"
                          effect="plain"
                          style="border-radius: 4px"
                        >
                          {{ getEvalStatusText(item) }}
                        </el-tag>
                      </div>
                      <div class="card-content">
                        <div class="info-item">
                          <span class="label">基座模型：</span>
                          <auto-tooltip :content="item.base_model">
                            <span class="value">{{ item.base_model }}</span>
                          </auto-tooltip>
                        </div>
                        <div class="info-item">
                          <span class="label">微调方法：</span>
                          <auto-tooltip :content="item.finetuning_type">
                            <span class="value">{{ item.finetuning_type }}</span>
                          </auto-tooltip>
                        </div>
                        <div class="info-item">
                          <span class="label">训练阶段：</span>
                          <auto-tooltip :content="item.train_info.training_stage">
                            <span class="value">{{ item.train_info.training_stage }}</span>
                          </auto-tooltip>
                        </div>
                        <div class="info-item">
                          <span class="label">训练数据集：</span>
                          <auto-tooltip :content="item.train_info.dataset?.join(', ') || ''">
                            <span
                              v-for="(dataset, index) in item.train_info.dataset"
                              :key="index"
                              class="value"
                            >
                              {{ dataset }}
                              <span v-if="index < item.train_info.dataset.length - 1">, </span>
                            </span>
                          </auto-tooltip>
                        </div>
                      </div>
                    </CardBox>
                  </el-col>
                </el-row>
              </InfiniteScroll>
            </div>
            <div v-else class="flex-center page-height">
              <el-empty description="暂无模型数据" />
            </div>
          </div>
        </div>
      </el-col>
      <el-col :span="7" class="flex-center right">
        <div class="right-container">
          <el-card shadow="never" class="info-card mb-16">
            <template #header>
              <div class="card-header">
                <span class="header-title">模型评测介绍</span>
              </div>
            </template>
            <div class="info-content">
              <p class="info-desc">
                模型评测是对AI模型进行性能测试和质量评估的过程，通过多种指标衡量模型的准确性和实用性。
              </p>
              <div class="metrics-list">
                <el-tag size="small" class="metric-tag">BLEU-4</el-tag>
                <el-tag size="small" class="metric-tag">ROUGE-1</el-tag>
                <el-tag size="small" class="metric-tag">ROUGE-2</el-tag>
              </div>
            </div>
          </el-card>
          <el-card shadow="never" class="task-card mb-16">
            <template #header>
              <div class="card-header">
                <span class="header-title">服务器任务进展</span>
              </div>
            </template>
            <div class="task-content">
              <div class="task-item">
                <div class="task-info">
                  <span class="task-name">模型评测任务</span>
                  <span class="task-status running">进行中</span>
                </div>
                <el-progress :percentage="65" :stroke-width="6" />
                <div class="task-detail">已完成 13/20 步骤</div>
              </div>

              <div class="server-stats">
                <div class="stat-item">
                  <span class="stat-label">CPU使用率:</span>
                  <span class="stat-value">45%</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">内存使用:</span>
                  <span class="stat-value">6.2GB</span>
                </div>
              </div>
            </div>
          </el-card>
          <el-card shadow="never" class="action-card">
            <template #header>
              <div class="card-header">
                <span class="header-title">快捷操作</span>
              </div>
            </template>
            <div class="action-content">
              <div class="action-row">
                <el-dropdown placement="top-start" style="width: 100%" @command="startEvaluation">
                  <el-button type="primary" class="action-btn primary-btn">快速评测</el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item
                        :command="item.id"
                        :key="item.id"
                        v-for="item in quickEvalOptions"
                        >{{ item.model_name }}</el-dropdown-item
                      >
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
              <div class="action-row">
                <!-- <el-button @click="exportReport" class="action-btn">导出报告</el-button> -->
                <el-button @click="goLateralComparison" class="action-btn">横向对比</el-button>
                <el-button @click="evalCompareRecordDialogRef.openDialog()" class="action-btn"
                  >横向对比记录</el-button
                >
              </div>
            </div>
          </el-card>
        </div>
      </el-col>
    </el-row>

    <!-- 底部选中区域 -->
    <transition name="slide-up">
      <div v-if="isComparisonMode" class="comparison-bottom-panel">
        <div class="panel-content">
          <div class="selected-models-area">
            <div class="selected-title">
              <el-icon><MessageBox /></el-icon>
              已选择模型 ({{ selectedModelsForComparison.length }})
            </div>
            <div class="selected-models-list">
              <transition-group name="card-list" tag="div" class="models-container">
                <div
                  v-for="model in selectedModelsForComparison"
                  :key="model.id"
                  class="selected-model-card"
                >
                  <div class="model-avatar">
                    <AppIcon iconName="app-smartModel-icon" class="avatar-icon"></AppIcon>
                  </div>
                  <div class="model-info">
                    <div class="model-name-row">
                      <div class="model-name">{{ model.model_name }}</div>
                      <div class="model-status">
                        <el-tag :type="getEvalStatusType(model)" effect="plain" size="small">
                          {{ getEvalStatusText(model) }}
                        </el-tag>
                      </div>
                    </div>
                    <!-- <div class="model-desc">{{ model.model_desc || model.base_model }}</div> -->
                    <div>
                      <div class="info-item">
                        <span class="label">基座模型：</span>
                        <auto-tooltip :content="model.model_desc || model.base_model">
                          <span class="value">{{ model.model_desc || model.base_model }}</span>
                        </auto-tooltip>
                      </div>
                    </div>
                  </div>
                  <el-button
                    type="danger"
                    size="small"
                    circle
                    @click="removeFromComparison(model.id)"
                    class="remove-btn"
                  >
                    <el-icon><Close /></el-icon>
                  </el-button>
                </div>
              </transition-group>
            </div>
          </div>
          <div class="panel-actions">
            <el-button
              type="primary"
              size="large"
              :disabled="selectedModelsForComparison.length === 0"
              @click="goLateralComparison"
              class="action-btn primary-btn big-size"
            >
              <el-icon class="btn-icon"><TrendCharts /></el-icon>
              <span class="btn-text">开始横向对比</span>
              <span class="btn-count">({{ selectedModelsForComparison.length }})</span>
            </el-button>
            <el-button size="large" @click="cancelComparison" class="action-btn cancel-btn">
              <el-icon class="btn-icon"><Close /></el-icon>
              <span class="btn-text">取消横向对比</span>
            </el-button>
          </div>
        </div>
      </div>
    </transition>
    <evalCompareRecordDialog ref="evalCompareRecordDialogRef"></evalCompareRecordDialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
// import modelEvaApi from '@/api/train-evaluation'
import * as modelEvaApi from '@/api/train-training'
import { MsgWarning } from '@/utils/message'
import { useRouter } from 'vue-router'
import evaluationApi from '@/api/train-evaluation'
import useStore from '@/stores'
import evalCompareRecordDialog from './components/evalCompareRecordDialog.vue'

const { evaModelSelected } = useStore()
const evalCompareRecordDialogRef = ref()
const router = useRouter()
const loading = ref(false)
const tableData = ref<any[]>([])
const quickEvalOptions = computed(() => {
  return tableData.value.filter(
    (item) =>
      !item.eval_obj.find(
        (i: any) => i.eval_status === 2 || item.eval_obj.find((i: any) => i.eval_status === 1)
      )
  )
})
const searchValue = ref('')
const paginationConfig = reactive({
  current_page: 1,
  page_size: 20,
  total: 0
})
function startEvaluation(item: any) {
  router.push('/model-control-desk/evaluation-detail?trainLogId=' + item)
}
function exportReport() {
  // 导出报告逻辑
  console.log('导出报告')
}

// 获取数据列表
const getList = async () => {
  console.log('getlist-----')

  loading.value = true
  const params = {
    kw: searchValue.value || '',
    train_status: '2'
  }
  try {
    // todo:后续需要更换接口
    const res = await modelEvaApi.GetTrainLog(paginationConfig, params)
    paginationConfig.total = res.data.total
    let newData = res.data.records
    let list: any = []
    newData.forEach((item: any) => {
      list.push(
        evaluationApi.GetEvalInfoByTrainId(item.id).then((res) => {
          item.eval_obj = res.data
          return res
        })
      )
    })
    Promise.all(list)
      .then((res) => {
        if (paginationConfig.current_page === 1) {
          tableData.value = newData
        } else {
          tableData.value = [...tableData.value, ...newData]
        }
        console.log(tableData.value)
      })
      .finally(() => {
        loading.value = false
      })
  } catch (error) {
    console.error(error)
    loading.value = false
  } finally {
    console.log('guanbi ')
  }
}

function searchHandle() {
  paginationConfig.total = 0
  paginationConfig.current_page = 1
  tableData.value = []
  getList()
}

function goLateralComparison() {
  if (!isComparisonMode.value) {
    // 进入多选模式
    isComparisonMode.value = true
    selectedIds.value = []
  } else {
    if (selectedIds.value.length === 0) {
      MsgWarning('请先选择数据')
      return
    }

    // 通过id筛选出选中的完整数据，并只保留 status === 2 的评测数据
    const selectedModels = tableData.value
      .filter((item) => selectedIds.value.includes(item.id))
      .map((item) => {
        // 只保留 status === 2 的评测数据
        const completedEval = item.eval_obj?.find((item: any) => item.eval_status === 2)
        return {
          ...item,
          eval_obj: completedEval ? [completedEval] : []
        }
      })
      .filter((item) => item.eval_obj.length > 0) // 过滤掉没有完成评测的数据

    console.log(selectedIds.value, 'selectedIds.value')
    console.log(selectedModels, 'filteredSelectedModels')

    evaModelSelected.setSelectedModels(selectedModels)
    router.push({
      path: '/model-control-desk/model-evaluation/lateralComparison'
    })
  }
}

const handleEvaluation = (record: any) => {
  if (isComparisonMode.value) {
    toggleSelect(record.id)
  } else {
    if (!record.id) return
    router.push('/model-control-desk/evaluation-detail?trainLogId=' + record.id)
  }
}

// ----- 多选 进行横向对比 ---
const isComparisonMode = ref(false)
const selectedModelsForComparison = computed(() => {
  return tableData.value.filter((item) => selectedIds.value.includes(item.id))
})
const selectedIds = ref<number[]>([])
function toggleSelect(id: number) {
  // 找到对应的项目
  const item = tableData.value.find((item) => item.id === id)
  if (!item || !canSelect(item)) {
    return MsgWarning('该模型暂未完成评测，无法进行横向对比') // 如果不能选择，直接返回
  }

  const idx = selectedIds.value.indexOf(id)
  if (idx > -1) {
    selectedIds.value.splice(idx, 1)
  } else {
    selectedIds.value.push(id)
  }
  console.log(selectedIds.value, 'selectedIds.value')
}
// 取消横向对比模式
function cancelComparison() {
  isComparisonMode.value = false
  selectedIds.value = []
}

// 从底部区域删除选中的模型
function removeFromComparison(id: number) {
  const idx = selectedIds.value.indexOf(id)
  if (idx > -1) {
    selectedIds.value.splice(idx, 1)
  }
}

onMounted(() => {
  getList()
})
// 暴露方法供父组件调用
defineExpose({
  getList
})

// 获取评测状态文本
function getEvalStatusText(item: any) {
  if (!item.eval_obj || !Array.isArray(item.eval_obj) || item.eval_obj.length === 0) {
    return '未评测'
  }

  // 优先查找 status === 2 的数据
  const completedEval = item.eval_obj.find((item: any) => item.eval_status === 2)
  if (completedEval) {
    return '已完成'
  }

  // 其次查找 status === 1 的数据
  const inProgressEval = item.eval_obj.find((item: any) => item.eval_status === 1)
  if (inProgressEval) {
    return '进行中'
  }

  return '未评测'
}

// 获取评测状态标签类型
function getEvalStatusType(item: any) {
  if (!item.eval_obj || !Array.isArray(item.eval_obj) || item.eval_obj.length === 0) {
    return 'info'
  }

  // 优先查找 status === 2 的数据
  const completedEval = item.eval_obj.find((item: any) => item.eval_status === 2)
  if (completedEval) {
    return 'success' // 已完成 - 绿色
  }

  // 其次查找 status === 1 的数据
  const inProgressEval = item.eval_obj.find((item: any) => item.eval_status === 1)
  if (inProgressEval) {
    return 'warning' // 进行中 - 橙色
  }

  return 'info' // 未评测 - 灰色
}

// 检查是否可以选择（只有 status === 2 的可以选择）
function canSelect(item: any) {
  if (!item.eval_obj || !Array.isArray(item.eval_obj) || item.eval_obj.length === 0) {
    return false
  }

  return item.eval_obj.some((item: any) => item.eval_status === 2)
}
</script>

<style lang="scss" scoped>
.flex-center {
  display: flex;
  justify-content: center;
  align-items: center;
}
.page-height {
  height: calc(100vh - 56px);
}
.right {
  position: absolute;
  right: 0px;
  width: 100%;
  padding: 65px 12px 12px;
  .right-container {
    width: 100%;
    background-color: #fff;
    border-radius: 8px;
    padding: 16px;
  }

  .card-header {
    display: flex;
    align-items: center;
    font-weight: 500;
    font-size: 14px;
    color: var(--app-text-color-primary);
    margin-bottom: 4px;
  }

  // 介绍卡片样式
  .info-card {
    margin-bottom: 16px;

    .info-content {
      .info-desc {
        font-size: 13px;
        color: var(--app-text-color-secondary);
        line-height: 1.5;
        margin-bottom: 12px;
      }

      .metrics-list {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;

        .metric-tag {
          font-size: 12px;
        }
      }
    }
  }
  // 任务进展卡片样式
  .task-card {
    .task-content {
      .task-item {
        margin-bottom: 16px;

        .task-info {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 8px;

          .task-name {
            font-size: 13px;
            font-weight: 500;
          }

          .task-status {
            font-size: 12px;
            padding: 2px 8px;
            border-radius: 12px;

            &.running {
              background-color: rgba(230, 162, 60, 0.1);
              color: #e6a23c;
            }
          }
        }

        .task-detail {
          font-size: 12px;
          color: var(--app-text-color-secondary);
          margin-top: 8px;
        }
      }

      .server-stats {
        margin-top: 16px;
        padding-top: 12px;
        border-top: 1px solid var(--el-border-color-lighter);

        .stat-item {
          display: flex;
          gap: 8px;
          margin-bottom: 8px;
          font-size: 13px;

          .stat-label {
            color: var(--app-text-color-secondary);
          }

          .stat-value {
            color: var(--app-text-color-primary);
            font-weight: 500;
          }
        }
      }
    }
  }
  // 操作卡片样式
  .action-card {
    .action-content {
      .action-row {
        display: flex;
        gap: 12px;
        margin-bottom: 12px;

        &:last-child {
          margin-bottom: 0;
        }

        .el-button {
          flex: 1;
        }

        // 响应式适配 - 小屏幕垂直布局
        @media (max-width: 768px) {
          flex-direction: column;
          gap: 8px;

          .el-button {
            width: 100%;
            flex: none;
          }
          .el-button + .el-button {
            margin-left: 0 !important;
          }
        }
      }
    }
  }
}
.container-title {
  display: flex;
  align-items: center;
  gap: 16px;
}
// .application-card {
.card-content {
  margin-top: 12px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 6px;
  font-size: 12px;
  color: var(--app-text-color-secondary);

  .label {
    flex-shrink: 0;
    font-weight: 500;
  }

  .value {
    flex: 1;
    color: #333439;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    min-width: 0;
  }
}

.card-icon {
  font-size: 14px;
  color: #5e6772;
  border: 1px solid #dfe2e5;
  border-radius: 4px;
  padding: 4px;
  margin-right: 8px;
}
.status-tag {
  position: absolute;
  right: 16px;
  // top: 20px;
  top: 16px;
}
// }
.dropdown-custom-switch {
  padding: 5px 11px;
  font-size: 14px;
  font-weight: 400;
  span {
    margin-right: 26px;
  }
}
.footer {
  text-align: center;
  padding: 10px 0;
  width: 100%;
  position: fixed;
  bottom: 0;
  left: 0;
  color: #909399;
  background-color: var(--app-layout-bg-color);
}

.boxShadow:hover {
  background: linear-gradient(
      179deg,
      rgba(64, 158, 255, 0.22) -8.26%,
      hsla(0deg, 0%, 100%, 0) 44.84%
    ),
    #fff;
  box-shadow: 0px 12px 30px rgba(122, 161, 225, 0.2);
}
// 横向对比模式card样式
// .comparison-mode-tip {
//   margin-right: 16px;
// }

.comparison-mode {
  transition: all 0.2s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(64, 158, 255, 0.15);
  }
}

.selected-card {
  border: 1px solid #409eff !important;
  background: linear-gradient(135deg, #ecf5ff 0%, #f0f9ff 100%);

  .card-icon {
    color: #409eff;
    border-color: #409eff;
  }
}

// 底部面板样式
.comparison-bottom-panel {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 180px; // 固定高度
  background: linear-gradient(135deg, #ffffff 0%, #f0f4ff 100%);
  border-top: 1px solid #e4e7ed;
  box-shadow: 0 -8px 32px rgba(0, 0, 0, 0.12);
  z-index: 1000;
  backdrop-filter: blur(8px);

  .panel-content {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    padding: 16px 24px;
    max-width: 1500px;
    margin: 0 auto;
    gap: 24px;
    height: 100%;
    box-sizing: border-box;
  }

  .selected-models-area {
    flex: 1;
    min-width: 0;
    height: 100%;
    display: flex;
    flex-direction: column;

    .selected-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-weight: 600;
      font-size: 16px;
      color: #409eff;
      margin-bottom: 12px;
      flex-shrink: 0;

      .el-icon {
        font-size: 18px;
      }
    }

    .selected-models-list {
      flex: 1;
      min-height: 0;

      .models-container {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        height: 120px; // 固定容器高度
        overflow-y: auto;
        padding: 4px 8px 4px 4px;

        // 自定义滚动条
        &::-webkit-scrollbar {
          width: 6px;
        }

        &::-webkit-scrollbar-track {
          background: #f1f1f1;
          border-radius: 3px;
        }

        &::-webkit-scrollbar-thumb {
          background: #c1c1c1;
          border-radius: 3px;

          &:hover {
            background: #a8a8a8;
          }
        }
      }
    }

    .selected-model-card {
      display: flex;
      align-items: center;
      background: #fff;
      border: 1px solid #e1e8ff;
      border-radius: 8px;
      padding: 10px 12px;
      min-width: 260px;
      max-width: 300px;
      height: 52px; // 固定卡片高度
      position: relative;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      box-shadow: 0 2px 8px rgba(64, 158, 255, 0.08);
      flex-shrink: 0;

      &:hover {
        border-color: #409eff;
        box-shadow: 0 4px 16px rgba(64, 158, 255, 0.15);
        transform: scale(1.02);

        .remove-btn {
          opacity: 1;
          transform: scale(1);
        }
      }

      .model-avatar {
        flex-shrink: 0;
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, #409eff 0%, #3370ff 100%);
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 10px;

        .avatar-icon {
          color: #fff;
          font-size: 14px;
        }
      }

      .model-info {
        flex: 1;
        min-width: 0;

        .model-name-row {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 6px;
          margin-bottom: 2px;
        }

        .model-name {
          font-size: 13px;
          font-weight: 600;
          color: #303133;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
          flex: 1;
          min-width: 0;
        }

        .model-status {
          flex-shrink: 0;

          .el-tag {
            font-size: 10px;
            height: 18px;
            line-height: 16px;
            padding: 0 6px;
          }
        }

        .model-desc {
          font-size: 11px;
          color: #909399;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }
      }

      .remove-btn {
        position: absolute;
        top: -4px;
        right: -4px;
        width: 18px;
        height: 18px;
        opacity: 0;
        transform: scale(0.8);
        transition: all 0.2s ease;
        background: #409eff;
        border-color: #409eff;

        &:hover {
          background: #3370ff;
          border-color: #3370ff;
        }

        .el-icon {
          font-size: 9px;
          color: #fff;
        }
      }
    }
  }

  .panel-actions {
    display: flex;
    flex-direction: column;
    gap: 20px;
    flex-shrink: 0;
    justify-content: center;
    height: 100%;

    :deep(.el-button + .el-button) {
      margin-left: 0 !important;
    }

    .cancel-btn {
      min-width: 180px;
      height: 36px;
      border-radius: 6px;
      border: 1px solid #dcdfe6;
      color: #606266;
      background: #fff;
      transition: all 0.3s ease;

      &:hover {
        border-color: #409eff;
        color: #409eff;
        background: #ecf5ff;
      }

      .el-icon {
        margin-right: 6px;
      }
    }
  }
}

// 优化过渡动画
.slide-up-enter-active {
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.slide-up-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.6, 1);
}

.slide-up-enter-from {
  transform: translateY(100%);
  opacity: 0;
}

.slide-up-leave-to {
  transform: translateY(100%);
  opacity: 0;
}

// 卡片列表动画
.card-list-enter-active {
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.card-list-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.6, 1);
}

.card-list-enter-from {
  opacity: 0;
  transform: scale(0.8) translateY(20px);
}

.card-list-leave-to {
  opacity: 0;
  transform: scale(0.8) translateY(-20px);
}

.card-list-move {
  transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

// 响应式适配
@media (max-width: 1200px) {
  .comparison-bottom-panel {
    height: 200px; // 小屏幕稍微增加高度

    .panel-content {
      flex-direction: column;
      align-items: stretch;
      gap: 12px;
      padding: 12px 20px;
    }

    .selected-models-area {
      .models-container {
        height: 100px;
      }
    }

    .panel-actions {
      flex-direction: row;
      justify-content: center;

      .compare-btn,
      .cancel-btn {
        min-width: 140px;
        height: 36px;
      }
    }
  }
}
.action-btn {
  padding: 12px 28px;
  font-size: 15px;
  border-radius: 6px;
  transition: all 0.3s;
  // font-weight: 600;
  // min-width: 120px;
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
  &.big-size {
    height: 60px;
    font-size: 16px;
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
</style>
