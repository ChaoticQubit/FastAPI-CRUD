from fastapi import APIRouter, Depends, status, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.sqlalchemy_database import get_db
from sqlalchemy.orm import Session
from app import models, schemas, helperFuncs as hf, oauth2


router = APIRouter(
    prefix="/auth",
    tags=['Auth']
)

@router.post("/login", response_model=schemas.Token)
def login(creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == creds.username).first()
    hf.raise401Exception(user)
    if not hf.verifyPassword(creds.password, user.password):
        hf.raise401Exception(user)
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}