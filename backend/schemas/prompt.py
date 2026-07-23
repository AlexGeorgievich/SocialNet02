from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PromptCreate(BaseModel):
    title: str
    content: str
    model: str = ""
    tags: str = "[]"
    is_public: bool = True


class PromptResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    model: str
    tags: str
    is_public: bool
    created_at: datetime
    user_first_name: str = ""
    user_last_name: str = ""
    user_avatar_url: str = ""

    model_config = {"from_attributes": True}
