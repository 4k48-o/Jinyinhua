"""
认证应用配置
"""
from apps.apps import BaseAppConfig


class AuthConfig(BaseAppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.auth'
    label = 'apps_auth'  # 避免与 Django 内置的 auth 应用冲突
    verbose_name = '认证管理'

