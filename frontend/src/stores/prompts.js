import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../composables/useApi'

export const usePromptsStore = defineStore('prompts', () => {
  const prompts = ref([])
  const loading = ref(false)

  async function fetchPrompts(userId = null) {
    loading.value = true
    try {
      const params = userId ? `?user_id=${userId}` : ''
      const res = await api.get(`/prompts${params}`)
      prompts.value = res.data
    } finally {
      loading.value = false
    }
  }

  async function createPrompt(data) {
    const res = await api.post('/prompts', data)
    prompts.value.unshift(res.data)
  }

  async function copyPrompt(id) {
    const res = await api.post(`/prompts/${id}/copy`)
    return res.data
  }

  async function deletePrompt(id) {
    await api.delete(`/prompts/${id}`)
    prompts.value = prompts.value.filter((p) => p.id !== id)
  }

  async function updatePrompt(id, data) {
    const res = await api.put(`/prompts/${id}`, data)
    const index = prompts.value.findIndex((prompt) => prompt.id === id)
    if (index !== -1) prompts.value[index] = res.data
    return res.data
  }

  return { prompts, loading, fetchPrompts, createPrompt, copyPrompt, updatePrompt, deletePrompt }
})
