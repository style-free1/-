from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.recommend_service import recommend_for_user
from ..auth import verify_token

router = APIRouter(tags=["recommend"])


@router.get("/api/recommend/{user_id}", dependencies=[Depends(verify_token)])
def recommend(user_id: int, db: Session = Depends(get_db)):
    return {"items": recommend_for_user(db, user_id, topn=10)}
