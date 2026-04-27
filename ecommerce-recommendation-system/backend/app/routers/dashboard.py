from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import dashboard_stats
from ..auth import verify_token

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/stats", dependencies=[Depends(verify_token)])
def stats(db: Session = Depends(get_db)):
    return dashboard_stats(db)
