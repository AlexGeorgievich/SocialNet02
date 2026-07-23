import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEMO_DATABASE_URL = os.getenv(
    "DEMO_DATABASE_URL", f"sqlite:///{BASE_DIR}/database.demo.db"
)
WORK_DATABASE_URL = os.getenv(
    "WORK_DATABASE_URL", os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/database.work.db")
)
# Backward-compatible alias used by external scripts.
DATABASE_URL = DEMO_DATABASE_URL
UPLOAD_DIR = BASE_DIR / "uploads"
JWT_SECRET = os.getenv("JWT_SECRET", "change-me-in-local-development")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "30"))
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    if origin.strip()
]
