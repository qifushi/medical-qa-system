import { type Dict } from '@/api/type/common'
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
  constructor(chat: chatType, ms?: number, loading?: Ref<boolean>,dhIframe?: any, commandId?: string) {
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
  }
  write() {
    this.chat.is_stop = false
    this.is_stop = false
    if (this.loading) {
      this.loading.value = true
    }
    let isFirst = true
    // this.id = setInterval(() => {
    //   // 处理思考内容
    //   if (this.chat?.think_buffer && this.chat.think_buffer.length > 0) {
    //     if (this.chat.think_text === undefined) this.chat.think_text = ''
    //     const text = this.chat.think_buffer.shift()
    //     this.chat.think_text += text
    //         // 发送到数字人
    //         if(this.dhIframe) {
    //           this.dhIframe.sendMessage({
    //             action: 'TEXT_STREAM_RENDER',
    //             body: JSON.stringify({
    //               first: isFirst,
    //               last: false,
    //               text: text
    //             }),
    //             requestId: this.commandId
    //           })
    //           isFirst = false
    //         }
    //   } else {
    //     // 思考内容显示完毕，处理普通回答
    //     if (this.chat.buffer.length > 20) {
    //       const text = this.chat.buffer.splice(0, this.chat.buffer.length - 20).join('')
    //       this.chat.answer_text += text
    //         // 发送到数字人
    //         if(this.dhIframe) {
    //           this.dhIframe.sendMessage({
    //             action: 'TEXT_STREAM_RENDER', 
    //             body: JSON.stringify({
    //               first: isFirst,
    //               last: false,
    //               text: text
    //             }),
    //             requestId: this.commandId
    //           })
    //           isFirst = false
    //         }
    //     } else if (this.is_close && this.chat.buffer.length === 0) {

    //       // 只有当思考内容和普通回答都完全显示完才结束
    //      const text = this.chat.buffer.splice(0).join('')
    //       this.chat.answer_text += text
          
    //       // 发送最后一条消息到数字人
    //       if(this.dhIframe && text) {
    //         this.dhIframe.sendMessage({
    //           action: 'TEXT_STREAM_RENDER',
    //           body: JSON.stringify({
    //             first: isFirst,
    //             last: true,
    //             text: text
    //           }),
    //           requestId: this.commandId
    //         })
    //       }
          
    //       this.chat.write_ed = true
    //       this.write_ed = true
    //       if (this.loading) {
    //         this.loading.value = false
    //       }
    //       if (this.id) {
    //         clearInterval(this.id)
    //       }
    //     } else {
    //       const text = this.chat.buffer.shift()
    //       if (text !== undefined) {
    //         this.chat.answer_text += text
    //         // 发送到数字人
    //         if(this.dhIframe) {
    //           this.dhIframe.sendMessage({
    //             action: 'TEXT_STREAM_RENDER',
    //             body: JSON.stringify({
    //               first: isFirst,
    //               last: false,
    //               text: text
    //             }),
    //             requestId: this.commandId
    //           })
    //           isFirst = false
    //         }
    //       }
    //     }
    //   }
    // }, this.ms)
    this.id = setInterval(() => {
      // 处理思考内容
      if (this.chat?.think_buffer && this.chat.think_buffer.length > 0) {
        if (this.chat.think_text === undefined) this.chat.think_text = ''
        
        if (this.chat.think_buffer.length > 20) {
          // 思考内容>20时批量处理
          const text = this.chat.think_buffer.splice(0, 20).join('')
          this.chat.think_text += text
          // 发送到数字人
          if(this.dhIframe) {
            this.dhIframe.sendMessage({
              action: 'TEXT_STREAM_RENDER',
              body: JSON.stringify({
                first: isFirst,
                last: false,
                text: text
              }),
              requestId: this.commandId
            })
            isFirst = false
          }
        } else {
          // 少量内容逐字显示
          const text = this.chat.think_buffer.shift()
          if (text !== undefined) {
            this.chat.think_text += text
            // 发送到数字人
            if(this.dhIframe) {
              this.dhIframe.sendMessage({
                action: 'TEXT_STREAM_RENDER',
                body: JSON.stringify({
                  first: isFirst,
                  last: false,
                  text: text
                }),
                requestId: this.commandId
              })
              isFirst = false
            }
          }
        }
      } else {
        // 思考内容显示完毕，处理普通回答
        // if (this.chat.buffer.length > 20) {
        //   // 普通回答>20时批量处理
        //   const text = this.chat.buffer.splice(0, 20).join('')
        //   this.chat.answer_text += text
        //   // 发送到数字人
        //   if(this.dhIframe) {
        //     this.dhIframe.sendMessage({
        //       action: 'TEXT_STREAM_RENDER',
        //       body: JSON.stringify({s
        //         first: isFirst,
        //         last: false,
        //         text: text
        //       }),
        //       requestId: this.commandId
        //     })
        //     isFirst = false
        //   }
        // } else
         if (this.is_close && this.chat.buffer.length === 0) {
          // 最后一批数据处理
          const text = this.chat.buffer.splice(0).join('')
          this.chat.answer_text += text
          console.log('最后一条');
          
          // 发送最后一条消息到数字人
          if(this.dhIframe && text) {
            this.dhIframe.sendMessage({
              action: 'TEXT_STREAM_RENDER',
              body: JSON.stringify({
                first: isFirst,
                last: true,
                text: text
              }),
              requestId: this.commandId
            })
          }
          this.chat.write_ed = true
          this.write_ed = true
          if (this.loading) {
            this.loading.value = false
          }
          if (this.id) {
            clearInterval(this.id)
          }
        } else {
          // 少量内容逐字显示
          const text = this.chat.buffer.shift()
          if (text !== undefined) {
            this.chat.answer_text += text
            // 发送到数字人
            if(this.dhIframe) {
              this.dhIframe.sendMessage({
                action: 'TEXT_STREAM_RENDER',
                body: JSON.stringify({
                  first: isFirst,
                  last: false,
                  text: text
                }),
                requestId: this.commandId
              })
              isFirst = false
            }
          }
        }
      }
    }, this.ms)
  }
  stop() {
    clearInterval(this.id)
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

  static addChatRecord(chat: chatType, ms: number, loading?: Ref<boolean>,dhIframe?: any,
    commandId?: string) {
    this.chatMessageContainer[chat.id] = new ChatRecordManage(chat, ms, loading,dhIframe, commandId)
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
