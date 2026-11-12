import { Client } from "@gradio/client";

const baseUrl = "https://brain.jrsoft.com.cn/train_engine/";
let client = null;
let isInitializing = false;
let initPromise = null;

/**
 * 初始化 Gradio 客户端
 * @returns {Promise<Client>} 返回初始化后的客户端实例
 */
export const InitClient = async () => {
  // 如果已经在初始化中，返回同一个 Promise
  if (isInitializing) {
    return initPromise;
  }

  // 如果已经初始化，直接返回
  if (client) {
    return client;
  }

  // 设置初始化标志
  isInitializing = true;

  return initPromise = new Promise(async (resolve, reject) => {
    try {
      client = await Client.connect(baseUrl);
      resolve(client);
    } catch (error) {
      reject(error);
    } finally {
      isInitializing = false;
    }
  });
};

/**
 * 确保客户端已初始化
 * @returns {Promise<Client>} 返回初始化后的客户端实例
 */
const EnsureClientInitialized = async () => {
  if (client) return client;

  return await InitClient();

};

/**
 * 获取模型信息
 * @param {string} [model_name=''] 模型名称
 * @returns {Promise<any>} 返回模型信息
 */
export const GetModelInfo = async (model_name = '') => {
  const client = await EnsureClientInitialized();

  return new Promise(async (resolve, reject) => {
    try {
      const result = await client.predict("/get_model_info", { model_name });
      resolve(result);
    } catch (error) {
      reject(error);
    }
  });
};

/**
 * 运行训练任务
 * @param {Object} [params={}] 训练参数
 * @returns {Promise<any>} 返回训练句柄
 */
export const RunTrain = async (params = {}) => {
  const client = await EnsureClientInitialized();

  return new Promise(async (resolve, reject) => {
    try {
      const trainHandle = await client.predict("/run_train", params);
      resolve(trainHandle);
    } catch (error) {
      reject(error);
    }
  });
};

/**
 * 获取数据集列表
 * @param {Object} [params={}] 查询参数
 * @returns {Promise<any>} 返回数据集列表
 */
export const GetDatasets = async (params = {}) => {
  const client = await EnsureClientInitialized();

  return new Promise(async (resolve, reject) => {
    try {
      const result = await client.predict("/list_datasets", params);
      resolve(result);
    } catch (error) {
      reject(error);
    }
  });
};

/**
 * 获取模板列表
 * @param {string} [model_name=''] 模型名称
 * @returns {Promise<any>} 返回模板列表
 */
export const GetTemplateList = async (model_name = '') => {
  const client = await EnsureClientInitialized();

  return new Promise(async (resolve, reject) => {
    try {
      const result = await client.predict("/check_template", {
        lang: "zh",
        template: "alpaca",
      });
      resolve(result);
    } catch (error) {
      reject(error);
    }
  });
};

/**
 * 中断训练任务
 * @returns {Promise<any>} 返回中断结果
 */
export const FnBreakOff = async () => {
  const client = await EnsureClientInitialized();

  return new Promise(async (resolve, reject) => {
    try {
      const result = await client.predict("/set_abort");
      resolve(result);
    } catch (error) {
      reject(error);
    }
  });
};
/**
 * 校验检查点
 */
export const FnCheckOutput = async (params) => {
  const client = await EnsureClientInitialized();

  return new Promise(async (resolve, reject) => {
    try {
      const result = await client.predict("/check_output_dir", params);
      resolve(result);
    } catch (error) {
      reject(error);
    }
  });
};
/**
 * 监控训练过程
 * @param {Object} params 监控参数
 * @returns {Promise<any>} 返回监控结果
 */
export const FnMonitor = async (params) => {
  const client = await EnsureClientInitialized();

  return new Promise(async (resolve, reject) => {
    try {
      const result = await client.predict("/custom_monitor", params);
      resolve(result);
    } catch (error) {
      reject(error);
    }
  });
};

/**
 * 获取训练进程
 * @param {Object} params 查询参数
 * @returns {Promise<any>} 返回训练进程信息
 */
export const GetProcesses = async () => {
  const client = await EnsureClientInitialized();

  return new Promise(async (resolve, reject) => {
    try {
      const result = await client.predict("/train_processes",);
      resolve(result);
    } catch (error) {
      reject(error);
    }
  });
};

/**
 * 获取输出目录
 * @returns {Promise<any>} 返回输出目录列表
 */
export const GetOutputDirs = async () => {
  const client = await EnsureClientInitialized();

  return new Promise(async (resolve, reject) => {
    try {
      const result = await client.predict("/list_output_dirs_1");
      resolve(result);
    } catch (error) {
      reject(error);
    }
  });
};
export const GetCheckpoints = async (params) => {
  const client = await EnsureClientInitialized();

  return new Promise(async (resolve, reject) => {
    try {
      const result = await client.predict("/get_checkpoints", params);
      resolve(result);
    } catch (error) {
      reject(error);
    }
  });
};

/**
 * 运行评测任务
 * @param {Object} [params={}] 评测参数
 * @returns {Promise<any>} 返回评测句柄
 */
export const RunEval = async (params = {}) => {
  const client = await EnsureClientInitialized();

  return new Promise(async (resolve, reject) => {
    try {
      const trainHandle = await client.predict("/run_eval", params);
      resolve(trainHandle);
    } catch (error) {
      reject(error);
    }
  });
};



/**
 * 导出模型
 */
export const SaveModel = async (params = {}) => {
  const client = await EnsureClientInitialized();

  return new Promise(async (resolve, reject) => {
    try {
      const trainHandle = await client.predict("/save_model", params);
      resolve(trainHandle);
    } catch (error) {
      reject(error);
    }
  });
};
// 应用启动时自动初始化客户端
InitClient().catch(() => {
});