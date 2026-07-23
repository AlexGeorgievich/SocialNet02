<template>
  <div class="post-card glass-card">
    <div class="post-header">
      <router-link :to="`/profile/${post.user_id}`" class="post-author">
        <img
          v-if="post.user_avatar_url"
          :src="post.user_avatar_url"
          class="avatar"
        />
        <div v-else class="avatar avatar-placeholder">{{ initials }}</div>
        <span>{{ post.user_first_name }} {{ post.user_last_name }}</span>
      </router-link>
      <span class="tag">{{ categoryLabel }}</span>
    </div>
    <div class="post-image-wrap">
      <img
        :src="post.image_url"
        class="post-image"
        :alt="post.title"
        title="Нажмите, чтобы увеличить"
        @click="openImage"
      />
    </div>
    <div class="post-body">
      <h3 class="post-title">{{ post.title }}</h3>
      <p v-if="post.description" class="post-desc">{{ post.description }}</p>
    </div>
    <div class="post-actions">
      <button class="btn-icon" :class="{ favorited }" :aria-label="favorited ? 'Убрать из избранного' : 'Добавить в избранное'" @click="$emit('favorite', post.id)">
        <svg width="20" height="20" viewBox="0 0 24 24" :fill="favorited ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2">
          <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
        </svg>
      </button>
      <button v-if="showEdit" class="btn btn-secondary btn-small" @click="$emit('edit', post)">
        Изменить
      </button>
      <button
        v-if="showDelete"
        class="btn-icon btn-danger-icon"
        @click="$emit('delete', post.id)"
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
        </svg>
      </button>
    </div>
  </div>

  <Teleport to="body">
    <div
      v-if="imageOpen"
      class="image-lightbox"
      role="dialog"
      aria-modal="true"
      :aria-label="`Увеличенное изображение: ${post.title}`"
      @click.self="closeImage"
    >
      <button class="lightbox-close" type="button" aria-label="Закрыть" @click="closeImage">×</button>
      <img
        :src="post.image_url"
        class="lightbox-image"
        :alt="post.title"
        title="Нажмите, чтобы свернуть"
        @click="closeImage"
      />
      <div class="lightbox-caption">{{ post.title }}</div>
    </div>
  </Teleport>
</template>

<script setup>
import { computed, onBeforeUnmount, ref } from 'vue'
import { categoryLabel as getCategoryLabel } from '../constants/categories'

const props = defineProps({
  post: Object,
  showDelete: Boolean,
  showEdit: Boolean,
  favorited: Boolean,
})

defineEmits(['favorite', 'delete', 'edit'])
const imageOpen = ref(false)

function openImage() {
  imageOpen.value = true
  document.body.style.overflow = 'hidden'
  window.addEventListener('keydown', handleLightboxKey)
}

function closeImage() {
  imageOpen.value = false
  document.body.style.overflow = ''
  window.removeEventListener('keydown', handleLightboxKey)
}

function handleLightboxKey(event) {
  if (event.key === 'Escape') closeImage()
}

onBeforeUnmount(closeImage)

const initials = computed(() => {
  const f = props.post.user_first_name?.[0] || ''
  const l = props.post.user_last_name?.[0] || ''
  return (f + l).toUpperCase() || '?'
})

const categoryLabel = computed(() => getCategoryLabel(props.post.category))
</script>

<style scoped>
.post-card {
  padding: 0;
  overflow: hidden;
  animation: slideIn 0.4s ease forwards;
}

@keyframes slideIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.post-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
}

.post-author {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: var(--text-primary);
  font-weight: 500;
  font-size: 14px;
}

.post-author:hover {
  color: var(--accent-purple);
}

.avatar-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gradient-main);
  color: white;
  font-size: 12px;
  font-weight: 600;
}

.post-image-wrap {
  width: 100%;
  aspect-ratio: 16/10;
  overflow: hidden;
  background: var(--glass);
}

.post-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
  cursor: zoom-in;
}

.post-card:hover .post-image {
  transform: scale(1.05);
}

.post-body {
  padding: 16px 20px;
}

.post-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
}

.post-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
}

.post-actions {
  display: flex;
  gap: 8px;
  padding: 0 20px 16px;
}

.btn-icon {
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  transition: var(--transition);
  display: flex;
  align-items: center;
}

.btn-icon:hover {
  color: var(--accent-pink);
  background: rgba(236, 72, 153, 0.1);
}

.btn-icon.favorited { color: var(--accent-pink); }

.btn-danger-icon:hover {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}

.image-lightbox {
  position: fixed;
  inset: 0;
  z-index: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 24px 64px;
  background: rgba(4, 2, 10, 0.94);
  backdrop-filter: blur(12px);
  cursor: zoom-out;
}

.lightbox-image {
  display: block;
  max-width: min(1400px, 96vw);
  max-height: calc(100vh - 110px);
  object-fit: contain;
  border-radius: 10px;
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.6);
  cursor: zoom-out;
}

.lightbox-close {
  position: fixed;
  top: 18px;
  right: 24px;
  width: 42px;
  height: 42px;
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.35);
  color: white;
  font-size: 30px;
  line-height: 1;
  cursor: pointer;
}

.lightbox-caption {
  position: fixed;
  bottom: 20px;
  left: 24px;
  right: 24px;
  color: white;
  text-align: center;
  font-size: 14px;
}
</style>
