import { Result } from '@/request/Result'
import { get, post, del, put } from '@/request/index'
import { type Ref } from 'vue'
import type { pageRequest } from '@/api/type/common'
import type {
    ModelReleaseType
} from '@/api/type/model-release'

const prefix = '/train/publish_info'

/**
 * 新增模型发布
 * @param request 请求对象
 * @param loading 加载器
 * @returns
 */
const addModelRelease: (
    data: ModelReleaseType,
    loading?: Ref<boolean>
) => Promise<Result<any>> = (data, loading) => {
    return post(`${prefix}`, data, undefined, loading)
}

/**
 * 获取训练数据源列表
  */
const postModelReleaseList: (page: pageRequest, data: any, loading?: Ref<boolean>) => Promise<Result<any>> = (
    page,
    data,
    loading
) => {
    return post(`${prefix}/${page.current_page}/${page.page_size}`, data, undefined, loading)
}

/**
 * 通过 publish_id 查询模型发布
 * @query 参数 
 * data
 */
const getModelReleaseById: (publish_id: string, loading?: Ref<boolean>) => Promise<Result<any>> = (
    publish_id,
    loading
  ) => {
    return get(`${prefix}/${publish_id}`, undefined, loading)
  }

/**
 * 修改模型发布
 * @param publish_id 数据源id
 * @param loading 接口加载器
 * @returns
 */
const putModelRelease: (
  publish_id: string,
  data:any,
  loading?: Ref<boolean>
) => Promise<Result<any>> = (publish_id,data, loading) => {
  return put(`${prefix}/${publish_id}`, data, undefined, loading)
}

  /**
   * 删除模型发布
   * @param 参数 publish_id
   */
const delModelRelease: (publish_id: String) => Promise<Result<boolean>> = (publish_id) => {
    return del(`${prefix}/${publish_id}`)
  }

/**
 * 模型发布状态切换
 */
const putModelReleaseStatus: (
    publish_id: string,
    status: number,
    loading?: Ref<boolean>
) => Promise<Result<any>> = (publish_id, status, loading) => {
    return put(`${prefix}/${publish_id}/${status}`, {}, undefined, loading)
}


export default {
    addModelRelease,
    postModelReleaseList,
    getModelReleaseById,
    putModelRelease,
    delModelRelease,
    putModelReleaseStatus
}