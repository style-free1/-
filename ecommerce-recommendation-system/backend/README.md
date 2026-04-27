# Backend（FastAPI）

## 1. 安装
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 2. 配置数据库
默认连接串：`mysql+pymysql://root:123456@127.0.0.1:3306/ecommerce_rec?charset=utf8mb4`。
可用环境变量覆盖：
```bash
set DATABASE_URL=mysql+pymysql://root:password@127.0.0.1:3306/ecommerce_rec?charset=utf8mb4
```

## 3. 初始化表与模拟数据
```bash
mysql -uroot -p < init_mysql.sql
python -m app.utils.seed_data
```

## 4. 启动
```bash
uvicorn app.main:app --reload
```
访问：
- Swagger 文档：http://127.0.0.1:8000/docs
- ReDoc：http://127.0.0.1:8000/redoc

## 5. 测试账号
- 用户名：admin
- 密码：admin123
