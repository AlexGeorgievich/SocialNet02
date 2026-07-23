<template>
  <div class="auth-page">
    <div class="auth-card glass-card">
      <div class="auth-header">
        <span class="logo-icon">&#x2728;</span>
        <h1>Регистрация в S-Art</h1>
        <p>Создайте свой аккаунт</p>
      </div>
      <form @submit.prevent="handleRegister" class="auth-form">
        <div class="form-row">
          <div class="form-group">
            <label>Имя</label>
            <input v-model="form.first_name" type="text" class="input" placeholder="Имя" />
          </div>
          <div class="form-group">
            <label>Фамилия</label>
            <input v-model="form.last_name" type="text" class="input" placeholder="Фамилия" />
          </div>
        </div>
        <div class="form-group">
          <label>Email</label>
          <input v-model="form.email" type="email" class="input" placeholder="your@email.com" required />
        </div>
        <div class="form-group">
          <label>Пароль</label>
          <input v-model="form.password" type="password" class="input" placeholder="Минимум 6 символов" required minlength="6" />
        </div>
        <label class="consent">
          <input v-model="form.privacy_consent" type="checkbox" required />
          <span>
            Я свободно, своей волей и в своём интересе даю отдельное согласие
            на обработку и хранение моих персональных данных в соответствии с
            <router-link to="/privacy" target="_blank">Политикой обработки персональных данных</router-link>.
          </span>
        </label>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" class="btn btn-primary auth-btn" :disabled="loading">
          {{ loading ? 'Создание...' : 'Создать аккаунт' }}
        </button>
      </form>
      <p class="auth-link">
        Уже есть аккаунт? <router-link to="/login">Войти</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()

const form = ref({
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  privacy_consent: false,
})
const error = ref('')
const loading = ref(false)

async function handleRegister() {
  error.value = ''
  loading.value = true
  try {
    await auth.register(form.value)
    router.push('/')
  } catch (e) {
    error.value = e.response?.data?.detail
      || (e.request ? 'Сервер недоступен. Запустите backend.' : 'Ошибка регистрации')
  } finally {
    loading.value = false
  }
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
  font-size: 22px;
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

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
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

.error {
  color: #ef4444;
  font-size: 13px;
  text-align: center;
  padding: 8px;
  background: rgba(239, 68, 68, 0.1);
  border-radius: 8px;
}

.consent {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  color: var(--text-secondary);
  font-size: 12px;
  line-height: 1.45;
  cursor: pointer;
}

.consent input {
  flex: 0 0 auto;
  width: 17px;
  height: 17px;
  margin-top: 2px;
  accent-color: var(--accent-purple);
}

.consent a {
  color: var(--accent-purple);
  font-weight: 600;
}
</style>
