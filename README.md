# CMDB 系统

这是一个基于Python和Flask的CMDB（配置管理数据库）系统。

## 功能特性

- 用户认证和授权（JWT）
- 基本的增删改查操作
- 日志记录功能

## 安装

1. 克隆项目
2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 配置

1. 修改 `config/database.py` 中的数据库连接信息：
```python
DATABASE_URL = "mysql+pymysql://username:password@localhost/cmdb"
```

2. 修改 `src/app.py` 中的 JWT 密钥：
```python
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
```

## 运行

```bash
python src/app.py
```

## API 接口

### 认证
- POST /api/login - 用户登录

### 受保护的接口
- GET /api/protected - 示例受保护接口 