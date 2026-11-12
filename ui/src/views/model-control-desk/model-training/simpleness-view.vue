<template>
  <div class="model-training">
    <div class="training-left">
      <div class="training-left-container">
        <h4 class="page-title">快速训练</h4>
        <div class="steps-wrap">
          <CustomSteps v-model="currentStep" :steps="steps" :disabled="isSwitchableSteps" />
        </div>
        <div class="btn-wrap">
          <div class="btn-group">
            <el-button
              v-if="[1, 2].includes(currentStep)"
              class="action-btn prev-btn"
              @click="fnPrevStep"
            >
              上一步
            </el-button>
            <el-button
              v-if="[0, 1].includes(currentStep)"
              class="action-btn next-btn primary-btn"
              @click="fnNextStep"
            >
              下一步
            </el-button>
            <el-button
              class="action-btn next-btn primary-btn"
              v-if="[2].includes(currentStep)"
              @click="fnStartTraining"
            >
              开始训练
            </el-button>

            <el-button
              class="action-btn interrupt-btn danger-btn"
              @click="handleInterrupt"
              v-if="[3].includes(currentStep) && trainingLoading"
            >
              中断
            </el-button>
            <el-button
              class="action-btn next-btn primary-btn"
              v-if="
                [3].includes(currentStep) && trainInstance.train_status == 3 && !trainingLoading
              "
              @click="fnContinueTraining"
            >
              继续训练
            </el-button>
          </div>
          <div class="btn-group">
            <template v-if="[0, 1, 2].includes(currentStep)">
              <el-button class="action-btn" @click="openTrainLogModal"> 载入训练参数 </el-button>
            </template>
            <el-button class="action-btn prev-btn" @click="handleBack"> 返回 </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧内容 -->
    <div class="training-right">
      <CmpBreadcrumb :items="breadcrumbItems" separatorIcon="ArrowRight" theme="light" />

      <transition :name="transitionName" mode="out-in">
        <!-- 基础配置 -->
        <div v-if="currentStep === 0" class="step-card" key="step-0">
          <div class="step-title">基础配置</div>
          <div class="step-content">
            <div id="step-basic" class="config-module">
              <div class="module-content">
                <el-form :model="formData" hide-required-asterisk label-position="top">
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
                    <!-- <el-col :sm="12" :md="16" :lg="6" :xl="6">
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
                          <el-option
                            v-for="item in constantsOptions.ModelPath"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                          />
                        </el-select>
                        <el-input
                          v-model="formData.model_path"
                          style="width: 100%"
                          placeholder="请输入"
                        />
                      </el-form-item>
                    </el-col> -->
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
                            量化方法
                            <TooltipList :list="constantsDes.quantization_method" />
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
                            RoPE 插值方法
                            <TooltipList :list="constantsDes.rope_scaling" />
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
                            加速方式
                            <TooltipList :list="constantsDes.booster" />
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
                <el-form :model="formData" hide-required-asterisk label-position="top">
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
                      <el-form-item required>
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
                            <TooltipList :list="constantsDes.training_stage" />
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
                          <div class="input-draggable-progress">
                            <InputDraggableProgress
                              v-model="formData.gradient_accumulation_steps"
                              :min="1"
                              :max="1024"
                              :defaultValue="8"
                            />
                          </div>

                          <div class="form-des">梯度累积的步数。</div>
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
                          <div class="input-draggable-progress">
                            <InputDraggableProgress
                              v-model="formData.val_size"
                              :step="0.001"
                              :min="0"
                              :max="1"
                            />
                          </div>
                          <div class="form-des">验证集占全部样本的百分比。</div>
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
                            <TooltipList :list="constantsDes.lr_scheduler_type" />
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

        <!-- 输出配置 -->
        <div v-else-if="currentStep === 2" class="step-card" key="step-3">
          <div class="step-title">输出配置</div>
          <div class="step-content">
            <!-- 原有输出配置表单内容 -->
            <div id="step-output" class="config-module">
              <div class="module-content">
                <el-form :model="formData" hide-required-asterisk label-position="top">
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
                          readonly
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
        <div v-else-if="currentStep === 3" class="step-card train-result" key="step-4">
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
      :category="0"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import DraggableProgress from '@/components/draggable-progress/index.vue'
import InputDraggableProgress from '@/components/input-draggable-progress/index.vue'
import constantsOptions from '@/views/model-control-desk/utils/constantsOptions'
import constantsDes from '@/views/model-control-desk/utils/constantsDes'
import CustomSteps from '@/components/custom-steps/index.vue'
import TooltipList from '@/components/TooltipList/index.vue' // 添加这行
import 'md-editor-v3/lib/style.css'
import MdPreview from '@/components/markdown/MdPreviewBlack.vue'
// 导入混入
import trainingMixin from './modules/trainingCommon.ts'
import TrainLogModal from './modules/trainLogModal.vue'
import CmpBreadcrumb from '@/views/gateway-page/modules/CmpBreadcrumb.vue'

const steps = [
  { title: '基础配置' },
  { title: '训练配置' },
  { title: '输出配置' },
  { title: '模型训练' }
]
const refLogContentDom = ref(null)
const refTrainLogModal = ref(null)
const breadcrumbItems = computed(() => {
  let list = [
    { title: '模型训练', path: '/model-control-desk/model-training' },
    { title: '快速训练', path: '' },
    { title: '', path: '' }
  ]
  if (trainInstance.value.id) {
    list[list.length - 1].title = trainInstance.value.model_name
  } else {
    list[list.length - 1].title = '新建快速训练'
  }
  return list
})
// 使用混入
const {
  currentStep,
  datasetOptions,
  outputDirOptions,
  configPathOptions,
  transitionName,
  fnNextStep,
  fnPrevStep,
  handleModelChange,
  fnGetDateSetOptions,
  fnStartTraining,
  fnContinueTraining,
  formData,
  trainLogMd,
  trainingLoading,
  trainProgress,
  handleInterrupt,
  handleBack,
  openTrainLogModal,
  isSwitchableSteps,
  handleLoadParams,
  trainInstance
} = trainingMixin.setup({ steps: steps, refLogContentDom, refTrainLogModal, train_category: 0 })
// 0akudg1tdl3j
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
