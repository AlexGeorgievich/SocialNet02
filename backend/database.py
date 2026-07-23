from fastapi import HTTPException, Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DEMO_DATABASE_URL, WORK_DATABASE_URL


def make_engine(url: str):
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    return create_engine(url, connect_args=connect_args)


demo_engine = make_engine(DEMO_DATABASE_URL)
work_engine = make_engine(WORK_DATABASE_URL)
DemoSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=demo_engine)
WorkSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=work_engine)

# seed.py intentionally operates on the committed demonstration database.
engine = demo_engine
SessionLocal = DemoSessionLocal
Base = declarative_base()


def get_app_mode(request: Request) -> str:
    mode = request.headers.get("X-S-Art-Mode", "demo").lower()
    if mode not in {"demo", "work"}:
        raise HTTPException(status_code=400, detail="Неизвестный режим приложения")
    return mode


def ensure_schema(target_engine):
    """Apply small SQLite migrations without deleting existing data."""
    if target_engine.dialect.name != "sqlite":
        return
    with target_engine.begin() as connection:
        columns = {row[1] for row in connection.exec_driver_sql("PRAGMA table_info(users)")}
        if columns and "role" not in columns:
            connection.exec_driver_sql(
                "ALTER TABLE users ADD COLUMN role VARCHAR NOT NULL DEFAULT 'user'"
            )
        if columns and "privacy_consent" not in columns:
            connection.exec_driver_sql(
                "ALTER TABLE users ADD COLUMN privacy_consent BOOLEAN NOT NULL DEFAULT 0"
            )
        if columns and "privacy_consent_version" not in columns:
            connection.exec_driver_sql(
                "ALTER TABLE users ADD COLUMN privacy_consent_version VARCHAR NOT NULL DEFAULT ''"
            )
        if columns and "privacy_consent_at" not in columns:
            connection.exec_driver_sql(
                "ALTER TABLE users ADD COLUMN privacy_consent_at DATETIME"
            )


def get_db(request: Request):
    mode = get_app_mode(request)
    request.state.app_mode = mode
    session_factory = DemoSessionLocal if mode == "demo" else WorkSessionLocal
    db = session_factory()
    try:
        yield db
    finally:
        db.close()
