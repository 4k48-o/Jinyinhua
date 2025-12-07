# 切面日志功能说明

## 概述

项目提供了三种切面（AOP）方式来统一收集和保存日志，无需在每个方法中手动添加日志记录代码。

## 三种切面方式

### 1. 中间件切面（RequestLoggingMiddleware）

**位置**：`backend/middleware/logging.py`

**功能**：
- 自动拦截所有 HTTP 请求
- 记录请求方法、路径、参数、状态码、执行时间、IP、用户信息
- 自动记录操作日志（AuditLog）到数据库
- 支持结构化日志（JSON 格式）

**特点**：
- ✅ 完全自动化，无需修改业务代码
- ✅ 覆盖所有 API 请求
- ⚠️ 从路径推断资源类型，可能不够精确

**使用方式**：
已在 `settings.py` 中配置，自动生效：
```python
MIDDLEWARE = [
    ...
    'middleware.logging.RequestLoggingMiddleware',
    ...
]
```

### 2. 装饰器切面（@audit_log）

**位置**：`backend/apps/common/audit.py`

**功能**：
- 装饰函数/方法，自动记录操作日志
- 自动获取 request、user、执行时间等信息
- 支持自定义操作类型、资源类型、描述

**特点**：
- ✅ 精确控制，可以自定义日志内容
- ✅ 适用于任何函数/方法
- ⚠️ 需要手动添加装饰器

**使用方式**：
```python
from apps.common.audit import audit_log

@audit_log(action='create', resource_type='user', description='创建用户')
def create_user(request, ...):
    ...
```

### 3. ViewSet 切面（AuditLogMixin）

**位置**：`backend/apps/common/mixins.py`

**功能**：
- 自动记录 ViewSet 的 CRUD 操作
- 自动获取资源类型、资源ID、资源名称
- 自动记录执行时间、操作状态、错误信息
- 支持自定义资源类型名称

**特点**：
- ✅ 完全自动化，只需继承 Mixin
- ✅ 精确获取资源信息（从模型实例）
- ✅ 支持控制是否记录 retrieve 和 list 操作

**使用方式**：
```python
from apps.common.mixins import AuditLogMixin
from rest_framework import viewsets

class UserViewSet(AuditLogMixin, viewsets.ModelViewSet):
    """
    用户管理视图集
    自动记录所有 CRUD 操作的日志
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    # 可选配置
    resource_type_name = 'user'  # 自定义资源类型名称
    log_retrieve = True  # 记录查看详情操作（默认 False）
    log_list = True  # 记录列表查询操作（默认 False）
```

## 三种方式对比

| 特性 | 中间件切面 | 装饰器切面 | ViewSet 切面 |
|------|-----------|-----------|-------------|
| 自动化程度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 精确度 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 适用场景 | 所有请求 | 特定函数 | ViewSet CRUD |
| 资源信息获取 | 从路径推断 | 手动指定 | 自动从实例获取 |
| 代码侵入性 | 无 | 需要装饰器 | 需要继承 Mixin |

## 推荐使用方案

### 方案一：完全自动化（推荐）

使用 **中间件切面** + **ViewSet 切面**：

```python
# 1. 中间件已在 settings.py 中配置，自动记录所有请求

# 2. ViewSet 继承 AuditLogMixin
class UserViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

**优点**：
- 完全自动化，无需手动添加日志代码
- 中间件记录所有请求，ViewSet 切面记录精确的 CRUD 操作
- 双重保障，确保重要操作都被记录

### 方案二：精确控制

使用 **装饰器切面** 在关键操作上：

```python
from apps.common.audit import audit_log

class UserViewSet(viewsets.ModelViewSet):
    @audit_log(action='create', resource_type='user', description='创建用户')
    def create(self, request, *args, **kwargs):
        ...
    
    @audit_log(action='update', resource_type='user', description='更新用户')
    def update(self, request, *args, **kwargs):
        ...
```

**优点**：
- 精确控制每个操作的日志内容
- 可以自定义操作描述和资源信息

## 日志记录内容

所有切面方式都会记录以下信息：

- **用户信息**：user_id, username
- **操作信息**：action, resource_type, resource_id, resource_name
- **请求信息**：request_method, request_path, request_params, ip_address, user_agent
- **执行信息**：status, error_message, execution_time
- **时间信息**：created_at

## 注意事项

1. **日志记录失败不影响主业务**：所有日志记录都使用 try-except 包裹，失败不会影响正常业务
2. **敏感字段自动过滤**：密码、token 等敏感字段会自动替换为 `***`
3. **性能考虑**：日志记录是同步的，如果日志量很大，可以考虑异步记录
4. **数据库存储**：操作日志存储在 `sys_audit_log` 表中，需要定期归档旧数据

## 示例：迁移现有 ViewSet 到切面方式

### 迁移前（手动记录日志）

```python
class UserViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        start_time = time.time()
        try:
            response = super().create(request, *args, **kwargs)
            # 手动记录日志
            log_audit(
                action='create',
                resource_type='user',
                resource_id=response.data.get('id'),
                request=request,
                status=1,
            )
            return response
        except Exception as e:
            log_audit(
                action='create',
                resource_type='user',
                request=request,
                status=0,
                error_message=str(e),
            )
            raise
```

### 迁移后（使用切面）

```python
from apps.common.mixins import AuditLogMixin

class UserViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        # 只需调用父类方法，日志自动记录
        return super().create(request, *args, **kwargs)
```

**优势**：
- 代码更简洁
- 减少重复代码
- 统一日志格式
- 自动处理异常情况

实际 这些日志是为了审计使用。通过系统管理的日志管理功能中，我们可以做审计日志的存储配置。可以配置到mongo中，也可以配置到系统数据库中，也可以配置到oss中。并可以设置日志保存的时长。