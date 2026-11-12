import type { CustomFormType } from '@/api/type/custom'
import { Result } from '@/request/Result'
import { del, get, post } from '@/request/index'
import { type Ref } from 'vue'

const prefix = '/custom'

/**
 * 获取全部指令
 * @param 参数
 */
const getAllCustom: (loading?: Ref<boolean>) => Promise<Result<any[]>> = (loading) => {
  return get(`${prefix}/prompt_list`, undefined, loading)
}

/**
 * 创建指令
 * @param 参数
 */
const postCustom: (data: CustomFormType, loading?: Ref<boolean>) => Promise<Result<any>> = (
  data,
  loading
) => {
  return post(`${prefix}/prompt_add`, data, undefined, loading)
}

/**
 * 删除指令
 * @param 参数 application_id
 */
const delCustom: (prompt_id: String, loading?: Ref<boolean>) => Promise<Result<boolean>> = (
  prompt_id,
  loading
) => {
  return del(`${prefix}/prompt/${prompt_id}`, undefined, {}, loading)
}

export default {
  getAllCustom,
  postCustom,
  delCustom
}
