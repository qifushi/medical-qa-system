import { Result } from '@/request/Result'
import { get, post, del, put, exportExcel } from '@/request/index'
import type { pageRequest } from '@/api/type/common'
import { type Ref } from 'vue'

const prefix = '/train'
export const GetTrainLog: (page: pageRequest, data: any, loading?: Ref<boolean>) => Promise<Result<any>> = (
  page,
  data,
  loading
) => {
  return post(`${prefix}/train_info/${page.current_page}/${page.page_size}`, data, undefined, loading)
}

export const AddTrainLog: (data: any, loading?: Ref<boolean>) => Promise<Result<any>> = (
  data,
  loading
) => {
  return post(`${prefix}/train_info`, data, undefined, loading)
}

export const UpdateTrainLog: (id: string, data: any, loading?: Ref<boolean>) => Promise<Result<any>> = (
  id,
  data,
  loading
) => {
  return put(`${prefix}/train_info/${id}`, data, undefined, loading)
}

export const DelTrainLog: (id: string,) => Promise<Result<any>> = (
  id,
) => {
  return del(`${prefix}/train_info/${id}`)
}

export const GetTrainLogDetail: (id: string, data?: any, loading?: Ref<boolean>) => Promise<Result<any>> = (
  id,
  data,
) => {
  return get(`${prefix}/train_info/${id}`, data, undefined,)
}
