from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models import Favorite, Post, Prompt, User
from services.auth import get_current_user

router = APIRouter(prefix="/api/favorites", tags=["favorites"])


class FavoriteCreate(BaseModel):
    item_id: int
    item_type: str


@router.get("")
def list_favorites(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    favorites = db.query(Favorite).filter(Favorite.user_id == current_user.id).all()
    result = []
    for favorite in favorites:
        item = {"id": favorite.id, "item_id": favorite.item_id,
                "item_type": favorite.item_type, "created_at": favorite.created_at}
        if favorite.item_type == "post":
            post = db.query(Post).filter(Post.id == favorite.item_id).first()
            if post:
                author = db.query(User).filter(User.id == post.user_id).first()
                item["post"] = {
                    "id": post.id, "user_id": post.user_id, "title": post.title,
                    "description": post.description, "image_url": post.image_url,
                    "category": post.category, "created_at": post.created_at,
                    "user_first_name": author.first_name if author else "",
                    "user_last_name": author.last_name if author else "",
                    "user_avatar_url": author.avatar_url if author else "",
                }
        elif favorite.item_type == "prompt":
            prompt = db.query(Prompt).filter(Prompt.id == favorite.item_id).first()
            if prompt:
                author = db.query(User).filter(User.id == prompt.user_id).first()
                item["prompt"] = {
                    "id": prompt.id, "user_id": prompt.user_id, "title": prompt.title,
                    "content": prompt.content, "model": prompt.model, "tags": prompt.tags,
                    "is_public": prompt.is_public, "created_at": prompt.created_at,
                    "user_first_name": author.first_name if author else "",
                    "user_last_name": author.last_name if author else "",
                    "user_avatar_url": author.avatar_url if author else "",
                }
        result.append(item)
    return result


@router.post("")
def add_favorite(
    data: FavoriteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.item_id == data.item_id,
        Favorite.item_type == data.item_type,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already in favorites")
    
    fav = Favorite(user_id=current_user.id, item_id=data.item_id, item_type=data.item_type)
    db.add(fav)
    db.commit()
    return {"detail": "Added to favorites", "id": fav.id}


@router.delete("/{fav_id}")
def remove_favorite(
    fav_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    fav = db.query(Favorite).filter(Favorite.id == fav_id, Favorite.user_id == current_user.id).first()
    if not fav:
        raise HTTPException(status_code=404, detail="Favorite not found")
    db.delete(fav)
    db.commit()
    return {"detail": "Removed from favorites"}
