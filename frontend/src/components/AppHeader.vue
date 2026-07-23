<template>
  <header class="header">
    <div class="header-inner">
      <router-link to="/" class="logo">
        <span class="logo-icon">&#x2728;</span>
        <span class="logo-text">S-Art</span>
      </router-link>

      <nav class="nav">
        <router-link to="/" class="nav-link">Лента</router-link>
        <router-link to="/explore" class="nav-link">Исследовать</router-link>
        <router-link to="/friends" class="nav-link friends-link">
          Друзья <span v-if="friends.requests.length" class="request-badge">{{ friends.requests.length }}</span>
        </router-link>
        <router-link to="/favorites" class="nav-link">Избранное</router-link>
        <router-link v-if="auth.user?.role === 'admin'" to="/admin" class="nav-link admin-link">Администратор</router-link>
      </nav>

      <div class="header-right">
        <button class="theme-toggle" type="button" @click="toggleTheme" :title="isDark ? 'Включить светлую тему' : 'Включить тёмную тему'">
          <span>{{ isDark ? '☀️' : '🌙' }}</span>
          <span class="theme-label">{{ isDark ? 'Светлая' : 'Тёмная' }}</span>
        </button>
        <router-link to="/profile" class="user-menu" title="Мой профиль">
          <img
            v-if="auth.user?.avatar_url"
            :src="auth.user.avatar_url"
            class="avatar"
          />
          <div v-else class="avatar avatar-placeholder">
            {{ initials }}
          </div>
        </router-link>
        <router-link to="/settings" class="settings-link" title="Настройки">⚙</router-link>
        <button class="btn btn-secondary btn-small" @click="handleLogout">Выйти</button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useTheme } from '../composables/useTheme'
import { useFriendsStore } from '../stores/friends'

const auth = useAuthStore()
const router = useRouter()
const { isDark, toggleTheme } = useTheme()
const friends = useFriendsStore()

onMounted(() => friends.fetchRequests())

const initials = computed(() => {
  const f = auth.user?.first_name?.[0] || ''
  const l = auth.user?.last_name?.[0] || ''
  return (f + l).toUpperCase() || '?'
})

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: var(--header-bg);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--glass-border);
}

.admin-link { color: #f59e0b; }

.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 12px 24px;
  display: flex;
  align-items: center;
  gap: 24px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  font-size: 20px;
  font-weight: 700;
}

.logo-text {
  background: var(--gradient-main);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.logo-icon {
  font-size: 24px;
}

.nav {
  display: flex;
  gap: 4px;
  flex: 1;
}

.nav-link {
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  text-decoration: none;
  color: var(--text-secondary);
  font-weight: 500;
  font-size: 14px;
  transition: var(--transition);
}

.nav-link:hover {
  color: var(--text-primary);
  background: var(--glass);
}

.nav-link.router-link-active {
  color: var(--accent-purple);
  background: rgba(168, 85, 247, 0.1);
}

.friends-link { display: inline-flex; align-items: center; gap: 6px; }
.request-badge { min-width: 19px; height: 19px; padding: 0 5px; display: inline-flex; align-items: center; justify-content: center; border-radius: 10px; background: #ef4444; color: white; font-size: 11px; font-weight: 700; }

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.theme-toggle {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 10px;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-sm);
  background: var(--glass);
  color: var(--text-primary);
  font: inherit;
  font-size: 12px;
  cursor: pointer;
}

.theme-toggle:hover { border-color: var(--accent-purple); }

.user-menu {
  text-decoration: none;
}

.settings-link { color: var(--text-secondary); text-decoration: none; font-size: 18px; }
.settings-link:hover { color: var(--accent-purple); }

.avatar-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gradient-main);
  color: white;
  font-size: 14px;
  font-weight: 600;
}

@media (max-width: 768px) {
  .nav {
    display: none;
  }
  .theme-label { display: none; }
}
</style>
