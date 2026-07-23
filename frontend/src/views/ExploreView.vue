<template>
  <div class="explore-page">
    <h1 class="page-title">Исследовать</h1>

    <div class="tabs glass-card">
      <button class="tab" :class="{ active: tab === 'posts' }" @click="tab = 'posts'">Работы</button>
      <button class="tab" :class="{ active: tab === 'prompts' }" @click="tab = 'prompts'">Промпты</button>
    </div>

    <div v-if="tab === 'posts'">
      <div v-if="postsStore.loading" class="loading"><div class="spinner"></div></div>
      <div v-else-if="postsStore.posts.length === 0" class="empty-state">
        <h3>Нет работ</h3>
      </div>
      <div v-else class="grid grid-3">
        <PostCard
          v-for="post in postsStore.posts"
          :key="post.id"
          :post="post"
          :favorited="favoritesStore.isFavorited(post.id, 'post')"
          @favorite="(id) => toggleFav(id, 'post')"
        />
      </div>
    </div>

    <div v-if="tab === 'prompts'">
      <div v-if="promptsStore.loading" class="loading"><div class="spinner"></div></div>
      <div v-else-if="promptsStore.prompts.length === 0" class="empty-state">
        <h3>Нет промптов</h3>
      </div>
      <div v-else class="grid grid-2">
        <PromptCard
          v-for="prompt in promptsStore.prompts"
          :key="prompt.id"
          :prompt="prompt"
          :favorited="favoritesStore.isFavorited(prompt.id, 'prompt')"
          @copy="handleCopy"
          @favorite="(id) => toggleFav(id, 'prompt')"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { usePostsStore } from '../stores/posts'
import { usePromptsStore } from '../stores/prompts'
import { useFavoritesStore } from '../stores/favorites'
import PostCard from '../components/PostCard.vue'
import PromptCard from '../components/PromptCard.vue'

const postsStore = usePostsStore()
const promptsStore = usePromptsStore()
const favoritesStore = useFavoritesStore()

const tab = ref('posts')

watch(tab, (val) => {
  if (val === 'posts') postsStore.fetchPosts()
  else promptsStore.fetchPrompts()
})

onMounted(() => {
  postsStore.fetchPosts()
  promptsStore.fetchPrompts()
  favoritesStore.fetchFavorites()
})

async function handleCopy(id) {
  await promptsStore.copyPrompt(id)
  alert('Промпт скопирован в ваш профиль!')
}

function toggleFav(id, type) {
  if (favoritesStore.isFavorited(id, type)) {
    favoritesStore.removeFavorite(favoritesStore.getFavId(id, type))
  } else {
    favoritesStore.addFavorite(id, type)
  }
}
</script>

<style scoped>
.tabs {
  display: flex;
  gap: 4px;
  margin-bottom: 24px;
  padding: 8px;
}

.tab {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--text-secondary);
  font-family: inherit;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: var(--transition);
}

.tab:hover {
  color: var(--text-primary);
  background: var(--glass);
}

.tab.active {
  background: var(--gradient-main);
  color: white;
}
</style>
