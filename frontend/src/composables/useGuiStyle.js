import { computed, ref } from 'vue'

const savedStyle = localStorage.getItem('sart_gui_style')
const guiStyle = ref(savedStyle === 'classic' ? 'classic' : 'gallery')
const isSwitchingGui = ref(false)
let switchTimer = null

function applyGuiStyle(animate = false) {
  const root = document.documentElement

  if (animate) {
    isSwitchingGui.value = true
    root.classList.add('gui-switching')
  }

  root.dataset.gui = guiStyle.value
  localStorage.setItem('sart_gui_style', guiStyle.value)

  if (animate) {
    clearTimeout(switchTimer)
    switchTimer = setTimeout(() => {
      root.classList.remove('gui-switching')
      isSwitchingGui.value = false
    }, 80)
  }
}

export function useGuiStyle() {
  const isGallery = computed(() => guiStyle.value === 'gallery')

  function setGuiStyle(style) {
    const nextStyle = style === 'classic' ? 'classic' : 'gallery'
    if (nextStyle === guiStyle.value || isSwitchingGui.value) return
    guiStyle.value = nextStyle
    applyGuiStyle(true)
  }

  function toggleGuiStyle() {
    setGuiStyle(isGallery.value ? 'classic' : 'gallery')
  }

  applyGuiStyle()

  return { guiStyle, isGallery, isSwitchingGui, setGuiStyle, toggleGuiStyle }
}
