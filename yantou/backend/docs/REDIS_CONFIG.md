# Redis 配置和使用文档

## 概述

本项目使用 Redis 作为缓存和 JWT Token 黑名单存储。Redis 提供了高性能的内存数据存储，用于：

- **缓存**：提高应用性能，减少数据库查询
- **JWT Token 黑名单**：管理已失效的 JWT Token
- **会话存储**（可选）：存储用户会话信息

## Redis 服务配置

### Docker 容器

项目使用 Docker Compose 管理 Redis 服务：

```yaml
redis:
  image: redis:7-alpine
  container_name: yantou-redis
  command: redis-server --requirepass sj1qaz
  ports:
    - "6379:6379"
  volumes:
    - yantou-redis-data:/data
  restart: unless-stopped
```

### 启动 Redis

```bash
# 使用 Docker Compose 启动
docker-compose up -d redis

# 或单独启动 Redis 容器
docker start yantou-redis
```

### 连接信息

- **主机**: `localhost` (开发环境)
- **端口**: `6379`
- **密码**: `sj1qaz`
- **数据库**: `0` (默认)
- **连接 URL**: `redis://:sj1qaz@localhost:6379/0`

## Django 配置

### 环境变量

在 `.env` 文件中配置 Redis 连接信息：

```env
# Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=sj1qaz
```

### 缓存配置

在 `config/settings/base.py` 中配置了 Redis 缓存：

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,
                'retry_on_timeout': True,
            },
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
            'IGNORE_EXCEPTIONS': True,  # 缓存失败时不影响应用运行
        },
        'KEY_PREFIX': 'yantou',
        'TIMEOUT': 300,  # 默认缓存超时时间（秒）
    }
}
```

### JWT Token 黑名单配置

JWT Token 黑名单使用 Redis 存储已失效的 Token：

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,  # 刷新后加入黑名单
    # ... 其他配置
}
```

已安装的应用：
- `django_redis`: Redis 缓存支持
- `rest_framework_simplejwt.token_blacklist`: JWT Token 黑名单

## 使用方法

### 1. 缓存操作

#### 基本缓存操作

```python
from django.core.cache import cache

# 设置缓存
cache.set('key', 'value', timeout=300)  # 300 秒后过期

# 获取缓存
value = cache.get('key')

# 删除缓存
cache.delete('key')

# 检查键是否存在
if cache.has_key('key'):
    value = cache.get('key')

# 设置多个键值对
cache.set_many({'key1': 'value1', 'key2': 'value2'})

# 获取多个键
values = cache.get_many(['key1', 'key2'])

# 删除多个键
cache.delete_many(['key1', 'key2'])

# 清空所有缓存（谨慎使用）
cache.clear()
```

#### 使用缓存装饰器

```python
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView

# 函数视图
@cache_page(60 * 15)  # 缓存 15 分钟
def my_view(request):
    return HttpResponse("Hello")

# 类视图
@method_decorator(cache_page(60 * 15), name='dispatch')
class MyView(APIView):
    def get(self, request):
        return Response({"data": "cached"})
```

#### 缓存模板片段

```django
{% load cache %}
{% cache 500 sidebar %}
    .. sidebar ..
{% endcache %}
```

### 2. JWT Token 黑名单

#### Token 刷新和黑名单

当用户刷新 Token 时，旧的 Refresh Token 会自动加入黑名单：

```python
from rest_framework_simplejwt.tokens import RefreshToken

# 创建 Token
refresh = RefreshToken.for_user(user)
access_token = str(refresh.access_token)
refresh_token = str(refresh)

# 刷新 Token（旧 Token 会自动加入黑名单）
refresh = RefreshToken(refresh_token)
new_access_token = str(refresh.access_token)
new_refresh_token = str(refresh)

# 将 Token 加入黑名单（登出时使用）
refresh = RefreshToken(refresh_token)
refresh.blacklist()
```

#### 使用工具函数

项目提供了 JWT 工具函数（`utils/jwt.py`）：

```python
from utils.jwt import create_token_pair, blacklist_token, refresh_access_token

# 创建 Token 对
tokens = create_token_pair(user)
# 返回: {'access': '...', 'refresh': '...'}

# 刷新 Access Token
new_tokens = refresh_access_token(refresh_token)
# 返回: {'access': '...'}

# 将 Token 加入黑名单
success = blacklist_token(refresh_token)
# 返回: True/False
```

### 3. 会话存储（可选）

如果需要使用 Redis 存储会话，可以配置：

```python
# 在 settings.py 中
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

## 监控和维护

### 检查 Redis 连接

```bash
# 使用 Redis CLI 连接
docker exec -it yantou-redis redis-cli -a sj1qaz

# 测试连接
PING
# 应该返回: PONG

# 查看信息
INFO server
INFO stats
```

### 查看缓存键

```bash
# 连接 Redis
docker exec -it yantou-redis redis-cli -a sj1qaz

# 查看所有键（使用前缀）
KEYS yantou:*

# 查看特定键的值
GET yantou:your_key

# 查看键的过期时间
TTL yantou:your_key
```

### 监控 Redis 性能

```bash
# 查看 Redis 统计信息
docker exec yantou-redis redis-cli -a sj1qaz INFO stats

# 查看内存使用
docker exec yantou-redis redis-cli -a sj1qaz INFO memory

# 查看客户端连接
docker exec yantou-redis redis-cli -a sj1qaz CLIENT LIST
```

### 清理缓存

```bash
# 连接 Redis
docker exec -it yantou-redis redis-cli -a sj1qaz

# 删除所有以 yantou: 开头的键
KEYS yantou:* | xargs redis-cli -a sj1qaz DEL

# 或使用 Python
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
```

## 性能优化

### 1. 连接池配置

已配置连接池，最大连接数为 50：

```python
'CONNECTION_POOL_KWARGS': {
    'max_connections': 50,
    'retry_on_timeout': True,
}
```

### 2. 压缩

启用了压缩功能，减少内存使用：

```python
'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
```

### 3. 异常处理

配置了 `IGNORE_EXCEPTIONS: True`，确保 Redis 故障时不影响应用运行。

### 4. 缓存策略

- **短期缓存**：频繁访问的数据，设置较短的过期时间（如 5-15 分钟）
- **长期缓存**：不经常变化的数据，设置较长的过期时间（如 1 小时或更长）
- **永久缓存**：几乎不变的数据，不设置过期时间（谨慎使用）

## 故障排查

### 问题 1: Redis 连接失败

**症状**: `ConnectionError` 或 `TimeoutError`

**解决方案**:
1. 检查 Redis 容器是否运行：`docker ps | grep redis`
2. 检查端口是否正确：`netstat -an | grep 6379`
3. 检查密码是否正确
4. 检查防火墙设置

### 问题 2: 缓存不工作

**症状**: 缓存设置后无法获取

**解决方案**:
1. 检查 Redis 连接：`python manage.py shell` 然后 `from django.core.cache import cache; cache.set('test', 'value'); cache.get('test')`
2. 检查键前缀是否正确
3. 检查缓存过期时间

### 问题 3: JWT Token 黑名单不生效

**症状**: 已加入黑名单的 Token 仍然有效

**解决方案**:
1. 检查 `rest_framework_simplejwt.token_blacklist` 是否在 `INSTALLED_APPS` 中
2. 运行迁移：`python manage.py migrate`
3. 检查数据库表是否存在：`token_blacklist_blacklistedtoken`

## 安全建议

1. **密码保护**: 生产环境必须设置强密码
2. **网络隔离**: 生产环境应将 Redis 放在内网，不暴露公网端口
3. **定期备份**: 重要数据需要定期备份
4. **监控告警**: 设置 Redis 监控和告警
5. **访问控制**: 限制 Redis 的访问权限

## 相关文档

- [Django Redis 文档](https://github.com/jazzband/django-redis)
- [Redis 官方文档](https://redis.io/documentation)
- [djangorestframework-simplejwt 文档](https://django-rest-framework-simplejwt.readthedocs.io/)

## 更新日志

- **2025-12-06**: 初始配置 Redis 和 JWT Token 黑名单
  - 配置 Redis 缓存
  - 集成 JWT Token 黑名单
  - 添加 Docker Compose 配置
  - 创建工具函数

