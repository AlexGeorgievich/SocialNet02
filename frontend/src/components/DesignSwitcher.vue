<template>
  <nav class="design-switcher" aria-label="Выбор дизайна S-Art">
    <span class="switcher-label">Design Lab</span>
    <router-link to="/" @click="saveDesign('classic')">Классический</router-link>
    <router-link to="/ui/gallery" @click="saveDesign('gallery')">Галерея</router-link>
    <router-link to="/ui/neo" @click="saveDesign('neo')">Neo-Art</router-link>
    <router-link to="/ui/canvas" @click="saveDesign('canvas')">Холст</router-link>
  </nav>
</template>

<script setup>
import { useDesignPreference } from '../composables/useDesignPreference'
const { saveDesign } = useDesignPreference()
</script>

<style scoped>
.design-switcher {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 24px;
  padding: 8px;
  overflow-x: auto;
  border: 1px solid rgba(128, 112, 150, .2);
  border-radius: 12px;
  background: rgba(18, 14, 25, .82);
  box-shadow: 0 10px 35px rgba(0, 0, 0, .18);
}
.switcher-label {
  padding: 0 10px;
  color: #a99bb7;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: .12em;
  text-transform: uppercase;
  white-space: nowrap;
}
a {
  flex: 0 0 auto;
  padding: 8px 13px;
  border-radius: 8px;
  color: #c9bed7;
  font-size: 12px;
  font-weight: 650;
  text-decoration: none;
}
a:hover { color: #fff; background: rgba(255,255,255,.08); }
a.router-link-exact-active {
  color: #fff;
  background: linear-gradient(135deg, #7c3aed, #db2777);
}
:global(:root[data-theme='light']) .design-switcher {
  border-color: rgba(67, 48, 78, .16);
  background: rgba(255, 252, 247, .9);
  box-shadow: 0 10px 30px rgba(70, 50, 80, .1);
}
:global(:root[data-theme='light']) .switcher-label { color: #74667c; }
:global(:root[data-theme='light']) a { color: #5f5268; }
:global(:root[data-theme='light']) a:hover { color: #251d2b; background: rgba(70,45,80,.08); }
:global(:root[data-theme='light']) a.router-link-exact-active { color: #fff; }
@media (max-width: 600px) {
  .switcher-label { display: none; }
}
</style>
