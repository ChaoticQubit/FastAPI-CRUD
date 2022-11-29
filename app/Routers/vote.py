from fastapi import Body, Depends, status, APIRouter
from app import models, schemas, sqlalchemy_database as sdb, oauth2, helperFuncs as hf
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/votes",
    tags=['Votes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_vote(vote : schemas.VoteCreate, db: Session = Depends(sdb.get_db), currUser: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Posts).filter(models.Posts.id == vote.post_id).first()
    hf.raise404Exception(post)
    voteQuer = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == currUser.id)
    foundVote = voteQuer.first()
    if vote.voteDir == 1:
        if foundVote:
            hf.raise409Exception("Post is already Liked!")
        newVote = models.Votes(post_id=vote.post_id, user_id=currUser.id)
        db.add(newVote)
        db.commit()
        return "Post Liked!"
    else:
        if not foundVote:
            hf.raise409Exception("Vote does not exist!")
        voteQuer.delete(synchronize_session=False)
        db.commit()
        return "Post Unliked!"