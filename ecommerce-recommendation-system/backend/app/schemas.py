"""Pydantic 数据结构。"""
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserBase(BaseModel):
    username: str
    email: EmailStr
    age: int = 18
    gender: str = "unknown"
    city: str = ""


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    city: Optional[str] = None


class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    category: str
    price: float
    sales: int = 0
    rating: float = 0
    description: str = ""


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    sales: Optional[int] = None
    rating: Optional[float] = None
    description: Optional[str] = None


class ProductOut(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class BehaviorBase(BaseModel):
    user_id: int
    product_id: int
    behavior_type: str
    score: float = 1
    remark: str = ""


class BehaviorCreate(BehaviorBase):
    pass


class BehaviorOut(BehaviorBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PredictRequest(BaseModel):
    user_id: int
    product_id: int


class PredictResponse(BaseModel):
    click_prob: float
    cart_prob: float
    buy_prob: float


class RecommendItem(BaseModel):
    product_id: int
    product_name: str
    reason: str
    score: float


class DashboardStats(BaseModel):
    user_count: int
    product_count: int
    behavior_count: int
    recommend_ctr: float
    behavior_distribution: dict
    recommend_trend: List[dict]
