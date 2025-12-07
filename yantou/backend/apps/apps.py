"""
应用配置基类
"""
from django.apps import AppConfig


class BaseAppConfig(AppConfig):
    """应用配置基类"""
    default_auto_field = 'django.db.models.BigAutoField'

