<template>
  <section class="gallery-page">
    <DesignSwitcher />
    <div class="gallery-lights" aria-hidden="true"><i></i><i></i><i></i></div>
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

/* Exhibition hall: skylit white cube by day, spotlit charcoal room by night. */
.gallery-page {
  position:relative;
  overflow:hidden;
  border:1px solid #cbc6be;
  background-image:
    linear-gradient(90deg, transparent 0 32%, rgba(70,65,62,.055) 32.1% 32.25%, transparent 32.35% 66%, rgba(70,65,62,.055) 66.1% 66.25%, transparent 66.35%),
    linear-gradient(#eeece7, #dedbd5);
  box-shadow:inset 0 30px 60px rgba(255,255,255,.72);
}
.gallery-page > * { position:relative; z-index:2; }
.gallery-lights {
  position:absolute;
  z-index:1;
  top:64px;
  left:0;
  right:0;
  display:flex;
  justify-content:space-around;
  pointer-events:none;
}
.gallery-lights i {
  display:block;
  width:28%;
  height:260px;
  background:linear-gradient(165deg,rgba(255,255,255,.72),transparent 64%);
  clip-path:polygon(43% 0,57% 0,100% 100%,0 100%);
}
.gallery-hero {
  margin:12px 0 26px;
  padding:42px 30px 34px;
  border:1px solid #c9c4bc;
  background:#f9f8f5;
  box-shadow:0 14px 35px rgba(42,38,35,.08);
}
.gallery-hero h1 { color:#1f1d20; }
.gallery-grid { gap:30px 24px; padding:12px 10px 34px; }
.gallery-grid :deep(.post-card) {
  padding:12px;
  border:1px solid #bcb6ad;
  background:#fdfcf9;
  box-shadow:0 12px 24px rgba(50,45,42,.12);
}
.gallery-grid :deep(.post-image-wrap) {
  border:8px solid #eeeae3;
  outline:1px solid #c7c0b7;
  box-shadow:inset 0 0 0 1px #fff;
}

:global(:root:not([data-theme='light'])) .gallery-page {
  border-color:#343237;
  background-image:
    linear-gradient(90deg,transparent 0 32%,rgba(255,255,255,.025) 32.1% 32.25%,transparent 32.35% 66%,rgba(255,255,255,.025) 66.1% 66.25%,transparent 66.35%),
    linear-gradient(#1b1a1e,#111114);
  box-shadow:inset 0 30px 70px rgba(0,0,0,.72);
}
:global(:root:not([data-theme='light'])) .gallery-lights i {
  background:linear-gradient(165deg,rgba(255,225,166,.2),transparent 66%);
}
:global(:root:not([data-theme='light'])) .gallery-hero {
  border-color:#454148;
  background:#211f24;
  box-shadow:0 18px 42px rgba(0,0,0,.35);
}
:global(:root:not([data-theme='light'])) .gallery-hero h1 { color:#f4efe8; }
:global(:root:not([data-theme='light'])) .gallery-grid :deep(.post-card) {
  border-color:#4a464d;
  background:#201e23;
  box-shadow:0 16px 34px rgba(0,0,0,.46);
}
:global(:root:not([data-theme='light'])) .gallery-grid :deep(.post-image-wrap) {
  border-color:#302d33;
  outline-color:#5a555e;
  box-shadow:0 0 28px rgba(255,205,126,.09);
}
@media(max-width:650px){.gallery-page{margin:-8px;padding:12px}.gallery-hero{align-items:flex-start;flex-direction:column}.gallery-grid{grid-template-columns:1fr}}
</style>
