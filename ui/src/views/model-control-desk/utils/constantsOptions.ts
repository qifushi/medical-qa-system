// 微调方法
const MethodOption = [{
  label: "全参微调",
  value: "full"
}, {
  label: "冻结微调",
  value: "freeze"
}, {
  label: "lora",
  value: "lora"
},]

// 量化等级
const QuantizationBit = [{
  label: "none",
  value: "none"
}, {
  label: "8",
  value: "8"
}, {
  label: "4",
  value: "4"
},]
// 量化方法
const QuantizationMethod = [{
  label: "bnb",
  value: "bnb"
}, {
  label: "hqq",
  value: "hqq"
}, {
  label: "eetq",
  value: "eetq"
},]
// 对话模板
const Template = [{}]

// RoPE 插值方法
const RopeScaling = [{
  label: "禁用插值",
  value: "none"
}, {
  label: "线性缩放位置索引‌",
  value: "linear"
}, {
  label: "动态调整缩放因子‌",
  value: "dynamic"
}, {
  label: "分段优化插值‌",
  value: "yarn"
}, {
  label: "llama3",
  value: "llama3"
},]
// 加速方法
const Booster = [{
  label: "auto",
  value: "auto"
}, {
  label: "flashattn2",
  value: "flashattn2"
}, {
  label: "unsloth",
  value: "unsloth"
}, {
  label: "liger_kernel",
  value: "liger_kernel"
},]

// 训练阶段
const TrainingStage = [
  {
    label: "Supervised Fine-Tuning",
    value: "Supervised Fine-Tuning"
  },
  { label: "Reward Modeling", value: "Reward Modeling" },
  { label: "PPO", value: "PPO" },
  { label: "DPO", value: "DPO" },
  { label: "KTO", value: "KTO" },
  { label: "Pre-Training", value: "Pre-Training" }]

// 计算类型
const ComputeType = [
  { label: "bf16", value: "bf16" },
  { label: "fp16", value: "fp16" },
  { label: "fp32", value: "fp32" },
  { label: "pure_bf16", value: "pure_bf16" }
]
// 启用外部记录面板
const ReportTo = [
  { label: "none", value: "none" },
  { label: "wandb", value: "wandb" },
  { label: "mlflow", value: "mlflow" },
  { label: "neptune", value: "neptune" },
  { label: "tensorboard", value: "tensorboard" },
  { label: "all", value: "all" },
]
// 损失类型
const Sigmoid = [
  { label: "sigmoid", value: "sigmoid" },
  { label: "hinge", value: "hinge" },
  { label: "ipo", value: "ipo" },
  { label: "kto_pair", value: "kto_pair" },
  { label: "orpo", value: "orpo" },
  { label: "simpo", value: "simpo" },
]

// BAdam 模式
const BadamMode = [
  { label: "layer", value: "layer" },
  { label: "ratio", value: "ratio" },

]
// Layer-wise BAdam 优化器的块切换策略。
const BadamWwitchMode = [
  { label: "ascending", value: "ascending" },
  { label: "descending", value: "descending" },
  { label: "random", value: "random" },
  { label: "fixed", value: "fixed" },
]
// SwanLab 模式
const SwanlabMode = [
  { label: "cloud", value: "cloud" },
  { label: "local", value: "local" },
]
// DeepSpeed stage
const DsStage = [
  { label: "none", value: "none" },
  { label: "2", value: "2" },
  { label: "3", value: "3" },

]

// const ModelOptions = [
//   { label: "Aya-23-8B-Chat", value: "Aya-23-8B-Chat" },
//   { label: "Qwen3-0.6B-Base", value: "Qwen3-0.6B-Base" },
// ]


// 对话模板
const TemplateOption = [
  { label: "alpaca", value: "alpaca" },
  { label: "aquila", value: "aquila" },
  { label: "atom", value: "atom" },
  { label: "baichuan", value: "baichuan" },
  { label: "baichuan2", value: "baichuan2" },
  { label: "bailing", value: "bailing" },
  { label: "belle", value: "belle" },
  { label: "bluelm", value: "bluelm" },
  { label: "breeze", value: "breeze" },
  { label: "chatglm2", value: "chatglm2" },
  { label: "chatglm3", value: "chatglm3" },
  { label: "chatml", value: "chatml" },
  { label: "chatml_de", value: "chatml_de" },
  { label: "codegeex2", value: "codegeex2" },
  { label: "codegeex4", value: "codegeex4" },
  { label: "cohere", value: "cohere" },
  { label: "cpm", value: "cpm" },
  { label: "cpm3", value: "cpm3" },
  { label: "dbrx", value: "dbrx" },
  { label: "deepseek", value: "deepseek" },
  { label: "deepseek3", value: "deepseek3" },
  { label: "deepseekr1", value: "deepseekr1" },
  { label: "deepseekcoder", value: "deepseekcoder" },
  { label: "default", value: "default" },
  { label: "empty", value: "empty" },
  { label: "exaone", value: "exaone" },
  { label: "falcon", value: "falcon" },
  { label: "fewshot", value: "fewshot" },
  { label: "gemma", value: "gemma" },
  { label: "gemma3", value: "gemma3" },
  { label: "glm4", value: "glm4" },
  { label: "glmz1", value: "glmz1" },
  { label: "granite3", value: "granite3" },
  { label: "granite3_vision", value: "granite3_vision" },
  { label: "index", value: "index" },
  { label: "hunyuan", value: "hunyuan" },
  { label: "intern", value: "intern" },
  { label: "intern2", value: "intern2" },
  { label: "intern_vl", value: "intern_vl" },
  { label: "kimi_vl", value: "kimi_vl" },
  { label: "llama2", value: "llama2" },
  { label: "llama2_zh", value: "llama2_zh" },
  { label: "llama3", value: "llama3" },
  { label: "llama4", value: "llama4" },
  { label: "mllama", value: "mllama" },
  { label: "moonlight", value: "moonlight" },
  { label: "llava", value: "llava" },
  { label: "llava_next", value: "llava_next" },
  { label: "llava_next_llama3", value: "llava_next_llama3" },
  { label: "llava_next_mistral", value: "llava_next_mistral" },
  { label: "llava_next_qwen", value: "llava_next_qwen" },
  { label: "llava_next_yi", value: "llava_next_yi" },
  { label: "llava_next_video", value: "llava_next_video" },
  { label: "llava_next_video_mistral", value: "llava_next_video_mistral" },
  { label: "llava_next_video_yi", value: "llava_next_video_yi" },
  { label: "marco", value: "marco" },
  { label: "mimo", value: "mimo" },
  { label: "mimo_vl", value: "mimo_vl" },
  { label: "minicpm_v", value: "minicpm_v" },
  { label: "minicpm_o", value: "minicpm_o" },
  { label: "ministral", value: "ministral" },
  { label: "mistral", value: "mistral" },
  { label: "mistral_small", value: "mistral_small" },
  { label: "olmo", value: "olmo" },
  { label: "openchat", value: "openchat" },
  { label: "openchat-3.6", value: "openchat-3.6" },
  { label: "opencoder", value: "opencoder" },
  { label: "orion", value: "orion" },
  { label: "paligemma", value: "paligemma" },
  { label: "paligemma_chat", value: "paligemma_chat" },
  { label: "phi", value: "phi" },
  { label: "phi_small", value: "phi_small" },
  { label: "phi4", value: "phi4" },
  { label: "pixtral", value: "pixtral" },
  { label: "qwen", value: "qwen" },
  { label: "qwen3", value: "qwen3" },
  { label: "qwen2_audio", value: "qwen2_audio" },
  { label: "qwen2_omni", value: "qwen2_omni" },
  { label: "qwen2_vl", value: "qwen2_vl" },
  { label: "sailor", value: "sailor" },
  { label: "seed_coder", value: "seed_coder" },
  { label: "skywork_o1", value: "skywork_o1" },
  { label: "smollm", value: "smollm" },
  { label: "smollm2", value: "smollm2" },
  { label: "solar", value: "solar" },
  { label: "starchat", value: "starchat" },
  { label: "telechat", value: "telechat" },
  { label: "telechat2", value: "telechat2" },
  { label: "vicuna", value: "vicuna" },
  { label: "video_llava", value: "video_llava" },
  { label: "xuanyuan", value: "xuanyuan" },
  { label: "xverse", value: "xverse" },
  { label: "yayi", value: "yayi" },
  { label: "yi", value: "yi" },
  { label: "yi_vl", value: "yi_vl" },
  { label: "yuan", value: "yuan" },
  { label: "zephyr", value: "zephyr" },
  { label: "ziya", value: "ziya" },

]

const ModelPath = [
  { label: "Qwen3-0.6B-Instruct", value: "/root/autodl-tmp/workspace/model/Qwen3-0.6B" },

]
// 学习率调节器
const LrSchedulerType = [
  { label: "线性衰减", value: "linear" },
  { label: "余弦衰减", value: "cosine" },
  { label: "带重启的余弦衰减", value: "cosine_with_restarts" },
  { label: "多项式衰减", value: "polynomial" },
  { label: "常数", value: "constant" },
  { label: "带预热期的常数", value: "constant_with_warmup" },
  { label: "倒数平方根衰减", value: "inverse_sqrt" },
  { label: "平台衰减", value: "reduce_lr_on_plateau" },
  { label: "带最小值的余弦衰减", value: "cosine_with_min_lr" },
  { label: "预热后稳定衰减", value: "warmup_stable_decay" },
]

const TrainStatusOption = [
  { label: "未开始", value: 0 },
  { label: "进行中", value: 1 },
  { label: "已完成", value: 2 },
  { label: "中断", value: 3 },
  { label: "训练失败", value: 4 },
]
const TrainCategoryOption = [
  { value: 0, label: "快速训练", abbreviation: '快' },
  { value: 1, label: "高级训练", abbreviation: '高' },
]
export default {
  MethodOption,
  QuantizationBit,
  QuantizationMethod,
  Template,
  RopeScaling,
  Booster,
  TrainingStage,
  ComputeType,
  ReportTo,
  Sigmoid,
  BadamMode,
  BadamWwitchMode,
  SwanlabMode,
  DsStage,
  // ModelOptions,
  ModelPath,
  TemplateOption,
  LrSchedulerType,
  TrainStatusOption,
  TrainCategoryOption
}