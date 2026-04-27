from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import PredictRequest, PredictResponse
from ..services.predict_service import predict_behavior
from ..auth import verify_token

router = APIRouter(tags=["predict"])


@router.post("/api/predict", response_model=PredictResponse, dependencies=[Depends(verify_token)])
def predict(req: PredictRequest, db: Session = Depends(get_db)):
    return predict_behavior(db, req.user_id, req.product_id)
