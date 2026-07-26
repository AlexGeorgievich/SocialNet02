<template>
  <div class="app">
    <AppHeader v-if="auth.isLoggedIn" />
    <main class="main-content">
      <router-view />
    </main>
    <AppFooter />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from './stores/auth'
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
import { useDesignPreference } from './composables/useDesignPreference'

const auth = useAuthStore()
const { syncDesign } = useDesignPreference()

onMounted(async () => {
  if (auth.isLoggedIn) {
    await auth.fetchMe()
    syncDesign(auth.user?.ui_style)
  }
})
</script>
