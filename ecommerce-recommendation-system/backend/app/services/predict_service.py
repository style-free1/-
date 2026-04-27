"""行为预测服务。"""
from pathlib import Path
import joblib
import numpy as np
from sqlalchemy.orm import Session
from .feature_service import build_features

MODEL_PATH = Path(__file__).resolve().parents[2] / "models" / "model.pkl"


def predict_behavior(db: Session, user_id: int, product_id: int):
    features = build_features(db, user_id, product_id)
    base = np.array(
        [
            features["user_behavior_count"],
            features["product_click_count"],
            features["product_buy_count"],
            hash(features["product_category"]) % 100,
            features["product_price"],
            features["category_pref_score"],
        ]
    ).reshape(1, -1)

    if MODEL_PATH.exists():
        model = joblib.load(MODEL_PATH)
        buy_prob = float(model.predict_proba(base)[0][1])
    else:
        buy_prob = min(0.95, 0.05 + features["category_pref_score"] * 0.02)

    click_prob = min(0.99, buy_prob + 0.25)
    cart_prob = min(0.98, buy_prob + 0.1)

    return {
        "click_prob": round(click_prob, 4),
        "cart_prob": round(cart_prob, 4),
        "buy_prob": round(buy_prob, 4),
    }
