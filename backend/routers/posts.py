from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, Form, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import Post, User
from schemas.post import PostCreate, PostResponse
from services.auth import get_current_user
from services.upload import save_upload
from services.cache import cache_key, get_json, invalidate_all, set_json

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.get("", response_model=list[PostResponse])
def list_posts(
    request: Request,
    category: Optional[str] = Query(None),
    user_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    key = cache_key(request.state.app_mode, "posts", category, user_id)
    cached = get_json(key)
    if cached is not None:
        return cached

    q = db.query(Post)
    if category:
        q = q.filter(Post.category == category)
    if user_id:
        q = q.filter(Post.user_id == user_id)
    posts = q.order_by(Post.created_at.desc()).all()
    author_ids = {post.user_id for post in posts}
    authors = {
        user.id: user
        for user in db.query(User).filter(User.id.in_(author_ids)).all()
    } if author_ids else {}
    result = []
    for p in posts:
        user = authors.get(p.user_id)
        result.append(PostResponse(
            id=p.id, user_id=p.user_id, title=p.title,
            description=p.description, image_url=p.image_url,
            category=p.category, created_at=p.created_at,
            user_first_name=user.first_name if user else "",
            user_last_name=user.last_name if user else "",
            user_avatar_url=user.avatar_url if user else "",
        ))
    encoded = jsonable_encoder(result)
    set_json(key, encoded)
    return encoded


@router.post("", response_model=PostResponse)
async def create_post(
    title: str = Form(...),
    description: str = Form(""),
    category: str = Form("artwork"),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        url = await save_upload(file, "posts")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    post = Post(
        user_id=current_user.id,
        title=title,
        description=description,
        image_url=url,
        category=category,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    invalidate_all()
    return PostResponse(
        id=post.id, user_id=post.user_id, title=post.title,
        description=post.description, image_url=post.image_url,
        category=post.category, created_at=post.created_at,
        user_first_name=current_user.first_name,
        user_last_name=current_user.last_name,
        user_avatar_url=current_user.avatar_url,
    )


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(post)
    db.commit()
    invalidate_all()
    return {"detail": "Post deleted"}


@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    data: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    post.title, post.description, post.category = data.title, data.description, data.category
    db.commit()
    db.refresh(post)
    invalidate_all()
    return PostResponse(
        id=post.id, user_id=post.user_id, title=post.title,
        description=post.description, image_url=post.image_url,
        category=post.category, created_at=post.created_at,
        user_first_name=current_user.first_name, user_last_name=current_user.last_name,
        user_avatar_url=current_user.avatar_url,
    )
