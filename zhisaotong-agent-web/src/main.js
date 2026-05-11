import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import { createPinia } from 'pinia'

const isEdge = /edg\//i.test(navigator.userAgent)
if (isEdge) {
   const originalReplaceState = history.replaceState
   history.replaceState = function (...args) {
      // 最小化/页面隐藏时，禁止执行 replaceState
      if (document.visibilityState === 'hidden') {
         return
      }
      return originalReplaceState.apply(this, args)
   }
}

const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
   app.component(key, component)
}

app.use(createPinia())
app.use(router)
app.use(ElementPlus)
app.mount('#app')