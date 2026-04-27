from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud
from ..auth import verify_token

router = APIRouter(prefix="/api/behaviors", tags=["behaviors"])


@router.get("", response_model=list[schemas.BehaviorOut], dependencies=[Depends(verify_token)])
def list_behaviors(user_id: int | None = None, product_id: int | None = None, behavior_type: str | None = None, db: Session = Depends(get_db)):
    return crud.get_behaviors(db, user_id=user_id, product_id=product_id, behavior_type=behavior_type)


@router.post("", response_model=schemas.BehaviorOut, dependencies=[Depends(verify_token)])
def create_behavior(behavior: schemas.BehaviorCreate, db: Session = Depends(get_db)):
    return crud.create_behavior(db, behavior)
