import { defineStore } from 'pinia'
import {
  GetSmartPPT,
  AddSmartPPT,
  GetSmartPPTDetail,
  UpdateSmartPPT,
  DelSmartPPT
} from '@/api/smartPPT'
import { useSlidesStore } from './slides'
import { useOutLineStore } from './outLine'
interface SlideLog {
  id?: string,
  theme?: string,
  title?: string,
  lang?: string,
  style?: string,
  datasets?: string,
  files?: string,
  outline?: string,
  template_id?: string,
  ppt_json?: string,
  user_id?: string,
  user_name?: string,
  create_time?: string,
  update_time?: string,
  status?: string,
}

export interface PPTLogState {
  slideLog: SlideLog
}
export const usePPTLogStore = defineStore('pptLog', {
  state: (): PPTLogState => ({
    slideLog: {}
  }),
  actions: {
    restLog() {
      this.slideLog = {}
    },
    updateLog() {
      const { slides, viewportRatio, title, viewportSize, theme } = useSlidesStore()
      const { outline, description, lang, style, datasetIdList, selectedTemplate, pptThemText } = useOutLineStore()
      let ppt_json = {
        title: title,
        width: viewportSize,
        height: viewportSize * viewportRatio,
        theme: theme,
        slides: slides,
      }
      let params = Object.assign({}, this.slideLog, {
        title,
        theme: pptThemText,
        description,
        lang,
        style,
        datasets: datasetIdList,
        template_id: selectedTemplate,
        ppt_json,
        outline,
      })
      if (this.slideLog.id) {
        UpdateSmartPPT(this.slideLog.id, params).then(res => {
          this.slideLog = res.data
        })
      } else {
        AddSmartPPT(params).then(res => {
          this.slideLog = res.data
        })
      }

    },
  }
})