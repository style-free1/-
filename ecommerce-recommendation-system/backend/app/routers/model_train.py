from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
import pandas as pd
import joblib
from ..database import get_db
from .. import models
from ..auth import verify_token

router = APIRouter(prefix="/api/model", tags=["model"])

MODEL_PATH = Path(__file__).resolve().parents[2] / "models" / "model.pkl"


@router.post("/train", dependencies=[Depends(verify_token)])
def train_model(db: Session = Depends(get_db)):
    # 从行为日志构建基础训练数据
    rows = db.query(models.UserBehavior).all()
    if len(rows) < 20:
        return {"message": "样本不足，至少需要 20 条行为日志", "trained": False}

    data = []
    for r in rows:
        prod = db.query(models.Product).filter(models.Product.id == r.product_id).first()
        data.append(
            {
                "user_behavior_count": db.query(models.UserBehavior).filter(models.UserBehavior.user_id == r.user_id).count(),
                "product_click_count": db.query(models.UserBehavior).filter(models.UserBehavior.product_id == r.product_id, models.UserBehavior.behavior_type == "view").count(),
                "product_buy_count": db.query(models.UserBehavior).filter(models.UserBehavior.product_id == r.product_id, models.UserBehavior.behavior_type == "buy").count(),
                "category": hash(prod.category if prod else "unknown") % 100,
                "price": prod.price if prod else 0,
                "category_pref": db.query(models.UserBehavior).join(models.Product, models.Product.id == models.UserBehavior.product_id).filter(models.UserBehavior.user_id == r.user_id, models.Product.category == (prod.category if prod else "unknown")).count(),
                "label": 1 if r.behavior_type == "buy" else 0,
            }
        )

    df = pd.DataFrame(data)
    x = df[["user_behavior_count", "product_click_count", "product_buy_count", "category", "price", "category_pref"]]
    y = df["label"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=120, random_state=42)
    model.fit(x_train, y_train)

    pred = model.predict(x_test)
    acc = accuracy_score(y_test, pred)
    p = precision_score(y_test, pred, zero_division=0)
    r = recall_score(y_test, pred, zero_division=0)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    metric = models.ModelMetric(model_name="RandomForestClassifier", accuracy=acc, precision=p, recall=r, auc=0)
    db.add(metric)
    db.commit()

    return {
        "trained": True,
        "model_path": str(MODEL_PATH),
        "accuracy": round(acc, 4),
        "precision": round(p, 4),
        "recall": round(r, 4),
    }


@router.post("/import", dependencies=[Depends(verify_token)])
async def import_csv(data_type: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = pd.read_csv(file.file)
    if data_type == "users":
        for _, row in df.iterrows():
            db.add(models.User(username=row["username"], email=row["email"], age=int(row.get("age", 18)), gender=row.get("gender", "unknown"), city=row.get("city", "")))
    elif data_type == "products":
        for _, row in df.iterrows():
            db.add(models.Product(name=row["name"], category=row["category"], price=float(row.get("price", 0)), sales=int(row.get("sales", 0)), rating=float(row.get("rating", 0)), description=row.get("description", "")))
    elif data_type == "behaviors":
        for _, row in df.iterrows():
            db.add(models.UserBehavior(user_id=int(row["user_id"]), product_id=int(row["product_id"]), behavior_type=row["behavior_type"], score=float(row.get("score", 1)), remark=row.get("remark", "")))
    else:
        return {"message": "data_type 必须是 users/products/behaviors"}
    db.commit()
    return {"message": f"{data_type} 导入成功", "rows": len(df)}
