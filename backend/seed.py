"""Idempotent demo data generator for S-Art."""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from database import Base, SessionLocal, engine
from models import Favorite, Friendship, Post, Prompt, User
from services.auth import hash_password


DEMO_PASSWORD = "demo123"
DEMO_USERS = [
    ("akari@demo.local", "Анна", "Новак", "Люблю яркий арт", "online"),
    ("mio@demo.local", "Мария", "Коста", "Рисую свет и природу", "online"),
    ("yuki@demo.local", "Юки", "Мори", "Люблю сказки", "offline"),
    ("rin@demo.local", "Клара", "Мартин", "Дизайнер персонажей", "online"),
    ("hana@demo.local", "Хана", "Ито", "Собираю промпты", "offline"),
    ("elena.rossi@demo.local", "Елена", "Росси", "Снимаю Италию", "online"),
    ("lucas.meyer@demo.local", "Лукас", "Майер", "Люблю старые города", "offline"),
    ("sophie.dubois@demo.local", "Софи", "Дюбуа", "Парижская фотография", "online"),
    ("noah.vandijk@demo.local", "Ноа", "Ван Дейк", "Город и вода", "offline"),
]

POSTS = [
    ("akari@demo.local", "Неоновая модель", "Портрет в розово-бирюзовом свете", "portrait", "tokyo", "#7c3aed", "#ec4899"),
    ("mio@demo.local", "Белая сакура", "Цветы на весеннем солнце", "nature", "garden", "#f472b6", "#fbbf24"),
    ("yuki@demo.local", "У неоновой вывески", "Контрастный ночной портрет", "portrait", "ice", "#2563eb", "#67e8f9"),
    ("rin@demo.local", "Вывески ночного Токио", "Японские рестораны после заката", "maid", "coffee", "#92400e", "#f59e0b"),
    ("hana@demo.local", "Лестница в переулке", "Ночной японский квартал", "maid", "maid", "#6d28d9", "#f9a8d4"),
    ("akari@demo.local", "Синий портрет", "Мужчина в кинематографическом свете", "portrait", "space", "#312e81", "#a855f7"),
    ("mio@demo.local", "Красный зонт", "Дождь под цветущей сакурой", "nature", "rain", "#1e3a8a", "#64748b"),
    ("yuki@demo.local", "Сакура в переулке", "Тихая городская улица", "maid", "forest", "#14532d", "#84cc16"),
    ("rin@demo.local", "Тёплый неон", "Портрет в янтарно-бирюзовом свете", "portrait", "comet", "#be185d", "#8b5cf6"),
    ("hana@demo.local", "Пурпурный профиль", "Портрет в ночных огнях", "portrait", "alchemy", "#4c1d95", "#fb7185"),
    ("akari@demo.local", "Вечерний Синдзюку", "Городская улица в синий час", "maid", "festival", "#dc2626", "#fbbf24"),
    ("mio@demo.local", "Поезд среди сакуры", "Весна в японском пригороде", "maid", "ocean", "#0891b2", "#c4b5fd"),
]

# Fixed free-to-use Pexels photos. Source pages use the same numeric photo IDs.
STOCK_PHOTO_IDS = [
    33034116, 36766267, 8790397, 20392882, 35637731, 31428951,
    31459052, 21838504, 28879242, 34939489, 37126958, 32118622,
]

PROMPTS = [
    ("akari@demo.local", "Неоновая героиня", "Героиня в неоновом Токио", "Стабильная диффузия", ["аниме", "город"]),
    ("mio@demo.local", "Мягкий портрет", "Портрет в утреннем свете", "Миджорни", ["портрет", "пастель"]),
    ("yuki@demo.local", "Ледяное королевство", "Маг в ледяном дворце", "ДАЛЛ-И", ["сказка", "магия"]),
    ("rin@demo.local", "Дизайн персонажа", "Лист образов персонажа", "Стабильная диффузия", ["дизайн", "герой"]),
    ("hana@demo.local", "Уютное кафе", "Тёплое японское кафе", "Миджорни", ["интерьер", "уют"]),
    ("akari@demo.local", "Космическая опера", "Капитан на звездолёте", "ДАЛЛ-И", ["космос", "фантастика"]),
    ("mio@demo.local", "Город после дождя", "Улица после дождя", "Стабильная диффузия", ["дождь", "город"]),
    ("yuki@demo.local", "Дух леса", "Хранитель древнего леса", "Миджорни", ["лес", "природа"]),
]

Q_POSTS = [
    ("Неоновый квартал", "Ночной Токио с высоты", "maid", "first-art", "#2563eb", "#a855f7"),
    ("Ночной переулок", "Фонари и рестораны Токио", "maid", "night-hero", "#111827", "#db2777"),
    ("Дождливый Токио", "Зонты и мокрый асфальт", "maid", "tea-story", "#92400e", "#f59e0b"),
    ("Неон Акихабары", "Витрины и прохожие ночью", "maid", "maid-lu", "#6d28d9", "#f472b6"),
    ("Террасы в горах", "Зелёные рисовые поля в утреннем свете", "nature", "terraces", "#166534", "#a3e635"),
]

Q_STOCK_IMAGES = [
    "01-neon-tokyo.jpg", "02-tokyo-night.jpg",
    "03-rainy-tokyo.jpg", "04-vibrant-night.jpg",
    "11-user-terraces.jpg",
]

CATEGORY_MOCKS = [
    ("akari@demo.local", "Тропическая лагуна", "Бирюзовая вода", "nature", "09-ocean.jpg"),
    ("rin@demo.local", "Ледяная невеста", "Героиня тёмной сказки", "fantasy", "08-fantasy-cosplay.jpg"),
    ("mio@demo.local", "Изумрудный портрет", "Яркий макияж", "portrait", "07-fantasy-costume.jpg"),
    ("yuki@demo.local", "Сакура у домов", "Весенний квартал", "architecture", "05-sakura-city.jpg"),
    ("hana@demo.local", "Весенний перекрёсток", "Сакура на солнечной городской улице", "architecture", "06-sakura-street.jpg"),
]

# Verified free-to-use Pexels images cover categories that are not represented
# by the local demo-photo set. "other" intentionally remains the last category.
CATEGORY_COVERAGE_MOCKS = [
    ("akari@demo.local", "Цветовой портрет", "Иллюстрация маркерами на рабочем столе", "artwork",
     28892332),
    ("rin@demo.local", "Героиня фестиваля", "Детализированный образ персонажа", "waifu",
     17800015),
    ("sophie.dubois@demo.local", "Цветовой поток", "Фактурная абстрактная живопись", "abstract",
     1988692),
    ("lucas.meyer@demo.local", "Лис в осеннем лесу", "Рыжий лис среди золотых листьев", "animals",
     34590366),
    ("elena.rossi@demo.local", "Классический натюрморт", "Фрукты и керамика в мягком свете", "food",
     36913055),
    ("noah.vandijk@demo.local", "Цифровой код", "Программный код и человек в потоке данных", "technology",
     3861969),
    ("hana@demo.local", "Творческий блокнот", "Свободный визуальный эксперимент", "other",
     34790848),
]

LEGACY_CATEGORY_TITLES = {
    "Зелёные террасы", "Морская принцесса", "Синяя героиня",
    "Квартал ночью", "Тихий переулок", "Неоновые линии",
    "Городские отражения",
}

EUROPE_POSTS = [
    ("sophie.dubois@demo.local", "Улица Парижа", "Классические фасады", "architecture", 33645279),
    ("elena.rossi@demo.local", "Вечер в Комо", "Итальянский переулок", "architecture", 30464954),
    ("noah.vandijk@demo.local", "Канал Амстердама", "Вода и старые дома", "nature", 16092979),
    ("lucas.meyer@demo.local", "Солнечный Амстердам", "Лодки у набережной", "architecture", 18936486),
]

Q_PROMPTS = [
    ("Синий портрет", "Портрет в синем свете", "Стабильная диффузия", ["портрет", "свет"]),
    ("Ночной город", "Город ночью, яркие огни", "Миджорни", ["город", "ночь"]),
    ("Тёплый вечер", "Уютная комната вечером", "ДАЛЛ-И", ["уют", "интерьер"]),
]


def get_or_create_user(db, email, first_name, last_name, description, status):
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.first_name, user.last_name = first_name, last_name
        user.description, user.status = description, status
        return user
    user = User(email=email, password_hash=hash_password(DEMO_PASSWORD), first_name=first_name,
                last_name=last_name, description=description, status=status)
    db.add(user)
    db.flush()
    return user


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        users = {item[0]: get_or_create_user(db, *item) for item in DEMO_USERS}
        demo_admin = db.query(User).filter(User.email == "q@q.com").first()
        if not demo_admin:
            demo_admin = User(
                email="q@q.com",
                password_hash=hash_password("tester"),
                first_name="q",
                last_name="q",
                description="Администратор демонстрационного пространства",
                status="online",
                role="admin",
                privacy_consent=True,
                privacy_consent_version="2026-07-23",
                privacy_consent_at=datetime.now(timezone.utc),
            )
            db.add(demo_admin)
            db.flush()
        else:
            demo_admin.role = "admin"
        upload_dir = Path(__file__).parent / "uploads" / "demo"
        category_upload_dir = upload_dir / "categories"

        if category_upload_dir.exists():
            for placeholder in category_upload_dir.glob("*.svg"):
                placeholder.unlink()

        for index, (email, title, description, category, slug, c1, c2) in enumerate(POSTS):
            photo_id = STOCK_PHOTO_IDS[index]
            image_url = f"https://images.pexels.com/photos/{photo_id}/pexels-photo-{photo_id}.jpeg?auto=compress&cs=tinysrgb&w=1200"
            exists = db.query(Post).filter(Post.image_url.like(f"%/{photo_id}/%")).first()
            if exists:
                exists.user_id, exists.title = users[email].id, title
                exists.description, exists.category, exists.image_url = description, category, image_url
            else:
                db.add(Post(user_id=users[email].id, title=title, description=description,
                            category=category, image_url=image_url,
                            created_at=datetime.now(timezone.utc) - timedelta(hours=index * 5)))

        for index, (email, title, content, model, tags) in enumerate(PROMPTS):
            exists = db.query(Prompt).filter(Prompt.title == title, Prompt.user_id == users[email].id).first()
            if exists:
                exists.content, exists.model = content, model
                exists.tags = json.dumps(tags, ensure_ascii=False)
            else:
                db.add(Prompt(user_id=users[email].id, title=title, content=content, model=model,
                              tags=json.dumps(tags, ensure_ascii=False), is_public=True,
                              created_at=datetime.now(timezone.utc) - timedelta(hours=index * 7)))
        db.flush()

        # Migrate the former Hana mock which duplicated q's uploaded rice-terrace image.
        old_hana_post = db.query(Post).filter(
            Post.user_id == users["hana@demo.local"].id,
            Post.title == "Ритм террас",
        ).first()
        if old_hana_post:
            old_hana_post.title = "Весенний перекрёсток"
            old_hana_post.description = "Сакура на солнечной городской улице"
            old_hana_post.category = "architecture"
            old_hana_post.image_url = "/uploads/demo/q/06-sakura-street.jpg"
        db.flush()

        for index, (email, title, description, category, filename) in enumerate(CATEGORY_MOCKS):
            user = users[email]
            image_url = f"/uploads/demo/q/{filename}"
            stale_posts = db.query(Post).filter(
                Post.title == title, Post.user_id != user.id
            ).all()
            for stale in stale_posts:
                db.query(Favorite).filter_by(item_type="post", item_id=stale.id).delete()
                db.delete(stale)
            post = db.query(Post).filter(Post.user_id == user.id, Post.image_url == image_url).first()
            if post:
                post.title, post.description = title, description
                post.category, post.image_url = category, image_url
            else:
                db.add(Post(
                    user_id=user.id, title=title, description=description,
                    category=category, image_url=image_url,
                    created_at=datetime.now(timezone.utc) - timedelta(minutes=index + 1),
                ))
        db.flush()

        for index, (email, title, description, category, photo_id) in enumerate(
            CATEGORY_COVERAGE_MOCKS
        ):
            user = users[email]
            image_url = (
                f"https://images.pexels.com/photos/{photo_id}/"
                f"pexels-photo-{photo_id}.jpeg?auto=compress&cs=tinysrgb&w=1200"
            )
            post = db.query(Post).filter(
                Post.user_id == user.id,
                Post.category == category,
                Post.image_url.like("/uploads/demo/categories/%"),
            ).first()
            if not post:
                post = db.query(Post).filter(
                    Post.user_id == user.id,
                    Post.image_url.like(f"%/{photo_id}/%"),
                ).first()
            if post:
                post.title, post.description = title, description
                post.category, post.image_url = category, image_url
            else:
                db.add(Post(
                    user_id=user.id,
                    title=title,
                    description=description,
                    category=category,
                    image_url=image_url,
                    created_at=datetime.now(timezone.utc) - timedelta(minutes=10 + index),
                ))
        db.flush()

        legacy_posts = db.query(Post).filter(Post.title.in_(LEGACY_CATEGORY_TITLES)).all()
        for legacy in legacy_posts:
            db.query(Favorite).filter_by(item_type="post", item_id=legacy.id).delete()
            db.delete(legacy)

        for index, (email, title, description, category, photo_id) in enumerate(EUROPE_POSTS):
            user = users[email]
            image_url = (
                f"https://images.pexels.com/photos/{photo_id}/"
                f"pexels-photo-{photo_id}.jpeg?auto=compress&cs=tinysrgb&w=1200"
            )
            post = db.query(Post).filter(Post.user_id == user.id, Post.title == title).first()
            if post:
                post.description, post.category, post.image_url = description, category, image_url
            else:
                db.add(Post(
                    user_id=user.id, title=title, description=description,
                    category=category, image_url=image_url,
                    created_at=datetime.now(timezone.utc) - timedelta(minutes=30 + index),
                ))
        db.flush()

        current = db.query(User).filter(User.email == "q@q.com").first()
        if current:
            q_upload_dir = upload_dir / "q"
            for index, (title, description, category, slug, color1, color2) in enumerate(Q_POSTS):
                image_url = f"/uploads/demo/q/{Q_STOCK_IMAGES[index]}"
                post = db.query(Post).filter(Post.user_id == current.id, Post.image_url == image_url).first()
                if post:
                    post.title, post.description = title, description
                    post.category, post.image_url = category, image_url
                else:
                    db.add(Post(user_id=current.id, title=title, description=description,
                                category=category, image_url=image_url,
                                created_at=datetime.now(timezone.utc) - timedelta(hours=index + 1)))

            for index, (title, content, model, tags) in enumerate(Q_PROMPTS):
                prompt = db.query(Prompt).filter(Prompt.user_id == current.id, Prompt.title == title).first()
                if prompt:
                    prompt.content, prompt.model = content, model
                    prompt.tags = json.dumps(tags, ensure_ascii=False)
                else:
                    db.add(Prompt(user_id=current.id, title=title, content=content, model=model,
                                  tags=json.dumps(tags, ensure_ascii=False), is_public=True,
                                  created_at=datetime.now(timezone.utc) - timedelta(hours=index + 2)))
            db.flush()

            for friend in list(users.values())[:3]:
                exists = db.query(Friendship).filter(
                    ((Friendship.user_id == current.id) & (Friendship.friend_id == friend.id)) |
                    ((Friendship.user_id == friend.id) & (Friendship.friend_id == current.id))
                ).first()
                if not exists:
                    db.add(Friendship(user_id=current.id, friend_id=friend.id, status="accepted"))
            for post in db.query(Post).filter(Post.image_url.like("/uploads/demo/%")).limit(3):
                exists = db.query(Favorite).filter_by(user_id=current.id, item_id=post.id, item_type="post").first()
                if not exists:
                    db.add(Favorite(user_id=current.id, item_id=post.id, item_type="post"))
            for prompt in db.query(Prompt).filter(Prompt.is_public.is_(True)).limit(2):
                exists = db.query(Favorite).filter_by(user_id=current.id, item_id=prompt.id, item_type="prompt").first()
                if not exists:
                    db.add(Favorite(user_id=current.id, item_id=prompt.id, item_type="prompt"))

        db.commit()
        print("Demo data ready, including q@q.com content in uploads/demo/q")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
