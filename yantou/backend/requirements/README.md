# 依赖管理说明

## 文件说明

- **base.txt**: 基础依赖，所有环境都需要
- **development.txt**: 开发环境依赖，包含开发工具和测试框架
- **production.txt**: 生产环境依赖，包含生产服务器和监控工具

## 安装方式

### 开发环境

```bash
pip install -r requirements/development.txt
```

### 生产环境

```bash
pip install -r requirements/production.txt
```

### 仅安装基础依赖

```bash
pip install -r requirements/base.txt
```

## 依赖说明

### 核心依赖

- **Django**: Web 框架
- **djangorestframework**: RESTful API 框架
- **djangorestframework-simplejwt**: JWT 认证
- **django-cors-headers**: CORS 跨域支持
- **django-filter**: 过滤和搜索
- **python-decouple**: 环境变量管理
- **Pillow**: 图片处理
- **psycopg2-binary**: PostgreSQL 数据库驱动

### 开发工具

- **black**: 代码格式化
- **isort**: 导入排序
- **flake8**: 代码检查
- **pytest**: 测试框架
- **django-debug-toolbar**: 调试工具
- **drf-spectacular**: API 文档生成

### 生产工具

- **gunicorn**: WSGI 服务器
- **sentry-sdk**: 错误监控
- **redis**: 缓存支持
- **django-redis**: Django Redis 集成

## 版本管理

建议使用 `pip freeze > requirements.txt` 锁定具体版本，但本项目的 requirements 文件使用版本范围，便于更新。

## 更新依赖

```bash
# 更新所有依赖
pip install --upgrade -r requirements/development.txt

# 检查过时的包
pip list --outdated
```

