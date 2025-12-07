# API 文档使用指南

## 📋 概述

本项目使用 `drf-spectacular` 自动生成 API 文档，基于 OpenAPI 3.0 规范，提供 Swagger UI 和 ReDoc 两种文档界面。

## 🚀 访问文档

### 开发环境

启动开发服务器后，可以通过以下地址访问 API 文档：

1. **Swagger UI**（交互式文档）
   ```
   http://localhost:8000/api/docs/
   ```
   - 支持在线测试 API
   - 可以查看请求/响应示例
   - 支持 JWT 认证

2. **ReDoc**（美观的文档）
   ```
   http://localhost:8000/api/redoc/
   ```
   - 更美观的文档展示
   - 适合阅读和分享

3. **OpenAPI Schema**（JSON 格式）
   ```
   http://localhost:8000/api/schema/
   ```
   - 原始 OpenAPI 3.0 JSON 格式
   - 可用于导入 Postman、Insomnia 等工具

### 生产环境

生产环境默认不提供文档访问（仅在 DEBUG=True 时可用）。如需在生产环境提供文档，需要：

1. 配置访问权限
2. 使用 Nginx 等反向代理限制访问
3. 或使用独立的文档服务器

## 📝 文档内容

### 已包含的 API

#### 认证相关 (`/api/v1/auth/`)

1. **用户注册**
   - `POST /api/v1/auth/register/`
   - 描述：新用户注册
   - 请求体：`username`, `password`, `password_confirm`
   - 响应：包含 JWT Token 和用户信息

2. **用户登录**
   - `POST /api/v1/auth/login/`
   - 描述：用户登录
   - 请求体：`username`, `password`, `captcha`（可选）
   - 响应：包含 JWT Token 和用户信息

3. **获取验证码**
   - `GET /api/v1/auth/captcha/`
   - 描述：获取登录验证码（登录失败次数过多时需要）
   - 响应：验证码字符串

4. **刷新 Token**
   - `POST /api/v1/auth/refresh/`
   - 描述：使用 Refresh Token 获取新的 Access Token
   - 请求体：`refresh`
   - 响应：新的 Access Token 和 Refresh Token（如果启用了 Token 旋转）

5. **用户登出**
   - `POST /api/v1/auth/logout/`
   - 描述：用户登出，将 Refresh Token 加入黑名单
   - 需要认证：是
   - 请求体：`refresh`

#### 系统相关

1. **健康检查**
   - `GET /api/v1/health/` 或 `GET /health/`
   - 描述：检查系统健康状态和数据库连接
   - 响应：系统状态信息

## 🔐 认证说明

### JWT 认证

所有需要认证的 API 都需要在请求头中携带 JWT Token：

```
Authorization: Bearer <access_token>
```

### 在 Swagger UI 中使用认证

1. 点击右上角的 **"Authorize"** 按钮
2. 在弹出框中输入：`Bearer <your_access_token>`
3. 点击 **"Authorize"** 确认
4. 之后的所有请求都会自动携带 Token

### 获取 Token

1. 通过注册接口获取（注册成功后自动返回）
2. 通过登录接口获取（登录成功后返回）

## 📊 响应格式

### 成功响应

```json
{
  "success": true,
  "code": 200,
  "message": "操作成功",
  "data": {
    // 响应数据
  },
  "request_id": "req_abc123def456",
  "timestamp": "2025-12-06T16:00:00Z"
}
```

### 错误响应

```json
{
  "success": false,
  "code": "E001001",
  "message": "错误描述",
  "error": "详细错误信息",
  "errors": {
    "field_name": ["具体错误"]
  },
  "data": null,
  "request_id": "req_abc123def456",
  "error_id": "err_789xyz012abc",
  "timestamp": "2025-12-06T16:00:00Z"
}
```

## 🛠️ 使用示例

### 1. 用户注册

```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123",
    "password_confirm": "password123"
  }'
```

### 2. 用户登录

```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### 3. 使用 Token 访问受保护的 API

```bash
curl -X GET http://localhost:8000/api/v1/users/me/ \
  -H "Authorization: Bearer <access_token>"
```

### 4. 刷新 Token

```bash
curl -X POST http://localhost:8000/api/v1/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "<refresh_token>"
  }'
```

## 📦 导出文档

### 导出 OpenAPI Schema

```bash
# 获取 JSON 格式的 Schema
curl http://localhost:8000/api/schema/ > openapi.json

# 获取 YAML 格式的 Schema
curl http://localhost:8000/api/schema/?format=openapi > openapi.yaml
```

### 导入到其他工具

#### Postman

1. 打开 Postman
2. 点击 **Import**
3. 选择 **Link**
4. 输入：`http://localhost:8000/api/schema/`
5. 点击 **Continue** 导入

#### Insomnia

1. 打开 Insomnia
2. 点击 **Create** > **Import/Export** > **Import Data**
3. 选择 **From URL**
4. 输入：`http://localhost:8000/api/schema/`
5. 点击 **Import**

## 🔧 配置说明

### 文档配置位置

文档配置在 `config/settings/base.py` 中的 `SPECTACULAR_SETTINGS`：

```python
SPECTACULAR_SETTINGS = {
    'TITLE': '企业级应用 API 文档',
    'DESCRIPTION': '基于 Django REST Framework 的企业级应用后端 API 文档',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'],
    'SERVE_AUTHENTICATION': None,
    'SCHEMA_PATH_PREFIX': '/api/v1/',
    'TAGS': [
        {'name': '认证', 'description': '用户认证相关接口'},
        {'name': '用户', 'description': '用户管理相关接口'},
        {'name': '权限', 'description': '权限管理相关接口'},
        {'name': '系统', 'description': '系统相关接口'},
    ],
    # ... 更多配置
}
```

### 自定义文档

#### 在视图中添加文档注释

使用 `@extend_schema` 装饰器：

```python
from drf_spectacular.utils import extend_schema, OpenApiExample

@extend_schema(
    tags=['认证'],
    summary='用户登录',
    description='用户登录接口的详细描述',
    request=LoginSerializer,
    responses={
        200: {
            'description': '登录成功',
            'examples': [
                OpenApiExample(
                    '成功响应',
                    value={
                        'success': True,
                        'data': {...}
                    }
                )
            ]
        }
    }
)
def post(self, request):
    # 视图逻辑
    pass
```

#### 在序列化器中添加字段说明

```python
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        help_text='用户名',
        description='用户的登录用户名'
    )
    password = serializers.CharField(
        write_only=True,
        help_text='密码',
        description='用户的登录密码'
    )
```

## 📚 相关资源

- [drf-spectacular 官方文档](https://drf-spectacular.readthedocs.io/)
- [OpenAPI 3.0 规范](https://swagger.io/specification/)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)
- [ReDoc](https://github.com/Redocly/redoc)

## 🎯 最佳实践

1. **保持文档更新**
   - 每次修改 API 时更新文档注释
   - 添加清晰的描述和示例

2. **使用标签分类**
   - 将相关 API 归类到同一标签
   - 便于前端开发者查找

3. **提供示例**
   - 为每个 API 提供请求/响应示例
   - 包含成功和失败场景

4. **说明认证要求**
   - 明确标注哪些 API 需要认证
   - 说明认证方式（JWT、Session 等）

5. **错误码文档**
   - 在文档中说明错误码含义
   - 参考 `docs/ERROR_CODES.md`

---

**文档版本**: v1.0.0  
**最后更新**: 2025-12-06

