<template>
  <div class="friends-page">
    <h1 class="page-title">Друзья</h1>

    <div v-if="friendsStore.requests.length > 0" class="section">
      <h2 class="section-title">Запросы на добавление <span class="request-count">{{ friendsStore.requests.length }}</span></h2>
      <div class="grid grid-3">
        <div v-for="req in friendsStore.requests" :key="req.id" class="glass-card request-card">
          <router-link :to="`/profile/${req.user_id}`" class="request-info">
            <img v-if="req.avatar_url" :src="req.avatar_url" class="avatar" />
            <div v-else class="avatar avatar-placeholder">{{ getInitials(req) }}</div>
            <span>{{ req.first_name }} {{ req.last_name }}</span>
          </router-link>
          <div class="request-actions">
            <router-link :to="`/profile/${req.user_id}`" class="btn btn-secondary btn-small">Открыть профиль</router-link>
            <button class="btn btn-primary btn-small" @click="friendsStore.acceptFriend(req.user_id)">Принять</button>
            <button class="btn btn-danger btn-small" @click="friendsStore.removeFriend(req.user_id)">Отклонить</button>
          </div>
        </div>
      </div>
    </div>

    <div class="section">
      <h2 class="section-title">Мои друзья ({{ friendsStore.friends.length }})</h2>
      <div v-if="friendsStore.friends.length === 0" class="empty-state">
        <h3>Пока нет друзей</h3>
        <p>Найдите людей в профиле и добавьте их!</p>
      </div>
      <div v-else class="grid grid-3">
        <div v-for="friend in friendsStore.friends" :key="friend.id" class="glass-card friend-card">
          <router-link :to="`/profile/${friend.id}`" class="friend-info">
            <img v-if="friend.avatar_url" :src="friend.avatar_url" class="avatar" />
            <div v-else class="avatar avatar-placeholder">{{ getInitials(friend) }}</div>
            <div>
              <h3>{{ friend.first_name }} {{ friend.last_name }}</h3>
              <span class="friend-status">{{ friend.status }}</span>
            </div>
          </router-link>
          <button class="btn btn-danger btn-small" @click="friendsStore.removeFriend(friend.id)">Удалить</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useFriendsStore } from '../stores/friends'

const friendsStore = useFriendsStore()

onMounted(() => {
  friendsStore.fetchFriends()
  friendsStore.fetchRequests()
})

function getInitials(user) {
  const f = user.first_name?.[0] || ''
  const l = user.last_name?.[0] || ''
  return (f + l).toUpperCase() || '?'
}
</script>

<style scoped>
.section {
  margin-bottom: 32px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 16px;
  color: var(--text-secondary);
}

.request-card, .friend-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
}

.request-info, .friend-info {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: var(--text-primary);
}

.request-actions {
  display: flex;
  gap: 8px;
}

.request-count { display: inline-flex; min-width: 22px; height: 22px; align-items: center; justify-content: center; border-radius: 12px; background: #ef4444; color: white; font-size: 12px; }

.avatar-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gradient-main);
  color: white;
  font-size: 14px;
  font-weight: 600;
}

.friend-status {
  font-size: 12px;
  color: var(--text-muted);
}
</style>
