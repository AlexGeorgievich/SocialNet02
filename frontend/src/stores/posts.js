import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../composables/useApi'

export const usePostsStore = defineStore('posts', () => {
  const posts = ref([])
  const loading = ref(false)

  async function fetchPosts(filters = {}) {
    loading.value = true
    try {
      const params = new URLSearchParams()
      if (filters.category) params.set('category', filters.category)
      if (filters.user_id) params.set('user_id', filters.user_id)
      const res = await api.get(`/posts?${params}`)
      posts.value = res.data
    } finally {
      loading.value = false
    }
  }

  async function createPost(formData) {
    const res = await api.post('/posts', formData)
    posts.value.unshift(res.data)
  }

  async function deletePost(id) {
    await api.delete(`/posts/${id}`)
    posts.value = posts.value.filter((p) => p.id !== id)
  }

  async function updatePost(id, data) {
    const res = await api.put(`/posts/${id}`, data)
    const index = posts.value.findIndex((post) => post.id === id)
    if (index !== -1) posts.value[index] = res.data
    return res.data
  }

  return { posts, loading, fetchPosts, createPost, updatePost, deletePost }
})
