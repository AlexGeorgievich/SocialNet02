import { computed, ref } from 'vue'

const savedStyle = localStorage.getItem('sart_gui_style')
const guiStyle = ref(savedStyle === 'classic' ? 'classic' : 'gallery')

function applyGuiStyle() {
  document.documentElement.dataset.gui = guiStyle.value
  localStorage.setItem('sart_gui_style', guiStyle.value)
}

export function useGuiStyle() {
  const isGallery = computed(() => guiStyle.value === 'gallery')

  function setGuiStyle(style) {
    guiStyle.value = style === 'classic' ? 'classic' : 'gallery'
    applyGuiStyle()
  }

  function toggleGuiStyle() {
    setGuiStyle(isGallery.value ? 'classic' : 'gallery')
  }

  applyGuiStyle()

  return { guiStyle, isGallery, setGuiStyle, toggleGuiStyle }
}
