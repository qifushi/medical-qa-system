import { Result } from '@/request/Result'
import { get, post, del, put,exportExcel } from '@/request/index'
import type { pageRequest } from '@/api/type/common'
import { type Ref } from 'vue'

const prefix = '/train'
/**
 * 创建训练数据源
 * @param 参数 
 * data
 */
   const postTrainSource: (data: any, loading?: Ref<boolean>) => Promise<Result<any>> = (
    data,
    loading
  ) => {
    return post(`${prefix}/datasource`, data, undefined, loading)
  }
/**
 * 通过id查询训练数据源
 * @query 参数 
 * data
 */
   const getTrainSourceById: (data_source_id: string, loading?: Ref<boolean>) => Promise<Result<any>> = (
    data_source_id,
    loading
  ) => {
    return get(`${prefix}/datasource/${data_source_id}`, undefined, loading)
  }
/**
 * 修改训练数据源
 * @param data_source_id 数据源id
 * @param loading 接口加载器
 * @returns
 */
const putTrainSource: (
  data_source_id: string,
  data:any,
  loading?: Ref<boolean>
) => Promise<Result<any>> = (data_source_id,data, loading) => {
  return put(`${prefix}/datasource/${data_source_id}`, data, undefined, loading)
}

/**
 * 获取训练数据源列表
 * @param 参数 
 * page  {
              "current_page": "string",
              "page_size": "string",
            }
 * @data 参数 
   data
 */
   const postTrainSourceList: (page: pageRequest, data: any, loading?: Ref<boolean>) => Promise<Result<any>> = (
    page,
    data,
    loading
  ) => {
    return post(`${prefix}/datasource/${page.current_page}/${page.page_size}`, data, undefined, loading)
  }

/**
 * 上传训练数据源文件
 * @param 参数 
 * formData
 */
const uploadTrainSource: (data_source_id:string,formData: FormData, loading?: Ref<boolean>) => Promise<Result<any>> = (
  data_source_id,
  formData,
  loading
) => {
  return post(`${prefix}/datasource/data/${data_source_id}`, formData, undefined, loading)
}
/**
 * 获取训练数据源文件列表
 * @query 参数 
   data_source_id
 */
   const getUploadTrainSource: (
    data_source_id:string,
    loading?: Ref<boolean>
  ) => Promise<Result<any>> = (data_source_id, loading) => {
    return get(
      `${prefix}/datasource/data/${data_source_id}`,
      undefined,
      loading
    )
  }
  /**
   * 删除训练数据源
   * @param 参数 data_source_id
   */
  const delTrainSource: (data_source_id: String) => Promise<Result<boolean>> = (data_source_id) => {
    return del(`${prefix}/datasource/${data_source_id}`)
  }
  /**
   * 删除训练数据源文件
   * @param 参数 data_source_id
   */
  const delTrainSourceFile: (data_source_item_id: String) => Promise<Result<boolean>> = (data_source_item_id) => {
    return del(`${prefix}/datasource/delete/${data_source_item_id}`)
  }

/**
 * 下载训练数据源文件
 * @query 参数 
   data_source_item_id
 */
   const getTrainSourceFile: (
    fileName: string,
    data_source_item_id:string,
    loading?: Ref<boolean>
  ) => Promise<Result<any>> = (fileName,data_source_item_id, loading) => {
    return exportExcel(fileName,
      `${prefix}/datasource/download/${data_source_item_id}`,
      undefined,
      loading
    )
  }

export default {
  getTrainSourceById,
  postTrainSourceList,
  postTrainSource,
  uploadTrainSource,
  getUploadTrainSource,
  putTrainSource,
  delTrainSource,
  delTrainSourceFile,
  getTrainSourceFile
}
