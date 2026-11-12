<template>
  <div class="model-training">
    <div class="training-left">
      <div class="training-left-container">
        <h4 class="page-title">高级训练</h4>
        <div class="steps-wrap">
          <CustomSteps v-model="currentStep" :steps="steps" :disabled="isSwitchableSteps" />
        </div>
        <div class="btn-wrap">
          <div class="btn-group">
            <el-button
              v-if="[1, 2, 3].includes(currentStep)"
              class="action-btn prev-btn"
              @click="fnPrevStep"
            >
              上一步
            </el-button>
            <el-button
              v-if="[0, 1, 2].includes(currentStep)"
              class="action-btn next-btn primary-btn"
              @click="fnNextStep"
            >
              下一步
            </el-button>
            <el-button
              class="action-btn next-btn primary-btn"
              v-if="[3].includes(currentStep)"
              @click="fnStartTraining"
            >
              开始训练
            </el-button>
            <el-button
              class="action-btn interrupt-btn danger-btn"
              @click="handleInterrupt"
              v-if="[4].includes(currentStep) && trainingLoading"
            >
              中断
            </el-button>
            <el-button
              class="action-btn next-btn primary-btn"
              v-if="
                [4].includes(currentStep) && trainInstance.train_status == 3 && !trainingLoading
              "
              @click="fnContinueTraining"
            >
              继续训练
            </el-button>
          </div>
          <div class="btn-group">
            <template v-if="[0, 1, 2, 3].includes(currentStep)">
              <el-button class="action-btn" @click="openTrainLogModal"> 载入训练参数 </el-button>
            </template>
            <el-button class="action-btn prev-btn" @click="handleBack"> 返回 </el-button>
          </div>
        </div>
      </div>
    </div>
    <div class="training-right">
      <CmpBreadcrumb :items="breadcrumbItems" separatorIcon="ArrowRight" theme="light" />
      <transition :name="transitionAnimationName" mode="out-in">
        <!-- 基础配置 -->
        <div v-if="currentStep === 0" class="step-card" key="step-0">
          <div class="step-title">基础配置</div>
          <div class="step-content">
            <div id="step-basic" class="config-module">
              <div class="module-content">
                <el-form :model="formData" label-position="top">
                  <el-row :gutter="36">
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label required">模型名称</div>
                          <div class="form-des">本次训练模型的名称</div>
                        </template>
                        <el-input
                          v-model="formData.model_log_name"
                          style="width: 100%"
                          placeholder="请输入"
                        />
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">基座模型</div>
                          <div class="form-des">输入首单词以检索模型。</div>
                        </template>
                        <el-select
                          v-model="formData.model_path"
                          placeholder="请选择"
                          style="width: 100%"
                          filterable
                          @change="handleModelChange"
                        >
                          <el-option
                            v-for="item in constantsOptions.ModelPath"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                          />
                        </el-select>
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="16" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">模型路径</div>
                          <div class="form-des">本地模型的文件路径</div>
                        </template>
                        <el-select
                          v-model="formData.model_path"
                          placeholder="请选择"
                          style="width: 100%"
                        >
                          <!-- <el-option
                            v-for="item in constantsOptions.QuantizationBit"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                          /> -->
                        </el-select>
                        <!-- <el-input
                          v-model="formData.model_path"
                          style="width: 100%"
                          placeholder="请输入"
                        /> -->
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">
                            微调方法
                            <TooltipList :list="constantsDes.finetuning_type" />
                          </div>
                          <div class="form-des">训练的微调方法</div>
                        </template>
                        <el-select
                          v-model="formData.finetuning_type"
                          placeholder="请选择"
                          style="width: 100%"
                        >
                          <el-option
                            v-for="item in constantsOptions.MethodOption"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                          />
                        </el-select>
                      </el-form-item>
                    </el-col>
                    <!-- <el-col :sm="12" :md="16" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">检查点路径</div>
                          <div class="form-des">指定训练断点保存位置</div>
                        </template>
                        <el-select
                          v-model="formData.checkpoint_path"
                          placeholder="请选择"
                          style="width: 100%"
                        >
                          <el-option
                            v-for="item in options"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                          />
                        </el-select>
                      </el-form-item>
                    </el-col> -->
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">
                            量化等级
                            <TooltipList :list="constantsDes.quantization_bit" />
                          </div>
                          <div class="form-des">启用量化（QLoRA）</div>
                        </template>
                        <el-select
                          v-model="formData.quantization_bit"
                          placeholder="请选择"
                          style="width: 100%"
                        >
                          <el-option
                            v-for="item in constantsOptions.QuantizationBit"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                          />
                        </el-select>
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">
                            量化方法 <TooltipList :list="constantsDes.quantization_method" />
                          </div>
                          <div class="form-des">使用的量化算法。</div>
                        </template>
                        <el-select
                          v-model="formData.quantization_method"
                          placeholder="请选择"
                          style="width: 100%"
                        >
                          <el-option
                            v-for="item in constantsOptions.QuantizationMethod"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                          />
                        </el-select>
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">
                            对话模板
                            <TooltipList :list="constantsDes.template" />
                          </div>
                          <div class="form-des">构建提示词时使用的模板。</div>
                        </template>
                        <el-select
                          v-model="formData.template"
                          placeholder="请选择"
                          style="width: 100%"
                        >
                          <el-option
                            v-for="item in constantsOptions.TemplateOption"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                          />
                        </el-select>
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">
                            RoPE 插值方法 <TooltipList :list="constantsDes.rope_scaling" />
                          </div>
                          <div class="form-des">RoPE 插值时使用的方法。</div>
                        </template>
                        <el-select
                          v-model="formData.rope_scaling"
                          placeholder="请选择"
                          style="width: 100%"
                        >
                          <el-option
                            v-for="item in constantsOptions.RopeScaling"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                          />
                        </el-select>
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">
                            加速方式 <TooltipList :list="constantsDes.booster" />
                          </div>
                          <div class="form-des">使用的加速方法。</div>
                        </template>
                        <el-select
                          v-model="formData.booster"
                          placeholder="请选择"
                          style="width: 100%"
                        >
                          <el-option
                            v-for="item in constantsOptions.Booster"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                          />
                        </el-select>
                      </el-form-item>
                    </el-col>
                  </el-row>
                </el-form>
              </div>
            </div>
          </div>
        </div>

        <!-- 训练参数 -->
        <div v-else-if="currentStep === 1" class="step-card" key="step-1">
          <div class="step-title">训练配置</div>
          <div class="step-content">
            <!-- 原有训练参数表单内容 -->
            <div id="step-params" class="config-module">
              <div class="module-content">
                <el-form :model="formData" label-position="top">
                  <el-row :gutter="36">
                    <el-col :sm="12" :md="16" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">
                            训练阶段
                            <TooltipList :list="constantsDes.training_stage" />
                          </div>
                          <div class="form-des">目前采用的训练方式。</div>
                        </template>
                        <el-select
                          v-model="formData.training_stage"
                          placeholder="请选择"
                          style="width: 100%"
                          @change="fnGetDateSetOptions"
                        >
                          <el-option
                            v-for="item in constantsOptions.TrainingStage"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                          />
                        </el-select>
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">数据路径</div>
                          <div class="form-des">数据文件夹的路径。</div>
                        </template>
                        <el-input
                          v-model="formData.dataset_dir"
                          @change="fnGetDateSetOptions"
                          style="width: 100%"
                          placeholder="请输入"
                        />
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="24" :lg="12" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">数据集</div>
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
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">
                            学习率
                            <TooltipList :list="constantsDes.learning_rate" />
                          </div>
                          <div class="form-des">AdamW 优化器的初始学习率。</div>
                        </template>
                        <el-input
                          v-model="formData.learning_rate"
                          style="width: 100%"
                          placeholder="请输入"
                        />
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">
                            训练轮数
                            <TooltipList :list="constantsDes.num_train_epochs" />
                          </div>
                          <div class="form-des">需要执行的训练总轮数。</div>
                          <div class="input-draggable-progress">
                            <InputDraggableProgress
                              v-model="formData.num_train_epochs"
                              :min="1"
                              :defaultValue="100"
                              :max="10000"
                            />
                          </div>
                        </template>
                        <DraggableProgress
                          v-model="formData.num_train_epochs"
                          :min="1"
                          :max="10000"
                        />
                        <!-- <el-input
                          v-model="formData.num_train_epochs"
                          style="width: 100%"
                          placeholder="请输入"
                        /> -->
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">
                            最大梯度范数
                            <TooltipList :list="constantsDes.max_grad_norm" />
                          </div>
                          <div class="form-des">用于梯度裁剪的范数。</div>
                        </template>
                        <el-input
                          v-model="formData.max_grad_norm"
                          style="width: 100%"
                          placeholder="请输入"
                        />
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">
                            最大样本数
                            <TooltipList :list="constantsDes.max_samples" />
                          </div>
                          <div class="form-des">每个数据集的最大样本数。</div>
                        </template>
                        <el-input
                          v-model="formData.max_samples"
                          style="width: 100%"
                          placeholder="请输入"
                        />
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">
                            计算类型
                            <TooltipList :list="constantsDes.compute_type" />
                          </div>
                          <div class="form-des">是否使用混合精度训练。</div>
                        </template>
                        <el-select
                          v-model="formData.compute_type"
                          placeholder="请选择"
                          style="width: 100%"
                        >
                          <el-option
                            v-for="item in constantsOptions.ComputeType"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                          />
                        </el-select>
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">
                            截断长度
                            <TooltipList :list="constantsDes.cutoff_len" />
                          </div>
                          <div class="form-des">输入序列分词后的最大长度。</div>
                          <div class="input-draggable-progress">
                            <InputDraggableProgress
                              v-model="formData.cutoff_len"
                              :min="4"
                              :max="131072"
                              :defaultValue="2048"
                            />
                          </div>
                        </template>
                        <DraggableProgress v-model="formData.cutoff_len" :min="4" :max="131072" />
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">
                            批处理大小
                            <TooltipList :list="constantsDes.batch_size" />
                          </div>
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
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">
                            梯度累积
                            <TooltipList :list="constantsDes.gradient_accumulation_steps" />
                          </div>
                          <div class="form-des">梯度累积的步数。</div>
                          <div class="input-draggable-progress">
                            <InputDraggableProgress
                              v-model="formData.gradient_accumulation_steps"
                              :min="1"
                              :max="1024"
                              :defaultValue="8"
                            />
                          </div>
                        </template>
                        <DraggableProgress
                          v-model="formData.gradient_accumulation_steps"
                          :min="1"
                          :max="1024"
                        />
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">
                            验证集比例
                            <TooltipList :list="constantsDes.val_size" />
                          </div>
                          <div class="form-des">验证集占全部样本的百分比。</div>
                          <div class="input-draggable-progress">
                            <InputDraggableProgress
                              v-model="formData.val_size"
                              :step="0.001"
                              :min="0"
                              :max="1"
                              :defaultValue="0.001"
                            />
                          </div>
                        </template>
                        <DraggableProgress
                          v-model="formData.val_size"
                          :step="0.001"
                          :min="0"
                          :max="1"
                        />
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">
                            学习率调节器
                            <TooltipList :list="constantsDes.LrSchedulerType" />
                          </div>
                          <div class="form-des">学习率调度器的名称。</div>
                        </template>
                        <el-select
                          v-model="formData.lr_scheduler_type"
                          placeholder="请选择"
                          style="width: 100%"
                        >
                          <el-option
                            v-for="item in constantsOptions.LrSchedulerType"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                          />
                        </el-select>
                      </el-form-item>
                    </el-col>
                  </el-row>
                </el-form>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="currentStep === 2" class="step-card" key="step-2">
          <div class="step-title">额外配置</div>
          <div class="step-content">
            <div id="step-extra" class="config-module">
              <div class="module-content">
                <el-form :model="formData" label-position="top">
                  <el-row :gutter="36">
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">
                            日志间隔
                            <TooltipList :list="constantsDes.logging_steps" />
                          </div>
                          <div class="form-des">每两次日志输出间的更新步数。</div>
                          <div class="input-draggable-progress">
                            <InputDraggableProgress
                              v-model="formData.logging_steps"
                              :min="0"
                              :step="1"
                              :max="1000"
                              :defaultValue="5"
                            />
                          </div>
                        </template>
                        <DraggableProgress
                          v-model="formData.logging_steps"
                          :min="0"
                          :step="5"
                          :max="1000"
                        />
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">
                            保存间隔
                            <TooltipList :list="constantsDes.save_steps" />
                          </div>
                          <div class="form-des">每两次断点保存间的更新步数。</div>
                          <div class="input-draggable-progress">
                            <InputDraggableProgress
                              v-model="formData.save_steps"
                              :step="10"
                              :min="10"
                              :max="5000"
                              :defaultValue="100"
                            />
                          </div>
                        </template>
                        <DraggableProgress
                          v-model="formData.save_steps"
                          :step="10"
                          :min="10"
                          :max="5000"
                        />
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">
                            预热步数
                            <TooltipList :list="constantsDes.warmup_steps" />
                          </div>
                          <div class="form-des">学习率预热采用的步数。</div>
                          <div class="input-draggable-progress">
                            <InputDraggableProgress
                              v-model="formData.warmup_steps"
                              :min="0"
                              :max="5000"
                              :defaultValue="0"
                            />
                          </div>
                        </template>
                        <DraggableProgress v-model="formData.warmup_steps" :min="0" :max="5000" />
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">
                            NEFTune 噪声参数
                            <TooltipList :list="constantsDes.freeze_trainable_layers" />
                          </div>
                          <div class="form-des">嵌入向量所添加的噪声大小。</div>
                          <div class="input-draggable-progress">
                            <InputDraggableProgress
                              v-model="formData.freeze_trainable_layers"
                              :step="0.1"
                              :min="0"
                              :max="10"
                              :defaultValue="2"
                            />
                          </div>
                        </template>
                        <DraggableProgress
                          v-model="formData.neftune_alpha"
                          :step="0.1"
                          :min="0"
                          :max="10"
                        />
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">额外参数</div>
                          <div class="form-des">以 JSON 格式传递给训练器的额外参数。</div>
                        </template>
                        <el-input
                          v-model="formData.extra_args"
                          style="width: 100%"
                          placeholder="请输入"
                        />
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">
                            序列打包
                            <TooltipList :list="constantsDes.packing" />
                          </div>
                          <div class="form-des">将序列打包为等长样本。</div>
                        </template>
                        <el-switch v-model="formData.packing" />
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">
                            使用无污染打包
                            <TooltipList :list="constantsDes.neat_packing" />
                          </div>
                          <div class="form-des">避免打包后的序列产生交叉注意力。</div>
                        </template>
                        <el-switch v-model="formData.neat_packing" />
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">学习提示词</div>
                          <div class="form-des">不在提示词的部分添加掩码（仅适用于 SFT）</div>
                        </template>
                        <el-switch v-model="formData.train_on_prompt" />
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">不学习历史对话</div>
                          <div class="form-des">仅学习最后一轮对话（仅适用于 SFT）。</div>
                        </template>
                        <el-switch v-model="formData.mask_history" />
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">更改词表大小</div>
                          <div class="form-des">更改分词器词表和嵌入层的大小。</div>
                        </template>
                        <el-switch v-model="formData.resize_vocab" />
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">使用 LLaMA Pro</div>
                          <div class="form-des">仅训练块扩展后的参数。</div>
                        </template>
                        <el-switch v-model="formData.use_llama_pro" />
                      </el-form-item>
                    </el-col>

                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">启用思考模式</div>
                          <div class="form-des">是否启用推理模型的思考模式。</div>
                        </template>
                        <el-switch v-model="formData.enable_thinking" />
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">启用外部记录面板</div>
                          <div class="form-des">使用 TensorBoard 或 wandb 记录实验。</div>
                        </template>
                        <el-select
                          v-model="formData.report_to"
                          placeholder="请选择"
                          style="width: 100%"
                        >
                          <el-option
                            v-for="item in constantsOptions.ReportTo"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                          />
                        </el-select>
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">可训练层数</div>
                          <div class="form-des">最末尾（+）/最前端（-）可训练隐藏层的数量。</div>
                          <div class="input-draggable-progress">
                            <InputDraggableProgress
                              v-model="formData.freeze_trainable_layers"
                              :min="-128"
                              :max="128"
                              :defaultValue="2"
                            />
                          </div>
                        </template>
                        <DraggableProgress
                          v-model="formData.freeze_trainable_layers"
                          :min="-128"
                          :max="128"
                        />
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="12" :lg="12" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">可训练模块</div>
                          <div class="form-des">可训练模块的名称。使用英文逗号分隔多个名称。</div>
                        </template>
                        <el-input
                          v-model="formData.freeze_trainable_modules"
                          style="width: 100%"
                          placeholder="请输入"
                        />
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="12" :lg="12" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">额外模块（非必填）</div>
                          <div class="form-des">
                            除隐藏层以外的可训练模块名称。使用英文逗号分隔多个名称。
                          </div>
                        </template>
                        <el-input
                          v-model="formData.freeze_extra_modules"
                          style="width: 100%"
                          placeholder="请输入"
                        />
                      </el-form-item>
                    </el-col>
                  </el-row>
                  <div class="sub-config-container">
                    <div class="sub-config-title">LoRA 参数设置</div>
                    <div>
                      <el-row :gutter="36">
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">
                                LoRA 秩
                                <TooltipList :list="constantsDes.lora_rank" />
                              </div>
                              <div class="form-des">LoRA 矩阵的秩大小。</div>
                              <div class="input-draggable-progress">
                                <InputDraggableProgress
                                  v-model="formData.lora_rank"
                                  :min="1"
                                  :max="1024"
                                  :defaultValue="8"
                                />
                              </div>
                            </template>
                            <DraggableProgress v-model="formData.lora_rank" :min="1" :max="1024" />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">
                                LoRA 缩放系数
                                <TooltipList :list="constantsDes.lora_alpha" />
                              </div>
                              <div class="form-des">LoRA 缩放系数大小。</div>
                              <div class="input-draggable-progress">
                                <InputDraggableProgress
                                  v-model="formData.lora_alpha"
                                  :min="1"
                                  :max="2048"
                                  :defaultValue="16"
                                />
                              </div>
                            </template>
                            <DraggableProgress v-model="formData.lora_alpha" :min="1" :max="2048" />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">
                                LoRA 随机丢弃
                                <TooltipList :list="constantsDes.lora_dropout" />
                              </div>
                              <div class="form-des">LoRA 权重随机丢弃的概率。</div>
                              <div class="input-draggable-progress">
                                <InputDraggableProgress
                                  v-model="formData.lora_dropout"
                                  :step="0.01"
                                  :min="0"
                                  :max="1"
                                  :defaultValue="0"
                                />
                              </div>
                            </template>
                            <DraggableProgress
                              v-model="formData.lora_dropout"
                              :step="0.01"
                              :min="0"
                              :max="1"
                            />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">
                                LoRA+ 学习率比例
                                <TooltipList :list="constantsDes.loraplus_lr_ratio" />
                              </div>
                              <div class="form-des">LoRA+ 中 B 矩阵的学习率倍数。</div>
                              <div class="input-draggable-progress">
                                <InputDraggableProgress
                                  v-model="formData.loraplus_lr_ratio"
                                  :step="0.01"
                                  :min="0"
                                  :max="64"
                                  :defaultValue="0"
                                />
                              </div>
                            </template>
                            <DraggableProgress
                              v-model="formData.loraplus_lr_ratio"
                              :step="0.01"
                              :min="0"
                              :max="64"
                            />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">新建适配器</div>
                              <div class="form-des">
                                在现有的适配器上创建一个随机初始化后的新适配器。
                              </div>
                            </template>
                            <el-switch v-model="formData.create_new_adapter" />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">使用 rslora</div>
                              <div class="form-des">对 LoRA 层使用秩稳定缩放方法。</div>
                            </template>
                            <el-switch v-model="formData.use_rslora" />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">使用 DoRA</div>
                              <div class="form-des">使用权重分解的 LoRA。</div>
                            </template>
                            <el-switch v-model="formData.use_dora" />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">使用 PiSSA</div>
                              <div class="form-des">使用 PiSSA 方法。</div>
                            </template>
                            <el-switch v-model="formData.use_pissa" />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="12" :lg="12" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">LoRA 作用模块（非必填）</div>
                              <div class="form-des">
                                应用 LoRA 的模块名称。使用英文逗号分隔多个名称。
                              </div>
                            </template>
                            <el-input
                              v-model="formData.lora_target"
                              style="width: 100%"
                              placeholder="请输入"
                            />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="12" :lg="12" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">LoRA 附加模块（非必填）</div>
                              <div class="form-des">
                                除 LoRA 层以外的可训练模块名称。使用英文逗号分隔多个名称。
                              </div>
                            </template>
                            <el-input
                              v-model="formData.additional_target"
                              style="width: 100%"
                              placeholder="请输入"
                            />
                          </el-form-item>
                        </el-col>
                      </el-row>
                    </div>
                  </div>
                  <div class="sub-config-container">
                    <div class="sub-config-title">RLHF 参数设置</div>
                    <div>
                      <el-row :gutter="36">
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">Beta 参数</div>
                              <div class="form-des">损失函数中 beta 超参数大小。</div>
                              <div class="input-draggable-progress">
                                <InputDraggableProgress
                                  v-model="formData.pref_beta"
                                  :step="0.01"
                                  :min="0"
                                  :max="1"
                                  :defaultValue="0.1"
                                />
                              </div>
                            </template>
                            <DraggableProgress
                              v-model="formData.pref_beta"
                              :step="0.01"
                              :min="0"
                              :max="1"
                            />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">Ftx gamma</div>
                              <div class="form-des">损失函数中 SFT 损失的权重大小。</div>
                              <div class="input-draggable-progress">
                                <InputDraggableProgress
                                  v-model="formData.pref_ftx"
                                  :step="0.01"
                                  :min="0"
                                  :max="10"
                                  :defaultValue="0"
                                />
                              </div>
                            </template>
                            <DraggableProgress
                              v-model="formData.pref_ftx"
                              :step="0.01"
                              :min="0"
                              :max="10"
                            />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">损失类型</div>
                              <div class="form-des">损失函数的类型。</div>
                            </template>
                            <el-select
                              v-model="formData.pref_loss"
                              placeholder="请选择"
                              style="width: 100%"
                            >
                              <el-option
                                v-for="item in constantsOptions.Sigmoid"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                              />
                            </el-select>
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">奖励模型</div>
                              <div class="form-des">PPO 训练中奖励模型的适配器路径</div>
                            </template>
                            <el-select
                              v-model="formData.reward_model"
                              placeholder="请选择"
                              style="width: 100%"
                            >
                            </el-select>
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">归一化分数</div>
                              <div class="form-des">PPO 训练中归一化奖励分数。</div>
                            </template>
                            <el-switch v-model="formData.ppo_score_norm" />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">白化奖励</div>
                              <div class="form-des">PPO 训练中将奖励分数做白化处理。</div>
                            </template>
                            <el-switch v-model="formData.ppo_whiten_rewards" />
                          </el-form-item>
                        </el-col>
                      </el-row>
                    </div>
                  </div>
                  <div class="sub-config-container">
                    <div class="sub-config-title">多模态参数设置</div>
                    <div>
                      <el-row :gutter="36">
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">图像最大像素</div>
                              <div class="form-des">输入图像的最大像素数。</div>
                            </template>
                            <el-input
                              v-model="formData.image_max_pixels"
                              style="width: 100%"
                              placeholder="请输入"
                            />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">图像最小像素</div>
                              <div class="form-des">输入图像的最小像素数。</div>
                            </template>
                            <el-input
                              v-model="formData.image_min_pixels"
                              style="width: 100%"
                              placeholder="请输入"
                            />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">视频最大像素</div>
                              <div class="form-des">输入视频的最大像素数。</div>
                            </template>
                            <el-input
                              v-model="formData.video_max_pixels"
                              style="width: 100%"
                              placeholder="请输入"
                            />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">视频最小像素</div>
                              <div class="form-des">输入视频的最小像素数。</div>
                            </template>
                            <el-input
                              v-model="formData.video_min_pixels"
                              style="width: 100%"
                              placeholder="请输入"
                            />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">冻结视觉编码器</div>
                              <div class="form-des">冻结模型中的视觉编码器。</div>
                            </template>
                            <el-switch v-model="formData.freeze_vision_tower" />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">冻结多模态投影器</div>
                              <div class="form-des">冻结模型中的多模态投影器。</div>
                            </template>
                            <el-switch v-model="formData.freeze_multi_modal_projector" />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">冻结语言模型</div>
                              <div class="form-des">冻结模型中的语言模型。</div>
                            </template>
                            <el-switch v-model="formData.freeze_language_model" />
                          </el-form-item>
                        </el-col>
                      </el-row>
                    </div>
                  </div>
                  <div class="sub-config-container">
                    <div class="sub-config-title">
                      GaLore 参数设置
                      <el-switch v-model="formData.use_galore" />
                    </div>
                    <div v-show="formData.use_galore">
                      <el-row :gutter="36">
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">GaLore 秩</div>
                              <div class="form-des">GaLore 梯度的秩大小。</div>
                              <div class="input-draggable-progress">
                                <InputDraggableProgress
                                  v-model="formData.galore_rank"
                                  :min="1"
                                  :max="1024"
                                  :defaultValue="16"
                                />
                              </div>
                            </template>
                            <DraggableProgress
                              v-model="formData.galore_rank"
                              :min="1"
                              :max="1024"
                            />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">更新间隔</div>
                              <div class="form-des">相邻两次投影更新的步数。</div>
                              <div class="input-draggable-progress">
                                <InputDraggableProgress
                                  v-model="formData.galore_update_interval"
                                  :min="1"
                                  :max="2048"
                                  :defaultValue="200"
                                />
                              </div>
                            </template>
                            <DraggableProgress
                              v-model="formData.galore_update_interval"
                              :min="1"
                              :max="2048"
                            />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">GaLore 缩放系数</div>
                              <div class="form-des">GaLore 缩放系数大小。</div>
                              <div class="input-draggable-progress">
                                <InputDraggableProgress
                                  v-model="formData.galore_scale"
                                  :step="0.1"
                                  :min="0"
                                  :max="100"
                                  :defaultValue="2"
                                />
                              </div>
                            </template>
                            <DraggableProgress
                              v-model="formData.galore_scale"
                              :step="0.1"
                              :min="0"
                              :max="100"
                            />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">GaLore 作用模块</div>
                              <div class="form-des">
                                应用 GaLore 的模块名称。使用英文逗号分隔多个名称。
                              </div>
                            </template>
                            <el-input
                              v-model="formData.galore_target"
                              style="width: 100%"
                              placeholder="请输入"
                            />
                          </el-form-item>
                        </el-col>
                      </el-row>
                    </div>
                  </div>
                  <div class="sub-config-container">
                    <div class="sub-config-title">
                      APOLLO 参数设置
                      <el-switch v-model="formData.use_apollo" />
                    </div>
                    <div v-show="formData.use_apollo">
                      <el-row :gutter="36">
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">APOLLO 秩</div>
                              <div class="form-des">APOLLO 梯度的秩大小。</div>
                              <div class="input-draggable-progress">
                                <InputDraggableProgress
                                  v-model="formData.apollo_rank"
                                  :min="1"
                                  :max="1024"
                                  :defaultValue="16"
                                />
                              </div>
                            </template>
                            <DraggableProgress
                              v-model="formData.apollo_rank"
                              :min="1"
                              :max="1024"
                            />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">更新间隔</div>
                              <div class="form-des">相邻两次投影更新的步数。</div>
                              <div class="input-draggable-progress">
                                <InputDraggableProgress
                                  v-model="formData.apollo_update_interval"
                                  :min="1"
                                  :max="2048"
                                  :defaultValue="200"
                                />
                              </div>
                            </template>
                            <DraggableProgress
                              v-model="formData.apollo_update_interval"
                              :min="1"
                              :max="2048"
                            />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">APOLLO 缩放系数</div>
                              <div class="form-des">APOLLO 缩放系数大小。</div>
                              <div class="input-draggable-progress">
                                <InputDraggableProgress
                                  v-model="formData.apollo_scale"
                                  :step="0.1"
                                  :min="0"
                                  :max="100"
                                  :defaultValue="32"
                                />
                              </div>
                            </template>
                            <DraggableProgress
                              v-model="formData.apollo_scale"
                              :step="0.1"
                              :min="0"
                              :max="100"
                            />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">APOLLO 作用模块</div>
                              <div class="form-des">
                                应用 APOLLO 的模块名称。使用英文逗号分隔多个名称。
                              </div>
                            </template>
                            <el-input
                              v-model="formData.apollo_target"
                              style="width: 100%"
                              placeholder="请输入"
                            />
                          </el-form-item>
                        </el-col>
                      </el-row>
                    </div>
                  </div>
                  <div class="sub-config-container">
                    <div class="sub-config-title">
                      BAdam 参数设置
                      <el-switch v-model="formData.use_badam" />
                    </div>
                    <div v-show="formData.use_badam">
                      <el-row :gutter="36">
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">BAdam 模式</div>
                              <div class="form-des">
                                使用 layer-wise 或 ratio-wise BAdam 优化器。
                              </div>
                            </template>
                            <el-select
                              v-model="formData.badam_mode"
                              placeholder="请选择"
                              style="width: 100%"
                            >
                              <el-option
                                v-for="item in constantsOptions.BadamMode"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                              />
                            </el-select>
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">切换策略</div>
                              <div class="form-des">Layer-wise BAdam 优化器的块切换策略。</div>
                            </template>
                            <el-select
                              v-model="formData.badam_switch_mode"
                              placeholder="请选择"
                              style="width: 100%"
                            >
                              <el-option
                                v-for="item in constantsOptions.BadamWwitchMode"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                              />
                            </el-select>
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">切换频率</div>
                              <div class="form-des">Layer-wise BAdam 优化器的块切换频率。</div>
                              <div class="input-draggable-progress">
                                <InputDraggableProgress
                                  v-model="formData.badam_switch_interval"
                                  :min="1"
                                  :max="1024"
                                  :defaultValue="50"
                                />
                              </div>
                            </template>
                            <DraggableProgress
                              v-model="formData.badam_switch_interval"
                              :min="1"
                              :max="1024"
                            />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="8" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">Block 更新比例</div>
                              <div class="form-des">Ratio-wise BAdam 优化器的更新比例。</div>
                              <div class="input-draggable-progress">
                                <InputDraggableProgress
                                  v-model="formData.badam_update_ratio"
                                  :step="0.01"
                                  :min="0"
                                  :max="1"
                                  :defaultValue="0.05"
                                />
                              </div>
                            </template>
                            <DraggableProgress
                              v-model="formData.badam_update_ratio"
                              :step="0.01"
                              :min="0"
                              :max="1"
                            />
                          </el-form-item>
                        </el-col>
                      </el-row>
                    </div>
                  </div>
                  <!-- <div class="sub-config-container">
                    <div class="sub-config-title">
                      SwanLab 参数设置
                      <el-switch v-model="formData.use_swanlab" />
                    </div>
                    <div>
                      <el-row :gutter="36">
                        <el-col :sm="12" :md="16" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">项目名</div>
                              <div class="form-des">SwanLab的项目名</div>
                            </template>
                            <el-input
                              v-model="formData.swanlab_project"
                              style="width: 100%"
                              placeholder="请输入"
                            />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="16" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">实验名（非必填）</div>
                              <div class="form-des">SwanLab的实验名</div>
                            </template>
                            <el-input
                              v-model="formData.swanlab_run_name"
                              style="width: 100%"
                              placeholder="请输入"
                            />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="16" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">SwanLab 工作区（非必填）</div>
                              <div class="form-des">SwanLab 的工作区，默认在个人工作区下。</div>
                            </template>
                            <el-input
                              v-model="formData.swanlab_workspace"
                              style="width: 100%"
                              placeholder="请输入"
                            />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="16" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">SwanLab API 密钥（非必填）</div>
                              <div class="form-des">
                                用于在编程环境登录 SwanLab，已登录则无需填写。
                              </div>
                            </template>
                            <el-input
                              v-model="formData.swanlab_api_key"
                              style="width: 100%"
                              placeholder="请输入"
                            />
                          </el-form-item>
                        </el-col>
                        <el-col :sm="12" :md="16" :lg="6" :xl="6">
                          <el-form-item>
                            <template #label>
                              <div class="form-label">SwanLab 模式</div>
                              <div class="form-des">使用云端版或离线版 SwanLab。</div>
                            </template>
                            <el-select
                              v-model="formData.swanlab_mode"
                              placeholder="请选择"
                              style="width: 100%"
                            >
                              <el-option
                                v-for="item in constantsOptions.SwanlabMode"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                              />
                            </el-select>
                          </el-form-item>
                        </el-col>
                      </el-row>
                    </div>
                  </div> -->
                </el-form>
              </div>
            </div>
          </div>
        </div>

        <!-- 输出配置 -->
        <div v-else-if="currentStep === 3" class="step-card" key="step-3">
          <div class="step-title">输出配置</div>
          <div class="step-content">
            <!-- 原有输出配置表单内容 -->
            <div id="step-output" class="config-module">
              <div class="module-content">
                <el-form :model="formData" label-position="top">
                  <el-row :gutter="36">
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">输出目录</div>
                          <div class="form-des">保存结果的路径。</div>
                        </template>
                        <el-select
                          v-model="formData.output_dir"
                          placeholder="请选择"
                          style="width: 100%"
                        >
                          <el-option
                            v-for="item in outputDirOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                          />
                        </el-select>
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">配置路径</div>
                          <div class="form-des">保存训练参数的配置文件路径。</div>
                        </template>
                        <el-select
                          v-model="formData.config_path"
                          placeholder="请选择"
                          style="width: 100%"
                        >
                          <el-option
                            v-for="item in configPathOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                          />
                        </el-select>
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">设备数量</div>
                          <div class="form-des">当前可用的运算设备数</div>
                        </template>
                        <el-input
                          v-model="formData.device_count"
                          style="width: 100%"
                          placeholder="请输入"
                        />
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">DeepSpeed stage</div>
                          <div class="form-des">多卡训练的 DeepSpeed stage。</div>
                        </template>
                        <el-select
                          v-model="formData.ds_stage"
                          placeholder="请选择"
                          style="width: 100%"
                        >
                          <el-option
                            v-for="item in constantsOptions.DsStage"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                          />
                        </el-select>
                      </el-form-item>
                    </el-col>
                    <el-col :sm="12" :md="8" :lg="6" :xl="6">
                      <el-form-item>
                        <template #label>
                          <div class="form-label">使用offload</div>
                          <div class="form-des">使用 DeepSpeed offload（会减慢速度）。</div>
                        </template>
                        <el-switch v-model="formData.ds_offload" />
                      </el-form-item>
                    </el-col>
                  </el-row>
                </el-form>
              </div>
            </div>
          </div>
        </div>
        <!-- 模型训练 -->
        <div v-else-if="currentStep === 4" class="step-card train-result" key="step-4">
          <!-- <div class="step-title">模型训练</div> -->
          <div class="step-content">
            <div class="train-progress-wrap">
              <div
                style="
                  font-size: 16px;
                  font-weight: bold;
                  color: #333;
                  text-align: center;
                  margin-bottom: 12px;
                "
              >
                当前训练进度{{ trainProgress }}%
              </div>
              <el-progress
                :text-inside="true"
                striped
                :stroke-width="16"
                :percentage="trainProgress"
              />
            </div>
            <div class="step-loss">
              <div
                style="
                  font-size: 16px;
                  font-weight: bold;
                  color: #333;
                  text-align: center;
                  margin: 12px 0;
                "
              >
                模型训练损失图
              </div>
              <div class="step-chart" id="refChartDom"></div>
            </div>
            <div class="step-log-wrap">
              <div>
                <div
                  style="
                    font-size: 16px;
                    font-weight: bold;
                    color: #333;
                    text-align: center;
                    margin: 12px 0;
                  "
                >
                  训练日志
                </div>
                <div class="log-content" ref="refLogContentDom">
                  <MdPreview
                    noIconfont
                    ref="editorRef"
                    editorId="preview-only"
                    :modelValue="trainLogMd"
                    class="maxkb-md"
                    :codeFoldable="false"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>
    <TrainLogModal
      ref="refTrainLogModal"
      :isCheckable="true"
      @loadParams="handleLoadParams"
      :category="1"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import DraggableProgress from '@/components/draggable-progress/index.vue'
import InputDraggableProgress from '@/components/input-draggable-progress/index.vue'
import constantsOptions from '@/views/model-control-desk/utils/constantsOptions'
import constantsDes from '@/views/model-control-desk/utils/constantsDes'
import CustomSteps from '@/components/custom-steps/index.vue'
import TrainLogModal from './modules/trainLogModal.vue'
import TooltipList from '@/components/TooltipList/index.vue'
import MdPreview from '@/components/markdown/MdPreviewBlack.vue'
import trainingMixin from './modules/trainingCommon.ts'
import CmpBreadcrumb from '@/views/gateway-page/modules/CmpBreadcrumb.vue'

const steps = [
  { title: '基础配置' },
  { title: '训练配置' },
  { title: '额外配置' },
  { title: '输出配置' },
  { title: '模型训练' }
]

const refTrainLogModal = ref(null)
const refLogContentDom = ref(null)
const breadcrumbItems = computed(() => {
  let list = [
    { title: '模型训练', path: '/model-control-desk/model-training' },
    { title: '高级训练', path: '' },
    { title: '', path: '' }
  ]
  if (trainInstance.value.id) {
    list[list.length - 1].title = trainInstance.value.model_name
  } else {
    list[list.length - 1].title = '新建高级训练'
  }
  return list
})

// 使用混入
const {
  currentStep,
  datasetOptions,
  outputDirOptions,
  configPathOptions,
  transitionAnimationName,
  fnNextStep,
  fnPrevStep,
  handleModelChange,
  fnGetDateSetOptions,
  fnStartTraining,
  openTrainLogModal,
  formData,
  trainLogMd,
  trainingLoading,
  trainProgress,
  handleInterrupt,
  handleBack,
  isSwitchableSteps,
  handleLoadParams,
  trainInstance,
  fnContinueTraining
} = trainingMixin.setup({ steps: steps, refLogContentDom, refTrainLogModal, train_category: 1 })
</script>

<style lang="scss" scoped>
@import './modules//commoncss.scss';
::v-deep {
  .el-col-24,
  .el-col-24.is-guttered {
    margin-bottom: 24px;
  }
}
</style>
<style lang="scss">
.model-training {
  .el-form-item__label {
    margin-bottom: 4px !important;
    position: relative !important;
    width: 100% !important;
  }
}
</style>
