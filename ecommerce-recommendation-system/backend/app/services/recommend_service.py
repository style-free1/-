"""混合推荐服务。"""
from collections import defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models

BEHAVIOR_WEIGHT = {
    "view": 1,
    "favorite": 2,
    "cart": 3,
    "buy": 5,
    "review": 4,
}


def _hot_products(db: Session, limit=10):
    return (
        db.query(models.Product)
        .order_by((models.Product.sales * 0.6 + models.Product.rating * 10).desc())
        .limit(limit)
        .all()
    )


def recommend_for_user(db: Session, user_id: int, topn=10):
    behaviors = db.query(models.UserBehavior).filter(models.UserBehavior.user_id == user_id).all()

    if not behaviors:
        # 新用户：热门兜底
        return [
            {
                "product_id": p.id,
                "product_name": p.name,
                "reason": "新用户热门推荐",
                "score": round(p.sales * 0.1 + p.rating, 4),
            }
            for p in _hot_products(db, topn)
        ]

    cate_score = defaultdict(float)
    seen_products = set()
    for b in behaviors:
        prod = db.query(models.Product).filter(models.Product.id == b.product_id).first()
        if not prod:
            continue
        cate_score[prod.category] += BEHAVIOR_WEIGHT.get(b.behavior_type, 1)
        seen_products.add(prod.id)

    candidates = db.query(models.Product).all()
    result = []
    for p in candidates:
        behavior_part = cate_score.get(p.category, 0)
        cate_sim = 2 if p.category in cate_score else 0
        hot_part = p.sales * 0.05 + p.rating * 0.5
        new_product_bonus = 1 if p.sales < 5 else 0
        score = behavior_part + cate_sim + hot_part + new_product_bonus
        if p.id in seen_products:
            score *= 0.6
        reason = "行为偏好+分类相似+热度混合"
        if p.sales < 5:
            reason += "（新商品属性补充）"
        result.append(
            {
                "product_id": p.id,
                "product_name": p.name,
                "reason": reason,
                "score": round(score, 4),
            }
        )

    result = sorted(result, key=lambda x: x["score"], reverse=True)[:topn]
    return result
