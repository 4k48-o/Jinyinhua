# 中间件说明

## 概述

本项目实现了三个自定义中间件，用于处理请求日志、异常处理和 CORS 配置。

## 中间件列表

### 1. CORS 中间件 (corsheaders.middleware.CorsMiddleware)

**功能**: 处理跨域资源共享（CORS）

**配置位置**: `config/settings/base.py`

**配置项**:
- `CORS_ALLOWED_ORIGINS`: 允许的跨域来源
- `CORS_ALLOW_CREDENTIALS`: 是否允许携带凭证
- `CORS_ALLOW_METHODS`: 允许的 HTTP 方法
- `CORS_ALLOW_HEADERS`: 允许的请求头

**使用**: 自动处理所有跨域请求，无需额外代码

### 2. 请求日志中间件 (middleware.logging.RequestLoggingMiddleware)

**功能**: 记录所有 HTTP 请求的详细信息

**记录内容**:
- 请求方法（GET, POST, PUT, DELETE 等）
- 请求路径
- 查询参数
- 响应状态码
- 执行时间（毫秒）
- 客户端 IP 地址
- 用户信息（如果已认证）

**日志级别**:
- `INFO`: 正常请求（2xx, 3xx）
- `WARNING`: 客户端错误（4xx）
- `ERROR`: 服务器错误（5xx）

**示例日志**:
```
INFO Request: {'method': 'GET', 'path': '/api/v1/users/', 'status_code': 200, 'execution_time_ms': 45.23, 'ip': '127.0.0.1', 'username': 'admin'}
```

### 3. 异常处理中间件 (middleware.exception.ExceptionHandlingMiddleware)

**功能**: 统一处理应用异常，返回标准格式的错误响应

**处理的异常类型**:
- `PermissionDenied`: 权限不足（403）
- `ValidationError`: 数据验证失败（400）
- `APIException`: DRF 异常（由 DRF 处理器处理）
- 其他未处理异常（500）

**响应格式**:
```json
{
  "code": 400,
  "message": "错误描述",
  "error": "详细错误信息",
  "errors": {
    "field_name": ["具体错误"]
  },
  "data": null
}
```

**开发环境**: 返回详细错误信息和堆栈跟踪
**生产环境**: 返回通用错误信息，不暴露内部细节

## 中间件执行顺序

中间件按照 `MIDDLEWARE` 列表的顺序执行：

1. SecurityMiddleware - 安全相关
2. SessionMiddleware - 会话管理
3. CorsMiddleware - CORS 处理
4. CommonMiddleware - 通用处理
5. CsrfViewMiddleware - CSRF 保护
6. AuthenticationMiddleware - 认证
7. MessageMiddleware - 消息框架
8. XFrameOptionsMiddleware - 点击劫持保护
9. **RequestLoggingMiddleware** - 请求日志（自定义）
10. **ExceptionHandlingMiddleware** - 异常处理（自定义）

## 自定义中间件

### 添加新的中间件

1. 在 `middleware/` 目录创建新的中间件文件
2. 继承 `MiddlewareMixin`
3. 实现需要的方法：
   - `process_request(request)`: 处理请求前
   - `process_response(request, response)`: 处理响应后
   - `process_exception(request, exception)`: 处理异常
4. 在 `config/settings/base.py` 的 `MIDDLEWARE` 列表中添加

### 示例

```python
from django.utils.deprecation import MiddlewareMixin

class CustomMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 处理请求前的逻辑
        return None
    
    def process_response(self, request, response):
        # 处理响应后的逻辑
        return response
```

## 测试中间件

### 测试请求日志

```bash
# 启动开发服务器
python manage.py runserver

# 发送请求，查看控制台日志
curl http://localhost:8000/admin/
```

### 测试异常处理

```python
# 在视图中抛出异常
from django.core.exceptions import PermissionDenied

def test_view(request):
    raise PermissionDenied("测试异常处理")
```

## 注意事项

1. **中间件顺序很重要**: 确保中间件在正确的位置
2. **性能影响**: 请求日志中间件会记录所有请求，生产环境注意性能
3. **异常处理**: 异常处理中间件应该放在最后，确保能捕获所有异常
4. **CORS 配置**: 生产环境需要正确配置 `CORS_ALLOWED_ORIGINS`

