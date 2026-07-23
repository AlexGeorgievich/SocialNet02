import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/login', name: 'Login', component: () => import('../views/LoginView.vue'), meta: { guest: true } },
  { path: '/register', name: 'Register', component: () => import('../views/RegisterView.vue'), meta: { guest: true } },
  { path: '/privacy', name: 'Privacy', component: () => import('../views/PrivacyView.vue') },
  { path: '/', name: 'Feed', component: () => import('../views/FeedView.vue'), meta: { auth: true } },
  { path: '/explore', name: 'Explore', component: () => import('../views/ExploreView.vue'), meta: { auth: true } },
  { path: '/profile/:id?', name: 'Profile', component: () => import('../views/ProfileView.vue'), meta: { auth: true } },
  { path: '/settings', name: 'Settings', component: () => import('../views/SettingsView.vue'), meta: { auth: true } },
  { path: '/friends', name: 'Friends', component: () => import('../views/FriendsView.vue'), meta: { auth: true } },
  { path: '/favorites', name: 'Favorites', component: () => import('../views/FavoritesView.vue'), meta: { auth: true } },
  { path: '/admin', name: 'Admin', component: () => import('../views/AdminView.vue'), meta: { auth: true, admin: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()
  if (to.meta.auth && !auth.isLoggedIn) return { name: 'Login' }
  if (to.meta.guest && auth.isLoggedIn) return { name: 'Feed' }
  if (to.meta.admin) {
    if (!auth.user) await auth.fetchMe()
    if (auth.user?.role !== 'admin') return { name: 'Feed' }
  }
})

export default router
