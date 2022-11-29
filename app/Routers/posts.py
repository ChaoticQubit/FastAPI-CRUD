from typing import List, Optional
from fastapi import Body, Depends, status, APIRouter
from app import models, schemas, helperFuncs as hf, oauth2
from app.sqlalchemy_database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db), currUser: int = Depends(oauth2.get_current_user), search: Optional[str] = ""):
    posts = db.query(models.Posts, func.count(models.Votes.post_id).label("likes")).join(
        models.Votes, models.Votes.post_id == models.Posts.id, isouter=True).group_by(
        models.Posts.id).filter(or_(
        models.Posts.title.contains(search), models.Posts.content.contains(search)), models.Posts.owner_id == currUser.id).all()
    hf.raise404Exception(posts)
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(post :schemas.PostCreate, db: Session = Depends(get_db), currUser: int = Depends(oauth2.get_current_user)):
    inserted_post = models.Posts(owner_id = currUser.id, **post.dict())
    db.add(inserted_post)
    db.commit()
    posts = db.query(models.Posts, func.count(models.Votes.post_id).label("likes")).join(
        models.Votes, models.Votes.post_id == models.Posts.id, isouter=True).group_by(
        models.Posts.id).filter(
        models.Posts.owner_id == currUser.id).order_by(models.Posts.created_at.desc()).first()
    return posts


@router.get("/latest", response_model=schemas.PostResponse)
async def get_latest_post(db: Session = Depends(get_db), currUser: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Posts, func.count(models.Votes.post_id).label("likes")).join(
        models.Votes, models.Votes.post_id == models.Posts.id, isouter=True).group_by(
        models.Posts.id).filter(
        models.Posts.owner_id == currUser.id).order_by(models.Posts.created_at.desc()).first()
    posts = hf.raise404Exception(posts)
    return posts


@router.get("/{post_id}", response_model=schemas.PostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db), currUser: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Posts, func.count(models.Votes.post_id).label("likes")).join(
        models.Votes, models.Votes.post_id == models.Posts.id, isouter=True).group_by(
        models.Posts.id).filter(
        models.Posts.owner_id == currUser.id, models.Posts.id == post_id).first()
    hf.raise404Exception(posts)
    return posts


@router.delete("/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db), currUser: int = Depends(oauth2.get_current_user)):
    postQuer = db.query(models.Posts).filter(models.Posts.id == post_id)
    post = postQuer.first()
    hf.raise404Exception(post)
    hf.raise403Exception(post.owner_id, currUser.id)
    postQuer.delete(synchronize_session=False)
    db.commit()
    return {
        "message": "Post deleted"
    }
    

@router.put("/{post_id}", response_model=schemas.PostResponse)
async def update_post(post_id: int, post: dict = Body(...), db: Session = Depends(get_db), currUser: int = Depends(oauth2.get_current_user)):
    postQuer = db.query(models.Posts).filter(models.Posts.id == post_id)
    checkPost = postQuer.first()
    checkPost = hf.raise404Exception(checkPost)
    hf.raise403Exception(checkPost.owner_id, currUser.id)
    postQuer.update({**post}, synchronize_session=False)
    db.commit()
    checkPost = db.query(models.Posts, func.count(models.Votes.post_id).label("likes")).join(
        models.Votes, models.Votes.post_id == models.Posts.id, isouter=True).group_by(
        models.Posts.id).filter(
        models.Posts.owner_id == currUser.id, models.Posts.id == post_id).first()
    return checkPost