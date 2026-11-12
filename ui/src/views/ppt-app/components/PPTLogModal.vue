<template>
  <el-dialog
    v-model="dialogVisible"
    title="智能PPT生成记录"
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
              placeholder="请输入关键词模糊查询,支持PPT标题/PPT内容描述/大纲"
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
      :row-key="(row: any) => row.id"
    >
      <el-table-column
        prop="title"
        label="PPT标题"
        width="120"
        fixed="left"
        header-align="center"
        align="center"
      />
      <el-table-column
        header-align="center"
        prop="theme"
        label="PPT主题"
        width="180"
        align="center"
      />
      <el-table-column
        header-align="center"
        prop="description"
        label="PPT内容描述"
        align="center"
        width="120"
      />
      <el-table-column header-align="center" prop="lang" label="语言" width="200" />
      <el-table-column align="center" prop="create_time" label="生成时间" width="180">
        <template #default="{ row }">
          {{ moment(row.create_time).format('YYYY-MM-DD HH:mm:ss') }}
        </template>
      </el-table-column>
      <el-table-column align="center" prop="user_name" label="操作人" width="130">
      </el-table-column>
      <el-table-column align="center" prop="action" label="操作" fixed="right" width="130">
        <template #default="{ row }">
          <el-button link type="primary" @click="handleDetail(row)"> 详情 </el-button>
        </template>
      </el-table-column>
    </el-table>
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
        <el-button @click="closeDialog"> 关闭 </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, defineProps, nextTick } from 'vue'
import type { FormInstance } from 'element-plus'
import moment from 'moment'
import {
  GetSmartPPT,
  AddSmartPPT,
  GetSmartPPTDetail,
  UpdateSmartPPT,
  DelSmartPPT
} from '@/api/smartPPT'
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

const colors: Record<number, string> = {
  1: '#67c23a',
  2: '#2F99FF',
  3: '#e6a23c',
  4: '#909399'
}

// 获取表格数据
const loadingData = ref(false)
const fetchTableData = async () => {
  loadingData.value = true
  GetSmartPPT(
    {
      current_page: iPagination.value.current_page,
      page_size: iPagination.value.page_size
    },
    Object.assign({}, queryParams)
  )
    .then((res: any) => {
      if (res.code == 200) {
        tableData.value = res.data.records || []
        total.value = res.data.total
      }
    })
    .finally(() => {
      loadingData.value = false
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

// 当前页变化
const handlePageChange = (val: number) => {
  iPagination.value.current_page = val
  fetchTableData()
}
const router = useRouter()
const handleDetail = (item: any) => {

  console.log('item', item)
}

// 暴露方法给父组件
defineExpose({
  openDialog,
  closeDialog
})
</script>

<style scoped>
.status-tag {
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
