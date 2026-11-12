import { post } from '@/request/index'
import { Result } from '@/request/Result'

const prefix = '/medical'

/**
 * 医疗助手对话
 * @param content 对话内容
 * @param smart_search 是否启动智能搜索（联网搜索）
 * @param deep_think 是否启动深度思考（生成思考过程）
 * @param kb_type 知识库类型（report_analysis, medical_service, medicine_analysis）
 * @returns 对话回复
 */
export interface KbSource {
  name: string
  kb: string
  score: number
}

export const chat = (content: string, smart_search: boolean = false, deep_think: boolean = false, kb_type?: string): Promise<Result<string> & { sources?: KbSource[] }> => {
  return post(`${prefix}/chat/`, { content, smart_search, deep_think, kb_type })
}

/**
 * 重置对话历史
 * @returns 重置结果
 */
export const resetHistory = (): Promise<Result<string>> => {
  return post(`${prefix}/reset_history/`)
}

export default {
  chat,
  resetHistory
}