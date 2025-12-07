# 国际化和结构化日志实现文档

## 📋 概述

本文档说明国际化和结构化日志的实现细节和使用方法。

**实现日期**: 2025-12-06  
**功能范围**: 国际化支持、结构化日志（JSON 格式）

---

## 🌍 国际化支持

### 功能特性

1. **多语言支持**
   - 简体中文 (zh-hans)
   - 英文 (en)
   - 繁体中文 (zh-hant)

2. **语言检测**
   - 从请求头 `X-Language` 检测（优先级最高）
   - 从请求头 `Accept-Language` 检测
   - 使用默认语言（配置中的 `LANGUAGE_CODE`）

3. **自动翻译**
   - 异常消息自动翻译
   - API 响应消息自动翻译
   - 使用 Django i18n 框架

### 配置

#### settings.py 配置

```python
# 国际化配置
LANGUAGE_CODE = config('LANGUAGE_CODE', default='zh-hans')
USE_I18N = True
USE_L10N = True
USE_TZ = True

# 支持的语言列表
LANGUAGES = [
    ('zh-hans', '简体中文'),
    ('en', 'English'),
    ('zh-hant', '繁體中文'),
]

# 翻译文件路径
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
```

#### 中间件配置

```python
MIDDLEWARE = [
    # ...
    'middleware.locale.LocaleMiddleware',  # 自定义语言检测中间件
    # ...
]
```

### 使用方法

#### 1. 在代码中使用翻译

```python
from django.utils.translation import gettext_lazy as _

class MyException(BaseAPIException):
    default_detail = _('错误消息')  # 使用 gettext_lazy
```

#### 2. 在视图中使用翻译

```python
from django.utils.translation import gettext
from apps.common.response import APIResponse

def my_view(request):
    message = gettext('操作成功')
    return APIResponse.success(data=result, message=message)
```

#### 3. 客户端指定语言

**方式 1: 使用自定义请求头**
```http
GET /api/v1/users/ HTTP/1.1
X-Language: en
```

**方式 2: 使用 Accept-Language 头**
```http
GET /api/v1/users/ HTTP/1.1
Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8
```

### 翻译文件

翻译文件位于 `locale/{language}/LC_MESSAGES/django.po`：

- `locale/zh_Hans/LC_MESSAGES/django.po` - 简体中文
- `locale/en/LC_MESSAGES/django.po` - 英文
- `locale/zh_Hant/LC_MESSAGES/django.po` - 繁体中文

### 编译翻译文件

```bash
# 编译所有翻译文件
python manage.py compilemessages

# 更新翻译文件（从代码中提取需要翻译的字符串）
python manage.py makemessages -l en
python manage.py makemessages -l zh_Hans
python manage.py makemessages -l zh_Hant
```

### 语言代码映射

中间件会自动处理以下语言代码映射：

| 原始代码 | 标准化代码 |
|---------|-----------|
| zh-CN | zh-hans |
| zh-Hans-CN | zh-hans |
| zh-TW | zh-hant |
| zh-Hant-TW | zh-hant |
| zh-HK | zh-hant |
| en-US | en |
| en-GB | en |

---

## 📊 结构化日志

### 功能特性

1. **JSON 格式日志**
   - 所有日志以 JSON 格式输出
   - 便于日志聚合和分析
   - 支持 ELK、Loki 等日志系统

2. **结构化字段**
   - timestamp: 时间戳
   - level: 日志级别
   - logger: 日志记录器名称
   - message: 日志消息
   - module: 模块名
   - function: 函数名
   - line: 行号
   - request_id: 请求 ID（如果存在）
   - error_id: 错误 ID（如果存在）
   - exception: 异常信息（如果存在）
   - extra_data: 额外数据（如果存在）

3. **环境配置**
   - 可通过环境变量 `USE_JSON_LOGGING` 控制
   - 默认使用文本格式（开发环境）
   - 生产环境建议使用 JSON 格式

### 配置

#### settings.py 配置

```python
# 日志格式配置
USE_JSON_LOGGING = config('USE_JSON_LOGGING', default=False, cast=bool)

LOGGING = {
    'version': 1,
    'formatters': {
        'json': {
            '()': JSONFormatter,  # 自定义 JSON 格式化器
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json' if USE_JSON_LOGGING else 'verbose',
        },
    },
    # ...
}
```

#### 环境变量配置

```bash
# .env 文件
USE_JSON_LOGGING=True
LOG_LEVEL=INFO
```

### 日志格式示例

#### JSON 格式日志

```json
{
  "timestamp": "2025-12-06 16:00:00",
  "level": "INFO",
  "logger": "django.request",
  "message": "HTTP Request",
  "module": "logging",
  "function": "process_response",
  "line": 73,
  "request_id": "req_abc123def456",
  "extra_data": {
    "method": "GET",
    "path": "/api/v1/users/",
    "status_code": 200,
    "execution_time_ms": 45.23,
    "ip": "127.0.0.1",
    "username": "admin"
  }
}
```

#### 错误日志示例

```json
{
  "timestamp": "2025-12-06 16:00:00",
  "level": "ERROR",
  "logger": "django.exception",
  "message": "API Exception: ValidationException: 数据验证失败",
  "module": "exceptions",
  "function": "custom_exception_handler",
  "line": 120,
  "request_id": "req_abc123def456",
  "error_id": "err_789xyz012abc",
  "extra_data": {
    "exception_type": "ValidationException",
    "exception_message": "数据验证失败",
    "path": "/api/v1/users/",
    "method": "POST",
    "error_code": "E001001"
  }
}
```

### 在代码中使用结构化日志

#### 基本使用

```python
import logging

logger = logging.getLogger('my_app')

# 创建日志记录
log_record = logging.LogRecord(
    name=logger.name,
    level=logging.INFO,
    pathname='',
    lineno=0,
    msg='My log message',
    args=(),
    exc_info=None,
)

# 添加额外字段
log_record.request_id = request.request_id
log_record.extra_data = {
    'user_id': user.id,
    'action': 'create',
}

# 记录日志
logger.handle(log_record)
```

#### 在中间件中使用

```python
# middleware/logging.py
log_record = logging.LogRecord(
    name=logger.name,
    level=logging.INFO,
    pathname='',
    lineno=0,
    msg='HTTP Request',
    args=(),
    exc_info=None,
)
log_record.request_id = request_id
log_record.extra_data = log_data
logger.handle(log_record)
```

### 日志聚合和分析

#### ELK Stack 集成

结构化日志可以直接被 ELK Stack 收集和分析：

1. **Logstash 配置**
```ruby
input {
  file {
    path => "/var/log/django/app.log"
    codec => json
  }
}

filter {
  json {
    source => "message"
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "django-logs-%{+YYYY.MM.dd}"
  }
}
```

2. **Kibana 可视化**
   - 创建仪表板
   - 分析错误趋势
   - 监控性能指标

#### Loki 集成

```yaml
# promtail-config.yaml
clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: django
    static_configs:
      - targets:
          - localhost
        labels:
          job: django
          __path__: /var/log/django/*.log
```

---

## 🔧 使用示例

### 示例 1: 多语言 API 响应

**请求（英文）**:
```http
GET /api/v1/users/ HTTP/1.1
X-Language: en
```

**响应**:
```json
{
  "success": true,
  "code": 200,
  "message": "Operation Successful",
  "data": {...},
  "request_id": "req_abc123",
  "timestamp": "2025-12-06T16:00:00Z"
}
```

**请求（中文）**:
```http
GET /api/v1/users/ HTTP/1.1
X-Language: zh-hans
```

**响应**:
```json
{
  "success": true,
  "code": 200,
  "message": "操作成功",
  "data": {...},
  "request_id": "req_abc123",
  "timestamp": "2025-12-06T16:00:00Z"
}
```

### 示例 2: 多语言错误响应

**请求（英文）**:
```http
POST /api/v1/users/ HTTP/1.1
X-Language: en
Content-Type: application/json

{
  "username": ""
}
```

**响应**:
```json
{
  "success": false,
  "code": "E001001",
  "message": "Data Validation Failed",
  "error": "Data Validation Failed",
  "data": null,
  "request_id": "req_abc123",
  "error_id": "err_xyz789",
  "timestamp": "2025-12-06T16:00:00Z"
}
```

### 示例 3: 结构化日志输出

**文本格式**（开发环境）:
```
INFO 2025-12-06 16:00:00 logging 12345 67890 HTTP Request
```

**JSON 格式**（生产环境）:
```json
{
  "timestamp": "2025-12-06 16:00:00",
  "level": "INFO",
  "logger": "django.request",
  "message": "HTTP Request",
  "module": "logging",
  "function": "process_response",
  "line": 73,
  "request_id": "req_abc123def456",
  "extra_data": {
    "method": "GET",
    "path": "/api/v1/users/",
    "status_code": 200,
    "execution_time_ms": 45.23,
    "ip": "127.0.0.1",
    "username": "admin"
  }
}
```

---

## 📝 最佳实践

### 国际化最佳实践

1. **使用 gettext_lazy**
   - 在模型和表单中使用 `gettext_lazy`
   - 在视图和序列化器中使用 `gettext`

2. **翻译消息键**
   - 使用有意义的键名
   - 保持键名的一致性

3. **测试多语言**
   - 测试所有支持的语言
   - 验证翻译的准确性

### 日志最佳实践

1. **使用结构化日志**
   - 生产环境使用 JSON 格式
   - 开发环境使用文本格式（便于阅读）

2. **添加上下文信息**
   - 包含请求 ID
   - 包含用户信息
   - 包含业务上下文

3. **日志级别**
   - DEBUG: 详细调试信息
   - INFO: 一般信息
   - WARNING: 警告信息
   - ERROR: 错误信息
   - CRITICAL: 严重错误

4. **日志聚合**
   - 使用 ELK、Loki 等工具
   - 设置日志保留策略
   - 配置告警规则

---

## 🔄 维护和更新

### 更新翻译

1. 提取需要翻译的字符串：
```bash
python manage.py makemessages -l en
python manage.py makemessages -l zh_Hans
python manage.py makemessages -l zh_Hant
```

2. 编辑翻译文件（`.po` 文件）

3. 编译翻译文件：
```bash
python manage.py compilemessages
```

### 添加新语言

1. 在 `settings.py` 中添加语言：
```python
LANGUAGES = [
    # ...
    ('ja', '日本語'),
]
```

2. 创建翻译文件：
```bash
python manage.py makemessages -l ja
```

3. 编辑翻译文件并编译

---

## 📚 相关文档

- [Django 国际化文档](https://docs.djangoproject.com/en/stable/topics/i18n/)
- [Python logging 文档](https://docs.python.org/3/library/logging.html)
- [异常处理改进文档](EXCEPTION_HANDLING_IMPROVEMENTS.md)

---

**文档版本**: v1.0  
**最后更新**: 2025-12-06

