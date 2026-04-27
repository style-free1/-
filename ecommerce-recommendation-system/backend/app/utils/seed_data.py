"""模拟数据生成脚本：python -m app.utils.seed_data"""
import random
from app.database import SessionLocal, Base, engine
from app import models


CATEGORIES = ["手机", "电脑", "家电", "服饰", "食品"]
BEHAVIORS = ["view", "favorite", "cart", "buy", "review"]


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if not db.query(models.User).first():
        for i in range(1, 51):
            db.add(models.User(username=f"user{i}", email=f"user{i}@demo.com", age=random.randint(18, 45), gender=random.choice(["male", "female"]), city=random.choice(["北京", "上海", "广州", "深圳"])))

    if not db.query(models.Product).first():
        for i in range(1, 81):
            db.add(models.Product(name=f"商品{i}", category=random.choice(CATEGORIES), price=round(random.uniform(39, 6999), 2), sales=random.randint(0, 1000), rating=round(random.uniform(3.0, 5.0), 1), description="毕业设计演示商品"))

    db.commit()

    users = db.query(models.User).all()
    products = db.query(models.Product).all()
    if not db.query(models.UserBehavior).first():
        for _ in range(1200):
            u = random.choice(users)
            p = random.choice(products)
            bt = random.choice(BEHAVIORS)
            db.add(models.UserBehavior(user_id=u.id, product_id=p.id, behavior_type=bt, score={"view": 1, "favorite": 2, "cart": 3, "buy": 5, "review": 4}[bt], remark="模拟行为"))

    db.commit()
    db.close()
    print("seed 完成")


if __name__ == "__main__":
    run()
