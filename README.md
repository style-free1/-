# ecommerce-recommendation-system

项目代码位于 `ecommerce-recommendation-system/` 目录。

## 部署到 GitHub（Windows）

> 你可以直接复制下面命令执行。

### 1) 在 GitHub 创建空仓库
例如仓库名：`ecommerce-recommendation-system`（不要勾选初始化 README）。

### 2) 在本地仓库配置远程并推送
```bash
git remote add origin https://github.com/<你的用户名>/ecommerce-recommendation-system.git
git branch -M main
git push -u origin main
```

### 3) 如果你使用 SSH（推荐）
```bash
git remote add origin git@github.com:<你的用户名>/ecommerce-recommendation-system.git
git branch -M main
git push -u origin main
```

### 4) 后续更新
```bash
git add .
git commit -m "feat: 更新项目"
git push
```

## 常见问题
1. `remote origin already exists`：
```bash
git remote remove origin
git remote add origin <你的仓库地址>
```
2. HTTPS 推送需要 token：使用 GitHub Personal Access Token 作为密码，或改用 SSH。
