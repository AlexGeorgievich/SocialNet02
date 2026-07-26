<template>
  <section class="canvas-page">
    <DesignSwitcher />

    <div class="studio-tools" aria-hidden="true">
      <span class="pencil pencil-one"></span>
      <span class="pencil pencil-two"></span>
      <span class="brush"></span>
      <span class="paint-dot dot-one"></span>
      <span class="paint-dot dot-two"></span>
      <span class="paint-dot dot-three"></span>
    </div>

    <header class="canvas-hero">
      <div class="binding" aria-hidden="true"></div>
      <div class="tape" aria-hidden="true"></div>
      <span>Творческий альбом S-Art</span>
      <h1>Живой холст</h1>
      <p>Эскизы, готовые работы и визуальные истории художников.</p>
      <router-link to="/profile" class="canvas-add">＋ Добавить на холст</router-link>
    </header>

    <div class="section-caption">
      <div>
        <b>Последние работы</b>
        <span>Новые листы сверху</span>
      </div>
      <i aria-hidden="true"></i>
    </div>

    <div class="canvas-filters">
      <button
        v-for="(item,index) in categories"
        :key="item.value"
        :class="{ active: activeCategory === item.value }"
        :style="{ '--tab': tabColors[index % tabColors.length] }"
        @click="activeCategory = item.value"
      >{{ item.label }}</button>
    </div>

    <div v-if="postsStore.loading" class="design-state">Раскладываем работы на холсте…</div>
    <div v-else-if="!postsStore.posts.length" class="design-state">На этой странице альбома пока пусто.</div>
    <div v-else class="canvas-grid">
      <PostCard
        v-for="(post,index) in postsStore.posts"
        :key="post.id"
        :post="post"
        :class="`tilt-${index % 3}`"
        :favorited="favoritesStore.isFavorited(post.id, 'post')"
        @favorite="toggleFavorite"
      />
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
const tabColors = ['#ef8b68', '#82aaa0', '#c99acb', '#e0b85e', '#829ac8']
const { postsStore, favoritesStore, activeCategory, toggleFavorite } = useDesignFeed()
const { saveDesign } = useDesignPreference()

onMounted(() => saveDesign('canvas'))
</script>

<style scoped>
.canvas-page {
  --desk: #e6e0d7;
  --desk-line: #d4ccc1;
  --paper: #fffdf7;
  --paper-raised: #fff;
  --ink: #292725;
  --muted-ink: #625c55;
  --edge: #c9c0b4;
  --shadow: rgba(54, 46, 39, .2);
  --accent: #9a452f;
  --accent-contrast: #fff;
  --tape: #efcd75;
  --tool: #34302d;
  position: relative;
  min-height: calc(100vh - 170px);
  margin: -16px;
  padding: 26px;
  overflow: hidden;
  border: 1px solid var(--edge);
  border-radius: 18px;
  color: var(--ink);
  background-color: var(--desk);
  background-image:
    linear-gradient(var(--desk-line) 1px, transparent 1px),
    linear-gradient(90deg, var(--desk-line) 1px, transparent 1px);
  background-size: 28px 28px;
  opacity: 1;
  filter: none;
  isolation: isolate;
  color-scheme: light;
}

.canvas-page > * { position: relative; z-index: 2; }

.studio-tools {
  position: absolute;
  inset: 80px 0 auto auto;
  z-index: 1;
  width: 240px;
  height: 210px;
  pointer-events: none;
}

.pencil, .brush {
  position: absolute;
  display: block;
  width: 150px;
  height: 12px;
  border-radius: 8px 2px 2px 8px;
  background: var(--tool);
  box-shadow: 0 7px 12px var(--shadow);
  transform-origin: right center;
}
.pencil::after, .brush::after {
  content: "";
  position: absolute;
  right: -18px;
  border-top: 6px solid transparent;
  border-bottom: 6px solid transparent;
  border-left: 18px solid #c6a77c;
}
.pencil-one { top: 35px; right: -25px; background: #b94b3b; transform: rotate(-18deg); }
.pencil-two { top: 80px; right: -12px; background: #315c78; transform: rotate(-31deg); }
.brush { top: 128px; right: -24px; height: 9px; background: #49362a; transform: rotate(-12deg); }
.paint-dot { position: absolute; width: 17px; height: 13px; border-radius: 65% 40% 70% 35%; }
.dot-one { top: 160px; right: 84px; background:#c84e3c; }
.dot-two { top: 178px; right: 55px; background:#e0aa31; }
.dot-three { top: 154px; right: 32px; background:#39788b; }

.canvas-hero {
  position: relative;
  max-width: 780px;
  margin: 24px auto 34px;
  padding: 40px 48px 38px 76px;
  text-align: center;
  border: 1px solid var(--edge);
  background:
    repeating-linear-gradient(0deg, transparent 0 29px, rgba(90,125,165,.13) 29px 30px),
    var(--paper);
  box-shadow: 8px 12px 0 var(--shadow);
  transform: rotate(-.35deg);
}
.binding {
  position: absolute;
  top: 18px;
  bottom: 18px;
  left: 20px;
  width: 20px;
  background: radial-gradient(circle, var(--desk) 0 4px, var(--edge) 4.5px 6px, transparent 6.5px) center top / 20px 28px repeat-y;
}
.tape {
  position: absolute;
  top: -14px;
  left: 54%;
  width: 110px;
  height: 29px;
  background: var(--tape);
  clip-path: polygon(3% 7%, 100% 0, 96% 94%, 0 100%);
  transform: translateX(-50%) rotate(1.5deg);
}
.canvas-hero > span { color: var(--accent); font-size: 11px; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; }
.canvas-hero h1 { margin: 12px 0 8px; font-family: "Segoe Print","Comic Sans MS",cursive; font-size: clamp(42px,7vw,72px); line-height: 1; }
.canvas-hero p { color: var(--muted-ink); font-family: Georgia,serif; font-style: italic; }
.canvas-add { display:inline-block; margin-top:22px; padding:11px 17px; border:2px solid var(--accent); color:var(--accent-contrast); background:var(--accent); font-weight:750; text-decoration:none; box-shadow:3px 4px 0 var(--shadow); transform:rotate(.7deg); }

.section-caption { display:flex; align-items:end; gap:14px; margin:0 4px 12px; }
.section-caption div { display:flex; flex-direction:column; gap:3px; }
.section-caption b { font-family:"Segoe Print","Comic Sans MS",cursive; font-size:15px; }
.section-caption span { color:var(--muted-ink); font:italic 12px Georgia,serif; }
.section-caption i { flex:1; height:1px; margin-bottom:5px; background:var(--edge); }

.canvas-filters { display:flex; flex-wrap:wrap; gap:8px; padding:0 0 30px; }
.canvas-filters button { padding:9px 13px; border:1px solid color-mix(in srgb, var(--tab), var(--ink) 32%); border-radius:2px 3px 9px 3px; color:#241f1b; background:var(--tab); font:700 12px inherit; cursor:pointer; box-shadow:1px 2px 0 var(--shadow); }
.canvas-filters button:hover { transform:translateY(-2px) rotate(-.5deg); }
.canvas-filters button.active { outline:2px solid var(--ink); outline-offset:2px; transform:translateY(-2px) rotate(-.7deg); }

.canvas-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(250px,1fr)); gap:32px 24px; padding:10px; }
.canvas-grid :deep(.post-card) { border:10px solid var(--paper); border-bottom-width:20px; border-radius:1px; color:var(--ink); background:var(--paper); box-shadow:7px 11px 18px var(--shadow); backdrop-filter:none; }
.canvas-grid :deep(.post-card:hover) { border-color:var(--paper-raised); background:var(--paper-raised); box-shadow:10px 16px 28px var(--shadow); transform:rotate(0) translateY(-5px); }
.canvas-grid :deep(.tilt-0) { transform:rotate(-1.2deg); }
.canvas-grid :deep(.tilt-1) { transform:rotate(.9deg); }
.canvas-grid :deep(.tilt-2) { transform:rotate(-.4deg); }
.canvas-grid :deep(.post-image-wrap) { aspect-ratio:4/3; background:var(--edge); }
.canvas-grid :deep(.post-title) { font-family:"Segoe Print","Comic Sans MS",cursive; }
.canvas-grid :deep(.post-author),
.canvas-grid :deep(.post-desc),
.canvas-grid :deep(.post-meta time) { color:var(--muted-ink); }
.canvas-grid :deep(.tag) { color:#3d3027; border:1px solid #c6a45d; background:#efd68f; }
.design-state { padding:70px 20px; color:var(--muted-ink); text-align:center; }

:global(:root:not([data-theme='light'])) .canvas-page {
  --desk: #211711;
  --desk-line: #34231a;
  --paper: #eadfc9;
  --paper-raised: #f5ead5;
  --ink: #302720;
  --muted-ink: #65574b;
  --edge: #6f503b;
  --shadow: rgba(0, 0, 0, .52);
  --accent: #bd5b3f;
  --accent-contrast: #fff8ed;
  --tape: #b78b42;
  --tool: #d2b28a;
  background-image:
    radial-gradient(circle at 72% 3%, rgba(255,186,91,.22), transparent 31%),
    repeating-linear-gradient(4deg, transparent 0 46px, rgba(114,75,50,.16) 47px 48px),
    linear-gradient(90deg, #1b120d, var(--desk) 48%, #190f0b);
  color-scheme: dark;
}
:global(:root:not([data-theme='light'])) .canvas-page::after {
  content:"";
  position:absolute;
  z-index:0;
  inset:0;
  pointer-events:none;
  background:radial-gradient(circle at 52% 15%, transparent 0 20%, rgba(9,5,3,.22) 70%, rgba(5,3,2,.5) 100%);
}
:global(:root:not([data-theme='light'])) .canvas-hero { background:repeating-linear-gradient(0deg,transparent 0 29px,rgba(88,112,135,.16) 29px 30px),var(--paper); box-shadow:10px 16px 24px rgba(0,0,0,.55); }
:global(:root:not([data-theme='light'])) .section-caption b { color:#f2dfc6; }
:global(:root:not([data-theme='light'])) .section-caption span { color:#c8ad91; }
:global(:root:not([data-theme='light'])) .section-caption i { background:#6d4d38; }
:global(:root:not([data-theme='light'])) .canvas-filters button.active { outline-color:#f2dfc6; }

@media(max-width:650px) {
  .canvas-page { margin:-8px; padding:12px; }
  .studio-tools { display:none; }
  .canvas-hero { padding:36px 20px 30px 52px; }
  .canvas-grid { grid-template-columns:1fr; }
}
</style>
