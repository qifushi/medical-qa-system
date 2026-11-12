import { Result } from '@/request/Result'
import { get, post, del, put, exportExcel } from '@/request/index'
import type { pageRequest } from '@/api/type/common'
import { type Ref } from 'vue'

const prefix = '/magic'
export const GetSmartPPT: (page: pageRequest, data: any, loading?: Ref<boolean>) => Promise<Result<any>> = (
  page,
  data,
  loading
) => {
  return post(`${prefix}/smart_ppt/${page.current_page}/${page.page_size}`, data, undefined, loading)
}

export const AddSmartPPT: (data: any, loading?: Ref<boolean>) => Promise<Result<any>> = (
  data,
  loading
) => {
  return post(`${prefix}/smart_ppt`, data, undefined, loading)
}

export const UpdateSmartPPT: (id: string, data: any, loading?: Ref<boolean>) => Promise<Result<any>> = (
  id,
  data,
  loading
) => {
  return put(`${prefix}/smart_ppt/${id}`, data, undefined, loading)
}

export const DelSmartPPT: (id: string,) => Promise<Result<any>> = (
  id,
) => {
  return del(`${prefix}/smart_ppt/${id}`)
}

export const GetSmartPPTDetail: (id: string, data?: any, loading?: Ref<boolean>) => Promise<Result<any>> = (
  id,
  data,
) => {
  return get(`${prefix}/smart_ppt/${id}`, data, undefined,)
}
