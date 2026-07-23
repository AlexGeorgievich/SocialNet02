# S-Art SocialNet02

S-Art — демонстрационная социальная сеть для авторов визуальных работ и
пользователей генеративного ИИ. Вторая архитектурная версия проекта работает в
Docker, использует PostgreSQL для постоянных данных, Redis для кеширования,
FastAPI для REST API и Vue/Nginx для пользовательского интерфейса.

Репозиторий: <https://github.com/AlexGeorgievich/SocialNet02>

## Основные возможности

- регистрация и JWT-авторизация;
- обязательное согласие на обработку персональных данных;
- демонстрационный и рабочий контуры;
- профили, аватары и настройки пользователей;
- публикация, редактирование и удаление работ;
- рубрики и фильтрация ленты;
- увеличение изображения по щелчку;
- хранение и копирование промптов;
- избранное с отметкой в виде сердца;
- запросы в друзья, принятие и удаление связей;
- светлая и тёмная темы;
- административная роль;
- встроенная справка по `F1`;
- фиксированные шапка и футер;
- статистика пользователей, работ и промптов;
- русскоязычный интерфейс и UTF-8-логи.

## Архитектура второй версии

```text
Браузер
   │
   ▼
Nginx :5173
   ├── Vue SPA
   ├── /api/*     ───────────────┐
   └── /uploads/* ───────────┐   │
                            ▼   ▼
                     FastAPI :8000
                     2 Uvicorn worker
                        │       │
                        ▼       ▼
                  PostgreSQL   Redis
                  ├─ sart_demo ├─ лента
                  └─ sart_work ├─ промпты
                               └─ статистика
```

В состав Docker Compose входят:

| Сервис | Назначение |
|---|---|
| `frontend` | Production-сборка Vue и Nginx |
| `backend` | FastAPI и Uvicorn |
| `postgres` | Две изолированные базы данных |
| `redis` | Кеш API с AOF |

Постоянные данные находятся в Docker volumes:

- `sart_postgres_data`;
- `sart_redis_data`;
- `sart_uploads_data`.

## Демо и рабочий режимы

Переключатель находится в фиксированном футере приложения.

### Демо

- база PostgreSQL `sart_demo`;
- автоматически заполняется при старте backend;
- содержит тестовых пользователей, работы, промпты и связи;
- предназначена для презентации и проверки функций.

### Рабочий

- база PostgreSQL `sart_work`;
- при первом запуске остаётся пустой;
- предназначена для регистрации новых пользователей;
- не смешивается с демонстрационными данными.

Frontend хранит отдельный JWT для каждого режима. Токен содержит название
контура, поэтому демо-токен нельзя применить к рабочей базе и наоборот.

## Технологии

### Frontend

- Vue 3;
- Vue Router;
- Pinia;
- Axios;
- Vite 8;
- Nginx 1.27.

### Backend

- Python 3.13;
- FastAPI 0.115;
- Uvicorn;
- SQLAlchemy 2;
- Pydantic 2;
- PostgreSQL 16;
- Psycopg 3;
- Redis 7;
- JWT и bcrypt.

### Инфраструктура

- Docker;
- Docker Compose;
- healthcheck каждого сервиса;
- именованные volumes;
- отдельная backend-сеть;
- UTF-8-конфигурация PostgreSQL и логов.

## Структура

```text
SocialNet02/
├── compose.yaml
├── .env.example
├── .dockerignore
├── README.md
├── Plan.md
├── docker/
│   └── postgres/
│       └── init.sql
├── backend/
│   ├── Dockerfile
│   ├── docker-entrypoint.sh
│   ├── uvicorn-log-config.json
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── seed.py
│   ├── requirements.txt
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   │   ├── auth.py
│   │   ├── cache.py
│   │   └── upload.py
│   └── uploads/demo/
└── frontend/
    ├── Dockerfile
    ├── nginx.conf
    ├── package.json
    └── src/
        ├── components/
        ├── composables/
        ├── router/
        ├── stores/
        └── views/
```

## Требования

Рекомендуется:

- Docker Desktop;
- Docker Compose v2+;
- не менее 4 ГБ свободной памяти;
- свободные порты `5173` и `8000`;
- интернет для первой загрузки образов и внешних Pexels-фотографий.

Проверка:

```powershell
docker --version
docker compose version
docker info
```

## Быстрый запуск

### 1. Подготовка окружения

Windows:

```powershell
Copy-Item .env.example .env
```

Linux/macOS:

```bash
cp .env.example .env
```

Перед публичным размещением измените в `.env`:

```dotenv
JWT_SECRET=длинное-случайное-значение
POSTGRES_PASSWORD=длинный-случайный-пароль
```

### 2. Сборка и запуск

```powershell
docker compose up -d --build
```

Первый запуск:

1. создаёт volumes и сеть;
2. запускает PostgreSQL и Redis;
3. создаёт базы `sart_demo` и `sart_work`;
4. создаёт таблицы;
5. заполняет демонстрационную базу;
6. запускает два Uvicorn worker;
7. запускает Nginx с Vue SPA.

### 3. Проверка

```powershell
docker compose ps
```

Все четыре сервиса должны иметь статус `healthy`.

Адреса:

- приложение: <http://localhost:5173>;
- API: <http://localhost:8000>;
- Swagger UI: <http://localhost:8000/docs>;
- healthcheck: <http://localhost:8000/api/health>.

Ответ healthcheck:

```json
{
  "status": "ok",
  "database": "ok",
  "cache": "ok"
}
```

## Управление контейнерами

Просмотр журналов:

```powershell
docker compose logs -f
docker compose logs -f backend
docker compose logs -f postgres
```

Перезапуск:

```powershell
docker compose restart
```

Пересборка после изменения исходников:

```powershell
docker compose up -d --build
```

Остановка с сохранением данных:

```powershell
docker compose down
```

Полный сброс:

```powershell
docker compose down -v
docker compose up -d --build
```

Команда `down -v` удаляет обе базы, Redis и загруженные пользователями файлы.

## Тестовые аккаунты

Перед входом выберите режим `Демо`.

| Пользователь | Email | Пароль | Роль |
|---|---|---|---|
| q q | `q@q.com` | `tester` | Администратор |
| Анна Новак | `akari@demo.local` | `demo123` | Пользователь |
| Мария Коста | `mio@demo.local` | `demo123` | Пользователь |
| Юки Мори | `yuki@demo.local` | `demo123` | Пользователь |
| Клара Мартин | `rin@demo.local` | `demo123` | Пользователь |
| Хана Ито | `hana@demo.local` | `demo123` | Пользователь |
| Елена Росси | `elena.rossi@demo.local` | `demo123` | Пользователь |
| Лукас Майер | `lucas.meyer@demo.local` | `demo123` | Пользователь |
| Софи Дюбуа | `sophie.dubois@demo.local` | `demo123` | Пользователь |
| Ноа Ван Дейк | `noah.vandijk@demo.local` | `demo123` | Пользователь |

Это публичные демонстрационные реквизиты. Их нельзя использовать как реальные
production-пароли.

## Основные пользовательские сценарии

### Публикация работы

1. Войдите в аккаунт.
2. Откройте собственный профиль.
3. В блоке «Добавить своё» нажмите `+ Работа`.
4. Укажите название, описание и рубрику.
5. Выберите изображение до 10 МБ.
6. Нажмите «Сохранить».

Форматы: JPG, JPEG, PNG, GIF, WebP и AVIF.

### Промпт

В собственном профиле нажмите `+ Промпт`, укажите название, текст, модель и
признак публичности. Собственные промпты можно изменять и удалять, публичные —
копировать.

### Друзья

Откройте профиль другого пользователя и нажмите «Добавить в друзья». Получатель
увидит запрос в разделе «Друзья» и сможет принять или отклонить его.

### Избранное

Нажмите сердце на карточке. Заполненное сердце означает, что объект сохранён.
Повторное нажатие удаляет его из избранного.

### Справка

Клавиша `F1` или кнопка в футере открывает справочник. `Esc` закрывает окно.

## Рубрики

- Иллюстрации;
- Персонажи;
- Городские сюжеты;
- Природа и пейзажи;
- Фэнтези;
- Портреты;
- Архитектура и интерьеры;
- Абстракция и эксперименты;
- Прочее.

## Redis-кеш

Кешируются:

- списки работ;
- списки промптов;
- статистика футера.

Ключ содержит режим приложения и параметры фильтра. TTL по умолчанию — 30
секунд. После регистрации, создания, изменения или удаления контента кеш
инвалидируется.

Redis работает в режиме `allkeys-lru` с ограничением 256 МБ и AOF. Если Redis
недоступен, backend регистрирует предупреждение и продолжает читать данные из
PostgreSQL.

Настройки:

```dotenv
REDIS_URL=redis://redis:6379/0
CACHE_TTL_SECONDS=30
```

## Производительность

Контрольный локальный тест кешированной ленты после перехода на PostgreSQL,
Redis, устранения N+1 и запуска двух workers:

| Параллельность | RPS | p50 | p95 | Ошибки |
|---:|---:|---:|---:|---:|
| 10 | 216 | 44 мс | 74 мс | 0 |
| 30 | 243 | 120 мс | 153 мс | 0 |

Тест состоял из двух серий по 500 запросов к `/api/posts`. Результат относится
к конкретному компьютеру и короткому тесту; он не является production-SLA.

До переработки лента обеспечивала примерно 23 RPS, поэтому наблюдаемое улучшение
составляет около десяти раз.

## API

Основные маршруты:

| Маршрут | Назначение |
|---|---|
| `POST /api/auth/register` | Регистрация |
| `POST /api/auth/login` | Вход |
| `GET /api/auth/me` | Текущий пользователь |
| `GET/POST /api/posts` | Лента и создание работы |
| `PUT/DELETE /api/posts/{id}` | Изменение и удаление |
| `GET/POST /api/prompts` | Промпты |
| `GET/POST/DELETE /api/favorites` | Избранное |
| `GET/POST/PUT/DELETE /api/friends` | Друзья |
| `GET /api/stats` | Статистика |
| `/api/admin/*` | Администрирование |

Frontend добавляет к запросам:

```http
Authorization: Bearer <JWT>
X-S-Art-Mode: demo
```

Значение режима: `demo` или `work`.

## Переменные окружения

| Переменная | Назначение |
|---|---|
| `POSTGRES_USER` | Пользователь PostgreSQL |
| `POSTGRES_PASSWORD` | Пароль PostgreSQL |
| `DEMO_DATABASE_URL` | Подключение к demo-базе |
| `WORK_DATABASE_URL` | Подключение к work-базе |
| `REDIS_URL` | Подключение к Redis |
| `CACHE_TTL_SECONDS` | TTL кеша |
| `JWT_SECRET` | Подпись JWT |
| `CORS_ORIGINS` | Разрешённые frontend origin |
| `WEB_CONCURRENCY` | Число Uvicorn workers |
| `SEED_DEMO_DATA` | Автозаполнение demo |

## Резервное копирование

Рабочая база:

```powershell
docker compose exec -T postgres pg_dump -U sart -d sart_work -Fc > sart_work.dump
```

Демо-база:

```powershell
docker compose exec -T postgres pg_dump -U sart -d sart_demo -Fc > sart_demo.dump
```

Изображения находятся в volume `sart_uploads_data` и должны резервироваться
отдельно.

## Диагностика

### Docker Engine недоступен

Запустите Docker Desktop и проверьте:

```powershell
docker info
```

### Контейнер не стал healthy

```powershell
docker compose ps
docker compose logs --tail=100 backend
docker compose logs --tail=100 postgres
docker compose logs --tail=100 redis
```

### Порт занят

```powershell
netstat -ano | Select-String ':5173|:8000'
```

Остановите старый локальный Vite/Uvicorn или измените опубликованные порты в
`compose.yaml`.

### Демо-данные не появились

```powershell
docker compose exec backend python seed.py
```

Проверьте, что `SEED_DEMO_DATA=true`.

### Redis недоступен

```powershell
docker compose exec redis redis-cli ping
```

Ожидаемый ответ: `PONG`.

### Проверка баз

```powershell
docker compose exec postgres psql -U sart -d sart_demo -c "SELECT COUNT(*) FROM users;"
docker compose exec postgres psql -U sart -d sart_work -c "SELECT COUNT(*) FROM users;"
```

## Безопасность

Текущая версия предназначена для демонстрации и локальной разработки. Перед
публичным production-запуском необходимо:

- заменить все значения `.env`;
- включить HTTPS;
- убрать публичные тестовые пароли;
- использовать внешний Secret Manager;
- внедрить Alembic;
- усилить проверку файлов;
- добавить rate limiting;
- реализовать refresh-токены и отзыв сессий;
- настроить резервное копирование;
- указать фактические реквизиты оператора персональных данных;
- провести security review.

SQLite-файл сохранён только как исторический fallback для ручной разработки.
Основная архитектура SocialNet02 — PostgreSQL и Redis в Docker Compose.
