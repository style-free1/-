from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud
from ..auth import verify_token

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("", response_model=list[schemas.ProductOut], dependencies=[Depends(verify_token)])
def list_products(db: Session = Depends(get_db)):
    return crud.get_products(db)


@router.post("", response_model=schemas.ProductOut, dependencies=[Depends(verify_token)])
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)


@router.put("/{product_id}", response_model=schemas.ProductOut, dependencies=[Depends(verify_token)])
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    obj = crud.update_product(db, product_id, product)
    if not obj:
        raise HTTPException(status_code=404, detail="商品不存在")
    return obj


@router.delete("/{product_id}", dependencies=[Depends(verify_token)])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_product(db, product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="商品不存在")
    return {"message": "删除成功"}
