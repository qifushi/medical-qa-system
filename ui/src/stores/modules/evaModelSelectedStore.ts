
import { defineStore } from 'pinia'

const useEvaModelSelectedStore = defineStore('evaModelSelectedStore', {
    state: () => ({
        selectedModels: [] as any[]
    }),
    actions: {
        setSelectedModels(models: any[]) {
            this.selectedModels = models
        },
        clearSelectedModels() {
            this.selectedModels = []
        }
    },
    persist: true // 开启持久化
})
export default useEvaModelSelectedStore