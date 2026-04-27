"""特征构造服务。"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models


def build_features(db: Session, user_id: int, product_id: int):
    user_behavior_count = (
        db.query(func.count(models.UserBehavior.id))
        .filter(models.UserBehavior.user_id == user_id)
        .scalar()
        or 0
    )
    product_click_count = (
        db.query(func.count(models.UserBehavior.id))
        .filter(
            models.UserBehavior.product_id == product_id,
            models.UserBehavior.behavior_type == "view",
        )
        .scalar()
        or 0
    )
    product_buy_count = (
        db.query(func.count(models.UserBehavior.id))
        .filter(
            models.UserBehavior.product_id == product_id,
            models.UserBehavior.behavior_type == "buy",
        )
        .scalar()
        or 0
    )
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    category = product.category if product else "unknown"
    category_pref = (
        db.query(func.count(models.UserBehavior.id))
        .join(models.Product, models.Product.id == models.UserBehavior.product_id)
        .filter(models.UserBehavior.user_id == user_id, models.Product.category == category)
        .scalar()
        or 0
    )
    price = product.price if product else 0

    return {
        "user_behavior_count": user_behavior_count,
        "product_click_count": product_click_count,
        "product_buy_count": product_buy_count,
        "product_category": category,
        "product_price": price,
        "category_pref_score": category_pref,
    }
