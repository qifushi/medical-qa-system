<template>
  <el-dialog
    v-model="dialogVisible"
    :close-on-click-modal="false"
    title="载入训练参数"
    width="80%"
    top="156px"
    destroy-on-close
  >
    <!-- 查询区域 -->
    <div class="query-section">
      <el-form :model="queryParams" inline>
        <el-form-item label="创建时间">
          <el-date-picker
            v-model="queryParams.createTime"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="模型名称">
          <el-input v-model="queryParams.modelName" placeholder="输入模型名称" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleQuery">
            <el-icon><Search /></el-icon>查询
          </el-button>
          <el-button @click="resetQuery">
            <el-icon><Refresh /></el-icon>重置
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 表格区域 - 修改为单选模式 -->
    <el-table
      :data="tableData"
      highlight-current-row
      @current-change="handleCurrentChange"
      style="width: 100%"
      border
      :row-key="(row) => row.id"
      :expand-row-attributes="expandRowAttributes"
      ref="singleTable"
    >
      <!-- 移除多选框列 -->
      <el-table-column type="expand">
        <template #default="props">
          <div class="detail-container">
            <div class="detail-grid">
              <div v-for="(value, key) in props.row.details" :key="key" class="detail-item">
                <div class="detail-label">{{ key }}:</div>
                <div class="detail-value">{{ value }}</div>
              </div>
            </div>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="createTime" label="创建时间" width="180" sortable />
      <el-table-column prop="modelName" label="模型名称" width="200" />
      <el-table-column prop="finetuningType" label="微调方法" width="150" />
      <el-table-column prop="outputDir" label="输出目录" min-width="200" show-overflow-tooltip />
    </el-table>
    <div style="margin: 6px 0 0; color: #999; font-size: 12px">提示：点击行选中训练参数</div>
    <!-- 分页区域 -->
    <div
      class="pagination-section"
      style="margin: 12px 0; width: 100%; display: flex; justify-content: flex-end"
    >
      <el-pagination
        v-model:current-page="pagination.currentPage"
        v-model:page-size="pagination.pageSize"
        :page-sizes="[5, 10, 20]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :disabled="!currentRow" @click="handleLoadParams">
          载入
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, defineExpose, nextTick } from 'vue'
import { Search, Refresh } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

// 载入参数弹窗相关状态
const dialogVisible = ref(false)
const currentRow = ref(null)
const singleTable = ref(null) // 表格引用

// 查询参数
const queryParams = ref({
  createTime: [],
  modelName: ''
})

// 分页配置
const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  total: 2
})

// 模拟表格数据
const tableData = ref([
  {
    id: 1,
    createTime: '2023-06-15 14:30:22',
    modelName: 'Llama-7B-FT',
    finetuningType: 'LoRA',
    outputDir: '/models/llama-7b-ft-v1',
    details: {
      模型路径: '/models/llama-7b',
      量化等级: '4-bit',
      量化方法: 'GPTQ',
      对话模板: 'Alpaca',
      训练阶段: 'SFT',
      学习率: '5e-5',
      训练轮数: '3',
      批处理大小: '4',
      梯度累积: '8',
      验证集比例: '0.1',
      截断长度: '2048',
      最大梯度范数: '1.0',
      日志间隔: '50',
      保存间隔: '500',
      RoPE插值: '线性',
      加速方式: 'DeepSpeed',
      设备数量: '2',
      'DeepSpeed stage': '2',
      使用offload: '是',
      LoRA秩: '8',
      'LoRA alpha': '32',
      'LoRA dropout': '0.05',
      数据集: 'Alpaca-GPT4',
      数据路径: '/data/alpaca-gpt4',
      计算类型: 'bf16',
      序列打包: '是',
      使用无污染打包: '是',
      最大样本数: '10000',
      输出目录: '/output/llama-7b-ft-v1',
      配置路径: '/config/llama-7b-ft.json'
    }
  },
  {
    id: 2,
    createTime: '2023-07-20 09:15:48',
    modelName: 'ChatGLM2-6B-RLHF',
    finetuningType: 'PPO',
    outputDir: '/models/chatglm2-6b-rlhf',
    details: {
      模型路径: '/models/llama-7b',
      量化等级: '4-bit',
      量化方法: 'GPTQ',
      对话模板: 'Alpaca',
      训练阶段: 'SFT',
      学习率: '5e-5',
      训练轮数: '3',
      批处理大小: '4',
      梯度累积: '8',
      验证集比例: '0.1',
      截断长度: '2048',
      最大梯度范数: '1.0',
      日志间隔: '50',
      保存间隔: '500',
      RoPE插值: '线性',
      加速方式: 'DeepSpeed',
      设备数量: '2',
      'DeepSpeed stage': '2',
      使用offload: '是',
      LoRA秩: '8',
      'LoRA alpha': '32',
      'LoRA dropout': '0.05',
      数据集: 'Alpaca-GPT4',
      数据路径: '/data/alpaca-gpt4',
      计算类型: 'bf16',
      序列打包: '是',
      使用无污染打包: '是',
      最大样本数: '10000',
      输出目录: '/output/llama-7b-ft-v1',
      配置路径: '/config/llama-7b-ft.json'
    }
  }
])

// 打开弹窗
const loadParameters = () => {
  dialogVisible.value = true
  currentRow.value = null
  // 重置选择状态
  nextTick(() => {
    if (singleTable.value) {
      singleTable.value.setCurrentRow(null)
    }
  })
}

// 处理查询
const handleQuery = () => {
  // 实际项目中这里会有API调用
  console.log('执行查询:', queryParams.value)
}

// 重置查询
const resetQuery = () => {
  queryParams.value = {
    createTime: [],
    modelName: ''
  }
  handleQuery()
}

// 处理行选择 - 单选模式
const handleCurrentChange = (row) => {
  currentRow.value = row
}

// 处理分页大小变化
const handleSizeChange = (size) => {
  pagination.value.pageSize = size
  // 实际项目中这里会重新获取数据
}

// 处理页码变化
const handlePageChange = (page) => {
  pagination.value.currentPage = page
  // 实际项目中这里会重新获取数据
}

// 处理载入参数
const handleLoadParams = () => {
  if (currentRow.value) {
    ElMessage.success(`成功载入配置: ${currentRow.value.modelName}`)
    dialogVisible.value = false
    // 触发事件通知父组件
    emit('load', currentRow.value.details)
  } else {
    ElMessage.warning('请先选择一条配置记录')
  }
}

// 展开行样式
const expandRowAttributes = ({ row }) => {
  return {
    style: {
      background: '#f9fafc',
      padding: '20px',
      boxShadow: 'inset 0 2px 5px rgba(0,0,0,0.05)'
    }
  }
}

// 添加事件发射器
const emit = defineEmits(['load'])

// 使用 defineExpose 暴露方法
defineExpose({
  loadParameters
})
</script>

<style lang="scss" scoped>
.dialog-content {
  max-height: 60vh;
  overflow-y: auto;
}
/* 查询区域样式 */
.query-section {
  background-color: #f5f7fa;
  padding: 15px 20px;
  border-radius: 4px;
  margin-bottom: 15px;

  .el-form-item {
    margin-bottom: 0;
    margin-right: 20px;
  }
}

/* 详情区域样式 */
.detail-container {
  padding: 15px;
  max-height: 40vh;
  overflow-y: auto;
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
  flex: 0 0 180px;
  font-weight: 600;
  color: #606266;
}

.detail-value {
  flex: 1;
  color: #303133;
}

/* 分页区域样式 */
.pagination-section {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* 对话框底部样式 */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  padding-top: 15px;
  border-top: 1px solid #ebeef5;
}

/* 展开行样式优化 */
:deep(.el-table__expand-column) .cell {
  display: flex;
  justify-content: center;
}

:deep(.el-table__expanded-cell) {
  padding: 0 !important;
}
</style>
