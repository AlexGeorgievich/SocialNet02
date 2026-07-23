import axios from 'axios'
import { tokenStorageKey, useAppMode } from './useAppMode'

const api = axios.create({ baseURL: '/api' })
const { appMode } = useAppMode()

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(tokenStorageKey())
  if (token) config.headers.Authorization = `Bearer ${token}`
  config.headers['X-S-Art-Mode'] = appMode.value
  return config
})

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem(tokenStorageKey())
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

export default api
