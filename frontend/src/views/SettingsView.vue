<template>
  <div class="settings-page">
    <h1 class="page-title">Настройки профиля</h1>

    <div class="settings-card glass-card">
      <div class="avatar-section">
        <img v-if="auth.user?.avatar_url" :src="auth.user.avatar_url" class="avatar avatar-large" />
        <div v-else class="avatar avatar-large avatar-placeholder">{{ initials }}</div>
        <div>
          <label class="btn btn-secondary btn-small">
            Загрузить аватарку
            <input type="file" accept="image/*" @change="handleAvatar" hidden />
          </label>
          <p class="hint">JPG, PNG, WebP. До 10MB.</p>
        </div>
      </div>

      <form @submit.prevent="handleSave" class="settings-form">
        <div class="form-row">
          <div class="form-group">
            <label>Имя</label>
            <input v-model="form.first_name" class="input" />
          </div>
          <div class="form-group">
            <label>Фамилия</label>
            <input v-model="form.last_name" class="input" />
          </div>
        </div>
        <div class="form-group">
          <label>Статус</label>
          <input v-model="form.status" class="input" placeholder="Онлайн" />
        </div>
        <div class="form-group">
          <label>Описание</label>
          <textarea v-model="form.description" class="input" placeholder="Расскажите о себе..."></textarea>
        </div>
        <p v-if="message" class="success">{{ message }}</p>
        <button type="submit" class="btn btn-primary" :disabled="saving">
          {{ saving ? 'Сохранение...' : 'Сохранить' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../composables/useApi'

const auth = useAuthStore()

const form = ref({ first_name: '', last_name: '', description: '', status: '' })
const saving = ref(false)
const message = ref('')

const initials = computed(() => {
  const f = auth.user?.first_name?.[0] || ''
  const l = auth.user?.last_name?.[0] || ''
  return (f + l).toUpperCase() || '?'
})

onMounted(() => {
  if (auth.user) {
    form.value = {
      first_name: auth.user.first_name || '',
      last_name: auth.user.last_name || '',
      description: auth.user.description || '',
      status: auth.user.status || '',
    }
  }
})

async function handleSave() {
  saving.value = true
  message.value = ''
  try {
    const res = await api.put('/users/me', form.value)
    auth.user = res.data
    message.value = 'Профиль обновлён!'
  } catch (e) {
    message.value = 'Ошибка: ' + (e.response?.data?.detail || 'неизвестная')
  } finally {
    saving.value = false
  }
}

async function handleAvatar(e) {
  const file = e.target.files[0]
  if (!file) return
  const formData = new FormData()
  formData.append('file', file)
  try {
    const res = await api.post('/users/me/avatar', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    auth.user = res.data
    message.value = 'Аватарка обновлена!'
  } catch (e) {
    message.value = 'Ошибка загрузки'
  }
}
</script>

<style scoped>
.settings-card {
  max-width: 600px;
}

.avatar-section {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 32px;
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

.hint {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 6px;
}

.settings-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.success {
  color: #22c55e;
  font-size: 13px;
  text-align: center;
  padding: 8px;
  background: rgba(34, 197, 94, 0.1);
  border-radius: 8px;
}
</style>
