from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from . import models
from .schemas import LoginRequest, TokenResponse
from .auth import create_token, verify_token
from .routers import users, products, behaviors, dashboard, predict, recommend, model_train

app = FastAPI(title="电商用户行为预测与推荐系统 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    # 初始化默认管理员
    with next(get_db()) as db:
        exists = db.query(models.Admin).filter(models.Admin.username == "admin").first()
        if not exists:
            db.add(models.Admin(username="admin", password_hash="admin123", role="super_admin"))
            db.commit()


@app.get("/")
def root():
    return {"message": "backend running", "swagger": "/docs"}


@app.post("/api/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.username == req.username).first()
    if not admin or admin.password_hash != req.password:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    return TokenResponse(access_token=create_token(req.username))


@app.get("/api/health", dependencies=[Depends(verify_token)])
def health():
    return {"status": "ok"}


app.include_router(users.router)
app.include_router(products.router)
app.include_router(behaviors.router)
app.include_router(dashboard.router)
app.include_router(predict.router)
app.include_router(recommend.router)
app.include_router(model_train.router)
