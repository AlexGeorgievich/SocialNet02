<template>
  <router-link :to="`/profile/${user.id}`" class="user-card glass-card">
    <img v-if="user.avatar_url" :src="user.avatar_url" class="avatar avatar-large" />
    <div v-else class="avatar avatar-large avatar-placeholder">{{ initials }}</div>
    <h3 class="user-name">{{ user.first_name }} {{ user.last_name }}</h3>
    <span class="user-status" :class="user.status">{{ user.status }}</span>
    <slot></slot>
  </router-link>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({ user: Object })

const initials = computed(() => {
  const f = props.user.first_name?.[0] || ''
  const l = props.user.last_name?.[0] || ''
  return (f + l).toUpperCase() || '?'
})
</script>

<style scoped>
.user-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: var(--text-primary);
  text-align: center;
  padding: 24px;
  cursor: pointer;
}

.avatar-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gradient-main);
  color: white;
  font-size: 28px;
  font-weight: 700;
}

.user-name {
  font-size: 16px;
  font-weight: 600;
  margin-top: 12px;
}

.user-status {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 4px;
}

.user-status.online {
  color: #22c55e;
}
</style>
