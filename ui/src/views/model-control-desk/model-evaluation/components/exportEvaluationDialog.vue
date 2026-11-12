<template>
  <el-dialog
    v-model="dialogVisible"
    title="保存横向对比记录"
    width="900px"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
  >
    <el-form ref="formRef" :model="form" :rules="rules" label-width="120px" label-position="top">
      <el-form-item label="记录名称" prop="taskName">
        <el-input v-model="form.taskName" placeholder="请输入" maxlength="50" show-word-limit />
      </el-form-item>
      <el-form-item label="保存量化数据集" prop="export_quantization_dataset">
        <template #label>
          <span class="form-label-flex">
            保存量化数据集
            <el-tooltip content="量化过程中使用的校准数据集。" placement="top">
              <span class="icon-flex">
                <AppIcon iconName="InfoFilled"></AppIcon>
              </span>
            </el-tooltip>
          </span>
        </template>
        <el-input v-model="form.export_quantization_dataset" placeholder="请输入" />
      </el-form-item>

      <el-form-item label="请选择保存模型" prop="selectedCheckpoint" class="form-item">
        <div class="model-cards-container">
          <div
            v-for="model in modelData"
            :key="model.id"
            class="model-card"
            :class="{
              selected: isModelSelected(model),
              exported: isModelExported(model),
              disabled: !canSelectModel(model)
            }"
            @click="handleCardSelect(model)"
          >
            <div class="card-header">
              <auto-tooltip :content="model.model_name" style="flex: 1">
                <h4 class="model-name">{{ model.model_name }}</h4>
              </auto-tooltip>
              <!-- 导出状态标识 -->
              <div v-if="isModelExported(model)" class="export-badge">
                <el-icon><Check /></el-icon>
                已导出
              </div>
            </div>
            <div class="metrics-grid">
              <div class="metric-item">
                <span class="metric-label">BLEU-4</span>
                <span class="metric-value">{{
                  model.eval_obj[0].eval_result['predict_bleu-4']
                }}</span>
              </div>
              <div class="metric-item">
                <span class="metric-label">ROUGE-1</span>
                <span class="metric-value">{{
                  model.eval_obj[0].eval_result['predict_rouge-1']
                }}</span>
              </div>
              <div class="metric-item">
                <span class="metric-label">ROUGE-2</span>
                <span class="metric-value">{{
                  model.eval_obj[0].eval_result['predict_rouge-2']
                }}</span>
              </div>
              <div class="metric-item">
                <span class="metric-label">ROUGE-L</span>
                <span class="metric-value">{{
                  model.eval_obj[0].eval_result['predict_rouge-l']
                }}</span>
              </div>
            </div>
          </div>
        </div>
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button type="primary" @click="handleConfirm" :loading="loading"> 保存 </el-button>
        <el-button @click="handleCancel">关闭</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import evaluationApi from '@/api/train-evaluation'
import { useRouter } from 'vue-router'
import { SaveModel } from '@/api/train-common'
const router = useRouter()

const dialogVisible = ref(false)
const loading = ref(false)
const formRef = ref<FormInstance>()

const form = reactive({
  taskName: '',
  selectedCheckpoints: [] as string[],
  export_quantization_dataset: '' // 导出量化数据集
})

const selectedRows = ref<any[]>([])

const rules: FormRules = {
  taskName: [
    { required: true, message: '请输入记录名称', trigger: 'blur' },
    { min: 2, max: 50, message: '记录名称长度在 2 到 50 个字符', trigger: 'blur' }
  ]
}

const modelData = ref<any[]>([])
const contrastData = ref<any>(null) // 存储完整的对比数据-用于新增横向对比记录

// 检查模型是否已导出
const isModelExported = (model: any) => {
  return model.eval_obj?.[0]?.export_status === 1
}
// 检查模型是否可选
const canSelectModel = (model: any) => {
  return !isModelExported(model)
}
// 检查模型是否已选中
const isModelSelected = (model: any) => {
  return form.selectedCheckpoints.includes(model.id)
}
const handleCardSelect = (model: any) => {
  // 检查是否已导出
  if (isModelExported(model)) {
    ElMessage.warning('该模型已导出，无法重复保存')
    return
  }
  const modelId = model.id
  const index = form.selectedCheckpoints.indexOf(modelId)
  if (index > -1) {
    // 已选中，取消选择
    form.selectedCheckpoints.splice(index, 1)
    const rowIndex = selectedRows.value.findIndex((row) => row.id === modelId)
    if (rowIndex > -1) {
      selectedRows.value.splice(rowIndex, 1)
    }
  } else {
    // 未选中，添加选择
    form.selectedCheckpoints.push(modelId)
    selectedRows.value.push(model)
  }
  console.log(form, 'form')
}

const open = (data?: any) => {
  console.log(data, 'datas')
  if (data) {
    contrastData.value = data //完整数据
    modelData.value = data.modelData
  }

  // 重置表单
  form.taskName = ''
  form.selectedCheckpoints = []
  selectedRows.value = []
  formRef.value?.clearValidate()

  dialogVisible.value = true
}

const handleCancel = () => {
  dialogVisible.value = false
}

const handleConfirm = async () => {
  if (!formRef.value) return
  console.log(selectedRows.value, 'selectedRows.value', form.selectedCheckpoints)

  try {
    await formRef.value.validate()

    loading.value = true

    // 构建 新增横向对比记录 数据
    const addEvaRecordData = {
      name: form.taskName,
      eval_ids: modelData.value.map((item) => item.id),
      train_ids: modelData.value.map((item) => item.eval_obj?.[0]?.id).filter(Boolean),
      eval_contrast_data: contrastData.value
    }
    const res = await evaluationApi.AddEvalContrastInfo(addEvaRecordData)
    if (res.code !== 200) {
      ElMessage.error('保存横向对比记录失败')
      return
    }
    // 轮循调用导出方法
    selectedRows.value.map(async (model) => {
      console.log('%c [ model ]-193', 'font-size:13px; background:pink; color:#bf2c9f;', model)
      const saveModelData = {
        lang: 'zh',
        model_name: model.base_model,
        model_path: model.train_info?.model_path || '',
        finetuning_type: model.finetuning_type || '',
        checkpoint_path: [model.train_output_dir || ''],
        template: model.train_info?.template || '',
        export_size: 5,
        export_device: 'cpu',
        export_quantization_bit: model.train_info?.quantization_bit || '',
        export_quantization_dataset: form.export_quantization_dataset || 'data/c4_demo.jsonl',
        export_legacy_format: false,
        export_dir: `/root/autodl-tmp/workspace/export_models/${model.id}`,
        export_hub_model_id: '',
        extra_args: '{}'
      }
      console.log('SaveModel 参数:', saveModelData)
      // 异步调用 SaveModel
      SaveModel(saveModelData)
        .then((saveRes: any) => {
          console.log('SaveModel 结果:', saveRes)
        })
        .catch((error: any) => {
          console.error(`模型 ${model.model_name} SaveModel 失败:`, error)
        })

      // 构建 UpdateEvalInfo 参数,调用更新接口，同时更新本地数据
      const evalInfo = model.eval_obj?.[0]
      if (evalInfo) {
        const updateParams = {
          ...evalInfo,
          export_status: 1,// 将导出状态改为：已导出
          export_path: saveModelData.export_dir
        }
        console.log('UpdateEvalInfo 参数:', updateParams)

        // 调用 UpdateEvalInfo
        const updateRes = await evaluationApi.UpdateEvalInfo(evalInfo.id, updateParams)
        console.log('UpdateEvalInfo 结果:', updateRes)

        if (updateRes.code === 200) {
          // 更新本地数据状态
          model.eval_obj[0].export_status = 1 // 将导出状态改为：已导出
          model.eval_obj[0].export_path = saveModelData.export_dir
          console.log(`模型 ${model.model_name} 状态更新成功`)
        }
      }
    })
    ElMessage.success(`已提交 ${selectedRows.value.length} 个模型的保存任务`)

    dialogVisible.value = false
    router.push({
      path: '/model-control-desk/model-evaluation/lateralComparison',
      query: { contrast_id: res.data.id }
    })
  } catch (error) {
    console.error('保存横向对比记录失败:', error)
  } finally {
    loading.value = false
  }
}

defineExpose({
  open
})
</script>

<style scoped lang="scss">
.form-item {
  .model-cards-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 12px;
    max-height: 450px;
    overflow-y: auto;
    padding: 4px;
  }
}
:deep(.el-form-item__content) {
  display: block;
  line-height: 18px !important;
}
.model-card {
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  padding: 12px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  background: #fff;
  position: relative;
  overflow: hidden;

  &:hover {
    border-color: #409eff;
    box-shadow: 0 2px 8px rgba(64, 158, 255, 0.15);
    transform: translateY(-1px);
  }

  &.selected {
    border-color: #409eff;
    background: linear-gradient(135deg, #ecf5ff 0%, #f0f9ff 100%);
    box-shadow: 0 2px 12px rgba(64, 158, 255, 0.25);

    .model-name,
    .auto-tooltip .model-name {
      color: #409eff !important;
    }

    .metric-value {
      color: #409eff;
      font-weight: 500;
    }
  }
  &.exported {
    border-color: #67c23a;
    background: linear-gradient(135deg, #f0f9ff 0%, #f5f7fa 100%);
    opacity: 0.8;
  }

  &.disabled {
    cursor: not-allowed;
    opacity: 0.6;
  }

  .export-badge {
    background: #67c23a;
    color: white;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 10px;
    display: flex;
    align-items: center;
    gap: 2px;
  }
}

.card-header {
  display: flex;
  margin-bottom: 8px;

  .model-name {
    font-size: 14px;
    font-weight: 600;
    color: #303133;
    transition: color 0.2s ease;
    line-height: 1.3;
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}

.metrics-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4px;
}

.metric-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 4px 6px;
  background: #fafbfc;
  border-radius: 3px;
  min-width: 0; // 让整个容器也能缩小

  .metric-label {
    font-size: 11px;
    color: #afb2b8;
    font-weight: 400;
    white-space: nowrap;
    flex-shrink: 0;
  }

  .metric-value {
    font-size: 12px;
    font-weight: 500;
    color: #0a0a0c;
    transition: color 0.2s ease;
    white-space: nowrap;
    width: 100%;
    max-width: 100%; // 确保不超出父容器
    min-width: 0; // 允许缩小
    text-align: left;
    overflow: hidden;
    text-overflow: ellipsis;
    font-family: 'Courier New', monospace;
    flex: 1; // 占据剩余空间
  }
}

// 滚动条美化
.model-cards-container::-webkit-scrollbar {
  width: 6px;
}

.model-cards-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.model-cards-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;

  &:hover {
    background: #a8a8a8;
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
