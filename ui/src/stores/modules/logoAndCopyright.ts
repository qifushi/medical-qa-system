import { defineStore } from 'pinia'

export interface showLogoAndCopyrightTypes {
  isShowLogoAndCopyright: boolean
}

const isShowLogoAndCopyright = defineStore({
  id: 'logoAndCopyright',
  state: (): showLogoAndCopyrightTypes => ({
    // 显示/隐藏 login、首页（应用、知识库）的logo和copyright
    isShowLogoAndCopyright: true
  })
})

export default isShowLogoAndCopyright
