import { defineStore } from 'pinia'

export interface ModelControlDeskTypes {
  tepInstructionsModalVisible: boolean

}

const useModelControlDeskStore = defineStore({
  id: 'modelControlDesk',
  state: (): ModelControlDeskTypes => ({
    tepInstructionsModalVisible: false,
  }),
  actions: {
    toggleModalVisible(flag: boolean) {
      this.tepInstructionsModalVisible = flag
    },

  }
})

export default useModelControlDeskStore
