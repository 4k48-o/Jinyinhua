# 企业级应用后端项目

基于 Django + Django REST Framework 的企业级应用后端系统。

## 项目结构

```
backend/
├── config/                 # Django 项目配置
│   ├── settings/          # 多环境配置
│   │   ├── base.py        # 基础配置
│   │   ├── development.py # 开发环境
│   │   ├── production.py  # 生产环境
│   │   └── testing.py    # 测试环境
│   ├── urls.py            # 主 URL 配置
│   ├── urls_api.py        # API 路由配置
│   └── wsgi.py            # WSGI 配置
│
├── apps/                   # 应用目录
│   ├── users/             # 用户管理应用
│   ├── auth/              # 认证应用
│   ├── permissions/       # 权限管理应用
│   └── common/            # 通用应用
│
├── middleware/             # 自定义中间件
├── utils/                 # 全局工具
├── requirements/           # 依赖管理
├── manage.py              # Django 管理脚本
├── docker-compose.yml     # Docker Compose 配置
└── README.md
```

## 快速开始

### 1. 启动 PostgreSQL 数据库

使用 Docker Compose 启动 PostgreSQL：

```bash
docker-compose up -d postgres
```

或者使用 Docker 命令：

```bash
docker run -d --name yantou-postgres \
  -e POSTGRES_PASSWORD=0qww294e \
  -e POSTGRES_DB=yantou_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_INITDB_ARGS="--encoding=UTF8 --locale=zh_CN.UTF-8" \
  -p 5432:5432 \
  -v yantou-postgres-data:/var/lib/postgresql/data \
  postgres:15-alpine
```

### 2. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements/base.txt
pip install -r requirements/development.txt
```

### 4. 配置环境变量

```bash
cp env.example .env
# 编辑 .env 文件，配置数据库等信息
```

默认数据库配置：
- 数据库名：`yantou_db`
- 用户名：`postgres`
- 密码：`0qww294e`
- 主机：`localhost`
- 端口：`5432`

### 5. 运行迁移

```bash
python manage.py migrate
```

### 6. 创建超级用户

```bash
python manage.py createsuperuser
```

### 7. 启动开发服务器

```bash
python manage.py runserver
```

## 环境配置

项目支持多环境配置：

- **开发环境**: `config.settings.development` (默认)
- **生产环境**: `config.settings.production`
- **测试环境**: `config.settings.testing`

通过环境变量 `DJANGO_SETTINGS_MODULE` 切换环境。

## 数据库配置

### PostgreSQL 配置

项目默认使用 PostgreSQL 数据库，配置信息：

- **数据库引擎**: `django.db.backends.postgresql`
- **数据库名称**: `yantou_db`
- **字符集**: UTF8
- **连接池**: 已配置，最大存活时间 600 秒

### 数据库连接

数据库连接配置在 `.env` 文件中：

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=yantou_db
DB_USER=postgres
DB_PASSWORD=0qww294e
DB_HOST=localhost
DB_PORT=5432
DB_CONN_MAX_AGE=600
```

## Redis 配置

### Redis 服务

项目使用 Redis 作为缓存和 JWT Token 黑名单存储：

- **主机**: `localhost`
- **端口**: `6379`
- **密码**: `sj1qaz`
- **数据库**: `0`

### Redis 连接

Redis 连接配置在 `.env` 文件中：

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=sj1qaz
```

### 启动 Redis

```bash
# 使用 Docker Compose
docker-compose up -d redis

# 或单独启动
docker start yantou-redis
```

### Redis 用途

- **缓存**: 提高应用性能，减少数据库查询
- **JWT Token 黑名单**: 管理已失效的 JWT Token
- **会话存储**: （可选）存储用户会话信息

详细配置和使用说明请参考 [Redis 配置文档](docs/REDIS_CONFIG.md)。

## 应用说明

- **apps.users**: 用户管理模块
- **apps.auth**: 认证模块（登录、注册、Token 等）
- **apps.permissions**: 权限管理模块（角色、权限）
- **apps.common**: 通用功能模块（响应、异常、日志等）

## Docker 使用

### 启动服务

```bash
docker-compose up -d
```

### 停止服务

```bash
docker-compose down
```

### 查看日志

```bash
docker-compose logs -f postgres
```

### 进入数据库

```bash
docker exec -it yantou-postgres psql -U postgres -d yantou_db
```

## 开发规范

- 遵循 PEP 8 代码风格
- 使用 Black 进行代码格式化
- 使用 isort 进行导入排序
- 添加类型提示（Type Hints）
