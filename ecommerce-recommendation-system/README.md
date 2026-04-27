# 基于多源数据的电商用户行为预测与推荐系统（前后端分离）

> 技术栈：Vue3 + Vite + Element Plus + ECharts + FastAPI + MySQL + SQLAlchemy + scikit-learn。

## 1. 项目简介
本系统适合作为本科毕业设计，完整覆盖：
- 电商用户、商品、行为日志管理
- 数据看板可视化
- 用户行为预测（点击/加购/购买概率）
- 个性化推荐（混合推荐）
- 模型训练与数据导入

## 2. 目录结构
```text
ecommerce-recommendation-system/
  backend/
    app/
      main.py
      database.py
      models.py
      schemas.py
      crud.py
      auth.py
      routers/
      services/
      utils/
    init_mysql.sql
    requirements.txt
    README.md
  frontend/
    src/
      api/
      router/
      views/
      components/
      store/
      App.vue
      main.js
    package.json
    vite.config.js
  README.md
```

## 3. 数据库设计
核心表：
1. users
2. products
3. user_behaviors
4. recommendations
5. model_metrics
6. admins

请执行 `backend/init_mysql.sql` 初始化。

## 4. 推荐算法设计（可运行基础版）
混合策略：
1. 行为权重（view=1, favorite=2, cart=3, review=4, buy=5）
2. 商品分类相似度
3. 热门商品兜底
4. 新用户：直接热门推荐
5. 新商品：使用分类和属性补充分值

## 5. 行为预测模型设计（可运行基础版）
- 特征：
  - 用户历史行为次数
  - 商品历史点击量
  - 商品历史购买量
  - 商品类别（编码）
  - 商品价格
  - 用户类别偏好分数
- 模型：RandomForestClassifier
- 模型文件：`backend/models/model.pkl`

## 6. Windows 本地运行步骤
### 6.1 后端
```bash
cd ecommerce-recommendation-system/backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
mysql -uroot -p < init_mysql.sql
python -m app.utils.seed_data
uvicorn app.main:app --reload
```

### 6.2 前端
```bash
cd ecommerce-recommendation-system/frontend
npm install
npm run dev
```
默认地址：`http://127.0.0.1:5173`

## 7. 测试账号
- 管理员：admin / admin123

## 8. 主要接口
- 登录：`POST /api/login`
- 用户管理：`/api/users`
- 商品管理：`/api/products`
- 行为日志：`/api/behaviors`
- 看板统计：`GET /api/dashboard/stats`
- 行为预测：`POST /api/predict`
- 推荐：`GET /api/recommend/{user_id}`
- 模型训练：`POST /api/model/train`
- 数据导入：`POST /api/model/import?data_type=users|products|behaviors`

## 9. 页面功能清单
1. 登录页
2. 首页看板（统计卡片 + 饼图 + 折线图）
3. 用户管理页
4. 商品管理页
5. 行为数据页（支持筛选）
6. 行为预测页
7. 个性化推荐页
8. 系统管理页（导入、训练、刷新）

## 10. 毕设说明
本项目具备功能完整性、可视化展示、算法实现、模型训练接口和清晰代码结构，可作为本科毕业设计基础版本，后续可继续扩展到深度学习推荐、在线学习和A/B测试。

## 11. GitHub 部署
1. 在 GitHub 创建空仓库（建议同名：`ecommerce-recommendation-system`）。
2. 本地执行：
```bash
git remote add origin https://github.com/<你的用户名>/ecommerce-recommendation-system.git
git branch -M main
git push -u origin main
```
3. 如果已有远程：
```bash
git remote remove origin
git remote add origin <你的仓库地址>
```
