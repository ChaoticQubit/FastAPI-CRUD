from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    password: str
    email: EmailStr
    username: str
class UserCreate(UserBase):
    pass
class UserResponse(BaseModel):
    username: str
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True



class userLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None



class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    likes: Optional[int] = 0
class PostCreate(PostBase):
    pass
class PostResponse(PostBase):
    created_at: datetime
    owner_id: int
    owner: UserResponse
    class Config:
        orm_mode = True