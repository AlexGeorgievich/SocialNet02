import { onMounted, ref, watch } from 'vue'
import { usePostsStore } from '../stores/posts'
import { useFavoritesStore } from '../stores/favorites'

export function useDesignFeed() {
  const postsStore = usePostsStore()
  const favoritesStore = useFavoritesStore()
  const activeCategory = ref('')

  async function loadPosts() {
    await postsStore.fetchPosts({ category: activeCategory.value })
  }

  async function toggleFavorite(postId) {
    if (favoritesStore.isFavorited(postId, 'post')) {
      await favoritesStore.removeFavorite(favoritesStore.getFavId(postId, 'post'))
    } else {
      await favoritesStore.addFavorite(postId, 'post')
    }
  }

  watch(activeCategory, loadPosts)
  onMounted(async () => {
    await Promise.all([loadPosts(), favoritesStore.fetchFavorites()])
  })

  return { postsStore, favoritesStore, activeCategory, toggleFavorite }
}
