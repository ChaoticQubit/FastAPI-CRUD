from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint


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
class PostCreate(PostBase):
    pass
class Post(PostBase):
    created_at: datetime
    owner_id: int
    id: int
    owner: UserResponse
    class Config:
        orm_mode = True

class PostResponse(BaseModel):
    Posts: Post
    likes: int
    
    class Config:
        orm_mode = True

class VoteBase(BaseModel):
    post_id: int
    voteDir: conint(le=1)

class VoteCreate(VoteBase):
    pass