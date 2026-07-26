<template>
  <section class="neo-page">
    <DesignSwitcher />
    <header class="neo-hero">
      <div class="neo-orb">S</div>
      <div><span>Creative signal / live</span><h1>NEO—ART<br>STUDIO</h1><p>Цифровое искусство, персонажи и визуальные эксперименты.</p></div>
      <router-link to="/profile" class="neo-add">＋ НОВАЯ РАБОТА</router-link>
    </header>
    <p class="latest-note">Последние работы / новые сигналы впереди</p>
    <div class="neo-filters">
      <button v-for="item in categories" :key="item.value" :class="{ active: activeCategory === item.value }" @click="activeCategory = item.value">{{ item.label }}</button>
    </div>
    <div v-if="postsStore.loading" class="design-loading">Синхронизация арт-потока…</div>
    <div v-else-if="!postsStore.posts.length" class="design-empty">Сигналов в этой категории пока нет.</div>
    <div v-else class="neo-grid">
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
const categories = [{ label: 'ВСЕ', value: '' }, ...POST_CATEGORIES]
const { postsStore, favoritesStore, activeCategory, toggleFavorite } = useDesignFeed()
const { saveDesign } = useDesignPreference()
onMounted(() => saveDesign('neo'))
</script>

<style scoped>
.neo-page { position:relative; min-height:calc(100vh - 170px); margin:-16px; padding:22px; overflow:hidden; border:1px solid #352257; border-radius:20px; color:#f7f1ff; background:radial-gradient(circle at 85% 5%,rgba(6,182,212,.18),transparent 28%),radial-gradient(circle at 12% 12%,rgba(219,39,119,.23),transparent 30%),#08060d; }
.neo-page::before { content:""; position:absolute; inset:0; pointer-events:none; opacity:.13; background-image:linear-gradient(rgba(255,255,255,.08) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.08) 1px,transparent 1px); background-size:40px 40px; }
.neo-page>* { position:relative; z-index:1; }
.neo-hero { display:grid; grid-template-columns:auto 1fr auto; align-items:center; gap:24px; padding:34px 10px; }
.neo-orb { display:grid; place-items:center; width:72px; height:72px; border:1px solid #22d3ee; border-radius:50%; color:#fff; font-size:32px; font-weight:900; box-shadow:0 0 35px rgba(34,211,238,.38),inset 0 0 25px rgba(219,39,119,.25); }
.neo-hero span { color:#22d3ee; font:700 10px monospace; letter-spacing:.15em; text-transform:uppercase; }
.neo-hero h1 { margin:8px 0; font-size:clamp(38px,6vw,70px); line-height:.82; letter-spacing:-.06em; }
.neo-hero p { color:#a99db9; font-size:13px; }
.neo-add { padding:12px 16px; border:1px solid #ec4899; border-radius:4px; color:#fff; background:rgba(236,72,153,.12); font:700 11px monospace; text-decoration:none; box-shadow:0 0 22px rgba(236,72,153,.18); }
.latest-note { margin:0 2px 12px; color:#9d90b0; font:11px monospace; }
.neo-filters { display:flex; flex-wrap:wrap; gap:8px; padding:0 0 25px; }
.neo-filters button { flex:0 0 auto; padding:8px 12px; border:1px solid #302743; border-radius:4px; color:#9d90b0; background:#0f0b17; font:650 11px monospace; cursor:pointer; }
.neo-filters button.active { color:#071015; border-color:#22d3ee; background:#22d3ee; box-shadow:0 0 18px rgba(34,211,238,.3); }
.neo-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:16px; }
.neo-grid :deep(.post-card) { border:1px solid #2e2340; border-radius:8px; color:#f8f4ff; background:#100c18; box-shadow:none; backdrop-filter:none; }
.neo-grid :deep(.post-card:hover) { border-color:#7c3aed; background:#151020; box-shadow:0 0 0 1px #7c3aed,0 18px 50px rgba(124,58,237,.2); }
.neo-grid :deep(.post-image-wrap) { aspect-ratio:1/1; background:#09070d; }
.neo-grid :deep(.post-author),.neo-grid :deep(.post-desc) { color:#aa9db8; }
.neo-grid :deep(.tag) { color:#22d3ee; border-color:rgba(34,211,238,.35); background:rgba(34,211,238,.08); font-family:monospace; }
.design-loading,.design-empty { padding:70px 20px; color:#9d90b0; text-align:center; }
:global(:root[data-theme='light']) .neo-page { color:#241d2d; border-color:#d8c9e8; background:radial-gradient(circle at 85% 5%,rgba(6,182,212,.13),transparent 28%),radial-gradient(circle at 12% 12%,rgba(219,39,119,.13),transparent 30%),#f6f2f9; }
:global(:root[data-theme='light']) .neo-page::before { opacity:.22; background-image:linear-gradient(rgba(85,55,100,.12) 1px,transparent 1px),linear-gradient(90deg,rgba(85,55,100,.12) 1px,transparent 1px); }
:global(:root[data-theme='light']) .neo-hero p,
:global(:root[data-theme='light']) .latest-note { color:#766782; }
:global(:root[data-theme='light']) .neo-add { color:#8f1d60; background:rgba(236,72,153,.08); }
:global(:root[data-theme='light']) .neo-filters button { color:#675a73; border-color:#d8cce1; background:#fff; }
:global(:root[data-theme='light']) .neo-filters button.active { color:#08373e; border-color:#22b8c7; background:#8ce6ed; box-shadow:none; }
:global(:root[data-theme='light']) .neo-grid :deep(.post-card) { color:#291f31; border-color:#ddd1e5; background:#fff; }
:global(:root[data-theme='light']) .neo-grid :deep(.post-card:hover) { border-color:#9b6ad0; background:#fff; box-shadow:0 15px 40px rgba(80,50,100,.14); }
:global(:root[data-theme='light']) .neo-grid :deep(.post-author),
:global(:root[data-theme='light']) .neo-grid :deep(.post-desc) { color:#74677d; }

/* High-contrast synth palettes without translucent white surfaces. */
:global(:root[data-theme='light']) .neo-page { color:#241b2d; border-color:#bfb0cb; background:radial-gradient(circle at 85% 5%,rgba(8,127,140,.14),transparent 28%),radial-gradient(circle at 12% 12%,rgba(167,25,98,.13),transparent 30%),#f3f0f7; color-scheme:light; }
:global(:root[data-theme='light']) .neo-hero span { color:#087783; }
:global(:root[data-theme='light']) .neo-hero p,
:global(:root[data-theme='light']) .latest-note { color:#5f5269; }
:global(:root[data-theme='light']) .neo-add { color:#fff; border-color:#a71962; background:#a71962; box-shadow:none; }
:global(:root[data-theme='light']) .neo-filters button { color:#564961; border-color:#c9bdd2; background:#fff; }
:global(:root[data-theme='light']) .neo-filters button:hover { border-color:#087f8c; }
:global(:root[data-theme='light']) .neo-filters button.active { color:#fff; border-color:#087f8c; background:#087f8c; }
:global(:root[data-theme='light']) .neo-grid :deep(.post-card) { color:#241b2d; border-color:#cfc3d9; background:#fff; }
:global(:root[data-theme='light']) .neo-grid :deep(.post-author),
:global(:root[data-theme='light']) .neo-grid :deep(.post-desc),
:global(:root[data-theme='light']) .neo-grid :deep(.post-meta time) { color:#5f5269; }
:global(:root[data-theme='light']) .neo-grid :deep(.tag) { color:#086f79; border-color:#087f8c; background:#f0fbfc; }
:global(:root:not([data-theme='light'])) .neo-page { color-scheme:dark; }
:global(:root:not([data-theme='light'])) .neo-grid :deep(.post-meta time) { color:#b6a9c3; }
@media(max-width:720px){.neo-page{margin:-8px;padding:12px}.neo-hero{grid-template-columns:1fr}.neo-orb{display:none}.neo-grid{grid-template-columns:1fr}}
</style>
