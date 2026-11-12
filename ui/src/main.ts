import { createApp } from 'vue'
import '@/styles/index.scss'
import ElementPlus from 'element-plus'
import * as ElementPlusIcons from '@element-plus/icons-vue'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import { store } from '@/stores'
import theme from '@/theme'
import directives from '@/directives'
import App from './App.vue'
import router from '@/router'
import Components from '@/components'
import i18n from './locales'
import { config } from 'md-editor-v3'

import screenfull from 'screenfull'

import katex from 'katex'
import 'katex/dist/katex.min.css'

import Cropper from 'cropperjs'
import 'cropperjs/dist/cropper.css'

import mermaid from 'mermaid'

import highlight from 'highlight.js'
import 'highlight.js/styles/atom-one-dark.css'

// ppt-app导入
import '@icon-park/vue-next/styles/index.css'
import 'prosemirror-view/style/prosemirror.css'
import 'animate.css'
import Icon from '@/views/ppt-app/plugins/icon'
import Directive from '@/views/ppt-app/plugins/directive'
config({
  editorExtensions: {
    highlight: {
      instance: highlight
    },
    screenfull: {
      instance: screenfull
    },
    katex: {
      instance: katex
    },
    cropper: {
      instance: Cropper
    },
    mermaid: {
      instance: mermaid
    }
  }
})

const app = createApp(App)
app.use(store)
app.use(directives)

for (const [key, component] of Object.entries(ElementPlusIcons)) {
  app.component(key, component)
}
app.use(ElementPlus, {
  locale: zhCn
})

app.use(theme)

app.use(router)
app.use(i18n)
app.use(Components)
app.use(Icon)
app.use(Directive)
app.mount('#app')
export { app }
