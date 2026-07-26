<template>
  <section class="gallery-page">
    <DesignSwitcher />
    <header class="gallery-hero">
      <div><span>Кураторская лента · S-Art</span><h1>Digital Gallery</h1></div>
      <router-link to="/profile" class="gallery-add">Добавить работу ↗</router-link>
    </header>
    <p class="latest-note">Последние работы · сначала новые</p>
    <div class="gallery-filters">
      <button v-for="item in categories" :key="item.value" :class="{ active: activeCategory === item.value }" @click="activeCategory = item.value">{{ item.label }}</button>
    </div>
    <div v-if="postsStore.loading" class="design-loading">Подготовка экспозиции…</div>
    <div v-else-if="!postsStore.posts.length" class="design-empty">В этой экспозиции пока нет работ.</div>
    <div v-else class="gallery-grid">
      <PostCard v-for="post in postsStore.posts" :key="post.id" :post="post" :favorited="favoritesStore.isFavorited(post.id, 'post')" @favorite="toggleFavorite" />
    </div>
  </section>
</template>

<script setup>
import { onMounted } from 'vue'
import DesignSwitcher from '../../components/DesignSwitcher.vue'
import PostCard from '../../components/PostCard.vue'
import { POST_CATEGORIES } from '../../constants/categories'
import { useDesignFeed } from '../../composables/useDesignFeed'
import { useDesignPreference } from '../../composables/useDesignPreference'
const categories = [{ label: 'Все работы', value: '' }, ...POST_CATEGORIES]
const { postsStore, favoritesStore, activeCategory, toggleFavorite } = useDesignFeed()
const { saveDesign } = useDesignPreference()
onMounted(() => saveDesign('gallery'))
</script>

<style scoped>
.gallery-page {
  min-height: calc(100vh - 170px);
  margin: -16px;
  padding: 22px;
  border-radius: 18px;
  color: #242126;
  background: #f0ede7;
}
.gallery-hero { display:flex; align-items:end; justify-content:space-between; gap:24px; padding:34px 8px 30px; border-bottom:1px solid #cfc8be; }
.gallery-hero span { color:#756e67; font-size:11px; font-weight:750; letter-spacing:.15em; text-transform:uppercase; }
.gallery-hero h1 { margin-top:8px; font-family:Georgia,serif; font-size:clamp(42px,7vw,82px); font-weight:400; line-height:.92; letter-spacing:-.055em; }
.gallery-add { padding:11px 16px; border:1px solid #272329; border-radius:999px; color:#272329; font-size:13px; text-decoration:none; white-space:nowrap; }
.gallery-add:hover { color:#fff; background:#272329; }
.latest-note { margin:18px 2px 4px; color:#756e67; font-size:12px; }
.gallery-filters { display:flex; flex-wrap:wrap; gap:6px; padding:12px 0 24px; }
.gallery-filters button { flex:0 0 auto; padding:7px 12px; border:0; border-radius:999px; color:#746d68; background:transparent; font:inherit; font-size:12px; cursor:pointer; }
.gallery-filters button.active { color:#fff; background:#262229; }
.gallery-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(265px,1fr)); gap:18px; }
.gallery-grid :deep(.post-card) { border:0; border-radius:4px; color:#272329; background:#faf9f6; box-shadow:none; backdrop-filter:none; }
.gallery-grid :deep(.post-card:hover) { border:0; background:#fff; box-shadow:0 18px 45px rgba(41,33,42,.13); transform:translateY(-3px); }
.gallery-grid :deep(.post-image-wrap) { aspect-ratio:4/3; background:#ddd8d0; }
.gallery-grid :deep(.post-title) { font-family:Georgia,serif; font-size:19px; }
.gallery-grid :deep(.post-author), .gallery-grid :deep(.post-desc) { color:#625b62; }
.gallery-grid :deep(.tag) { color:#625b62; border-color:#d8d1c8; background:transparent; }
.design-loading,.design-empty { padding:70px 20px; color:#756e67; text-align:center; }
:global(:root:not([data-theme='light'])) .gallery-page { color:#eee9e2; background:#111015; }
:global(:root:not([data-theme='light'])) .gallery-hero { border-color:#39343d; }
:global(:root:not([data-theme='light'])) .gallery-hero span,
:global(:root:not([data-theme='light'])) .latest-note { color:#9c929f; }
:global(:root:not([data-theme='light'])) .gallery-add { color:#eee9e2; border-color:#eee9e2; }
:global(:root:not([data-theme='light'])) .gallery-add:hover { color:#17131a; background:#eee9e2; }
:global(:root:not([data-theme='light'])) .gallery-filters button { color:#aaa0ac; }
:global(:root:not([data-theme='light'])) .gallery-filters button.active { color:#17131a; background:#eee9e2; }
:global(:root:not([data-theme='light'])) .gallery-grid :deep(.post-card) { color:#eee9e2; background:#1b181e; }
:global(:root:not([data-theme='light'])) .gallery-grid :deep(.post-card:hover) { background:#211d24; box-shadow:0 18px 45px rgba(0,0,0,.3); }
:global(:root:not([data-theme='light'])) .gallery-grid :deep(.post-author),
:global(:root:not([data-theme='light'])) .gallery-grid :deep(.post-desc) { color:#afa5b1; }
:global(:root:not([data-theme='light'])) .gallery-grid :deep(.tag) { color:#c3b9c5; border-color:#4c454f; }

/* Opaque museum palettes: warm paper by day, charcoal exhibition hall by night. */
.gallery-page { opacity:1; filter:none; mix-blend-mode:normal; isolation:isolate; }
:global(:root[data-theme='light']) .gallery-page { color:#211e22; background:#f1eee8; color-scheme:light; }
:global(:root[data-theme='light']) .gallery-hero { border-color:#bdb4a9; }
:global(:root[data-theme='light']) .gallery-hero span,
:global(:root[data-theme='light']) .latest-note { color:#625a55; }
:global(:root[data-theme='light']) .gallery-grid :deep(.post-card) { color:#211e22; border:1px solid #d2cbc2; background:#fffdfa; }
:global(:root[data-theme='light']) .gallery-grid :deep(.post-card:hover) { border-color:#aaa096; background:#fff; }
:global(:root[data-theme='light']) .gallery-grid :deep(.post-author),
:global(:root[data-theme='light']) .gallery-grid :deep(.post-desc),
:global(:root[data-theme='light']) .gallery-grid :deep(.post-meta time) { color:#5e565d; }
:global(:root:not([data-theme='light'])) .gallery-page { color-scheme:dark; }
:global(:root:not([data-theme='light'])) .gallery-grid :deep(.post-meta time) { color:#b7acb8; }
@media(max-width:650px){.gallery-page{margin:-8px;padding:12px}.gallery-hero{align-items:flex-start;flex-direction:column}.gallery-grid{grid-template-columns:1fr}}
</style>
