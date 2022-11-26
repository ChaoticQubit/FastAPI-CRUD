from typing import List
from fastapi import Depends, status, APIRouter
from app import models, schemas, helperFuncs as hf
from app.sqlalchemy_database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = hf.hash(user.password)
    inserted_user = models.User(**user.dict())
    db.add(inserted_user)
    db.commit()
    db.refresh(inserted_user)
    return inserted_user


@router.get("/", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    users = hf.raise404Exception(users)
    return users


@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    user = hf.raise404Exception(user)
    return user