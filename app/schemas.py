from pydantic import BaseModel
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    likes: Optional[int] = 0

class PostCreate(PostBase):
    pass