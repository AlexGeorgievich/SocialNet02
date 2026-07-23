<template>
  <footer class="app-footer">
    <div class="footer-inner">
      <span>Пользователей: <b>{{ stats.users }}</b></span>
      <span>Постов: <b>{{ stats.posts }}</b></span>
      <span>Промптов: <b>{{ stats.prompts }}</b></span>
      <router-link class="privacy-link" to="/privacy">Конфиденциальность</router-link>
      <button class="help-button" @click="helpOpen = true"><kbd>F1</kbd> Справочник</button>
    </div>
  </footer>

  <div v-if="helpOpen" class="help-overlay" @click.self="helpOpen = false">
    <section class="help-dialog glass-card" role="dialog" aria-modal="true" aria-labelledby="guide-title">
      <button class="help-close" @click="helpOpen = false">×</button>
      <header class="guide-header">
        <span class="guide-logo">✨</span>
        <div>
          <h2 id="guide-title">Справочник S-Art</h2>
          <p>Назначение и функциональные возможности</p>
        </div>
      </header>

      <div class="guide-content">
        <section>
          <h3>1. Назначение</h3>
          <p><b>S-Art</b> — социальная сеть для публикации визуальных работ, хранения промптов для генеративного ИИ, общения с авторами и создания личной коллекции.</p>
        </section>

        <section>
          <h3>2. Основная навигация</h3>
          <dl>
            <div><dt>Лента</dt><dd>Все опубликованные работы. Доступны фильтры по рубрикам и добавление в избранное.</dd></div>
            <div><dt>Исследовать</dt><dd>Переключение между работами и публичными промптами.</dd></div>
            <div><dt>Друзья</dt><dd>Входящие запросы, ссылки на профили и список принятых друзей.</dd></div>
            <div><dt>Избранное</dt><dd>Полные карточки сохранённых работ и промптов.</dd></div>
            <div><dt>Аватар</dt><dd>Переход в собственный профиль.</dd></div>
            <div><dt>⚙ Настройки</dt><dd>Имя, фамилия, статус, описание и аватар пользователя.</dd></div>
          </dl>
        </section>

        <section>
          <h3>3. Собственный профиль</h3>
          <p>Блок <b>«Добавить своё»</b> позволяет создавать два типа записей:</p>
          <ul>
            <li><b>Работа</b> — название, короткое описание, рубрика и изображение JPG, PNG, GIF, WebP или AVIF до 10 МБ.</li>
            <li><b>Промпт</b> — название, текст запроса, модель ИИ и признак публичности.</li>
          </ul>
          <p>На собственных карточках доступны команды <b>«Изменить»</b> и <b>«Удалить»</b>. После сохранения работа появляется в профиле и общей ленте.</p>
        </section>

        <section>
          <h3>4. Рубрики работ</h3>
          <p>Работы распределяются по рубрикам: <b>Иллюстрации</b>, <b>Персонажи</b>, <b>Городские сюжеты</b>, <b>Природа и пейзажи</b>, <b>Фэнтези</b>, <b>Портреты</b>, <b>Архитектура и интерьеры</b>, <b>Абстракция и эксперименты</b> и <b>Прочее</b>.</p>
        </section>

        <section>
          <h3>5. Избранное</h3>
          <p>Нажмите значок сердца на работе или промпте. Заполненное розовое сердце означает, что запись сохранена. Повторное нажатие удаляет её из избранного.</p>
        </section>

        <section>
          <h3>6. Друзья</h3>
          <ol>
            <li>Откройте профиль другого пользователя.</li>
            <li>Нажмите <b>«Добавить в друзья»</b>.</li>
            <li>Статус изменится на <b>«Запрос на добавление»</b>.</li>
            <li>Получатель увидит красный счётчик возле пункта «Друзья» и сможет принять или отклонить запрос.</li>
          </ol>
        </section>

        <section>
          <h3>7. Оформление и статистика</h3>
          <p>Переключатель в шапке меняет светлую и тёмную тему. Выбор сохраняется в браузере. Нижняя строка показывает актуальное количество пользователей, постов и промптов.</p>
        </section>

        <section v-if="auth.user?.role === 'admin'" class="admin-guide">
          <h3>8. Функции администратора</h3>
          <p>Раздел <b>«Администратор»</b> доступен только обладателям соответствующей роли.</p>
          <ul>
            <li>просмотр всех пользователей и переход к их профилям;</li>
            <li>назначение и снятие роли администратора;</li>
            <li>удаление пользователей и связанного контента;</li>
            <li>просмотр и удаление любых работ и промптов.</li>
          </ul>
        </section>

        <section>
          <h3>{{ auth.user?.role === 'admin' ? '9' : '8' }}. Горячие клавиши</h3>
          <div class="shortcut"><kbd>F1</kbd><span>Открыть или закрыть справочник</span></div>
          <div class="shortcut"><kbd>Esc</kbd><span>Закрыть справочник</span></div>
          <div class="shortcut"><kbd>Ctrl</kbd> + <kbd>F5</kbd><span>Полностью обновить приложение</span></div>
        </section>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import api from '../composables/useApi'
import { useAuthStore } from '../stores/auth'

const stats = reactive({ users: 0, posts: 0, prompts: 0 })
const helpOpen = ref(false)
const auth = useAuthStore()

async function loadStats() {
  const response = await api.get('/stats')
  Object.assign(stats, response.data)
}

function handleKey(event) {
  if (event.key === 'F1') {
    event.preventDefault()
    helpOpen.value = !helpOpen.value
  }
  if (event.key === 'Escape') helpOpen.value = false
}

onMounted(() => {
  loadStats()
  window.addEventListener('keydown', handleKey)
})
onBeforeUnmount(() => window.removeEventListener('keydown', handleKey))
</script>

<style scoped>
.app-footer { position: fixed; left: 0; right: 0; bottom: 0; z-index: 90; background: var(--header-bg); border-top: 1px solid var(--glass-border); backdrop-filter: blur(20px); }
.footer-inner { max-width: 1200px; height: 42px; margin: auto; padding: 0 24px; display: flex; align-items: center; gap: 24px; color: var(--text-secondary); font-size: 12px; }
.help-button { margin-left: auto; border: 0; background: transparent; color: var(--text-primary); cursor: pointer; }
.privacy-link { color: var(--text-secondary); text-decoration: none; white-space: nowrap; }
.privacy-link:hover { color: var(--accent-purple); }
kbd { padding: 2px 6px; border: 1px solid var(--glass-border); border-radius: 4px; background: var(--glass); }
.help-overlay { position: fixed; inset: 0; z-index: 300; display: grid; place-items: center; padding: 16px; background: rgba(0,0,0,.55); }
.help-dialog { width: min(760px, 100%); height: min(820px, calc(100dvh - 32px)); max-height: calc(100dvh - 32px); position: relative; display: flex; flex-direction: column; padding: 0; overflow: hidden; }
.guide-header { flex: 0 0 auto; display: flex; align-items: center; gap: 14px; padding: 24px 52px 18px 28px; border-bottom: 1px solid var(--glass-border); }
.guide-header h2 { margin: 0; }
.guide-header p { margin-top: 3px; color: var(--text-secondary); font-size: 13px; }
.guide-logo { font-size: 30px; }
.guide-content { flex: 1 1 auto; min-height: 0; overflow-y: auto; overscroll-behavior: contain; padding: 8px 28px 34px; scroll-behavior: smooth; scrollbar-gutter: stable; }
.guide-content section { padding: 17px 0; border-bottom: 1px solid var(--glass-border); }
.guide-content section:last-child { border-bottom: 0; }
.guide-content h3 { margin-bottom: 9px; font-size: 16px; color: var(--accent-purple); }
.guide-content p, .guide-content li, .guide-content dd { color: var(--text-secondary); font-size: 13px; line-height: 1.6; }
.guide-content ul, .guide-content ol { padding-left: 22px; margin-top: 8px; }
.guide-content dl div { display: grid; grid-template-columns: 120px 1fr; gap: 12px; padding: 6px 0; }
.guide-content dt { color: var(--text-primary); font-weight: 600; font-size: 13px; }
.admin-guide { background: rgba(245, 158, 11, .06); margin: 0 -12px; padding-left: 12px !important; padding-right: 12px !important; border-radius: 10px; }
.shortcut { display: flex; align-items: center; gap: 8px; margin: 8px 0; color: var(--text-secondary); font-size: 13px; }
.help-close { position: absolute; top: 10px; right: 14px; border: 0; background: transparent; color: var(--text-primary); font-size: 28px; cursor: pointer; }
@media (max-width: 760px) { .footer-inner { gap: 10px; padding: 0 12px; } .footer-inner > span { display: none; } .privacy-link { margin-right: auto; } .help-button { margin-left: 0; } .help-overlay { padding: 8px; } .help-dialog { height: calc(100dvh - 16px); max-height: calc(100dvh - 16px); } .guide-content { padding-left: 18px; padding-right: 18px; padding-bottom: 28px; } .guide-header { padding-left: 18px; padding-right: 48px; } .guide-content dl div { grid-template-columns: 1fr; gap: 2px; } }
</style>
