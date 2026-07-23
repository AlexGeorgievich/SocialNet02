<template>
  <div class="favorites-page">
    <h1 class="page-title">Избранное</h1>

    <div v-if="favoritesStore.favorites.length === 0" class="empty-state">
      <h3>Нет избранного</h3>
      <p>Добавляйте промпты и работы в избранное, чтобы не потерять!</p>
    </div>

    <div v-else class="grid grid-3">
      <template v-for="fav in favoritesStore.favorites" :key="fav.id">
        <PostCard v-if="fav.item_type === 'post' && fav.post" :post="fav.post" :favorited="true" @favorite="handleRemove(fav.id)" />
        <PromptCard v-else-if="fav.item_type === 'prompt' && fav.prompt" :prompt="fav.prompt" :favorited="true" @favorite="handleRemove(fav.id)" />
      </template>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useFavoritesStore } from '../stores/favorites'
import PostCard from '../components/PostCard.vue'
import PromptCard from '../components/PromptCard.vue'

const favoritesStore = useFavoritesStore()

onMounted(() => {
  favoritesStore.fetchFavorites()
})

function handleRemove(favId) {
  favoritesStore.removeFavorite(favId)
}
</script>
