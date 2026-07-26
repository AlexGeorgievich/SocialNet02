<template>
  <div class="auth-page">
    <div class="auth-card glass-card">
      <div class="auth-header">
        <span class="logo-icon">&#x2728;</span>
        <h1>Вход в S-Art</h1>
        <p>Добро пожаловать!</p>
      </div>
      <div class="mode-selector" aria-label="Контур приложения">
        <button type="button" :class="{ active: appMode === 'demo' }" @click="selectMode('demo')">
          Демо
        </button>
        <button type="button" :class="{ active: appMode === 'work' }" @click="selectMode('work')">
          Рабочий
        </button>
      </div>
      <p class="mode-hint">
        {{ appMode === 'demo'
          ? 'Демонстрационные пользователи и тестовое наполнение'
          : 'Изолированная рабочая база без демонстрационных аккаунтов' }}
      </p>
      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label>Email</label>
          <input v-model="form.email" type="email" class="input" placeholder="your@email.com" required />
        </div>
        <div class="form-group">
          <label>Пароль</label>
          <input v-model="form.password" type="password" class="input" placeholder="Минимум 6 символов" required />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" class="btn btn-primary auth-btn" :disabled="loading">
          {{ loading ? 'Вход...' : 'Войти' }}
        </button>
      </form>
      <p class="auth-link">
        Нет аккаунта? <router-link to="/register">Зарегистрироваться</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useAppMode } from '../composables/useAppMode'

const auth = useAuthStore()
const router = useRouter()
const { appMode, setAppMode } = useAppMode()

const form = ref({ email: '', password: '' })
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    const email = form.value.email.trim().toLowerCase()
    if (email === 'q@q.com' || email.endsWith('@demo.local')) {
      setAppMode('demo', false)
    }
    await auth.login(form.value)
    router.push('/')
  } catch (e) {
    error.value = e.response?.status === 401
      ? `Неверный email или пароль в контуре «${appMode.value === 'demo' ? 'Демо' : 'Рабочий'}»`
      : e.response?.data?.detail || 'Ошибка входа'
  } finally {
    loading.value = false
  }
}

function selectMode(mode) {
  error.value = ''
  setAppMode(mode, false)
}
</script>

<style scoped>
.auth-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
}

.auth-card {
  width: 100%;
  max-width: 420px;
  padding: 40px;
}

.auth-header {
  text-align: center;
  margin-bottom: 32px;
}

.auth-header .logo-icon {
  font-size: 48px;
  display: block;
  margin-bottom: 16px;
}

.auth-header h1 {
  font-size: 24px;
  font-weight: 700;
  background: var(--gradient-main);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.auth-header p {
  color: var(--text-secondary);
  margin-top: 4px;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.mode-selector {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4px;
  margin-bottom: 8px;
  padding: 4px;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-sm);
  background: var(--glass);
}

.mode-selector button {
  padding: 9px 12px;
  border: 0;
  border-radius: calc(var(--radius-sm) - 3px);
  background: transparent;
  color: var(--text-secondary);
  font: inherit;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.mode-selector button.active {
  background: var(--gradient-main);
  color: #fff;
}

.mode-hint {
  min-height: 34px;
  margin-bottom: 18px;
  color: var(--text-muted);
  font-size: 12px;
  line-height: 1.4;
  text-align: center;
}

.auth-btn {
  width: 100%;
  justify-content: center;
  padding: 14px;
  font-size: 16px;
  margin-top: 8px;
}

.auth-link {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: var(--text-secondary);
}

.auth-link a {
  color: var(--accent-purple);
  text-decoration: none;
  font-weight: 600;
}

.auth-link a:hover {
  text-decoration: underline;
}

.error {
  color: #ef4444;
  font-size: 13px;
  text-align: center;
  padding: 8px;
  background: rgba(239, 68, 68, 0.1);
  border-radius: 8px;
}
</style>
