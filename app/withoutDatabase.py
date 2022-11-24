from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import app.helperFuncs as hf


app = FastAPI()
all_posts = [
        {"title": "FastAPI and its advantages",
        "content": "lorem ipsum FastAPI and its advantages",
        "published": True,
        "rating": 3.5,
        "id": 1},

        {"title": "Implementing FastAPI",
        "content": "lorem ipsum Implementing FastAPI",
        "published": False,
        "rating": 4,
        "id": 2}
    ]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[float] = None
    id: Optional[int] = None

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts():
    return {"posts": all_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post :Post):
    global all_posts
    post_dict = post.dict()
    post_dict["id"] = len(all_posts) + 1
    all_posts += [post_dict]
    return {
        "message": "Post created",
        "data": all_posts
    }


@app.get("/posts/latest")
async def get_latest_post():
    if not all_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    return {
        "message": "Post found",
        "data": all_posts[-1]
    }


@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    index, post = hf.find_post(all_posts, post_id)
    hf.raise404Exception(post)
    return post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    global all_posts
    index, post = hf.find_post(all_posts, post_id)
    hf.raise404Exception(post)
    all_posts.pop(index)
    return {
        "message": "Post deleted",
        "data": all_posts
    }


@app.put("/posts/{post_id}")
async def update_post(post_id: int, post: Post):
    global all_posts
    index, prevPost = hf.find_post(all_posts, post_id)
    hf.raise404Exception(prevPost)
    post = post.dict()
    post["id"] = post_id
    post["rating"] = prevPost["data"]["rating"]
    post["published"] = prevPost["data"]["published"]
    all_posts[index] = post
    return {
        "message": "Post updated",
        "data": all_posts
    }