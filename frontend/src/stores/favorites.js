import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../composables/useApi'

export const useFavoritesStore = defineStore('favorites', () => {
  const favorites = ref([])

  async function fetchFavorites() {
    const res = await api.get('/favorites')
    favorites.value = res.data
  }

  async function addFavorite(itemId, itemType) {
    const res = await api.post('/favorites', { item_id: itemId, item_type: itemType })
    favorites.value.push({ id: res.data.id, item_id: itemId, item_type: itemType })
  }

  async function removeFavorite(favId) {
    await api.delete(`/favorites/${favId}`)
    favorites.value = favorites.value.filter((f) => f.id !== favId)
  }

  function isFavorited(itemId, itemType) {
    return favorites.value.some((f) => f.item_id === itemId && f.item_type === itemType)
  }

  function getFavId(itemId, itemType) {
    const f = favorites.value.find((f) => f.item_id === itemId && f.item_type === itemType)
    return f ? f.id : null
  }

  return { favorites, fetchFavorites, addFavorite, removeFavorite, isFavorited, getFavId }
})
