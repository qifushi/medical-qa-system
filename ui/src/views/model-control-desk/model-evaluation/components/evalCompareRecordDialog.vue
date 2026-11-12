<template>
  <el-dialog
    v-model="dialogVisible"
    title="横向对比记录"
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
              placeholder="请输入记录名称查询"
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
    <el-table :data="tableData" border style="width: 100%" v-loading="loadingData">
      <el-table-column
        prop="name"
        label="记录名称"
        min-width="200"
        fixed="left"
        header-align="left"
        align="left"
        show-overflow-tooltip
      />
      <el-table-column
        header-align="center"
        prop="eval_contrast_data.modelData.length"
        label="对比模型数量"
        width="160"
        align="center"
      />
      <el-table-column
        header-align="center"
        prop="update_time"
        label="对比时间"
        align="center"
        width="180"
      >
     <template #default="{ row }">
          {{ moment(row.update_time).format('YYYY-MM-DD HH:mm:ss') }}
        </template>
      </el-table-column>
      <el-table-column align="center" prop="username" label="操作人" width="130"> </el-table-column>
      <el-table-column align="center" prop="action" label="操作" fixed="right" width="130">
        <template #default="{ row }">
          <el-button link type="primary" @click="handleDetail(row)"> 详情 </el-button>
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
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 底部按钮区域 -->
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="closeDialog"> 关闭 </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, defineProps } from 'vue'
import type { FormInstance } from 'element-plus'
import { useRouter } from 'vue-router'
import evaluationApi from '@/api/train-evaluation'
import moment from 'moment'

const props = defineProps({
  isCheckable: {
    type: Boolean,
    default: false
  }
})
// 接口定义
interface QueryParams {
  kw?: string
}
// 接口定义
interface IPagination {
  current_page: number
  page_size: number
}
// 状态管理
const dialogVisible = ref(false)
const queryForm = ref<FormInstance>()
const total = ref(0)
const tableData = ref<any[]>([])
const iPagination = ref<IPagination>({ current_page: 1, page_size: 10 })
const queryParams = reactive<QueryParams>({})

// 打开弹窗
const openDialog = async () => {
  loadingData.value = true
  dialogVisible.value = true

  fetchTableData()
}

// 关闭弹窗
const closeDialog = () => {
  queryForm.value?.resetFields()
  tableData.value = []
  loadingData.value = false
  dialogVisible.value = false
}

// 获取表格数据
const loadingData = ref(false) // 表格数据加载状态
const fetchTableData = async () => {
  loadingData.value = true
  try {
    const res = await evaluationApi.postEvalContrastRecord(iPagination.value, queryParams)
    console.log('%c [ res ]-136', 'font-size:13px; background:pink; color:#bf2c9f;', res)
    if(res.code !== 200) return
    tableData.value = res.data.records || []
    total.value = res.data.total
  } finally {
    loadingData.value = false
  }
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

// 当前页变化
const handleCurrentChange = (val: number) => {
  iPagination.value.current_page = val
  fetchTableData()
}
const router = useRouter()
const handleDetail = (item: any) => {
router.push({
  path: '/model-control-desk/model-evaluation/lateralComparison',
  query: { contrast_id: item.id }
})
  console.log('item', item)
}

// 暴露方法给父组件
defineExpose({
  openDialog,
  closeDialog
})
</script>

<style scoped>
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
