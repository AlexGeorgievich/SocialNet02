<template>
  <div class="prompt-card glass-card">
    <div class="prompt-header">
      <router-link :to="`/profile/${prompt.user_id}`" class="prompt-author">
        <img v-if="prompt.user_avatar_url" :src="prompt.user_avatar_url" class="avatar" />
        <div v-else class="avatar avatar-placeholder">{{ initials }}</div>
        <span>{{ prompt.user_first_name }} {{ prompt.user_last_name }}</span>
      </router-link>
      <span v-if="prompt.model" class="tag">{{ prompt.model }}</span>
    </div>
    <div class="prompt-body">
      <h3 class="prompt-title">{{ prompt.title }}</h3>
      <div class="prompt-content">
        <pre>{{ prompt.content }}</pre>
      </div>
    </div>
    <div class="prompt-actions">
      <button class="btn btn-primary btn-small" @click="$emit('copy', prompt.id)">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
        </svg>
        Копировать
      </button>
      <button class="btn-icon" :class="{ favorited }" @click="$emit('favorite', prompt.id)">
        <svg width="20" height="20" viewBox="0 0 24 24" :fill="favorited ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2">
          <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
        </svg>
      </button>
      <button v-if="showEdit" class="btn btn-secondary btn-small" @click="$emit('edit', prompt)">Изменить</button>
      <button v-if="showDelete" class="btn btn-danger btn-small" @click="$emit('delete', prompt.id)">Удалить</button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({ prompt: Object, favorited: Boolean, showEdit: Boolean, showDelete: Boolean })
defineEmits(['copy', 'favorite', 'edit', 'delete'])

const initials = computed(() => {
  const f = props.prompt.user_first_name?.[0] || ''
  const l = props.prompt.user_last_name?.[0] || ''
  return (f + l).toUpperCase() || '?'
})
</script>

<style scoped>
.prompt-card {
  animation: slideIn 0.4s ease forwards;
}

.prompt-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.prompt-author {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: var(--text-primary);
  font-weight: 500;
  font-size: 14px;
}

.prompt-author:hover {
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

.prompt-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
}

.prompt-content {
  background: rgba(0, 0, 0, 0.3);
  border-radius: var(--radius-sm);
  padding: 12px;
  margin-bottom: 12px;
  overflow-x: auto;
}

.prompt-content pre {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  color: var(--accent-cyan);
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.5;
}

.prompt-actions {
  display: flex;
  align-items: center;
  gap: 12px;
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
}

.btn-icon:hover {
  color: var(--accent-pink);
  background: rgba(236, 72, 153, 0.1);
}

.btn-icon.favorited { color: var(--accent-pink); }

@keyframes slideIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
