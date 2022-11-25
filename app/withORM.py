from fastapi import FastAPI, status, Depends
from fastapi.params import Body
import app.helperFuncs as hf
from . import models, schemas
from app.sqlalchemy_database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    posts = {
        "message": "All posts",
        "data": db.query(models.Posts).all()
        }
    post = hf.raise404Exception(posts)
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post :schemas.PostCreate, db: Session = Depends(get_db)):
    inserted_post = models.Posts(**post.dict())
    db.add(inserted_post)
    db.commit()
    db.refresh(inserted_post)
    return {
        "message": "Post created",
        "data": inserted_post
    }


@app.get("/posts/latest")
async def get_latest_post(db: Session = Depends(get_db)):
    posts = {
        "message": "Post found",
        "data": db.query(models.Posts).order_by(models.Posts.created_at.desc()).first()
    }
    post = hf.raise404Exception(posts)
    return posts


@app.get("/posts/{post_id}")
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = {
        "message": "Post found",
        "data": db.query(models.Posts).filter(models.Posts.id == post_id).first()
    }
    post = hf.raise404Exception(post)
    return post


@app.delete("/posts/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    postQuer = db.query(models.Posts).filter(models.Posts.id == post_id)
    post = {
        "message": "Post found",
        "data": postQuer.first()
    }
    post = hf.raise404Exception(post)
    postQuer.delete(synchronize_session=False)
    db.commit()
    return {
        "message": "Post deleted"
    }


@app.put("/posts/{post_id}")
async def update_post(post_id: int, post: dict = Body(...), db: Session = Depends(get_db)):
    postQuer = db.query(models.Posts).filter(models.Posts.id == post_id)
    checkPost = {
        "message": "Post found",
        "data": postQuer.first()
    }
    checkPost = hf.raise404Exception(checkPost)
    postQuer.update({**post}, synchronize_session=False)
    db.commit()
    checkPost = {
        "message": "Post updated",
        "data": postQuer.first()
    }
    return checkPost