import { ref } from 'vue'
import api from './useApi'

const allowedDesigns = ['classic', 'gallery', 'neo', 'canvas']
const storedDesign = localStorage.getItem('sart_design')
const designPreference = ref(allowedDesigns.includes(storedDesign) ? storedDesign : 'classic')

export function useDesignPreference() {
  function saveDesign(design) {
    const safeDesign = allowedDesigns.includes(design) ? design : 'classic'
    designPreference.value = safeDesign
    localStorage.setItem('sart_design', safeDesign)
    api.put('/users/me', { ui_style: safeDesign }).catch(() => {
      // Local preference remains available if the profile request is offline.
    })
  }

  function syncDesign(design) {
    if (!allowedDesigns.includes(design)) return
    designPreference.value = design
    localStorage.setItem('sart_design', design)
  }

  return { designPreference, saveDesign, syncDesign, allowedDesigns }
}
