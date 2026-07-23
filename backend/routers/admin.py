from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import Favorite, Friendship, Post, Prompt, User
from services.auth import get_current_user
from services.cache import cache_key, get_json, invalidate_all, set_json

router = APIRouter(prefix="/api", tags=["admin"])


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Требуются права администратора")
    return current_user


@router.get("/stats")
def stats(request: Request, db: Session = Depends(get_db)):
    key = cache_key(request.state.app_mode, "stats")
    cached = get_json(key)
    if cached is not None:
        return cached
    value = {
        "users": db.query(User).count(),
        "posts": db.query(Post).count(),
        "prompts": db.query(Prompt).count(),
    }
    set_json(key, value)
    return value


@router.get("/admin/users")
def list_users(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    return [
        {
            "id": user.id, "email": user.email, "first_name": user.first_name,
            "last_name": user.last_name, "status": user.status, "role": user.role,
            "created_at": user.created_at,
        }
        for user in db.query(User).order_by(User.created_at.desc()).all()
    ]


@router.get("/admin/content")
def list_content(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    posts = db.query(Post).order_by(Post.created_at.desc()).all()
    prompts = db.query(Prompt).order_by(Prompt.created_at.desc()).all()
    return {
        "posts": [{"id": x.id, "title": x.title, "user_id": x.user_id} for x in posts],
        "prompts": [{"id": x.id, "title": x.title, "user_id": x.user_id} for x in prompts],
    }


class RoleUpdate(BaseModel):
    role: str


@router.put("/admin/users/{user_id}/role")
def update_role(
    user_id: int, data: RoleUpdate, admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    if data.role not in {"user", "admin"}:
        raise HTTPException(status_code=400, detail="Недопустимая роль")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if user.id == admin.id and data.role != "admin":
        raise HTTPException(status_code=400, detail="Нельзя снять роль с самого себя")
    user.role = data.role
    db.commit()
    return {"detail": "Роль обновлена", "role": user.role}


@router.delete("/admin/users/{user_id}")
def delete_user(
    user_id: int, admin: User = Depends(require_admin), db: Session = Depends(get_db),
):
    if user_id == admin.id:
        raise HTTPException(status_code=400, detail="Нельзя удалить самого себя")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    post_ids = [x.id for x in db.query(Post.id).filter(Post.user_id == user_id)]
    prompt_ids = [x.id for x in db.query(Prompt.id).filter(Prompt.user_id == user_id)]
    db.query(Favorite).filter(
        (Favorite.user_id == user_id)
        | ((Favorite.item_type == "post") & Favorite.item_id.in_(post_ids or [-1]))
        | ((Favorite.item_type == "prompt") & Favorite.item_id.in_(prompt_ids or [-1]))
    ).delete(synchronize_session=False)
    db.query(Friendship).filter(
        (Friendship.user_id == user_id) | (Friendship.friend_id == user_id)
    ).delete(synchronize_session=False)
    db.delete(user)
    db.commit()
    invalidate_all()
    return {"detail": "Пользователь удалён"}


@router.delete("/admin/posts/{post_id}")
def admin_delete_post(
    post_id: int, _: User = Depends(require_admin), db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Работа не найдена")
    db.query(Favorite).filter_by(item_type="post", item_id=post_id).delete()
    db.delete(post)
    db.commit()
    invalidate_all()
    return {"detail": "Работа удалена"}


@router.delete("/admin/prompts/{prompt_id}")
def admin_delete_prompt(
    prompt_id: int, _: User = Depends(require_admin), db: Session = Depends(get_db),
):
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Промпт не найден")
    db.query(Favorite).filter_by(item_type="prompt", item_id=prompt_id).delete()
    db.delete(prompt)
    db.commit()
    invalidate_all()
    return {"detail": "Промпт удалён"}
