import { type Dict } from '@/api/type/common'
import useStore from '@/stores'
import { type Ref } from 'vue'

interface ApplicationFormType {
  category?: string
  title?: string
  reasoning?: string
  name?: string
  desc?: string
  model_id?: string
  multiple_rounds_dialogue?: boolean
  prologue?: string
  dataset_id_list?: string[]
  dataset_setting?: any
  model_setting?: any
  problem_optimization?: boolean
  icon?: string | undefined
  type?: string
  work_flow?: any
  show_source?: boolean
}
interface chatType {
  id: string
  problem_text: string
  answer_text: string
  think_text?: string // 添加思考内容
  think_buffer?: Array<String> // 添加思考内容的buffer
  buffer: Array<String>
  /**
   * 是否写入结束
   */
  write_ed?: boolean
  /**
   * 是否暂停
   */
  is_stop?: boolean
  record_id: string
  vote_status: string
  status?: number
}
interface RenderOptions {
  token: string;
  text: string;
  tts: {
    per: string;
    spd: number;
    pit: number;
  };
  characterImage?: string;
  autoAnimoji?: boolean;
}
export class ChatRecordManage {
  id?: any
  ms: number
  chat: chatType
  is_close?: boolean
  write_ed?: boolean
  is_stop?: boolean
  loading?: Ref<boolean>
  isThinking: boolean = false // 是否正在思考
  thinkBuffer: string[] = [] // 思考内容的buffer
  dhIframe: any
  commandId: string
  iframeToken: string

  // 新增：数字人朗读相关变量
  dhTextBuffer: string = '' // 数字人朗读缓冲区
  dhRenderTimerId: any = null // 数字人朗读定时器ID

  constructor(
    chat: chatType,
    ms?: number,
    loading?: Ref<boolean>,
    dhIframe?: any,
    commandId?: string,
    iframeToken?: string
  ) {
    this.ms = ms ? ms : 10
    this.chat = chat
    this.loading = loading
    this.is_stop = false
    this.is_close = false
    this.write_ed = false
    // 初始化思考相关字段
    this.chat.think_text = ''
    this.chat.think_buffer = []
    this.dhIframe = dhIframe
    this.commandId = commandId ? commandId : ''
    this.iframeToken = iframeToken ? iframeToken : ''
    console.log('构造函数中的Token:', this.iframeToken)

    // 如果有数字人iframe，启动数字人朗读定时器
    if (this.dhIframe) {
      this.startDigitalHumanRenderer()
    }
  }
  // 添加获取音色的方法
  private getVoiceByCharacter(characterImage: string | null): string {
    if (!characterImage) return '7011_moxingxiaoxiao_16k'
    
    switch (characterImage) {
      case 'AR_RENDER-Male':  // charis角色
        return '7011_vc0038_16k'
      case 'AR_RENDER-COCO':  // coco角色
        return '7011_moxingxiaoxiao_16k'
      default:
        return '7011_moxingxiaoxiao_16k'
    }
  }
  // 新增：启动数字人朗读定时器
  startDigitalHumanRenderer() {
    // 获取 Pinia store
    const { digitalVideo } = useStore()

    // 清除可能存在的旧定时器
    if (this.dhRenderTimerId) {
      clearInterval(this.dhRenderTimerId)
    }

    // 每秒执行一次，发送3-5个字给数字人
    this.dhRenderTimerId = setInterval(() => {
      if (this.dhTextBuffer.length > 0) {
        try {
          // 每次发送最多50个字符
          const charsToSend = Math.min(50, this.dhTextBuffer.length)
          const textToSend = this.dhTextBuffer.substring(0, charsToSend)
          this.dhTextBuffer = this.dhTextBuffer.substring(charsToSend)

          let islastText = false
          // 如果这是最后一批要发送的内容，保存它用于后续比对
          if (this.write_ed && this.chat.buffer.length === 0 && this.dhTextBuffer.length === 0) {
            console.log('保存最后一段内容用于比对:', textToSend)
            // digitalVideo.setLastBufferContent(textToSend)
            islastText = true
          }

          if (textToSend.length > 0) {
            console.log('发送内容到数字人:', textToSend)
            const characterImage = localStorage.getItem('characterImage')
            const renderOptions:RenderOptions = {
              token: this.iframeToken,
              text: textToSend,
              tts: {
                per: this.getVoiceByCharacter(characterImage),  // 根据角色获取对应音色,
                spd: 5,
                pit: 5
              }
            }
         
            if (characterImage) {
              renderOptions.characterImage = characterImage
              renderOptions.autoAnimoji = true
            }
            console.log('renderOptions', renderOptions)

            this.dhIframe.textRender(renderOptions, ({ status, data }: any) => {
              digitalVideo.handleDigitalHumanStatus(status, data, islastText)
            })
          }
        } catch (error) {
          console.error('数字人朗读出错:', error)
        }
      } else if (this.is_close && this.write_ed && this.dhTextBuffer.length === 0) {
        // 所有内容处理完毕，清除定时器
        clearInterval(this.dhRenderTimerId)
        this.dhRenderTimerId = null
      }
    }, 1000) // 1秒执行一次
  }

  write() {
    console.log('开始执行write方法')
    console.log('数字人Token值:', this.iframeToken)

    this.chat.is_stop = false
    this.is_stop = false
    if (this.loading) {
      this.loading.value = true
    }

    // 打字机效果定时器 - 使用this.ms的速度（默认10毫秒）
    this.id = setInterval(() => {
      try {
        // 处理思考内容
        if (this.chat?.think_buffer && this.chat.think_buffer.length > 0) {
          if (this.chat.think_text === undefined) this.chat.think_text = ''

          // 处理一批思考内容（打字机效果）
          const batchSize = Math.min(20, this.chat.think_buffer.length)
          const text = this.chat.think_buffer.splice(0, batchSize).join('')
          this.chat.think_text += text

          // 将内容添加到数字人缓冲区
          this.dhTextBuffer += text
        } else {
          // 思考内容显示完毕后处理普通回答
          if (this.is_close && this.chat.buffer.length === 0) {
            // 处理最后一批数据
            const text = this.chat.buffer.splice(0).join('')
            this.chat.answer_text += text

            // 将内容添加到数字人缓冲区
            this.dhTextBuffer += text

            console.log('回答完成')
            this.chat.write_ed = true
            this.write_ed = true
            if (this.loading) {
              this.loading.value = false
            }
            if (this.id) {
              clearInterval(this.id)
            }
          } else if (this.chat.buffer.length > 0) {
            // 处理一批普通回答（打字机效果）
            const batchSize = Math.min(20, this.chat.buffer.length)
            const text = this.chat.buffer.splice(0, batchSize).join('')
            this.chat.answer_text += text

            // 将内容添加到数字人缓冲区
            this.dhTextBuffer += text
          }
        }
      } catch (error) {
        console.error('打字机效果处理出错:', error)
      }
    }, this.ms) // 使用this.ms的速度（默认10毫秒）
  }

  stop() {
    clearInterval(this.id)
    if (this.dhRenderTimerId) {
      clearInterval(this.dhRenderTimerId)
      this.dhRenderTimerId = null
    }
    this.is_stop = true
    this.chat.is_stop = true
    if (this.loading) {
      this.loading.value = false
    }
  }

  close() {
    this.is_close = true
  }

  append(answer_text_block: string) {
    if (answer_text_block.includes('<think>')) {
      this.isThinking = true
      // 初始化思考buffer
      this.chat.think_buffer = []
      this.chat.think_text = ''
      // 移除开始标签
      answer_text_block = answer_text_block.replace('<think>', '')
    }

    if (this.isThinking) {
      this.thinkBuffer.push(answer_text_block)
      // 直接将当前文本块放入think_buffer进行显示
      if (this.chat.think_buffer) {
        // 如果包含结束标签，先移除它
        if (answer_text_block.includes('</think>')) {
          answer_text_block = answer_text_block.replace('</think>', '')
          this.isThinking = false
        }
        for (let index = 0; index < answer_text_block.length; index++) {
          this.chat.think_buffer.push(answer_text_block[index])
        }
      }
    } else {
      for (let index = 0; index < answer_text_block.length; index++) {
        this.chat.buffer.push(answer_text_block[index])
      }
    }
  }
}
export class ChatManagement {
  static chatMessageContainer: Dict<ChatRecordManage> = {}

  static addChatRecord(
    chat: chatType,
    ms: number,
    loading?: Ref<boolean>,
    dhIframe?: any,
    commandId?: string,
    iframeToken?: string
  ) {
    this.chatMessageContainer[chat.id] = new ChatRecordManage(
      chat,
      ms,
      loading,
      dhIframe,
      commandId,
      iframeToken
    )
  }
  static append(chatRecordId: string, content: string) {
    const chatRecord = this.chatMessageContainer[chatRecordId]
    if (chatRecord) {
      chatRecord.append(content)
    }
  }
  static updateStatus(chatRecordId: string, code: number) {
    const chatRecord = this.chatMessageContainer[chatRecordId]
    if (chatRecord) {
      chatRecord.chat.status = code
    }
  }
  /**
   * 持续从缓存区 写出数据
   * @param chatRecordId 对话记录id
   */
  static write(chatRecordId: string) {
    const chatRecord = this.chatMessageContainer[chatRecordId]
    if (chatRecord) {
      chatRecord.write()
    }
  }
  /**
   * 等待所有数据输出完毕后 才会关闭流
   * @param chatRecordId 对话记录id
   * @returns boolean
   */
  static close(chatRecordId: string) {
    const chatRecord = this.chatMessageContainer[chatRecordId]
    if (chatRecord) {
      chatRecord.close()
    }
  }
  /**
   * 停止输出 立即关闭定时任务输出
   * @param chatRecordId 对话记录id
   * @returns boolean
   */
  static stop(chatRecordId: string) {
    const chatRecord = this.chatMessageContainer[chatRecordId]
    if (chatRecord) {
      chatRecord.stop()
    }
  }
  /**
   * 判断是否输出完成
   * @param chatRecordId 对话记录id
   * @returns boolean
   */
  static isClose(chatRecordId: string) {
    const chatRecord = this.chatMessageContainer[chatRecordId]
    return chatRecord ? chatRecord.is_close && chatRecord.write_ed : false
  }
  /**
   * 判断是否停止输出
   * @param chatRecordId 对话记录id
   * @returns
   */
  static isStop(chatRecordId: string) {
    const chatRecord = this.chatMessageContainer[chatRecordId]
    return chatRecord ? chatRecord.is_stop : false
  }
  /**
   * 清除无用数据 也就是被close掉的和stop的数据
   */
  static clean() {
    for (const key in Object.keys(this.chatMessageContainer)) {
      if (this.chatMessageContainer[key].is_close) {
        delete this.chatMessageContainer[key]
      }
    }
  }
}

export type { ApplicationFormType, chatType }
