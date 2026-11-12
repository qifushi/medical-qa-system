import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import useApplicationStore from './modules/application'
import useCommonStore from './modules/common'
import useDatasetStore from './modules/dataset'
import useDigitalVideoStore from './modules/digitalVideo'
import useDocumentStore from './modules/document'
import useLogStore from './modules/log'
import useShowLogoAndCopyrightStore from './modules/logoAndCopyright'
import useModelStore from './modules/model'
import useParagraphStore from './modules/paragraph'
import useProblemStore from './modules/problem'
import useUserStore from './modules/user'
import useModelControlDeskStore from './modules/modelControlDesk'
import useEvaModelSelectedStore from './modules/evaModelSelectedStore'
const store = createPinia()
store.use(piniaPluginPersistedstate)
export { store }

const useStore = () => ({
  common: useCommonStore(),
  user: useUserStore(),
  dataset: useDatasetStore(),
  paragraph: useParagraphStore(),
  model: useModelStore(),
  application: useApplicationStore(),
  document: useDocumentStore(),
  problem: useProblemStore(),
  log: useLogStore(),
  logoAndCopyright: useShowLogoAndCopyrightStore(),
  digitalVideo: useDigitalVideoStore(),
  modelControlDesk: useModelControlDeskStore(),
  evaModelSelected: useEvaModelSelectedStore()
})

export default useStore
