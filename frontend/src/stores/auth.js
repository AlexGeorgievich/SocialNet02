import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../composables/useApi'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || '')

  const isLoggedIn = computed(() => !!token.value)

  async function register(data) {
    const res = await api.post('/auth/register', data)
    token.value = res.data.access_token
    user.value = res.data.user
    localStorage.setItem('token', token.value)
  }

  async function login(data) {
    const res = await api.post('/auth/login', data)
    token.value = res.data.access_token
    user.value = res.data.user
    localStorage.setItem('token', token.value)
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
    localStorage.removeItem('token')
  }

  return { user, token, isLoggedIn, register, login, fetchMe, logout }
})
