<template>
  <el-dialog
    v-model="dialogVisible"
    title="模型训练记录"
    width="1000px"
    :close-on-click-modal="false"
  >
    <!-- 查询区域 -->
    <el-form :model="queryParams" ref="queryForm" label-width="100px" @submit.prevent>
      <el-row :gutter="20">
        <el-col :span="16">
          <el-form-item label="" prop="kw" label-width="0px">
            <el-input
              v-model="queryParams.kw"
              placeholder="请输入关键词模糊查询,支持基座名称/训练方法/训练数据集"
              clearable
              @keyup.enter="handleQuery"
            />
          </el-form-item>
        </el-col>
        <el-col :span="8" style="text-align: right">
          <el-button type="primary" @click="handleQuery">搜索</el-button>
          <el-button @click="resetQuery">重置</el-button>
        </el-col>
      </el-row>
    </el-form>

    <!-- 表格区域 -->
    <el-table
      :data="tableData"
      border
      ref="refTable"
      style="width: 100%"
      v-loading="loadingData"
      highlight-current-row
      @current-change="handleCurrentChange"
      :row-key="(row: any) => row.id"
    >
      <el-table-column type="expand" fixed="left">
        <template #default="props">
          <div class="detail-container">
            <div class="detail-grid">
              <template v-for="(dict, index) in FileDict">
                <div :key="index" class="detail-item" v-if="dict.label">
                  <div class="detail-label">{{ dict.label }}:</div>
                  <div class="detail-value">
                    <span v-if="!dict.fieldType">
                      {{ props.row.train_info[dict.value] }}
                    </span>
                    <el-switch
                      v-else-if="dict.fieldType === 'boolean'"
                      :value="props.row[dict.value]"
                    />
                  </div>
                </div>
                <template v-if="dict.child && props.row[dict.value]">
                  <div :key="item.value" class="detail-item" v-for="item in dict.child">
                    <div class="detail-label">{{ item.label }}:</div>
                    <div class="detail-value">
                      <span v-if="!item?.fieldType">
                        {{ props.row.train_info[item.value] }}
                      </span>
                      <el-switch
                        v-else-if="item?.fieldType === 'boolean'"
                        :value="props.row[item.value]"
                      />
                    </div>
                  </div>
                </template>
              </template>
            </div>
          </div>
        </template>
      </el-table-column>
      <el-table-column
        prop="model_name"
        label="模型名称"
        min-width="120"
        fixed="left"
        header-align="center"
        align="center"
      />
      <el-table-column
        header-align="center"
        prop="base_model"
        label="基座名称"
        width="180"
        align="center"
      />
      <el-table-column
        header-align="center"
        prop="finetuning_type"
        label="训练方法"
        align="center"
        width="120"
      />
      <el-table-column header-align="center" prop="train_dataset" label="训练数据集" width="200" />
      <!-- <el-table-column
        header-align="center"
        prop="train_output_dir"
        label="输出路径"
        min-width="150"
      /> -->
      <el-table-column align="center" prop="create_time" label="训练时间" width="180">
        <template #default="{ row }">
          {{ moment(row.create_time).format('YYYY-MM-DD HH:mm:ss') }}
        </template>
      </el-table-column>

      <el-table-column align="center" prop="username" label="操作人" width="130"> </el-table-column>
      <el-table-column
        align="center"
        prop="train_status"
        label="训练状态"
        width="130"
        fixed="right"
      >
        <template #default="{ row }">
          <el-tag :type="statusTagType(row.train_status)" class="status-tag">
            <div style="display: flex; align-items: center">
              <svg
                v-if="row.train_category == 0"
                class="icon-category"
                :style="{ fill: colors[row.train_status as number] }"
                viewBox="0 0 24 24"
              >
                <path d="M13 1L3 14H12L11 23L21 10H12L13 1Z" />
              </svg>
              <svg
                v-else
                class="icon-category"
                :style="{ fill: colors[row.train_status as number] }"
                viewBox="0 0 24 24"
              >
                <path d="M12 15.5A3.5 3.5 0 1 1 15.5 12 3.5 3.5 0 0 1 12 15.5z" />
                <path
                  d="M19.14 12.94c-.04-.3-.06-.61-.06-.94s.02-.64.06-.94l2.03-1.58a.49.49 0 0 0 .12-.61l-1.92-3.32a.488.488 0 0 0-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54a.484.484 0 0 0-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.71 8.87c-.14.23-.08.5.12.61l2.03 1.58c.04.3.06.61.06.94s-.02.64-.06.94l-2.03 1.58a.49.49 0 0 0-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.5-.12-.61l-2.01-1.58z"
                />
              </svg>
              {{ ` ${renderDictLabel(row.train_status, constantsOptions.TrainStatusOption)}` }}
              <span v-if="row.progressPercentage">{{ row.progressPercentage }}</span>
            </div>
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column align="center" prop="action" label="操作" fixed="right" width="130">
        <template #default="{ row }">
          <el-button link type="primary" @click="handleDetail(row)"> 详情 </el-button>
          <template v-if="row.train_status == 1">
            <el-button link type="danger" @click="handleInterrupt"> 中断 </el-button>
          </template>
        </template>
      </el-table-column>
    </el-table>
    <div v-if="props.isCheckable" style="margin: 6px 0 0; color: #999; font-size: 12px">
      提示：点击行选中训练参数
    </div>
    <!-- 分页区域 -->
    <div class="pagination-container">
      <el-pagination
        v-model:current-page="iPagination.current_page"
        v-model:page-size="iPagination.page_size"
        :total="total"
        :page-sizes="[10, 20, 30, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />
    </div>

    <!-- 底部按钮区域 -->
    <template #footer>
      <div class="dialog-footer">
        <el-button
          type="primary"
          v-if="props.isCheckable"
          :disabled="!currentRow"
          @click="handleLoadParams"
        >
          载入
        </el-button>
        <el-button @click="closeDialog"> 关闭 </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, defineProps, nextTick } from 'vue'
import type { FormInstance } from 'element-plus'
import { ElLoading } from 'element-plus'
import moment from 'moment'
import { FileDict } from '@/views/model-control-desk/utils/config'
import constantsOptions from '@/views/model-control-desk/utils/constantsOptions'
import {
  GetTrainLog,
  AddTrainLog,
  GetTrainLogDetail,
  UpdateTrainLog,
  DelTrainLog
} from '@/api/train-training'
import { GetProcesses, FnMonitor, FnBreakOff } from '@/api/train-common'
import useStore from '@/stores'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
const props = defineProps({
  isCheckable: {
    type: Boolean,
    default: false
  },
  category: {
    type: Number,
    default: 0
  }
})
// 接口定义
interface QueryParams {
  kw?: string
  train_status?: number
  train_category?: number
}
// 接口定义
interface IPagination {
  current_page: number
  page_size: number
}

interface TableItem {
  id: number
  base_model: string
  finetuning_type: string
  train_dataset: string
  train_output_dir: string
  create_time: string
  train_status: string
}
const refTable = ref()
const currentRow = ref()

// 状态管理
const dialogVisible = ref(false)
const queryForm = ref<FormInstance>()
const total = ref(0)
const tableData = ref<TableItem[]>([])
const iPagination = ref<IPagination>({ current_page: 1, page_size: 10 })
const processesInstance = ref<any>([])
const queryParams = reactive<QueryParams>({})

// 打开弹窗
const openDialog = async () => {
  loadingData.value = true
  dialogVisible.value = true
  let res = await GetProcesses()
  if (res.data && res.data[0]) {
    processesInstance.value = res.data[0]
      .filter((item: any) => item.name === 'llamafactory-cl')
      .map((item: any) => item.cmdline[item.cmdline.length - 1])
  }
  fetchTableData()
}

const clearChecked = () => {
  nextTick(() => {
    if (refTable.value) {
      currentRow.value = null
      refTable.value.setCurrentRow(null)
    }
  })
}
// 关闭弹窗
const closeDialog = () => {
  clearChecked()
  queryForm.value?.resetFields()
  tableData.value = []
  loadingData.value = false
  dialogVisible.value = false
}

const renderDictLabel = (value: any, options: Array<any>) => {
  let target = options.find((item: any) => item.value == value)
  if (target) return target?.abbreviation || target?.label
  else return '快'
}
const handleInterrupt = () => {
  const loading = ElLoading.service({
    lock: true,
    text: '训练中断中...请稍后！'
  })
  FnBreakOff().finally(() => {
    loading.close()
    fetchTableData()
  })
}
const colors: Record<number, string> = {
  1: '#67c23a',
  2: '#2F99FF',
  3: '#e6a23c',
  4: '#909399'
}
// 状态标签类型
const statusTagType = (status: any) => {
  switch (status) {
    case 1:
      return 'success'
    case 3:
      return 'warning'
    case 2:
      return 'primary'
    case 4:
      return 'info'
    default:
      return 'info'
  }
}
const FnCalculationProgress = (data: any[]) => {
  let target = data[data.length - 1]
  return (
    (target && Math.floor((target.current_steps / target.total_steps) * 10000) / 100 + '%') || '0%'
  )
}
// 获取表格数据
const loadingData = ref(false)
const fetchTableData = async () => {
  loadingData.value = true
  GetTrainLog(
    {
      current_page: iPagination.value.current_page,
      page_size: iPagination.value.page_size
    },
    Object.assign({}, queryParams, {
      train_category: props.category
    })
  )
    .then((res: any) => {
      if (res.code == 200) {
        tableData.value = res.data.records || []
        total.value = res.data.total
        let ajaxList = tableData.value.filter(
          (item) => item.train_status == '0' || item.train_status == '1'
        )
        Promise.all(
          ajaxList.map((item: any) => {
            let params = {
              do_train: true,
              output_dir: item.train_output_dir,
              finetuning_type: item.finetuning_type,
              lang: item.lang,
              model_name: item.base_model
            }
            return FnMonitor(params)
          })
        )
          .then((res) => {
            ajaxList.forEach((i, index) => {
              let target: any = tableData.value.find((item) => i.id == item.id)
              if (target && res[index].data && res[index].data[0]) {
                let finish_info = res[index].data[0].finish_info
                let running_info = res[index].data[0].running_info
                target.train_log = res[index].data[0].running_log
                let progressPercentage = FnCalculationProgress(running_info) || 0
                if (progressPercentage == 100) {
                  let finishInfoObj = {}
                  try {
                    finishInfoObj = JSON.parse(finish_info.replace(/```json\s*|\s*```/g, ''))
                  } catch (error) {
                    finishInfoObj = {}
                  }
                  target.train_result = finishInfoObj
                  target.train_log = running_info
                  target.train_status = 2
                } else {
                  let url = `saves/${target.base_model}/${target.finetuning_type}/${target.train_output_dir}/training_args.yaml`
                  if (processesInstance.value.includes(url)) {
                    target.train_status = 1
                    target.progressPercentage = progressPercentage
                  } else {
                    target.train_status = 3
                  }
                  target.train_result = {}
                }
                UpdateTrainLog(target.id, target)
              }
            })
          })
          .finally(() => {
            loadingData.value = false
          })
      }
    })
    .catch(() => {
      tableData.value = []
      total.value = 0
    })
}

// 处理查询
const handleQuery = () => {
  iPagination.value.current_page = 1
  fetchTableData()
}

// 重置查询
const resetQuery = () => {
  if (queryForm.value) {
    queryForm.value.resetFields()
  }
  iPagination.value.current_page = 1
  handleQuery()
}

// 分页大小变化
const handleSizeChange = (val: number) => {
  iPagination.value.page_size = val
  fetchTableData()
}
const handleCurrentChange = (row: any) => {
  currentRow.value = row
}
// 当前页变化
const handlePageChange = (val: number) => {
  clearChecked()
  iPagination.value.current_page = val
  fetchTableData()
}
const router = useRouter()
const handleDetail = (item: any) => {
  if (item.train_category == 0) {
    router.push('/model-control-desk/model-training/simpleness?trainLogId=' + item.id)
  } else {
    router.push('/model-control-desk/model-training/major?trainLogId=' + item.id)
  }
  console.log('item', item)
}
const emit = defineEmits(['loadParams'])
const handleLoadParams = () => {
  if (currentRow.value) {
    ElMessage.success(`成功载入配置`)
    emit('loadParams', currentRow.value.train_info)
    closeDialog()
  }
}

// 暴露方法给父组件
defineExpose({
  openDialog,
  closeDialog
})
</script>

<style scoped>
.status-tag{
  width: 100px;
}
.icon-category {
  width: 16px;
  height: 16px;
  fill: #4d6bfe;
  transition: all 0.3s ease;
  /* margin-right: 2px; */
}
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 24px;
}

/* 详情区域样式 */
.detail-container {
  padding: 15px;
  max-height: 40vh;
  overflow-y: auto;
  width: 800px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.detail-item {
  display: flex;
  border-bottom: 1px solid #ebeef5;
  padding: 8px 0;
}

.detail-label {
  flex: 0 0 140px;
  font-weight: 600;
  color: #606266;
}

.detail-value {
  flex: 1;
  color: #303133;
}
</style>
