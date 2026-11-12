import { defineStore } from 'pinia'

export const useOutLineStore = defineStore('outline', {
    state: () => ({
        outline: '',
        selectedTemplate: '',
        datasetIdList: [] as string[],
        lang: '',
        description: '',
        style: '',
        pptThemText: ''
    }),
    actions: {
        setOutline(outline: string) {
            this.outline = outline
        },
        setSelectedTemplate(template: string) {
            this.selectedTemplate = template
        },
        setDatasetIdList(datasetIdList: string[]) {
            this.datasetIdList = datasetIdList
        },
        setLang(lang: string) {
            this.lang = lang
        },
        setDescription(description: string) {
            this.description = description
        },
        setStyle(style: string) {
            this.style = style
        },
        setPPTThem(pptThemText: string) {
            this.pptThemText = pptThemText
        },

    }
})