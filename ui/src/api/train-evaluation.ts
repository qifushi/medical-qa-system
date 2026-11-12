import { Result } from '@/request/Result'
import { get, post, del, put, exportExcel } from '@/request/index'
import type { pageRequest } from '@/api/type/common'
import { type Ref } from 'vue'

const prefix = '/train/eval_info'

/**
 * 获取模型评测列表
  */
const postModelEvaList: (page: pageRequest, data: any, loading?: Ref<boolean>) => Promise<Result<any>> = (
    page,
    data,
    loading
) => {
    return post(`${prefix}/${page.current_page}/${page.page_size}`, data, undefined, loading)
}


// 根据训练id获取评测记录详情
const GetEvalInfoByTrainId: (train_id: string,) => Promise<Result<any>> = (
    train_id,
) => {
    return post(`${prefix}/query_by_train/${train_id}`,)
}
// 新增评测记录
const AddEvalInfo: (data: object,) => Promise<Result<any>> = (
    data,
) => {
    return post(`${prefix}`, data)
}
// 新增评测记录
const UpdateEvalInfo: (id: string, data: object,) => Promise<Result<any>> = (
    id,
    data,
) => {
    return put(`${prefix}/${id}`, data)
}
interface ApplicationProfile {
    id: string;
    [key: string]: any;
}

interface ChatSession {
    data: string; // chat_id
    [key: string]: any;
}

interface ChatMessageResponse {
    [key: string]: any;
}

const baseUrl = "/api/application"
/**
 * 使用 API Key 进行三步调用的工具方法
 * @param apiKey - 用户的 API Key
 * @returns 最终对话响应
 */
const callApiWithApiKey = async (
    apiKey: string,
    data: object
): Promise<any> => {
    const headers = {
        'authorization': apiKey,
        'Content-Type': 'application/json',

    };

    try {
        // 步骤1: 获取应用相关信息
        const profileResponse = await fetch(baseUrl + '/profile', {
            method: 'GET',
            headers
        });

        if (!profileResponse.ok) {
            throw new Error(`获取应用信息失败: ${profileResponse.status}`);
        }

        const profileData: ApplicationProfile = await profileResponse.json();
        console.log('应用信息:', profileData);
        const applicationId = profileData.data.id;

        // 步骤2: 获取会话ID
        const chatResponse = await fetch(`${baseUrl}/${applicationId}/chat/open`, {
            method: 'GET',
            headers
        });

        if (!chatResponse.ok) {
            throw new Error(`创建会话失败: ${chatResponse.status}`);
        }

        const chatData: ChatSession = await chatResponse.json();
        const chatId = chatData.data;

        // 步骤3: 发送对话消息

        const messageResponse = await fetch(`${baseUrl}/chat_message/${chatId}`, {
            method: 'POST',
            headers,
            body: JSON.stringify({
                "message": JSON.stringify(data),
                "re_chat": false,
                "stream": false,
                "online_search": false,
            })
        });

        if (!messageResponse.ok) {
            throw new Error(`发送消息失败: ${messageResponse.status}`);
        }

        const messageData: ChatMessageResponse = await messageResponse.json();
        return messageData;

    } catch (error) {
        console.error('调用 API 失败:', error);
        throw error;
    }
}


// 新增模型横向评测记录
const AddEvalContrastInfo: (data: object,) => Promise<Result<any>> = (
    data,
) => {
    return post(`${prefix}/contrast`, data)
}

// 根据 ID 查询模型横向评测记录
const getEvalContrastRecordById: (
    contrast_id: string,
    loading?: Ref<boolean>
) => Promise<Result<any>> = (contrast_id, loading) => {
    return get(`${prefix}/contrast/${contrast_id}`, loading)
}
// 分页查询模型横向评测记录
const postEvalContrastRecord: (page: pageRequest, data: any, loading?: Ref<boolean>) => Promise<Result<any>> = (
    page,
    data,
    loading
) => {
    return post(`${prefix}/contrast/${page.current_page}/${page.page_size}`, data, undefined, loading)
}
export default {
    postModelEvaList,
    GetEvalInfoByTrainId,
    AddEvalInfo,
    UpdateEvalInfo,
    callApiWithApiKey,
    AddEvalContrastInfo,
    getEvalContrastRecordById,
    postEvalContrastRecord
}