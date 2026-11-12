interface ModelReleaseType {
  model_path: string; // 模型路径
  infer_framework: string; // 推理框架 vllm, sglang
  model_name: string; //模型名称
  model_code: string; //模型编码
  publish_port: number | null; // 对外发布端口
  publish_ip?: string; //对外发布ip
  api_key: string; // api-key
  context_length?: number | null; //最大上下文长度
  model_desc?: string;//模型描述
  publish_status: number;//发布状态：默认0未发布，1已发布，2发布失败
  health_check_url?: string;//服务状态检测地址
  username?: string; //用户姓名
  id?: string; // 模型发布id
  gpu_memory_utilization: number; // GPU内存使用率
  health_status?: string; // 健康状态
}

export type { ModelReleaseType }