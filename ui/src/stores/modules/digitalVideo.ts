/**
 * 数字人视频模块
 * xlDigital.vue输入框输入关键词，点击搜索，根据关键词匹配视频资源
 * application-digital-local.ts匹配数字人最后一段关闭视频
 */
import { defineStore } from 'pinia'

export interface VideoTriggerConfig {
  keywords: string[] // 触发关键词列表
  videoSrc?: string // 视频资源路径
}

export interface DigitalVideoStateTypes {
  isVideoPlaying: boolean // 是否正在播放视频
  currentVideoSrc: string | null // 当前视频源
  triggerConfigs: VideoTriggerConfig[] // 触发配置列表
  shouldPlayOnSubtitle: boolean // 是否应该在收到SUBTITLE时播放视频
}

const useDigitalVideoStore = defineStore({
  id: 'digitalVideo',
  state: (): DigitalVideoStateTypes => ({
    isVideoPlaying: false,
    currentVideoSrc: null,
    triggerConfigs: [
      {
        keywords: ['介绍smartbrain'],
        videoSrc: '' // 默认使用组件中的视频源
      }
    ],
    shouldPlayOnSubtitle: false // 初始为false
  }),
  actions: {
    // 添加新的触发配置
    addTriggerConfig(config: VideoTriggerConfig) {
      this.triggerConfigs.push(config)
    },

    // 检查输入是否触发视频播放条件
    checkInputTrigger(inputValue: string) {
      console.log('检查输入触发:', inputValue)
      for (const config of this.triggerConfigs) {
        // 检查是否所有关键词都包含在输入中
        const allKeywordsIncluded = config.keywords.every(
          (keyword) => {
            const normalizedInput = inputValue.toLowerCase().replace(/\s+/g, '')
            const normalizedKeyword = keyword.toLowerCase().replace(/\s+/g, '')
            return normalizedInput.includes(normalizedKeyword);
          }
        )

        if (allKeywordsIncluded) {
          console.log('触发视频播放条件满足')
          // 设置标志，在下一个SUBTITLE状态时播放视频
          this.shouldPlayOnSubtitle = true
          this.currentVideoSrc = config.videoSrc || null
          return true
        }
      }
      return false
    },

    // 播放视频
    playVideo() {
      console.log('开始播放视频')
      this.isVideoPlaying = true
      this.shouldPlayOnSubtitle = false // 重置标志
    },

    // 处理数字人状态
    handleDigitalHumanStatus(status: string, data: any, islastText: boolean) {
      console.log('处理数字人状态:', status, data, islastText)

      // 如果是SUBTITLE状态
      if (status === 'SUBTITLE') {
        // 如果设置了应该在SUBTITLE时播放视频的标志，则开始播放
        if (this.shouldPlayOnSubtitle && !this.isVideoPlaying) {
          console.log('收到SUBTITLE，开始播放视频')
          this.playVideo()
        }
      }

      // 如果是RENDER_FINISH状态且是最后一段，停止视频
      if (status === 'RENDER_FINISH' && islastText) {
        console.log('最后一段文本朗读完毕，停止视频')
        this.stopVideo()
      }
    },

    // 停止视频
    stopVideo() {
      console.log('停止播放视频')
      this.isVideoPlaying = false
      this.shouldPlayOnSubtitle = false // 重置标志
    }
  }
})

export default useDigitalVideoStore
