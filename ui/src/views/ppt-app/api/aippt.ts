
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
    data: object,
    isStream: boolean 
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
                "stream": isStream,
                "online_search": false,
            })
        });

        if (!messageResponse.ok) {
            throw new Error(`发送消息失败: ${messageResponse.status}`);
        }
        console.log('%c [ messageResponse ]-116', 'font-size:13px; background:pink; color:#bf2c9f;', messageResponse)
        if (isStream){
            return messageResponse
        }else {
            const messageData: ChatMessageResponse = await messageResponse.json();
            return messageData;
        }

    } catch (error) {
        console.error('调用 API 失败:', error);
        throw error;
    }
}
export default {
    callApiWithApiKey
}