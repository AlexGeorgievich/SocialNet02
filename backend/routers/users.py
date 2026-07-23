import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas.user import UserUpdate, UserResponse
from services.auth import get_current_user
from services.upload import save_upload
from services.cache import invalidate_all

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)


@router.put("/me", response_model=UserResponse)
def update_profile(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    invalidate_all()
    return UserResponse.model_validate(current_user)


@router.post("/me/avatar", response_model=UserResponse)
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        url = await save_upload(file, "avatars")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    current_user.avatar_url = url
    db.commit()
    db.refresh(current_user)
    invalidate_all()
    return UserResponse.model_validate(current_user)
