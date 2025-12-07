"""
生产环境配置
"""
from .base import *
from decouple import config

DEBUG = False

# ==================== HTTPS 配置 ====================
# 强制 HTTPS 重定向（生产环境必须启用）
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)  # 1年
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ==================== Cookie 安全配置 ====================
# Session Cookie 安全
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'  # 防止 CSRF 攻击

# CSRF Cookie 安全
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='',
    cast=lambda v: [s.strip() for s in v.split(',') if s.strip()]
)

# ==================== XSS 防护配置 ====================
SECURE_BROWSER_XSS_FILTER = True  # 启用浏览器 XSS 过滤器
SECURE_CONTENT_TYPE_NOSNIFF = True  # 防止 MIME 类型嗅探

# ==================== 安全响应头配置 ====================
X_FRAME_OPTIONS = 'DENY'  # 防止点击劫持
X_CONTENT_TYPE_OPTIONS = 'nosniff'  # 防止 MIME 类型嗅探
X_XSS_PROTECTION = '1; mode=block'  # XSS 保护

# Content Security Policy (CSP) - 可根据需要配置
# SECURE_CSP_DEFAULT_SRC = "'self'"
# SECURE_CSP_SCRIPT_SRC = "'self' 'unsafe-inline'"
# SECURE_CSP_STYLE_SRC = "'self' 'unsafe-inline'"

# Referrer Policy
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Permissions Policy (原 Feature Policy)
SECURE_PERMISSIONS_POLICY = {
    'geolocation': [],
    'camera': [],
    'microphone': [],
    'payment': [],
}

# 生产环境数据库配置（从环境变量读取，必须使用 PostgreSQL）
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
        'OPTIONS': {
            'options': '-c client_encoding=UTF8',
        },
        'CONN_MAX_AGE': config('DB_CONN_MAX_AGE', default=600, cast=int),
        'ATOMIC_REQUESTS': True,
    }
}

# 生产环境日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

