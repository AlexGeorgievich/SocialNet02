from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Friendship, User
from services.auth import get_current_user

router = APIRouter(prefix="/api/friends", tags=["friends"])


@router.get("/status/{user_id}")
def friendship_status(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    friendship = db.query(Friendship).filter(
        ((Friendship.user_id == current_user.id) & (Friendship.friend_id == user_id)) |
        ((Friendship.user_id == user_id) & (Friendship.friend_id == current_user.id))
    ).first()
    if not friendship:
        return {"status": "none"}
    if friendship.status == "accepted":
        return {"status": "accepted"}
    direction = "sent" if friendship.user_id == current_user.id else "received"
    return {"status": "pending", "direction": direction}


@router.get("")
def list_friends(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    friendships = db.query(Friendship).filter(
        Friendship.status == "accepted",
        (Friendship.user_id == current_user.id) | (Friendship.friend_id == current_user.id)
    ).all()
    
    friend_ids = []
    for f in friendships:
        fid = f.friend_id if f.user_id == current_user.id else f.user_id
        friend_ids.append(fid)
    
    friends = db.query(User).filter(User.id.in_(friend_ids)).all()
    return [
        {
            "id": u.id, "first_name": u.first_name, "last_name": u.last_name,
            "avatar_url": u.avatar_url, "status": u.status,
        }
        for u in friends
    ]


@router.get("/requests")
def list_friend_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    requests = db.query(Friendship).filter(
        Friendship.friend_id == current_user.id,
        Friendship.status == "pending",
    ).all()
    
    result = []
    for r in requests:
        user = db.query(User).filter(User.id == r.user_id).first()
        if user:
            result.append({
                "id": r.id,
                "user_id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "avatar_url": user.avatar_url,
            })
    return result


@router.post("/{user_id}")
def add_friend(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot add yourself")
    
    existing = db.query(Friendship).filter(
        ((Friendship.user_id == current_user.id) & (Friendship.friend_id == user_id)) |
        ((Friendship.user_id == user_id) & (Friendship.friend_id == current_user.id))
    ).first()
    
    if existing:
        if existing.status == "accepted":
            raise HTTPException(status_code=400, detail="Already friends")
        if existing.user_id == current_user.id:
            raise HTTPException(status_code=400, detail="Request already sent")
        existing.status = "accepted"
        db.commit()
        return {"detail": "Friend request accepted"}
    
    friendship = Friendship(user_id=current_user.id, friend_id=user_id, status="pending")
    db.add(friendship)
    db.commit()
    return {"detail": "Friend request sent"}


@router.put("/{user_id}")
def accept_friend(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    friendship = db.query(Friendship).filter(
        Friendship.user_id == user_id,
        Friendship.friend_id == current_user.id,
        Friendship.status == "pending",
    ).first()
    if not friendship:
        raise HTTPException(status_code=404, detail="No pending request")
    friendship.status = "accepted"
    db.commit()
    return {"detail": "Friend request accepted"}


@router.delete("/{user_id}")
def remove_friend(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    friendship = db.query(Friendship).filter(
        ((Friendship.user_id == current_user.id) & (Friendship.friend_id == user_id)) |
        ((Friendship.user_id == user_id) & (Friendship.friend_id == current_user.id))
    ).first()
    if not friendship:
        raise HTTPException(status_code=404, detail="Friendship not found")
    db.delete(friendship)
    db.commit()
    return {"detail": "Friend removed"}
