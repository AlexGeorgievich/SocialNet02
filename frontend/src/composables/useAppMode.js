import { ref } from 'vue'

const storedMode = localStorage.getItem('sart_mode')
const appMode = ref(storedMode === 'work' ? 'work' : 'demo')

export function tokenStorageKey(mode = appMode.value) {
  return `token_${mode}`
}

export function setAppMode(mode, reload = true) {
  if (!['demo', 'work'].includes(mode) || mode === appMode.value) return
  appMode.value = mode
  localStorage.setItem('sart_mode', mode)
  if (reload) window.location.href = '/login'
}

export function useAppMode() {
  return { appMode, setAppMode }
}
