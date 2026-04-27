from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud
from ..auth import verify_token

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("", response_model=list[schemas.UserOut], dependencies=[Depends(verify_token)])
def list_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@router.post("", response_model=schemas.UserOut, dependencies=[Depends(verify_token)])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@router.put("/{user_id}", response_model=schemas.UserOut, dependencies=[Depends(verify_token)])
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    obj = crud.update_user(db, user_id, user)
    if not obj:
        raise HTTPException(status_code=404, detail="用户不存在")
    return obj


@router.delete("/{user_id}", dependencies=[Depends(verify_token)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"message": "删除成功"}
