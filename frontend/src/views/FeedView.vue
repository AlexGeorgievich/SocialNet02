<template>
  <div class="feed-page">
    <div class="feed-heading">
      <div>
        <span class="feed-kicker">Открытая коллекция</span>
        <h1 class="page-title">Лента</h1>
      </div>
      <router-link to="/profile" class="btn btn-primary add-art-button">＋ Добавить своё</router-link>
    </div>

    <div class="filters glass-card">
      <button
        v-for="cat in categories"
        :key="cat.value"
        class="filter-btn"
        :class="{ active: activeCategory === cat.value }"
        @click="setCategory(cat.value)"
      >
        {{ cat.label }}
      </button>
    </div>

    <div v-if="postsStore.loading" class="loading">
      <div class="spinner"></div>
    </div>

    <div v-else-if="postsStore.posts.length === 0" class="empty-state">
      <h3>Пока нет публикаций</h3>
      <p>Будьте первым, кто поделится своей работой!</p>
    </div>

    <div v-else class="grid grid-3">
      <PostCard
        v-for="post in postsStore.posts"
        :key="post.id"
        :post="post"
        :favorited="favoritesStore.isFavorited(post.id, 'post')"
        @favorite="handleFavorite"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { usePostsStore } from '../stores/posts'
import { useFavoritesStore } from '../stores/favorites'
import PostCard from '../components/PostCard.vue'
import { POST_CATEGORIES } from '../constants/categories'

const postsStore = usePostsStore()
const favoritesStore = useFavoritesStore()

const activeCategory = ref('')

const categories = [
  { label: 'Все', value: '' },
  ...POST_CATEGORIES,
]

function setCategory(cat) {
  activeCategory.value = cat
}

watch(activeCategory, () => {
  postsStore.fetchPosts({ category: activeCategory.value })
})

onMounted(() => {
  postsStore.fetchPosts()
  favoritesStore.fetchFavorites()
})

function handleFavorite(postId) {
  if (favoritesStore.isFavorited(postId, 'post')) {
    favoritesStore.removeFavorite(favoritesStore.getFavId(postId, 'post'))
  } else {
    favoritesStore.addFavorite(postId, 'post')
  }
}
</script>

<style scoped>
.feed-heading {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 20px;
}

.feed-kicker {
  display: none;
  margin-bottom: 8px;
  color: var(--text-muted);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: .16em;
  text-transform: uppercase;
}

.add-art-button { margin-bottom: 24px; }

.filters {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  padding: 12px 16px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 8px 16px;
  border: 1px solid var(--glass-border);
  border-radius: 20px;
  background: transparent;
  color: var(--text-secondary);
  font-family: inherit;
  font-weight: 500;
  font-size: 13px;
  cursor: pointer;
  transition: var(--transition);
}

.filter-btn:hover {
  color: var(--text-primary);
  border-color: var(--accent-purple);
}

.filter-btn.active {
  background: var(--gradient-main);
  color: white;
  border-color: transparent;
}

:global(:root[data-gui='classic']) .feed-heading .add-art-button {
  display: none;
}

:global(:root[data-gui='gallery']) .feed-kicker {
  display: block;
}

@media (max-width: 600px) {
  .feed-heading { align-items: flex-start; }
  .add-art-button { padding: 9px 12px; }
}
</style>
