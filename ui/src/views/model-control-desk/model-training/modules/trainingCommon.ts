import { ref, computed, watch, nextTick, onUnmounted, onMounted, watchEffect } from 'vue'
import { ElMessage, ElLoading } from 'element-plus'
import constantsOptions from '../../utils/constantsOptions'
import * as echarts from 'echarts';
import { AddTrainLog, UpdateTrainLog, GetTrainLogDetail, } from '@/api/train-training'
import { useRouter, useRoute } from 'vue-router'
import {
  RunTrain,
  GetDatasets,
  FnBreakOff,
  FnMonitor,
  GetProcesses,
  FnCheckOutput,
  GetCheckpoints
} from '@/api/train-common'
import { FieldMapping } from './config'
import { update } from 'lodash';

export default {
  setup(props: any) {
    interface OptionsType {
      value: string;              // 配置文件路径
      label: string;              // 显示名称
      [key: string]: any;         // 其他扩展属性
    }
    interface AnyType {
      [key: string]: any;         // 其他扩展属性
    }
    interface TrainingFormData {
      model_log_name: string,
      lang: string;
      model_name: string;
      model_path: string;
      finetuning_type: string;
      checkpoint_path: string[];
      quantization_bit: string;
      quantization_method: string;
      template: string;
      rope_scaling: string;
      booster: string;
      training_stage: string;
      dataset_dir: string;
      dataset: any[];
      learning_rate: string;
      num_train_epochs: number;
      max_grad_norm: string;
      max_samples: string;
      compute_type: string;
      cutoff_len: number;
      batch_size: number;
      gradient_accumulation_steps: number;
      val_size: number;
      lr_scheduler_type: string;
      logging_steps: number;
      save_steps: number;
      warmup_steps: number;
      neftune_alpha: number;
      extra_args: string;
      packing: boolean;
      neat_packing: boolean;
      train_on_prompt: boolean;
      mask_history: boolean;
      resize_vocab: boolean;
      use_llama_pro: boolean;
      enable_thinking: boolean;
      report_to: string;
      freeze_trainable_layers: number;
      freeze_trainable_modules: string;
      freeze_extra_modules: string;
      lora_rank: number;
      lora_alpha: number;
      lora_dropout: number;
      loraplus_lr_ratio: number;
      create_new_adapter: boolean;
      use_rslora: boolean;
      use_dora: boolean;
      use_pissa: boolean;
      lora_target: string;
      additional_target: string;
      pref_beta: number;
      pref_ftx: number;
      pref_loss: string;
      reward_model: any[];
      ppo_score_norm: boolean;
      ppo_whiten_rewards: boolean;
      freeze_vision_tower: boolean;
      freeze_multi_modal_projector: boolean;
      freeze_language_model: boolean;
      image_max_pixels: string;
      image_min_pixels: string;
      video_max_pixels: string;
      video_min_pixels: string;
      use_galore: boolean;
      galore_rank: number;
      galore_update_interval: number;
      galore_scale: number;
      galore_target: string;
      use_apollo: boolean;
      apollo_rank: number;
      apollo_update_interval: number;
      apollo_scale: number;
      apollo_target: string;
      use_badam: boolean;
      badam_mode: string;
      badam_switch_mode: string;
      badam_switch_interval: number;
      badam_update_ratio: number;
      use_swanlab: boolean;
      swanlab_project: string;
      swanlab_run_name: string;
      swanlab_workspace: string;
      swanlab_api_key: string;
      swanlab_mode: string;
      output_dir: string;
      config_path: string;
      device_count: number;
      ds_stage: string;
      ds_offload: boolean;
    }
    // 基础变量
    const router = useRouter()
    const route = useRoute()
    const alpha = ref(0.2)
    // 服务器训练cli列表
    const processesInstance = ref<string[]>([])
    // 训练记录实例
    const trainInstance = ref<Record<string, any>>({})
    // 训练日志的md内容
    const trainLogMd = ref('')
    // 页面模块，前一步、下一步相关内容
    const currentStep = ref(0)
    const isNext = ref(true)

    // 数据集的下拉options
    const datasetOptions = ref<OptionsType[]>([])
    // 输出路径的下拉options
    const outputDirOptions = ref<OptionsType[]>([])
    // 配置路径的下拉options
    const configPathOptions = ref<OptionsType[]>([])

    // 是否处于训练中
    const trainingLoading = ref(false)
    // 轮询定时器
    const pollingTimer = ref()
    // 当前训练进度百分比
    const trainProgress = ref(0)
    // 损失函数echart实例
    const refMainChart = ref()
    // 是否中断
    const isInterrupt = ref(false)
    // 用于保存事件监听引用
    const resizeHandler = ref()
    // loading弹窗dom
    const refElLoading = ref()
    // 最新的日志实例
    const logInstance = ref()
    // 训练表单参数
    const isFirst = ref(false)
    const formData = ref<TrainingFormData>({
      model_log_name: '',
      lang: 'zh',
      model_name: '',
      model_path: '',
      finetuning_type: 'lora',
      checkpoint_path: [],
      quantization_bit: 'none',
      quantization_method: 'bnb',
      template: 'default',
      rope_scaling: 'none',
      booster: 'auto',
      training_stage: 'Supervised Fine-Tuning',
      dataset_dir: '/opt/workspace/LLaMA-Factory/data/ceH9MOpIrX-9',
      dataset: [],
      learning_rate: '5e-5',
      num_train_epochs: 100,
      max_grad_norm: '1.0',
      max_samples: '100000',
      compute_type: 'bf16',
      cutoff_len: 2048,
      batch_size: 2,
      gradient_accumulation_steps: 8,
      val_size: 0,
      lr_scheduler_type: 'cosine',
      logging_steps: 1,
      save_steps: 100,
      warmup_steps: 0,
      neftune_alpha: 0,
      extra_args: '{"optim": "adamw_torch"}',
      packing: false,
      neat_packing: false,
      train_on_prompt: false,
      mask_history: false,
      resize_vocab: false,
      use_llama_pro: false,
      enable_thinking: true,
      report_to: 'none',
      freeze_trainable_layers: 2,
      freeze_trainable_modules: 'all',
      freeze_extra_modules: '',
      lora_rank: 8,
      lora_alpha: 16,
      lora_dropout: 0,
      loraplus_lr_ratio: 0,
      create_new_adapter: false,
      use_rslora: false,
      use_dora: false,
      use_pissa: false,
      lora_target: '',
      additional_target: '',
      pref_beta: 0.1,
      pref_ftx: 0,
      pref_loss: 'sigmoid',
      reward_model: [],
      ppo_score_norm: false,
      ppo_whiten_rewards: false,
      freeze_vision_tower: true,
      freeze_multi_modal_projector: true,
      freeze_language_model: false,
      image_max_pixels: '768*768',
      image_min_pixels: '32*32',
      video_max_pixels: '256*256',
      video_min_pixels: '16*16',
      use_galore: false,
      galore_rank: 16,
      galore_update_interval: 200,
      galore_scale: 2,
      galore_target: 'all',
      use_apollo: false,
      apollo_rank: 16,
      apollo_update_interval: 200,
      apollo_scale: 32,
      apollo_target: 'all',
      use_badam: false,
      badam_mode: 'layer',
      badam_switch_mode: 'ascending',
      badam_switch_interval: 50,
      badam_update_ratio: 0.05,
      use_swanlab: false,
      swanlab_project: 'llamafactory',
      swanlab_run_name: '',
      swanlab_workspace: '',
      swanlab_api_key: '',
      swanlab_mode: 'cloud',
      output_dir: '',
      config_path: '',
      device_count: 1,
      ds_stage: 'none',
      ds_offload: false
    })


    const fnFormatTimestamp = (timestamp: number) => {
      const date = new Date(timestamp)
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const hours = String(date.getHours()).padStart(2, '0')
      const minutes = String(date.getMinutes()).padStart(2, '0')
      const seconds = String(date.getSeconds()).padStart(2, '0')
      return `${year}-${month}-${day}-${hours}-${minutes}-${seconds}`
    }

    //  页面参数初始化
    const fnParamsInit = () => {
      fnGetDateSetOptions()
      const time = new Date().getTime()
      configPathOptions.value.push({
        label: fnFormatTimestamp(time),
        value: fnFormatTimestamp(time) + '.yaml'
      })
      outputDirOptions.value.push({
        label: 'train_' + fnFormatTimestamp(time),
        value: 'train_' + fnFormatTimestamp(time)
      })
      formData.value.output_dir = outputDirOptions.value[0].value
      formData.value.config_path = configPathOptions.value[0].value
      formData.value.model_path = '/root/autodl-tmp/workspace/model/Qwen3-0.6B'
      handleModelChange('/root/autodl-tmp/workspace/model/Qwen3-0.6B')
    }
    // 基座模型变化事件，更新表单模型名称
    const handleModelChange = (value: any) => {
      const target = constantsOptions.ModelPath.find((item) => item.value === value)
      if (target) {
        formData.value.model_name = target.label
      }
    }
    // 更新数据集下拉选项
    const fnGetDateSetOptions = () => {
      if (!formData.value.dataset_dir || !formData.value.training_stage) return
      datasetOptions.value = []
      formData.value.dataset = []
      GetDatasets({
        dataset_dir: formData.value.dataset_dir,
        training_stage: formData.value.training_stage
      }).then((res: any) => {
        const sourceList = (res.data[0] && res.data[0].choices) || []
        datasetOptions.value = sourceList.map((item: any) => {
          return {
            label: item[0],
            value: item[0]
          }
        })
      })
    }
    // 如果是已有记录，禁止修改参数
    const isSwitchableSteps = computed(() => {
      return !!trainInstance.value.id
    })
    const fnUpdateStatus = (train_status: number) => {
      const params = Object.assign({}, trainInstance.value)
      params.train_status = train_status
      return UpdateTrainLog(params.id, params).then(res => {
        trainInstance.value = res.data
      })
    }
    const setTrainResult = () => {
      const params = Object.assign({}, trainInstance.value)
      params.train_status = 2
      let finishInfoObj = {}
      try {
        finishInfoObj = JSON.parse(logInstance.value.finish_info.replace(/```json\s*|\s*```/g, ''))
      } catch (error) {
        finishInfoObj = {}
      }
      params.train_result = finishInfoObj
      trainingLoading.value = false
      return UpdateTrainLog(params.id, params).then(res => {
        trainInstance.value = res.data
      })
    }
    const updateTrainProgress = (data: any[]) => {
      const lastLogSteps = data[data.length - 1]
      if (lastLogSteps) {
        trainProgress.value = Math.floor((lastLogSteps.current_steps / lastLogSteps.total_steps * 10000)) / 100
      }
    }
    const handleDataZoom = () => {
      if (refMainChart.value) {
        refMainChart.value.on('dataZoom', (params: any) => {
          // 获取当前 zoom 范围
          const option = refMainChart.value.getOption();
          const startValue = option.xAxis[0].data[params.startIndex];
          const endValue = option.xAxis[0].data[params.endIndex];

          // 可以在这里根据范围优化数据展示
          // 比如只渲染可视范围内的点
        });
      }
    };
    const initChart = () => {
      const dom = document.getElementById('refChartDom')
      if (dom && !refMainChart.value) {
        refMainChart.value = echarts.init(dom)
        refMainChart.value.setOption({
          color: ['#1890FF', '#FF4D4F'],
          legend: {
            data: ['原始曲线', '平滑曲线'],
            top: '8%',
            right: '5%',
            textStyle: {
              fontSize: 12
            }
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'cross',
              label: {
                backgroundColor: '#6a7985'
              }
            },
          },
          grid: {
            top: '10px',
            bottom: '70px',
            right: '90px'
          },
          xAxis: {
            type: 'category',
            name: '训练步数',
            data: [],
            axisLabel: {
              rotate: 45 // 标签旋转避免重叠
            }
          },
          yAxis: {
            type: 'value',
            name: '损失值',
            nameLocation: 'end',
            nameGap: 20 // 名称与轴线间距
          },
          dataZoom: [
            {
              show: true,
              type: 'slider', // 明确指定类型
              realtime: true,
              start: 0,
              end: 100,
              throttle: 100,// 添加节流，减少重绘频率
              height: 20,      // 设置高度为 20px
              bottom: 10
            },
            {
              type: 'inside',
              realtime: true,
              start: 0,
              end: 100,
              throttle: 100 // 添加节流
            }
          ],
          series: [
            {
              name: '原始曲线',
              type: 'line',
              smooth: true,
              symbol: 'none', // 平滑线不显示数据点
              symbolSize: 4,
              data: [],
              sampling: 'average' // 添加采样策略
            },
            {
              name: '平滑曲线',
              type: 'line',
              smooth: true,
              symbol: 'none', // 平滑线不显示数据点
              data: [],
              sampling: 'average' // 添加采样策略
            }
          ]
        })
        // 添加 resize 事件监听
        resizeHandler.value = () => {
          if (refMainChart.value) {
            refMainChart.value.resize()
          }
        }
        handleDataZoom();
        window.addEventListener('resize', resizeHandler.value)
      }
    }
    // 损失函数原始数据转平滑数据
    const fnFormatSmoothLoss = (lossData: any[]) => {
      if (lossData.length === 0) return []; // 空数组处理
      const alphaVal = alpha.value; // 提取常量
      const smoothed = lossData.reduce((acc, curr, idx, array) => {
        if (idx === 0) return [curr.loss];
        if (array[idx - 1].current_steps != (curr.current_steps - 1)) {
          acc.push(curr.loss)
        } else {
          acc.push(alphaVal * curr.loss + (1 - alphaVal) * acc[idx - 1]);

        }
        return acc;
      }, []);
      return smoothed;
    };
    // 更新损失函数图
    const updateRenderLossChart = (dataSource: any[]) => {
      if (!refMainChart.value) {
        initChart()
      }
      const options = refMainChart.value.getOption()
      options.xAxis[0].data = dataSource.map(item => item.current_steps)
      // 提取步骤和损失值
      options.series[0].data = dataSource.map(item => item.loss)
      options.series[1].data = fnFormatSmoothLoss(dataSource)
      refMainChart.value.setOption(options);
    }

    // 设置定时器轮询查询日志
    const fnSetPoller = () => {
      pollingTimer.value = setInterval(() => {
        if (trainingLoading.value) {
          loadTrainLog()
        } else {
          clearInterval(pollingTimer.value)
        }
      }, 3000);
    }
    // 获取当前训练实例的训练日志
    const loadTrainLog = () => {
      const params = {
        do_train: true,
        output_dir: formData.value.output_dir,
        finetuning_type: formData.value.finetuning_type,
        lang: formData.value.lang,
        model_name: formData.value.model_name
      }
      return FnMonitor(params).then((res: any) => {
        const logTarget = res.data && res.data[0]
        if (logTarget) {
          logInstance.value = logTarget
          trainInstance.value.train_log = logTarget.running_info || []
          trainLogMd.value = logTarget.running_log
          if (logTarget.running_log) {
            refElLoading.value && refElLoading.value.close()
          }
          if (logTarget.running_log && trainingLoading.value && isFirst) {
            isFirst.value = false
            fnUpdateStatus(1)
          }
          let running_info = logTarget.running_info || []
          if (logTarget.finish_info == '训练出错。') {
            running_info.length && updateTrainProgress(running_info);
          } else {
            let finishInfoObj = {}
            try {
              const finishInfoStr = logInstance.value.finish_info // 假设这是从接口获取的原始字符串
              finishInfoObj = JSON.parse(finishInfoStr.replace(/```json\s*|\s*```/g, '')) // 去除 ```json 和 ``` 标记后解析为对象
            } catch (error) {
              finishInfoObj = {}
            }
            if (Object.keys(finishInfoObj).length != 0) {
              setTrainResult()
              trainProgress.value = 100
              trainingLoading.value = false
              pollingTimer.value && clearInterval(pollingTimer.value)
            }
          }
          nextTick(() => {
            setTimeout(() => {
              running_info.length && updateRenderLossChart(running_info);
              updateScroll()
            }, 200);
          })
        }
      })
    }
    const loadTrainDetail = () => {

      const loading = ElLoading.service({
        lock: true,
        text: '训练数据获取中！请稍后。。。',
        background: 'rgba(0, 0, 0, 0.7)'
      })
      GetTrainLogDetail(trainInstance.value.id).then(res => {
        if (res.code == 200) {
          trainInstance.value = res.data
          formData.value = res.data.train_info
          const url = `saves/${formData.value.model_name}/${formData.value.finetuning_type}/${formData.value.output_dir}/training_args.yaml`
          if (processesInstance.value.includes(url)) {
            trainingLoading.value = true
            fnSetPoller()
            loadTrainLog().finally(() => {
              loading.close()
            })
          } else {
            GetCheckpoints({
              model_name: formData.value.model_name,
              finetuning_type: formData.value.finetuning_type,
              output_dir: formData.value.output_dir,
            }).then((res: any) => {
              if (!res.data[0][0]) {
                fnUpdateStatus(4).finally(() => {
                  loading.close()
                })
              } else {
                loading.close()
              }
            })
            loadTrainLog()
          }


        }
      }).catch(() => {
        loading.close()
      })
    }
    const fnAddLog = () => {
      AddTrainLog({
        lang: formData.value.lang,
        base_model: formData.value.model_name,
        finetuning_type: formData.value.finetuning_type,
        train_dataset: formData.value.dataset.join(),
        train_output_dir: formData.value.output_dir,
        train_info: formData.value,
        train_log: [],
        train_status: 0,
        train_category: props.train_category,
        model_name: formData.value.model_log_name,
        train_result: {}
      }).then(res => {
        if (res.code === 200) {
          trainInstance.value = res.data
        }
      })
    }
    const trainCallback = (res: any) => {
      console.log('trainCallback', res)
      refElLoading.value && refElLoading.value.close()
      trainingLoading.value = false
      if (isInterrupt.value) {
        ElMessage.error('训练已中断')
        GetCheckpoints({
          model_name: formData.value.model_name,
          finetuning_type: formData.value.finetuning_type,
          output_dir: formData.value.output_dir,
        }).then((res: any) => {
          if (!res.data[0][0]) {
            fnUpdateStatus(4)
          } else {
            fnUpdateStatus(3)
          }
        })
      } else if (res.data && res.data[0].indexOf('训练出错。 Exit code:') > -1) {
        const loading = ElLoading.service({
          lock: true,
          text: '当前训练任务失败，请重新发起训练任务！',
          background: 'rgba(0, 0, 0, 0.7)',
        })
        fnUpdateStatus(4)
        setTimeout(() => {
          loading.close()
          handleBack()
        }, 5000);
        return
      } else {
        if (res.data && res.data[0] === '任务已存在，请先中断训练。') {
          const loading = ElLoading.service({
            lock: true,
            text: '当前服务器已有进程使用，请先稍后再试。5秒钟后自动回到首页！',
            background: 'rgba(0, 0, 0, 0.7)',
          })
          setTimeout(() => {
            loading.close()
            handleBack()
          }, 5000);
        }
        return
      }
      loadTrainLog()
    }
    const fnContinueTraining = () => {
      const params: AnyType = {}
      for (const i in FieldMapping) {
        params[i] = formData.value[FieldMapping[i] as keyof TrainingFormData];
      }
      params.param_4 = [formData.value.output_dir]
      trainingLoading.value = true
      fnUpdateStatus(1)
      refElLoading.value = ElLoading.service({
        lock: true,
        text: '模型训练准备中',
        background: 'rgba(0, 0, 0, 0.7)'
      })
      RunTrain(params).then((res: any) => {
        trainCallback(res)
      })
        .finally(() => {
          if (pollingTimer.value) {
            clearInterval(pollingTimer.value)
            pollingTimer.value = null
          }
        })
      fnSetPoller()
    }
    // 开始训练
    const fnStartTraining = () => {
      const params: AnyType = {}
      for (const i in FieldMapping) {
        params[i] = formData.value[FieldMapping[i] as keyof TrainingFormData];
      }
      if (!formData.value.model_log_name) {
        ElMessage({
          message: '基础配置=>模型名称参数缺失',
          type: 'warning'
        })
        return
      }

      if (!formData.value.dataset || formData.value.dataset.length == 0) {
        ElMessage({
          message: '训练配置=>数据集参数缺失',
          type: 'warning'
        })
        return
      }
      refElLoading.value = ElLoading.service({
        lock: true,
        text: '模型训练准备中',
        background: 'rgba(0, 0, 0, 0.7)'
      })
      fnAddLog()
      trainingLoading.value = true
      currentStep.value = props.steps.length - 1
      RunTrain(params).then((res: any) => {
        trainCallback(res)
      })
        .finally(() => {
          if (pollingTimer.value) {
            clearInterval(pollingTimer.value)
            pollingTimer.value = null
          }
        })
      fnSetPoller()
    }
    const handleBack = () => {
      router.back()
    }
    onMounted(() => {
      if (route.query.trainLogId) {
        let step = 0
        if (route.name == 'ModelTrainingSimpleness') {
          step = 3
        } else {
          step = 4
        }
        currentStep.value = step
        GetProcesses().then((serverStatus: any) => {
          if (serverStatus.data && serverStatus.data[0] && serverStatus.data[0].length) {
            processesInstance.value = serverStatus.data[0]
              .filter((item: any) => item.name === 'llamafactory-cl')
              .map((item: any) => item.cmdline[item.cmdline.length - 1])
          }
          trainInstance.value.id = route.query.trainLogId
          loadTrainDetail()
        })

      } else {
        fnParamsInit()
      }

    })
    onUnmounted(() => {
      // 清除训练日志定时器
      if (pollingTimer.value) {
        clearInterval(pollingTimer.value)
        pollingTimer.value = null
      }
      // 关闭加载状态（如果存在）
      if (refElLoading.value) {
        refElLoading.value.close()
        refElLoading.value = null
      }
      // 销毁图表实例
      if (refMainChart.value) {
        refMainChart.value.dispose()
        refMainChart.value = null
      }

      // 移除 resize 事件监听
      if (resizeHandler.value) {
        window.removeEventListener('resize', resizeHandler.value)
        resizeHandler.value = null
      }

    })
    // 公共方法
    const fnNextStep = () => {
      if (currentStep.value < 3) {
        isNext.value = true
        currentStep.value++
      }
    }

    const fnPrevStep = () => {
      if (currentStep.value > 0) {
        isNext.value = false
        currentStep.value--
      }
    }
    const transitionAnimationName = computed(() => {
      return isNext.value ? 'slide-next' : 'slide-prev'
    })

    // 模型手动中断
    const handleInterrupt = () => {
      isInterrupt.value = true
      const loading = ElLoading.service({
        lock: true,
        text: '训练中断中...请稍后！',
      })
      FnBreakOff().finally(() => {
        loading.close()
      })
    }
    const openTrainLogModal = () => {
      const refTrainLogModal = props.refTrainLogModal?.value;
      if (refTrainLogModal) refTrainLogModal.openDialog()
    }
    const handleLoadParams = (params: any) => {
      delete params.model_log_name
      Object.assign(formData.value, params)
      fnParamsInit()
    }
    const updateScroll = () => {
      const logContentDom = props.refLogContentDom?.value
      if (logContentDom) {
        logContentDom.scrollTo({
          top: logContentDom.scrollHeight,
          behavior: 'smooth'
        })
      }
    }
    return {
      formData,
      currentStep,
      isSwitchableSteps,
      trainProgress,
      trainLogMd,
      outputDirOptions,
      datasetOptions,
      configPathOptions,
      trainingLoading,
      trainInstance,
      transitionAnimationName,
      fnNextStep,
      fnPrevStep,
      handleModelChange,
      fnStartTraining,
      fnContinueTraining,
      handleBack,
      handleInterrupt,
      fnGetDateSetOptions,
      openTrainLogModal,
      handleLoadParams,
    }
  }
}