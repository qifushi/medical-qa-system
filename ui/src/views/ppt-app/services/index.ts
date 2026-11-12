import axios from './config'

// export const SERVER_URL = 'http://localhost:5000'
export const SERVER_URL = (import.meta.env.MODE === 'development') ? '/api' : 'https://server.pptist.cn'
export const ASSET_URL = 'https://asset.pptist.cn'
import slidesjson from "../mocks/pptTemplateData/slides.json"
import bingchuanwulan from "../mocks/pptTemplateData/bingchuanwulan.json"
import haiyanglan from "../mocks/pptTemplateData/haiyanglan.json"
import honglihong from "../mocks/pptTemplateData/honglihong.json"
import jianyuelan from "../mocks/pptTemplateData/jianyuelan.json"
import jihelan from "../mocks/pptTemplateData/jihelan.json"
import qingxinlv from "../mocks/pptTemplateData/qingxinlv.json"
import shangwucheng from "../mocks/pptTemplateData/shangwucheng.json"
import shensuilan from "../mocks/pptTemplateData/shensuilan.json"
import template_1 from "../mocks/pptTemplateData/template_1.json"
import template_2 from "../mocks/pptTemplateData/template_2.json"
import template_3 from "../mocks/pptTemplateData/template_3.json"
import template_4 from "../mocks/pptTemplateData/template_4.json"

interface AIPPTOutlinePayload {
  content: string
  language: string
  model: string
}

interface AIPPTPayload {
  content: string
  language: string
  style: string
  model: string
}

interface AIWritingPayload {
  content: string
  command: string
}

export default {
  getMockData(filename: string): Promise<any> {
    const obj = {
      slides: slidesjson,
      bingchuanwulan,
      haiyanglan,
      honglihong,
      jianyuelan,
      jihelan,
      qingxinlv,
      shangwucheng,
      shensuilan,
      template_1,
      template_2,
      template_3,
      template_4,
    } as const;
    const key = filename as keyof typeof obj;
    return Promise.resolve(obj[key]);
    // return  axios.get(`/pptTemplateData/${filename}.json`)
  },

  getFileData(filename: string): Promise<any> {
    return axios.get(`${ASSET_URL}/data/${filename}.json`)
  },

  AIPPT_Outline({
    content,
    language,
    model,
  }: AIPPTOutlinePayload): Promise<any> {
    return fetch(`${SERVER_URL}/tools/aippt_outline`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        content,
        language,
        model,
        stream: true,
      }),
    })
  },

  AIPPT({
    content,
    language,
    style,
    model,
  }: AIPPTPayload): Promise<any> {
    return fetch(`${SERVER_URL}/tools/aippt`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        content,
        language,
        model,
        style,
        stream: true,
      }),
    })
  },

  AI_Writing({
    content,
    command,
  }: AIWritingPayload): Promise<any> {
    return fetch(`${SERVER_URL}/tools/ai_writing`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        content,
        command,
        stream: true,
      }),
    })
  },
}