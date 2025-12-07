"""
Django 基础配置
所有环境共用的配置
"""
import os
from pathlib import Path
from decouple import config, Csv

# 构建项目路径
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 安全设置
# SECRET_KEY 必须从环境变量读取，生产环境不允许使用默认值
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')
# DEBUG 和 ALLOWED_HOSTS 在子配置文件中会被覆盖
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# 应用定义
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 第三方应用
    'rest_framework',
    'corsheaders',
    'django_filters',
    'django_redis',  # Redis 缓存支持
    'rest_framework_simplejwt.token_blacklist',  # JWT Token 黑名单（使用 Redis）
    'drf_spectacular',  # API 文档生成（OpenAPI/Swagger）
    
    # 本地应用（使用应用配置类避免标签冲突）
    'apps.common.apps.CommonConfig',
    'apps.users.apps.UsersConfig',
    'apps.auth.apps.AuthConfig',
    'apps.permissions.apps.PermissionsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS 中间件
    'django.middleware.common.CommonMiddleware',
    'middleware.locale.LocaleMiddleware',  # 自定义语言检测中间件（必须在 SessionMiddleware 之后）
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF 保护
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # 点击劫持防护（已由 SecurityHeadersMiddleware 增强）
    # 自定义中间件
    'middleware.request_id.RequestIDMiddleware',  # 请求 ID 中间件（最早执行，确保所有请求都有 ID）
    'middleware.security.SQLInjectionProtectionMiddleware',  # SQL 注入防护中间件
    'middleware.security.SecurityHeadersMiddleware',  # 安全响应头中间件
    'middleware.logging.RequestLoggingMiddleware',  # 请求日志中间件
    'middleware.exception.ExceptionHandlingMiddleware',  # 异常处理中间件
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# 数据库配置（子配置文件会覆盖）
DB_ENGINE = config('DB_ENGINE', default='django.db.backends.postgresql')
DATABASES = {
    'default': {
        'ENGINE': DB_ENGINE,
        'NAME': config('DB_NAME', default='yantou_db'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        } if DB_ENGINE.endswith('mysql') else {
            # PostgreSQL 选项
            'options': '-c client_encoding=UTF8',
        } if DB_ENGINE.endswith('postgresql') else {},
        'CONN_MAX_AGE': config('DB_CONN_MAX_AGE', default=600, cast=int),  # 连接池最大存活时间（秒）
        'ATOMIC_REQUESTS': True,  # 每个请求自动开启事务
    }
}

# 密码验证
# 密码验证策略配置
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {
            'user_attributes': ('username', 'email', 'first_name', 'last_name'),
            'max_similarity': 0.7,  # 密码与用户属性相似度阈值
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,  # 最小长度 8 位
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        # 不设置 OPTIONS，使用默认的常见密码列表
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 密码策略配置
PASSWORD_MIN_LENGTH = 8  # 最小长度
PASSWORD_REQUIRE_UPPERCASE = True  # 要求大写字母
PASSWORD_REQUIRE_LOWERCASE = True  # 要求小写字母
PASSWORD_REQUIRE_DIGITS = True  # 要求数字
PASSWORD_REQUIRE_SPECIAL = True  # 要求特殊字符
PASSWORD_MAX_AGE_DAYS = 90  # 密码最大有效期（天）
PASSWORD_HISTORY_COUNT = 5  # 密码历史记录数量（防止重复使用）

# 国际化
LANGUAGE_CODE = config('LANGUAGE_CODE', default='zh-hans')
TIME_ZONE = 'Asia/Shanghai'
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

# 国际化中间件（已在 MIDDLEWARE 中配置）
# 'django.middleware.locale.LocaleMiddleware'

# 安全增强配置
# 登录失败次数限制
LOGIN_MAX_ATTEMPTS = config('LOGIN_MAX_ATTEMPTS', default=5, cast=int)  # 最大失败次数
LOGIN_LOCKOUT_DURATION = config('LOGIN_LOCKOUT_DURATION', default=900, cast=int)  # 锁定持续时间（秒，默认15分钟）
LOGIN_WINDOW_DURATION = config('LOGIN_WINDOW_DURATION', default=3600, cast=int)  # 时间窗口（秒，默认1小时）

# 静态文件
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
] if (BASE_DIR / 'static').exists() else []

# 媒体文件
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 默认主键字段类型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework 配置
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT 认证
        'rest_framework.authentication.SessionAuthentication',  # Session 认证（备用）
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'apps.common.pagination.CustomPageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    # 自定义异常处理器
    'EXCEPTION_HANDLER': 'apps.common.exceptions.custom_exception_handler',
    # API 文档生成配置
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# CORS 配置
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000,http://127.0.0.1:3000',
    cast=Csv()
)
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'x-language',  # 自定义语言请求头
]

# Redis 缓存配置
REDIS_HOST = config('REDIS_HOST', default='localhost')
REDIS_PORT = config('REDIS_PORT', default='6379', cast=int)
REDIS_DB = config('REDIS_DB', default=0, cast=int)
REDIS_PASSWORD = config('REDIS_PASSWORD', default='')

# 构建 Redis URL
if REDIS_PASSWORD:
    REDIS_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
else:
    REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'

# 缓存配置（使用 Redis）
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

# 会话存储配置（使用 Redis，可选）
# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
# SESSION_CACHE_ALIAS = 'default'

# JWT 配置
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(
        minutes=config('JWT_ACCESS_TOKEN_LIFETIME', default=15, cast=int)
    ),
    'REFRESH_TOKEN_LIFETIME': timedelta(
        days=config('JWT_REFRESH_TOKEN_LIFETIME', default=7, cast=int)
    ),
    'ROTATE_REFRESH_TOKENS': True,  # 刷新 Token 时生成新的 Refresh Token
    'BLACKLIST_AFTER_ROTATION': True,  # 刷新后加入黑名单
    'UPDATE_LAST_LOGIN': True,
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    
    'JTI_CLAIM': 'jti',
    
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# 日志配置
import json
import logging

class JSONFormatter(logging.Formatter):
    """
    JSON 格式化器
    将日志记录格式化为 JSON 格式，便于日志聚合和分析
    """
    def format(self, record):
        """
        格式化日志记录为 JSON
        
        Args:
            record: 日志记录对象
            
        Returns:
            str: JSON 格式的日志字符串
        """
        log_data = {
            'timestamp': self.formatTime(record, self.datefmt),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # 添加请求 ID（如果存在）
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
        
        # 添加错误 ID（如果存在）
        if hasattr(record, 'error_id'):
            log_data['error_id'] = record.error_id
        
        # 添加异常信息（如果存在）
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # 添加额外字段（如果存在）
        if hasattr(record, 'extra_data'):
            log_data.update(record.extra_data)
        
        return json.dumps(log_data, ensure_ascii=False)

# 日志格式配置
USE_JSON_LOGGING = config('USE_JSON_LOGGING', default=False, cast=bool)

# 日志文件目录
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'json': {
            '()': JSONFormatter,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json' if USE_JSON_LOGGING else 'verbose',
        },
        # 业务日志文件处理器
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'django.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 10,
            'formatter': 'json' if USE_JSON_LOGGING else 'verbose',
            'encoding': 'utf-8',
        },
        # 错误日志文件处理器
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'django_error.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 10,
            'formatter': 'json' if USE_JSON_LOGGING else 'verbose',
            'level': 'ERROR',
            'encoding': 'utf-8',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': config('LOG_LEVEL', default='INFO'),
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': config('LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.exception': {
            'handlers': ['console', 'error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        # 业务日志记录器
        'django.business': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        # 审计日志记录器（用于记录审计日志保存失败的情况）
        'django.audit': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# API 文档配置（drf-spectacular）
SPECTACULAR_SETTINGS = {
    'TITLE': '企业级应用 API 文档',
    'DESCRIPTION': '基于 Django REST Framework 的企业级应用后端 API 文档',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'],  # 文档访问权限
    'SERVE_AUTHENTICATION': None,  # 文档访问不需要认证
    'COMPONENT_SPLIT_REQUEST': True,  # 分离请求和响应示例
    'COMPONENT_NO_READ_ONLY_REQUIRED': True,
    'SCHEMA_PATH_PREFIX': '/api/v1/',  # API 路径前缀
    'TAGS': [
        {'name': '认证', 'description': '用户认证相关接口'},
        {'name': '用户', 'description': '用户管理相关接口'},
        {'name': '权限', 'description': '权限管理相关接口'},
        {'name': '系统', 'description': '系统相关接口'},
    ],
    'CONTACT': {
        'name': '技术支持',
        'email': 'support@example.com',
    },
    'LICENSE': {
        'name': 'MIT License',
    },
    'EXTENSIONS_INFO': {
        'x-logo': {
            'url': 'https://via.placeholder.com/200x50.png?text=API+Logo',
            'altText': 'API Logo'
        }
    },
    # 自定义响应格式
    'DEFAULT_GENERATOR_CLASS': 'drf_spectacular.generators.SchemaGenerator',
    # 支持 JWT 认证
    'AUTHENTICATION_WHITELIST': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'APPEND_COMPONENTS': {
        'securitySchemes': {
            'Bearer': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
                'description': 'JWT Token 认证，格式：Bearer <token>',
            }
        }
    },
    'SECURITY': [{'Bearer': []}],  # 默认使用 Bearer 认证
}
