from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import Prompt, User
from schemas.prompt import PromptCreate, PromptResponse
from services.auth import get_current_user
from services.cache import cache_key, get_json, invalidate_all, set_json

router = APIRouter(prefix="/api/prompts", tags=["prompts"])


@router.get("", response_model=list[PromptResponse])
def list_prompts(
    request: Request,
    user_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    key = cache_key(request.state.app_mode, "prompts", user_id)
    cached = get_json(key)
    if cached is not None:
        return cached

    q = db.query(Prompt).filter(Prompt.is_public == True)
    if user_id:
        q = db.query(Prompt).filter(Prompt.user_id == user_id)
    prompts = q.order_by(Prompt.created_at.desc()).all()
    result = []
    for p in prompts:
        user = db.query(User).filter(User.id == p.user_id).first()
        result.append(PromptResponse(
            id=p.id, user_id=p.user_id, title=p.title,
            content=p.content, model=p.model, tags=p.tags,
            is_public=p.is_public, created_at=p.created_at,
            user_first_name=user.first_name if user else "",
            user_last_name=user.last_name if user else "",
            user_avatar_url=user.avatar_url if user else "",
        ))
    encoded = jsonable_encoder(result)
    set_json(key, encoded)
    return encoded


@router.post("", response_model=PromptResponse)
def create_prompt(
    data: PromptCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    prompt = Prompt(
        user_id=current_user.id,
        title=data.title,
        content=data.content,
        model=data.model,
        tags=data.tags,
        is_public=data.is_public,
    )
    db.add(prompt)
    db.commit()
    db.refresh(prompt)
    invalidate_all()
    return PromptResponse(
        id=prompt.id, user_id=prompt.user_id, title=prompt.title,
        content=prompt.content, model=prompt.model, tags=prompt.tags,
        is_public=prompt.is_public, created_at=prompt.created_at,
        user_first_name=current_user.first_name,
        user_last_name=current_user.last_name,
        user_avatar_url=current_user.avatar_url,
    )


@router.post("/{prompt_id}/copy", response_model=PromptResponse)
def copy_prompt(
    prompt_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    original = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not original:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    copy = Prompt(
        user_id=current_user.id,
        title=f"Copy of {original.title}",
        content=original.content,
        model=original.model,
        tags=original.tags,
        is_public=True,
    )
    db.add(copy)
    db.commit()
    db.refresh(copy)
    invalidate_all()
    return PromptResponse(
        id=copy.id, user_id=copy.user_id, title=copy.title,
        content=copy.content, model=copy.model, tags=copy.tags,
        is_public=copy.is_public, created_at=copy.created_at,
        user_first_name=current_user.first_name,
        user_last_name=current_user.last_name,
        user_avatar_url=current_user.avatar_url,
    )


@router.delete("/{prompt_id}")
def delete_prompt(
    prompt_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    if prompt.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(prompt)
    db.commit()
    invalidate_all()
    return {"detail": "Prompt deleted"}


@router.put("/{prompt_id}", response_model=PromptResponse)
def update_prompt(
    prompt_id: int,
    data: PromptCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    if prompt.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    prompt.title, prompt.content, prompt.model = data.title, data.content, data.model
    prompt.tags, prompt.is_public = data.tags, data.is_public
    db.commit()
    db.refresh(prompt)
    invalidate_all()
    return PromptResponse(
        id=prompt.id, user_id=prompt.user_id, title=prompt.title,
        content=prompt.content, model=prompt.model, tags=prompt.tags,
        is_public=prompt.is_public, created_at=prompt.created_at,
        user_first_name=current_user.first_name, user_last_name=current_user.last_name,
        user_avatar_url=current_user.avatar_url,
    )
