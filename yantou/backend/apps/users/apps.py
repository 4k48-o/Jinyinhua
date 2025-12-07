"""
用户管理应用配置
"""
from apps.apps import BaseAppConfig


class UsersConfig(BaseAppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    label = 'apps_users'  # 明确指定应用标签
    verbose_name = '用户管理'

