<template>
  <section class="canvas-page">
    <DesignSwitcher />
    <header class="canvas-hero">
      <div class="tape"></div><span>Творческий альбом S-Art</span><h1>Живой холст</h1>
      <p>Эскизы, готовые работы и визуальные истории художников.</p>
      <router-link to="/profile" class="canvas-add">＋ Добавить на холст</router-link>
    </header>
    <div class="canvas-filters">
      <button v-for="(item,index) in categories" :key="item.value" :class="{ active: activeCategory === item.value }" :style="{ '--tab': tabColors[index % tabColors.length] }" @click="activeCategory = item.value">{{ item.label }}</button>
    </div>
    <div v-if="postsStore.loading" class="design-loading">Раскладываем работы на холсте…</div>
    <div v-else-if="!postsStore.posts.length" class="design-empty">На этой странице альбома пока пусто.</div>
    <div v-else class="canvas-grid">
      <PostCard v-for="(post,index) in postsStore.posts" :key="post.id" :post="post" :class="`tilt-${index % 3}`" :favorited="favoritesStore.isFavorited(post.id, 'post')" @favorite="toggleFavorite" />
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
const categories = [{ label: 'Весь альбом', value: '' }, ...POST_CATEGORIES]
const tabColors = ['#ef8354','#7da9a1','#d19ad3','#e4bb62','#7d9bd1']
const { postsStore, favoritesStore, activeCategory, toggleFavorite } = useDesignFeed()
const { saveDesign } = useDesignPreference()
onMounted(() => saveDesign('canvas'))
</script>

<style scoped>
.canvas-page { min-height:calc(100vh - 170px); margin:-16px; padding:26px; border-radius:18px; color:#3d342e; background-color:#ded2be; background-image:linear-gradient(rgba(106,83,59,.055) 1px,transparent 1px),linear-gradient(90deg,rgba(106,83,59,.055) 1px,transparent 1px); background-size:24px 24px; }
.canvas-hero { position:relative; max-width:760px; margin:20px auto 30px; padding:34px 42px; text-align:center; background:#f8f0df; box-shadow:5px 8px 0 rgba(89,65,44,.12); transform:rotate(-.45deg); }
.tape { position:absolute; top:-13px; left:50%; width:100px; height:28px; background:rgba(239,193,105,.58); transform:translateX(-50%) rotate(2deg); }
.canvas-hero span { color:#8c6450; font-size:12px; font-weight:700; letter-spacing:.1em; text-transform:uppercase; }
.canvas-hero h1 { margin:10px 0 6px; font-family:"Segoe Print","Comic Sans MS",cursive; font-size:clamp(40px,7vw,72px); font-weight:600; line-height:1; }
.canvas-hero p { color:#77685d; font-family:Georgia,serif; font-style:italic; }
.canvas-add { display:inline-block; margin-top:20px; padding:10px 16px; border:2px solid #4d423b; color:#4d423b; background:#f4d477; font-weight:700; text-decoration:none; transform:rotate(1deg); }
.canvas-filters { display:flex; gap:7px; padding:8px 0 28px; overflow-x:auto; }
.canvas-filters button { flex:0 0 auto; padding:9px 13px; border:0; border-radius:3px 3px 10px 3px; color:#423833; background:var(--tab); font:650 12px inherit; cursor:pointer; opacity:.65; }
.canvas-filters button.active { opacity:1; box-shadow:2px 4px 0 rgba(76,56,40,.22); transform:translateY(-3px) rotate(-1deg); }
.canvas-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(250px,1fr)); gap:28px 22px; padding:8px; }
.canvas-grid :deep(.post-card) { border:10px solid #f9f4e9; border-bottom-width:20px; border-radius:2px; color:#423832; background:#f9f4e9; box-shadow:5px 8px 16px rgba(72,51,37,.2); backdrop-filter:none; }
.canvas-grid :deep(.post-card:hover) { border-color:#fffaf0; background:#fffaf0; box-shadow:8px 14px 24px rgba(72,51,37,.28); transform:rotate(0) translateY(-4px); }
.canvas-grid :deep(.tilt-0) { transform:rotate(-1deg); }.canvas-grid :deep(.tilt-1) { transform:rotate(.8deg); }.canvas-grid :deep(.tilt-2) { transform:rotate(-.3deg); }
.canvas-grid :deep(.post-image-wrap) { aspect-ratio:4/3; }
.canvas-grid :deep(.post-title) { font-family:"Segoe Print","Comic Sans MS",cursive; }
.canvas-grid :deep(.post-author),.canvas-grid :deep(.post-desc) { color:#75665d; }
.canvas-grid :deep(.tag) { color:#6f5446; border:0; background:#edd49d; }
.design-loading,.design-empty { padding:70px 20px; color:#77685d; text-align:center; }
@media(max-width:650px){.canvas-page{margin:-8px;padding:12px}.canvas-hero{padding:30px 18px}.canvas-grid{grid-template-columns:1fr}}
</style>
