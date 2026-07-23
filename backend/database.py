from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def ensure_schema():
    """Apply small SQLite migrations without deleting existing data."""
    with engine.begin() as connection:
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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
