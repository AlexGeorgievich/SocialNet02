from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from database import Base, demo_engine, ensure_schema, work_engine
from config import CORS_ORIGINS, UPLOAD_DIR

from routers import auth, users, posts, prompts, friends, favorites, admin

for database_engine in (demo_engine, work_engine):
    ensure_schema(database_engine)
    Base.metadata.create_all(bind=database_engine)

app = FastAPI(title="S-Art API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(prompts.router)
app.include_router(friends.router)
app.include_router(favorites.router)
app.include_router(admin.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import sys
    import uvicorn

    from logging_config import get_logging_config

    # Keep redirected Windows console output in the same encoding as log files.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_config=get_logging_config(),
    )
