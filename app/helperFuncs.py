from fastapi import status, HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")


def hash(pwd: str):
    return pwd_context.hash(pwd)


def find_post(all_posts, post_id):
    for index, post in enumerate(all_posts):
        if post["id"] == post_id:
            post = {
                "message": "Post found",
                "data": post
            }
            return index, post
    return -1, {
        "message": f"Post with ID: {post_id} was not found",
        "data": None
    }


def raise404Exception(post):
    if not post:
        post = {
            "message": f"No posts were found!",
            "data": None
        }
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=post)
    return post

def raise401Exception(error):
    if not error:
        error = {
            "message": f"Invalid Credentials. Please check your username and password!"
        }
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error)
    return error

def raise403Exception(id1, id2):
    if id1 != id2:
        error = {
            "message": f"Operation Forbidden!"
        }
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=error)

def raise409Exception(detail):
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)

def verifyPassword(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)