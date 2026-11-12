import constantsOptions from '@/views/model-control-desk/utils/constantsOptions'
// 定义基础字典项类型
export interface DictItem {
  value: string;
  label: string;
  options?: Array<{ label: string; value: string | number }>; // 选项类型
  fieldType?: 'boolean' | 'number'; // 字段类型
  child?: DictItem[]; // 子项
}

// 定义字段映射类型
export type FieldMappingType = Record<string, string>;

export const FieldMapping: FieldMappingType = {
  data: 'lang',
  param_1: 'model_name',
  param_2: 'model_path',
  param_3: 'finetuning_type',
  param_4: 'checkpoint_path',
  param_5: 'quantization_bit',
  param_6: 'quantization_method',
  param_7: 'template',
  param_8: 'rope_scaling',
  param_9: 'booster',
  param_10: 'training_stage',
  param_11: 'dataset_dir',
  param_12: 'dataset',
  param_13: 'learning_rate',
  param_14: 'num_train_epochs',
  param_15: 'max_grad_norm',
  param_16: 'max_samples',
  param_17: 'compute_type',
  param_18: 'cutoff_len',
  param_19: 'batch_size',
  param_20: 'gradient_accumulation_steps',
  param_21: 'val_size',
  param_22: 'lr_scheduler_type',
  param_23: 'logging_steps',
  param_24: 'save_steps',
  param_25: 'warmup_steps',
  param_26: 'neftune_alpha',
  param_27: 'extra_args',
  param_28: 'packing',
  param_29: 'neat_packing',
  param_30: 'train_on_prompt',
  param_31: 'mask_history',
  param_32: 'resize_vocab',
  param_33: 'use_llama_pro',
  param_34: 'enable_thinking',
  param_35: 'report_to',
  param_36: 'freeze_trainable_layers',
  param_37: 'freeze_trainable_modules',
  param_38: 'freeze_extra_modules',
  param_39: 'lora_rank',
  param_40: 'lora_alpha',
  param_41: 'lora_dropout',
  param_42: 'loraplus_lr_ratio',
  param_43: 'create_new_adapter',
  param_44: 'use_rslora',
  param_45: 'use_dora',
  param_46: 'use_pissa',
  param_47: 'lora_target',
  param_48: 'additional_target',
  param_49: 'pref_beta',
  param_50: 'pref_ftx',
  param_51: 'pref_loss',
  param_52: 'reward_model',
  param_53: 'ppo_score_norm',
  param_54: 'ppo_whiten_rewards',
  param_55: 'freeze_vision_tower',
  param_56: 'freeze_multi_modal_projector',
  param_57: 'freeze_language_model',
  param_58: 'image_max_pixels',
  param_59: 'image_min_pixels',
  param_60: 'video_max_pixels',
  param_61: 'video_min_pixels',
  param_62: 'use_galore',
  param_63: 'galore_rank',
  param_64: 'galore_update_interval',
  param_65: 'galore_scale',
  param_66: 'galore_target',
  param_67: 'use_apollo',
  param_68: 'apollo_rank',
  param_69: 'apollo_update_interval',
  param_70: 'apollo_scale',
  param_71: 'apollo_target',
  param_72: 'use_badam',
  param_73: 'badam_mode',
  param_74: 'badam_switch_mode',
  param_75: 'badam_switch_interval',
  param_76: 'badam_update_ratio',
  param_77: 'use_swanlab',
  param_78: 'swanlab_project',
  param_79: 'swanlab_run_name',
  param_80: 'swanlab_workspace',
  param_81: 'swanlab_api_key',
  param_82: 'swanlab_mode',
  param_83: 'device_count',
  param_84: 'output_dir',
  param_85: 'config_path',
  param_86: 'ds_stage',
  param_87: 'ds_offload'
}

export const FileDict: DictItem[] = [
  {
    value: "lang",
    label: "语言"
  },
  {
    value: "model_name",
    label: "基座名称"
  },
  {
    value: "model_path",
    label: "模型路径"
  },
  {
    value: "finetuning_type",
    label: "微调方法",
    options: constantsOptions.MethodOption
  },
  {
    value: "checkpoint_path",
    label: "检查点路径"
  },
  {
    value: "quantization_bit",
    label: "量化等级"
  },
  {
    value: "quantization_method",
    label: "量化方法",
    options: constantsOptions.QuantizationMethod
  },
  {
    value: "template",
    label: "对话模板"
  },
  {
    value: "rope_scaling",
    label: "RoPE 插值方法",
    options: constantsOptions.RopeScaling
  },
  {
    value: "booster",
    label: "加速方式",
    options: constantsOptions.Booster
  },
  {
    value: "training_stage",
    label: "训练阶段",
    options: constantsOptions.TrainingStage
  },
  {
    value: "dataset_dir",
    label: "数据路径"
  },
  {
    value: "dataset",
    label: "数据集"
  },
  {
    value: "learning_rate",
    label: "学习率"
  },
  {
    value: "num_train_epochs",
    label: ""
  },
  {
    value: "max_grad_norm",
    label: "训练轮数"
  },
  {
    value: "max_samples",
    label: "最大样本数"
  },
  {
    value: "compute_type",
    label: "计算类型",
    options: constantsOptions.ComputeType
  },
  {
    value: "cutoff_len",
    label: "截断长度"
  },
  {
    value: "batch_size",
    label: "批处理大小"
  },
  {
    value: "gradient_accumulation_steps",
    label: "梯度累积"
  },
  {
    value: "val_size",
    label: "验证集比例"
  },
  {
    value: "lr_scheduler_type",
    label: "学习率调节器",
    options: constantsOptions.LrSchedulerType
  },
  {
    value: "logging_steps",
    label: "日志间隔"
  },
  {
    value: "save_steps",
    label: "保存间隔"
  },
  {
    value: "warmup_steps",
    label: "预热步数"
  },
  {
    value: "neftune_alpha",
    label: "NEFTune 噪声参数"
  },
  {
    value: "extra_args",
    label: "额外参数"
  },
  {
    value: "packing",
    label: ""
  },
  {
    value: "neat_packing",
    label: "序列打包"
  },
  {
    value: "train_on_prompt",
    label: "使用无污染打包",
    fieldType: 'boolean'
  },
  {
    value: "mask_history",
    label: "不学习历史对话",
    fieldType: 'boolean'
  },
  {
    value: "resize_vocab",
    label: "更改词表大小",
    fieldType: 'boolean'
  },
  {
    value: "use_llama_pro",
    label: "使用 LLaMA Pro",
    fieldType: 'boolean'
  },
  {
    value: "enable_thinking",
    label: "启用思考模式",
    fieldType: 'boolean'
  },
  {
    value: "report_to",
    label: "启用外部记录面板",
    options: constantsOptions.ReportTo
  },
  {
    value: "freeze_trainable_layers",
    label: "可训练层数"
  },
  {
    value: "freeze_trainable_modules",
    label: "可训练模块"
  },
  {
    value: "freeze_extra_modules",
    label: "额外模块"
  },
  {
    value: "lora_rank",
    label: "LoRA 秩"
  },
  {
    value: "lora_alpha",
    label: "LoRA 缩放系数"
  },
  {
    value: "lora_dropout",
    label: "LoRA 随机丢弃"
  },
  {
    value: "loraplus_lr_ratio",
    label: "LoRA+ 学习率比例"
  },
  {
    value: "create_new_adapter",
    label: "新建适配器"
  },
  {
    value: "use_rslora",
    label: "使用 rslora",
    fieldType: 'boolean'
  },
  {
    value: "use_dora",
    label: "使用 DoRA",
    fieldType: 'boolean'
  },
  {
    value: "use_pissa",
    label: "使用 PiSSA",
    fieldType: 'boolean'
  },
  {
    value: "lora_target",
    label: "LoRA 作用模块"
  },
  {
    value: "additional_target",
    label: "LoRA 附加模块"
  },
  {
    value: "pref_beta",
    label: "Beta 参数"
  },
  {
    value: "pref_ftx",
    label: "Ftx gamma"
  },
  {
    value: "pref_loss",
    label: "损失类型",
    options: constantsOptions.Sigmoid
  },
  {
    value: "reward_model",
    label: "奖励模型"
  },
  {
    value: "ppo_score_norm",
    label: "归一化分数",
    fieldType: 'boolean'
  },
  {
    value: "ppo_whiten_rewards",
    label: "白化奖励",
    fieldType: 'boolean'
  },
  {
    value: "freeze_vision_tower",
    label: "冻结视觉编码器",
    fieldType: 'boolean'
  },
  {
    value: "freeze_multi_modal_projector",
    label: "冻结多模态投影器",
    fieldType: 'boolean'
  },
  {
    value: "freeze_language_model",
    label: "冻结语言模型",
    fieldType: 'boolean'
  },
  {
    value: "image_max_pixels",
    label: "图像最大像素"
  },
  {
    value: "image_min_pixels",
    label: "图像最小像素"
  },
  {
    value: "video_max_pixels",
    label: "视频最大像素"
  },
  {
    value: "video_min_pixels",
    label: "视频最小像素"
  },
  {
    value: "use_galore",
    label: "使用GaLore 参数设置",
    fieldType: 'boolean',
    child: [{
      value: "galore_rank",
      label: "GaLore 秩"
    }, {
      value: "galore_update_interval",
      label: "更新间隔"
    }, {
      value: "galore_scale",
      label: "GaLore 缩放系数"
    }, {
      value: "galore_target",
      label: "GaLore 作用模块"
    },]
  },
  {
    value: "use_apollo",
    label: "使用GAPOLLO 参数设置",
    fieldType: 'boolean',
    child: [{
      value: "apollo_rank",
      label: "APOLLO 秩",
      fieldType: 'number',
    }, {
      value: "apollo_update_interval",
      label: "更新间隔"
    }, {
      value: "apollo_scale",
      label: "APOLLO 缩放系数"
    }, {
      value: "apollo_target",
      label: "APOLLO 作用模块"
    },]
  },
  {
    value: "use_badam",
    label: "使用 BAdam 参数设置",
    fieldType: 'boolean',
    child: [{
      value: "badam_mode",
      label: "BAdam 模式",
      options: constantsOptions.BadamMode
    }, {
      value: "badam_switch_mode",
      label: "切换策略"
    }, {
      value: "badam_switch_interval",
      label: "切换频率"
    }, {
      value: "badam_update_ratio",
      label: "Block 更新比例"
    },]
  },






  {
    value: "use_swanlab",
    label: ""
  },
  {
    value: "swanlab_project",
    label: ""
  },
  {
    value: "swanlab_run_name",
    label: ""
  },
  {
    value: "swanlab_workspace",
    label: ""
  },
  {
    value: "swanlab_api_key",
    label: ""
  },
  {
    value: "swanlab_mode",
    label: ""
  },
  {
    value: "device_count",
    label: "设备数量"
  },
  {
    value: "output_dir",
    label: "输出目录"
  },
  {
    value: "config_path",
    label: "配置路径"
  },
  {
    value: "ds_stage",
    label: "DeepSpeed stage"
  },
  {
    value: "ds_offload",
    label: "使用offload",
    fieldType: 'boolean',
  }
]