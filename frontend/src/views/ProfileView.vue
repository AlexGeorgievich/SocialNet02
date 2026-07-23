<template>
  <div class="profile-page">
    <div v-if="loading" class="loading"><div class="spinner"></div></div>

    <template v-else-if="profile">
      <div class="profile-header glass-card">
        <div class="profile-info">
          <img v-if="profile.avatar_url" :src="profile.avatar_url" class="avatar avatar-large" />
          <div v-else class="avatar avatar-large avatar-placeholder">{{ initials }}</div>
          <div class="profile-details">
            <h1>{{ profile.first_name }} {{ profile.last_name }}</h1>
            <p class="profile-status">{{ profile.status || 'Онлайн' }}</p>
            <p v-if="profile.description" class="profile-desc">{{ profile.description }}</p>
          </div>
        </div>
        <div v-if="isOwn" class="profile-actions">
          <router-link to="/settings" class="btn btn-secondary">Редактировать</router-link>
        </div>
        <div v-else class="profile-actions">
          <button
            class="btn"
            :class="isFriend ? 'btn-danger' : 'btn-primary'"
            @click="toggleFriend"
          >
            {{ friendButtonText }}
          </button>
        </div>
      </div>

      <div v-if="isOwn" class="create-panel glass-card">
        <div class="create-heading">
          <div><h2>Добавить своё</h2><p>Опубликуйте работу или сохраните промпт</p></div>
          <div class="profile-actions">
            <button class="btn btn-primary" @click="openPostForm()">+ Работа</button>
            <button class="btn btn-secondary" @click="openPromptForm()">+ Промпт</button>
          </div>
        </div>

        <form v-if="editorType === 'post'" class="editor-form" @submit.prevent="savePost">
          <h3>{{ editingId ? 'Редактировать работу' : 'Новая работа' }}</h3>
          <input v-model="postForm.title" class="input" placeholder="Название" required />
          <textarea v-model="postForm.description" class="input" placeholder="Короткое описание"></textarea>
          <select v-model="postForm.category" class="input">
            <option value="artwork">Иллюстрации</option><option value="waifu">Персонажи</option>
            <option value="maid">Городские сюжеты</option><option value="other">Прочее</option>
            <option value="nature">Природа и пейзажи</option>
            <option value="fantasy">Фэнтези</option>
            <option value="portrait">Портреты</option>
            <option value="architecture">Архитектура и интерьеры</option>
            <option value="abstract">Абстракция и эксперименты</option>
          </select>
          <input v-if="!editingId" ref="postFile" type="file" class="input" accept=".jpg,.jpeg,.png,.gif,.webp,.avif" required />
          <p class="form-hint">JPG, PNG, GIF, WebP или AVIF, до 10 МБ</p>
          <p v-if="editorMessage" :class="editorError ? 'form-error' : 'form-success'">{{ editorMessage }}</p>
          <div class="editor-actions"><button class="btn btn-primary" :disabled="editorSaving">{{ editorSaving ? 'Сохранение...' : 'Сохранить' }}</button><button type="button" class="btn btn-secondary" @click="closeEditor">Отмена</button></div>
        </form>

        <form v-if="editorType === 'prompt'" class="editor-form" @submit.prevent="savePrompt">
          <h3>{{ editingId ? 'Редактировать промпт' : 'Новый промпт' }}</h3>
          <input v-model="promptForm.title" class="input" placeholder="Название" required />
          <textarea v-model="promptForm.content" class="input" placeholder="Текст промпта" required></textarea>
          <input v-model="promptForm.model" class="input" placeholder="Модель" />
          <label class="public-check"><input v-model="promptForm.is_public" type="checkbox" /> Публичный промпт</label>
          <div class="editor-actions"><button class="btn btn-primary">Сохранить</button><button type="button" class="btn btn-secondary" @click="closeEditor">Отмена</button></div>
        </form>
      </div>

      <div class="profile-tabs glass-card">
        <button class="tab" :class="{ active: activeTab === 'posts' }" @click="activeTab = 'posts'">
          Мои работы ({{ userPosts.length }})
        </button>
        <button class="tab" :class="{ active: activeTab === 'prompts' }" @click="activeTab = 'prompts'">
          Мои промпты ({{ userPrompts.length }})
        </button>
        <button class="tab" :class="{ active: activeTab === 'favorites' }" @click="activeTab = 'favorites'">
          Избранное ({{ userFavorites.length }})
        </button>
      </div>

      <div v-if="activeTab === 'posts'">
        <div v-if="userPosts.length === 0" class="empty-state"><h3>Нет работ</h3></div>
        <div v-else class="grid grid-3">
          <PostCard
            v-for="post in userPosts"
            :key="post.id"
            :post="post"
            :show-delete="isOwn"
            :show-edit="isOwn"
            :favorited="favoritesStore.isFavorited(post.id, 'post')"
            @delete="handleDeletePost"
            @edit="openPostForm"
          />
        </div>
      </div>

      <div v-if="activeTab === 'prompts'">
        <div v-if="userPrompts.length === 0" class="empty-state"><h3>Нет промптов</h3></div>
        <div v-else class="grid grid-2">
          <PromptCard
            v-for="prompt in userPrompts"
            :key="prompt.id"
            :prompt="prompt"
            :favorited="favoritesStore.isFavorited(prompt.id, 'prompt')"
            :show-edit="isOwn"
            :show-delete="isOwn"
            @copy="handleCopy"
            @favorite="(id) => toggleFav(id, 'prompt')"
            @edit="openPromptForm"
            @delete="handleDeletePrompt"
          />
        </div>
      </div>

      <div v-if="activeTab === 'favorites'">
        <div v-if="userFavorites.length === 0" class="empty-state"><h3>Нет избранного</h3></div>
        <div v-else class="grid grid-3">
          <template v-for="fav in userFavorites" :key="fav.id">
            <PostCard
              v-if="fav.item_type === 'post' && fav.post"
              :post="fav.post"
              :favorited="true"
              @favorite="(id) => toggleFav(id, 'post')"
            />
            <PromptCard
              v-else-if="fav.item_type === 'prompt' && fav.prompt"
              :prompt="fav.prompt"
              :favorited="true"
              @copy="handleCopy"
              @favorite="(id) => toggleFav(id, 'prompt')"
            />
          </template>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { usePostsStore } from '../stores/posts'
import { usePromptsStore } from '../stores/prompts'
import { useFavoritesStore } from '../stores/favorites'
import { useFriendsStore } from '../stores/friends'
import api from '../composables/useApi'
import PostCard from '../components/PostCard.vue'
import PromptCard from '../components/PromptCard.vue'

const route = useRoute()
const auth = useAuthStore()
const postsStore = usePostsStore()
const promptsStore = usePromptsStore()
const favoritesStore = useFavoritesStore()
const friendsStore = useFriendsStore()

const profile = ref(null)
const loading = ref(true)
const activeTab = ref('posts')
const friendship = ref({ status: 'none' })
const editorType = ref('')
const editingId = ref(null)
const postFile = ref(null)
const postForm = ref({ title: '', description: '', category: 'artwork' })
const promptForm = ref({ title: '', content: '', model: '', tags: '[]', is_public: true })
const editorSaving = ref(false)
const editorMessage = ref('')
const editorError = ref(false)

const userId = computed(() => {
  const id = route.params.id
  return id ? parseInt(id) : auth.user?.id
})

const isOwn = computed(() => userId.value === auth.user?.id)

const userPosts = computed(() => postsStore.posts.filter((p) => p.user_id === userId.value))
const userPrompts = computed(() => promptsStore.prompts.filter((p) => p.user_id === userId.value))
const userFavorites = computed(() => favoritesStore.favorites)

const isFriend = computed(() =>
  friendsStore.friends.some((f) => f.id === userId.value)
)
const friendButtonText = computed(() => {
  if (isFriend.value || friendship.value.status === 'accepted') return 'Удалить из друзей'
  if (friendship.value.status === 'pending' && friendship.value.direction === 'received') return 'Принять заявку'
  if (friendship.value.status === 'pending') return 'Запрос на добавление'
  return 'Добавить в друзья'
})

const initials = computed(() => {
  const f = profile.value?.first_name?.[0] || ''
  const l = profile.value?.last_name?.[0] || ''
  return (f + l).toUpperCase() || '?'
})

async function loadProfile() {
  loading.value = true
  try {
    const res = await api.get(`/users/${userId.value}`)
    profile.value = res.data
    await postsStore.fetchPosts({ user_id: userId.value })
    await promptsStore.fetchPrompts(userId.value)
    if (isOwn.value) await favoritesStore.fetchFavorites()
    await friendsStore.fetchFriends()
    if (!isOwn.value) friendship.value = await friendsStore.getFriendStatus(userId.value)
  } finally {
    loading.value = false
  }
}

async function toggleFriend() {
  if (isFriend.value || friendship.value.status === 'accepted') {
    await friendsStore.removeFriend(userId.value)
    friendship.value = { status: 'none' }
  } else if (friendship.value.status === 'pending' && friendship.value.direction === 'received') {
    await friendsStore.acceptFriend(userId.value)
    friendship.value = { status: 'accepted' }
  } else if (friendship.value.status === 'none') {
    await friendsStore.addFriend(userId.value)
    friendship.value = { status: 'pending', direction: 'sent' }
  }
}

async function handleCopy(id) {
  await promptsStore.copyPrompt(id)
  alert('Промпт скопирован!')
}

function toggleFav(id, type) {
  if (favoritesStore.isFavorited(id, type)) {
    favoritesStore.removeFavorite(favoritesStore.getFavId(id, type))
  } else {
    favoritesStore.addFavorite(id, type)
  }
}

async function handleDeletePost(id) {
  if (confirm('Удалить пост?')) await postsStore.deletePost(id)
}

async function handleDeletePrompt(id) {
  if (confirm('Удалить промпт?')) await promptsStore.deletePrompt(id)
}

function openPostForm(post = null) {
  editorType.value = 'post'
  editingId.value = post?.id || null
  postForm.value = post
    ? { title: post.title, description: post.description, category: post.category }
    : { title: '', description: '', category: 'artwork' }
}

function openPromptForm(prompt = null) {
  editorType.value = 'prompt'
  editingId.value = prompt?.id || null
  promptForm.value = prompt
    ? { title: prompt.title, content: prompt.content, model: prompt.model, tags: prompt.tags, is_public: prompt.is_public }
    : { title: '', content: '', model: '', tags: '[]', is_public: true }
}

function closeEditor() {
  editorType.value = ''
  editingId.value = null
  editorMessage.value = ''
}

async function savePost() {
  editorSaving.value = true
  editorMessage.value = ''
  editorError.value = false
  try {
    if (editingId.value) {
      await postsStore.updatePost(editingId.value, postForm.value)
    } else {
      const file = postFile.value?.files?.[0]
      if (!file) throw new Error('Выберите изображение')
      const data = new FormData()
      Object.entries(postForm.value).forEach(([key, value]) => data.append(key, value))
      data.append('file', file)
      await postsStore.createPost(data)
    }
    activeTab.value = 'posts'
    editorMessage.value = 'Работа опубликована'
    setTimeout(closeEditor, 700)
  } catch (error) {
    editorError.value = true
    editorMessage.value = error.response?.data?.detail || error.message || 'Не удалось сохранить работу'
  } finally {
    editorSaving.value = false
  }
}

async function savePrompt() {
  if (editingId.value) await promptsStore.updatePrompt(editingId.value, promptForm.value)
  else await promptsStore.createPrompt(promptForm.value)
  activeTab.value = 'prompts'
  closeEditor()
}

watch(() => route.params.id, loadProfile)
onMounted(loadProfile)
</script>

<style scoped>
.profile-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.profile-info {
  display: flex;
  align-items: center;
  gap: 20px;
}

.avatar-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gradient-main);
  color: white;
  font-size: 28px;
  font-weight: 700;
  flex-shrink: 0;
}

.profile-details h1 {
  font-size: 24px;
  font-weight: 700;
}

.profile-status {
  color: #22c55e;
  font-size: 13px;
  margin-top: 2px;
}

.profile-desc {
  color: var(--text-secondary);
  font-size: 14px;
  margin-top: 6px;
}

.profile-actions {
  display: flex;
  gap: 8px;
}

.profile-tabs {
  display: flex;
  gap: 4px;
  margin-bottom: 24px;
  padding: 8px;
}

.create-panel { margin-bottom: 20px; }
.create-heading { display: flex; align-items: center; justify-content: space-between; gap: 16px; }
.create-heading h2 { font-size: 18px; }
.create-heading p { color: var(--text-secondary); font-size: 13px; margin-top: 4px; }
.editor-form { display: grid; gap: 12px; margin-top: 20px; padding-top: 20px; border-top: 1px solid var(--glass-border); }
.editor-form h3 { font-size: 16px; }
.editor-actions { display: flex; gap: 8px; }
.public-check { color: var(--text-secondary); font-size: 13px; display: flex; align-items: center; gap: 8px; }
.form-hint { color: var(--text-muted); font-size: 12px; }
.form-error { color: #ef4444; font-size: 13px; }
.form-success { color: #22c55e; font-size: 13px; }

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

@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  .profile-info {
    flex-direction: column;
  }
  .create-heading { align-items: flex-start; flex-direction: column; }
}
</style>
