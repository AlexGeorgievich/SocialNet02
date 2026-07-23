from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PostCreate(BaseModel):
    title: str
    description: str = ""
    category: str = "artwork"


class PostResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    image_url: str
    category: str
    created_at: datetime
    user_first_name: str = ""
    user_last_name: str = ""
    user_avatar_url: str = ""

    model_config = {"from_attributes": True}
