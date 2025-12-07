"""
开发环境配置
"""
from .base import *
from decouple import config, Csv

# 开发环境可以从环境变量覆盖，但默认值为 True
DEBUG = config('DEBUG', default=True, cast=bool)

# 开发环境允许所有主机（可通过环境变量覆盖）
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=Csv())
if ALLOWED_HOSTS == ['*']:
    ALLOWED_HOSTS = ['*']

# 开发环境数据库配置（PostgreSQL）
# 可以通过环境变量覆盖，默认使用 PostgreSQL
from decouple import config
DB_ENGINE = config('DB_ENGINE', default='django.db.backends.postgresql')

if DB_ENGINE == 'django.db.backends.sqlite3':
    # 如果明确指定使用 SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # 默认使用 PostgreSQL
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': config('DB_NAME', default='yantou_db'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default='0qww294e'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
            'OPTIONS': {
                'options': '-c client_encoding=UTF8',
            },
            'CONN_MAX_AGE': 600,
            'ATOMIC_REQUESTS': True,
        }
    }

# 开发环境 CORS 配置（允许所有来源）
CORS_ALLOW_ALL_ORIGINS = True

# 开发环境日志级别
LOGGING['root']['level'] = 'DEBUG'
LOGGING['loggers']['django']['level'] = 'DEBUG'

