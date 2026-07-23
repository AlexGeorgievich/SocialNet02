<template>
  <div class="admin-page">
    <h1 class="page-title">Панель администратора</h1>

    <section class="glass-card admin-section">
      <h2>Пользователи ({{ users.length }})</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Пользователь</th><th>Email</th><th>Роль</th><th>Действия</th></tr></thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td><router-link :to="`/profile/${user.id}`">{{ user.first_name }} {{ user.last_name }}</router-link></td>
              <td>{{ user.email }}</td>
              <td><span class="tag">{{ user.role === 'admin' ? 'Администратор' : 'Пользователь' }}</span></td>
              <td class="actions">
                <button v-if="user.id !== auth.user?.id" class="btn btn-secondary btn-small" @click="toggleRole(user)">
                  {{ user.role === 'admin' ? 'Сделать пользователем' : 'Сделать администратором' }}
                </button>
                <button v-if="user.id !== auth.user?.id" class="btn btn-danger btn-small" @click="removeUser(user)">Удалить</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <div class="content-columns">
      <section class="glass-card admin-section">
        <h2>Работы ({{ content.posts.length }})</h2>
        <div v-for="post in content.posts" :key="post.id" class="content-row">
          <router-link :to="`/profile/${post.user_id}`">{{ post.title }}</router-link>
          <button class="btn btn-danger btn-small" @click="removeContent('posts', post.id)">Удалить</button>
        </div>
      </section>
      <section class="glass-card admin-section">
        <h2>Промпты ({{ content.prompts.length }})</h2>
        <div v-for="prompt in content.prompts" :key="prompt.id" class="content-row">
          <router-link :to="`/profile/${prompt.user_id}`">{{ prompt.title }}</router-link>
          <button class="btn btn-danger btn-small" @click="removeContent('prompts', prompt.id)">Удалить</button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import api from '../composables/useApi'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const users = ref([])
const content = reactive({ posts: [], prompts: [] })

async function load() {
  users.value = (await api.get('/admin/users')).data
  Object.assign(content, (await api.get('/admin/content')).data)
}
async function toggleRole(user) {
  const role = user.role === 'admin' ? 'user' : 'admin'
  await api.put(`/admin/users/${user.id}/role`, { role })
  user.role = role
}
async function removeUser(user) {
  if (!confirm(`Удалить пользователя ${user.email} и весь его контент?`)) return
  await api.delete(`/admin/users/${user.id}`)
  await load()
}
async function removeContent(type, id) {
  if (!confirm('Удалить запись?')) return
  await api.delete(`/admin/${type}/${id}`)
  await load()
}
onMounted(load)
</script>

<style scoped>
.admin-section { margin-bottom: 20px; }
.admin-section h2 { margin-bottom: 16px; font-size: 18px; }
.table-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; }
th, td { padding: 10px; text-align: left; border-bottom: 1px solid var(--glass-border); font-size: 13px; }
th { color: var(--text-secondary); }
td a, .content-row a { color: var(--text-primary); text-decoration: none; }
.actions { display: flex; gap: 8px; flex-wrap: wrap; }
.content-columns { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.content-row { display: flex; justify-content: space-between; align-items: center; gap: 12px; padding: 9px 0; border-bottom: 1px solid var(--glass-border); }
@media (max-width: 800px) { .content-columns { grid-template-columns: 1fr; } }
</style>
