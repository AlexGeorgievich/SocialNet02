import os
import uuid
from pathlib import Path
from fastapi import UploadFile
from config import UPLOAD_DIR

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif"}
MAX_FILE_SIZE = 10 * 1024 * 1024


async def save_upload(file: UploadFile, subfolder: str) -> str:
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"File type {ext} not allowed")
    
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise ValueError("File too large (max 10MB)")
    
    filename = f"{uuid.uuid4().hex}{ext}"
    upload_path = UPLOAD_DIR / subfolder
    upload_path.mkdir(parents=True, exist_ok=True)
    
    filepath = upload_path / filename
    with open(filepath, "wb") as f:
        f.write(content)
    
    return f"/uploads/{subfolder}/{filename}"
