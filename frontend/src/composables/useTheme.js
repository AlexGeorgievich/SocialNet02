import { computed, ref } from 'vue'

const theme = ref(localStorage.getItem('theme') || 'dark')

function applyTheme() {
  document.documentElement.dataset.theme = theme.value
  localStorage.setItem('theme', theme.value)
}

export function useTheme() {
  const isDark = computed(() => theme.value === 'dark')

  function toggleTheme() {
    theme.value = isDark.value ? 'light' : 'dark'
    applyTheme()
  }

  return { theme, isDark, applyTheme, toggleTheme }
}
