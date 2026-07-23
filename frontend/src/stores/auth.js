import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../composables/useApi'
import { tokenStorageKey } from '../composables/useAppMode'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const legacyToken = localStorage.getItem('token') || ''
  const token = ref(localStorage.getItem(tokenStorageKey()) || legacyToken)
  if (legacyToken && !localStorage.getItem(tokenStorageKey())) {
    localStorage.setItem(tokenStorageKey(), legacyToken)
    localStorage.removeItem('token')
  }

  const isLoggedIn = computed(() => !!token.value)

  async function register(data) {
    const res = await api.post('/auth/register', data)
    token.value = res.data.access_token
    user.value = res.data.user
    localStorage.setItem(tokenStorageKey(), token.value)
  }

  async function login(data) {
    const res = await api.post('/auth/login', data)
    token.value = res.data.access_token
    user.value = res.data.user
    localStorage.setItem(tokenStorageKey(), token.value)
  }

  async function fetchMe() {
    if (!token.value) return
    try {
      const res = await api.get('/auth/me')
      user.value = res.data
    } catch {
      logout()
    }
  }

  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem(tokenStorageKey())
  }

  return { user, token, isLoggedIn, register, login, fetchMe, logout }
})
