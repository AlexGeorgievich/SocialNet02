<template>
  <section class="canvas-page">
    <DesignSwitcher />
    <header class="canvas-hero">
      <div class="tape"></div><span>Творческий альбом S-Art</span><h1>Живой холст</h1>
      <p>Эскизы, готовые работы и визуальные истории художников.</p>
      <router-link to="/profile" class="canvas-add">＋ Добавить на холст</router-link>
    </header>
    <p class="latest-note">Последние работы · новые листы сверху</p>
    <div class="canvas-filters">
      <button v-for="(item,index) in categories" :key="item.value" :class="{ active: activeCategory === item.value }" :style="{ '--tab': tabColors[index % tabColors.length] }" @click="activeCategory = item.value">{{ item.label }}</button>
    </div>
    <div v-if="postsStore.loading" class="design-loading">Раскладываем работы на холсте…</div>
    <div v-else-if="!postsStore.posts.length" class="design-empty">На этой странице альбома пока пусто.</div>
    <div v-else class="canvas-grid">
      <PostCard v-for="(post,index) in postsStore.posts" :key="post.id" :post="post" :navigation-posts="postsStore.posts" :class="`tilt-${index % 3}`" :favorited="favoritesStore.isFavorited(post.id, 'post')" @favorite="toggleFavorite" />
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
.latest-note { margin:0 2px 12px; color:#77685d; font-family:Georgia,serif; font-size:12px; font-style:italic; }
.canvas-filters { display:flex; flex-wrap:wrap; gap:7px; padding:0 0 28px; }
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
:global(:root:not([data-theme='light'])) .canvas-page { color:#e9ddcc; background-color:#211b19; background-image:linear-gradient(rgba(230,210,180,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(230,210,180,.045) 1px,transparent 1px); }
:global(:root:not([data-theme='light'])) .canvas-hero { color:#392f2b; background:#d8c8ad; box-shadow:5px 8px 0 rgba(0,0,0,.24); }
:global(:root:not([data-theme='light'])) .canvas-hero p { color:#67574d; }
:global(:root:not([data-theme='light'])) .latest-note { color:#b8a99b; }
:global(:root:not([data-theme='light'])) .canvas-grid :deep(.post-card) { color:#3f352f; border-color:#d9cbb3; background:#d9cbb3; box-shadow:5px 8px 18px rgba(0,0,0,.35); }
:global(:root:not([data-theme='light'])) .canvas-grid :deep(.post-card:hover) { border-color:#eadcc5; background:#eadcc5; }

/* Sketchbook palettes: sunlit kraft paper and a dark studio desk. */
:global(:root[data-theme='light']) .canvas-page { color:#382e27; background-color:#d8c8ac; background-image:linear-gradient(rgba(82,62,45,.09) 1px,transparent 1px),linear-gradient(90deg,rgba(82,62,45,.09) 1px,transparent 1px); color-scheme:light; }
:global(:root[data-theme='light']) .canvas-hero { color:#382e27; background:#fff8e9; }
:global(:root[data-theme='light']) .canvas-hero span { color:#75442f; }
:global(:root[data-theme='light']) .canvas-hero p,
:global(:root[data-theme='light']) .latest-note { color:#645449; }
:global(:root[data-theme='light']) .canvas-grid :deep(.post-card) { color:#382e27; border-color:#fff8e9; background:#fff8e9; }
:global(:root[data-theme='light']) .canvas-grid :deep(.post-author),
:global(:root[data-theme='light']) .canvas-grid :deep(.post-desc),
:global(:root[data-theme='light']) .canvas-grid :deep(.post-meta time) { color:#625247; }
:global(:root[data-theme='light']) .canvas-grid :deep(.tag) { color:#4f382a; background:#ead08a; }
:global(:root:not([data-theme='light'])) .canvas-page { color-scheme:dark; }
:global(:root:not([data-theme='light'])) .canvas-grid :deep(.post-meta time) { color:#5f5045; }

/* Final canvas scheme: neutral linen/ink in light mode, graphite studio in dark mode. */
.canvas-page { opacity:1; filter:none; mix-blend-mode:normal; isolation:isolate; }
:global(:root[data-theme='light']) .canvas-page {
  color:#292725;
  background-color:#e5e1da;
  background-image:linear-gradient(#d6d0c7 1px,transparent 1px),linear-gradient(90deg,#d6d0c7 1px,transparent 1px);
}
:global(:root[data-theme='light']) .canvas-hero { color:#292725; background:#fffefa; box-shadow:5px 8px 0 #c8c1b7; }
:global(:root[data-theme='light']) .canvas-hero span { color:#8a3f2d; }
:global(:root[data-theme='light']) .canvas-hero p,
:global(:root[data-theme='light']) .latest-note { color:#5d5751; }
:global(:root[data-theme='light']) .canvas-add { color:#fff; border-color:#8a3f2d; background:#8a3f2d; }
:global(:root[data-theme='light']) .canvas-filters button { opacity:1; color:#292725; border:1px solid #aaa198; filter:none; }
:global(:root[data-theme='light']) .canvas-grid :deep(.post-card) { color:#292725; border-color:#fffefa; background:#fffefa; box-shadow:5px 8px 16px rgba(45,40,36,.2); }
:global(:root[data-theme='light']) .canvas-grid :deep(.post-card:hover) { border-color:#fff; background:#fff; }

:global(:root:not([data-theme='light'])) .canvas-page {
  color:#f1ece5;
  background-color:#17181a;
  background-image:linear-gradient(#292b2f 1px,transparent 1px),linear-gradient(90deg,#292b2f 1px,transparent 1px);
}
:global(:root:not([data-theme='light'])) .canvas-hero { color:#f1ece5; background:#26272b; box-shadow:5px 8px 0 #08090a; }
:global(:root:not([data-theme='light'])) .canvas-hero span { color:#ff9d7f; }
:global(:root:not([data-theme='light'])) .canvas-hero p,
:global(:root:not([data-theme='light'])) .latest-note { color:#c9c0b7; }
:global(:root:not([data-theme='light'])) .canvas-add { color:#17181a; border-color:#f0bd59; background:#f0bd59; }
:global(:root:not([data-theme='light'])) .canvas-filters button { opacity:1; color:#17181a; border:1px solid #17181a; filter:saturate(.82); }
:global(:root:not([data-theme='light'])) .canvas-filters button.active { filter:saturate(1.2); box-shadow:2px 4px 0 #08090a; }
:global(:root:not([data-theme='light'])) .canvas-grid :deep(.post-card) { color:#f1ece5; border-color:#292a2e; background:#292a2e; box-shadow:5px 8px 18px rgba(0,0,0,.48); }
:global(:root:not([data-theme='light'])) .canvas-grid :deep(.post-card:hover) { color:#fff; border-color:#34363b; background:#34363b; }
:global(:root:not([data-theme='light'])) .canvas-grid :deep(.post-author),
:global(:root:not([data-theme='light'])) .canvas-grid :deep(.post-desc),
:global(:root:not([data-theme='light'])) .canvas-grid :deep(.post-meta time) { color:#c9c0b7; }
:global(:root:not([data-theme='light'])) .canvas-grid :deep(.tag) { color:#17181a; border-color:#d2a94e; background:#e7bd5d; }

/*
 * Canvas has two deliberately different physical scenes.
 * Light: an open ruled sketchbook. Dark: artwork on a wooden desk under a lamp.
 */
:global(:root[data-theme='light']) .canvas-page {
  position:relative;
  overflow:hidden;
  border:1px solid #c8bfb1;
  color:#302d29;
  background-color:#f4f0e7;
  background-image:
    linear-gradient(90deg,transparent 0 70px,#e5a6a0 70px 72px,transparent 72px),
    repeating-linear-gradient(0deg,transparent 0 27px,#cbd8df 27px 28px);
  box-shadow:inset 22px 0 36px rgba(93,76,60,.08);
}
:global(:root[data-theme='light']) .canvas-page::before {
  content:"";
  position:absolute;
  z-index:0;
  top:84px;
  bottom:24px;
  left:18px;
  width:24px;
  pointer-events:none;
  background:radial-gradient(circle,#837b72 0 3px,#ded8cc 3.5px 6px,transparent 6.5px) center top/24px 30px repeat-y;
}
:global(:root[data-theme='light']) .canvas-page > * { position:relative; z-index:1; }
:global(:root[data-theme='light']) .canvas-hero {
  border:1px solid #d6cec0;
  color:#302d29;
  background:
    repeating-linear-gradient(0deg,transparent 0 29px,rgba(132,165,182,.16) 29px 30px),
    #fffdf8;
  box-shadow:6px 9px 0 #d7d0c4,0 18px 38px rgba(75,63,51,.12);
}
:global(:root[data-theme='light']) .canvas-hero::after {
  content:"СВЕТЛЫЙ СКЕТЧБУК";
  position:absolute;
  right:18px;
  bottom:14px;
  color:#8f8478;
  font:700 9px/1 monospace;
  letter-spacing:.13em;
}
:global(:root[data-theme='light']) .tape { background:#efd27d; }
:global(:root[data-theme='light']) .canvas-hero span { color:#994c38; }
:global(:root[data-theme='light']) .canvas-hero p,
:global(:root[data-theme='light']) .latest-note { color:#5d554d; }
:global(:root[data-theme='light']) .canvas-add {
  border-color:#8c4938;
  color:#fff;
  background:#8c4938;
  box-shadow:3px 4px 0 #d4c8b9;
}
:global(:root[data-theme='light']) .canvas-filters button {
  opacity:1;
  border:1px solid rgba(53,46,40,.28);
  color:#2d2925;
  filter:saturate(.82);
  box-shadow:1px 2px 0 rgba(75,62,51,.16);
}
:global(:root[data-theme='light']) .canvas-filters button.active {
  outline:2px solid #3d3731;
  outline-offset:2px;
  filter:saturate(1.12);
}
:global(:root[data-theme='light']) .canvas-grid :deep(.post-card) {
  border-color:#fffdf8;
  color:#302d29;
  background:#fffdf8;
  box-shadow:6px 10px 18px rgba(74,62,50,.18);
}
:global(:root[data-theme='light']) .canvas-grid :deep(.post-card:hover) {
  border-color:#fff;
  background:#fff;
  box-shadow:9px 15px 26px rgba(74,62,50,.25);
}

:global(:root:not([data-theme='light'])) .canvas-page {
  position:relative;
  overflow:hidden;
  border:1px solid #4d3020;
  color:#f1dfc8;
  background-color:#1c100a;
  background-image:
    radial-gradient(circle at 55% -5%,rgba(255,183,87,.3),transparent 36%),
    repeating-linear-gradient(3deg,transparent 0 44px,rgba(121,76,46,.18) 45px 47px),
    linear-gradient(90deg,#140b07,#2b180e 48%,#160c08);
  box-shadow:inset 0 0 90px rgba(0,0,0,.64);
}
:global(:root:not([data-theme='light'])) .canvas-page::before {
  content:"";
  position:absolute;
  z-index:0;
  top:-90px;
  left:42%;
  width:310px;
  height:310px;
  border-radius:50%;
  pointer-events:none;
  background:radial-gradient(circle,rgba(255,210,137,.22),rgba(255,163,68,.07) 48%,transparent 70%);
}
:global(:root:not([data-theme='light'])) .canvas-page > * { position:relative; z-index:1; }
:global(:root:not([data-theme='light'])) .canvas-hero {
  border:1px solid #a98962;
  color:#382d24;
  background:#eadcc4;
  box-shadow:9px 15px 25px rgba(0,0,0,.58);
}
:global(:root:not([data-theme='light'])) .canvas-hero::after {
  content:"ВЕЧЕРНЯЯ МАСТЕРСКАЯ";
  position:absolute;
  right:18px;
  bottom:14px;
  color:#765f49;
  font:700 9px/1 monospace;
  letter-spacing:.13em;
}
:global(:root:not([data-theme='light'])) .tape { background:#b58c4c; }
:global(:root:not([data-theme='light'])) .canvas-hero span { color:#873f2e; }
:global(:root:not([data-theme='light'])) .canvas-hero p { color:#604e40; }
:global(:root:not([data-theme='light'])) .canvas-add {
  border-color:#4a3829;
  color:#2b2119;
  background:#e8b74f;
  box-shadow:3px 4px 0 rgba(0,0,0,.28);
}
:global(:root:not([data-theme='light'])) .latest-note { color:#d7b994; }
:global(:root:not([data-theme='light'])) .canvas-filters button {
  opacity:1;
  border:1px solid #21130c;
  color:#211813;
  filter:saturate(.74);
  box-shadow:2px 3px 0 rgba(0,0,0,.38);
}
:global(:root:not([data-theme='light'])) .canvas-filters button.active {
  outline:2px solid #f0d7b8;
  outline-offset:2px;
  filter:saturate(1.16);
}
:global(:root:not([data-theme='light'])) .canvas-grid :deep(.post-card) {
  border-color:#dfceb3;
  color:#352b23;
  background:#dfceb3;
  box-shadow:8px 14px 23px rgba(0,0,0,.56);
}
:global(:root:not([data-theme='light'])) .canvas-grid :deep(.post-card:hover) {
  border-color:#eee0c9;
  color:#30261f;
  background:#eee0c9;
  box-shadow:11px 18px 30px rgba(0,0,0,.65);
}
:global(:root:not([data-theme='light'])) .canvas-grid :deep(.post-author),
:global(:root:not([data-theme='light'])) .canvas-grid :deep(.post-desc),
:global(:root:not([data-theme='light'])) .canvas-grid :deep(.post-meta time) { color:#665549; }
:global(:root:not([data-theme='light'])) .canvas-grid :deep(.tag) {
  color:#352719;
  border-color:#ae8743;
  background:#d5ad59;
}
@media(max-width:650px){.canvas-page{margin:-8px;padding:12px}.canvas-hero{padding:30px 18px}.canvas-grid{grid-template-columns:1fr}}
</style>
