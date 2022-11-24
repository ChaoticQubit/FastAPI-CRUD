from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import app.helperFuncs as hf
import app.database as db


app = FastAPI()
db_con = db.Database()
all_posts = [
        {"title": "FastAPI and its advantages",
        "content": "lorem ipsum FastAPI and its advantages",
        "published": True,
        "likes": 35,
        "id": 1},

        {"title": "Implementing FastAPI",
        "content": "lorem ipsum Implementing FastAPI",
        "published": False,
        "likes": 4,
        "id": 2}
    ]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    likes: Optional[int] = 0

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts():
    posts = {
        "message": "All posts",
        "data": db_con.select(db.TableConstants.POSTSTABLE)
        }
    post = hf.raise404Exception(posts)
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post :Post):
    inserted_post = db_con.insert(db.TableConstants.POSTSTABLE, db.TableConstants.POSTCOLS, post.dict())
    return {
        "message": "Post created",
        "data": inserted_post
    }


@app.get("/posts/latest")
async def get_latest_post():
    posts = {
        "message": "Post found",
        "data": db_con.select(db.TableConstants.POSTSTABLE, orderby="id DESC", limit=1)
    }
    post = hf.raise404Exception(posts)
    return posts


@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    post = {
        "message": "Post found",
        "data": db_con.select(db.TableConstants.POSTSTABLE, where=f"id = {post_id}")
    }
    post = hf.raise404Exception(post)
    return post


@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    post = {
        "message": "Post found",
        "data": db_con.select(db.TableConstants.POSTSTABLE, where=f"id = {post_id}")
    }
    post = hf.raise404Exception(post)
    mess = db_con.delete(db.TableConstants.POSTSTABLE, post_id)
    post["message"] = mess + f" with post_id = {post_id}."
    return post


@app.put("/posts/{post_id}")
async def update_post(post_id: int, post: dict = Body(...)):
    cols = list(post.keys())
    checkPost = {
        "message": "Post found",
        "data": db_con.select(db.TableConstants.POSTSTABLE, where=f"id = {post_id}")
    }
    checkPost = hf.raise404Exception(checkPost)
    checkPost = {
        "message": "Post updated",
        "data":  db_con.update(db.TableConstants.POSTSTABLE, cols=cols, where=f"id = {post_id}", post=post)
    }
    return checkPost