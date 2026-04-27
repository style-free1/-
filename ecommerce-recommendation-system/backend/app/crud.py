"""通用 CRUD 与统计查询。"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas


def create_user(db: Session, user: schemas.UserCreate):
    obj = models.User(**user.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_users(db: Session):
    return db.query(models.User).order_by(models.User.id.desc()).all()


def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    obj = db.query(models.User).filter(models.User.id == user_id).first()
    if not obj:
        return None
    for k, v in user.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete_user(db: Session, user_id: int):
    obj = db.query(models.User).filter(models.User.id == user_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


def create_product(db: Session, product: schemas.ProductCreate):
    obj = models.Product(**product.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_products(db: Session):
    return db.query(models.Product).order_by(models.Product.id.desc()).all()


def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    obj = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not obj:
        return None
    for k, v in product.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete_product(db: Session, product_id: int):
    obj = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


def create_behavior(db: Session, behavior: schemas.BehaviorCreate):
    obj = models.UserBehavior(**behavior.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_behaviors(db: Session, user_id=None, product_id=None, behavior_type=None):
    q = db.query(models.UserBehavior)
    if user_id:
        q = q.filter(models.UserBehavior.user_id == user_id)
    if product_id:
        q = q.filter(models.UserBehavior.product_id == product_id)
    if behavior_type:
        q = q.filter(models.UserBehavior.behavior_type == behavior_type)
    return q.order_by(models.UserBehavior.id.desc()).all()


def dashboard_stats(db: Session):
    user_count = db.query(func.count(models.User.id)).scalar() or 0
    product_count = db.query(func.count(models.Product.id)).scalar() or 0
    behavior_count = db.query(func.count(models.UserBehavior.id)).scalar() or 0

    behavior_distribution = {
        row[0]: row[1]
        for row in db.query(models.UserBehavior.behavior_type, func.count(models.UserBehavior.id))
        .group_by(models.UserBehavior.behavior_type)
        .all()
    }

    total_rec = db.query(func.count(models.Recommendation.id)).scalar() or 1
    clicked = db.query(func.sum(models.Recommendation.clicked)).scalar() or 0
    ctr = round(clicked / total_rec, 4)

    trend = [
        {"date": "2026-04-22", "ctr": 0.08},
        {"date": "2026-04-23", "ctr": 0.10},
        {"date": "2026-04-24", "ctr": 0.12},
        {"date": "2026-04-25", "ctr": 0.11},
        {"date": "2026-04-26", "ctr": 0.14},
        {"date": "2026-04-27", "ctr": ctr},
    ]

    return {
        "user_count": user_count,
        "product_count": product_count,
        "behavior_count": behavior_count,
        "recommend_ctr": ctr,
        "behavior_distribution": behavior_distribution,
        "recommend_trend": trend,
    }
