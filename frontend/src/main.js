import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/styles/main.css'
import { useTheme } from './composables/useTheme'

useTheme().applyTheme()

const app = createApp(App)
app.config.errorHandler = (error, instance, info) => {
  console.error('Ошибка Vue:', error, info)
  if (window.location.pathname.startsWith('/ui/')) {
    window.location.replace('/?design_fallback=1')
  }
}
app.use(createPinia())
app.use(router)
app.mount('#app')
