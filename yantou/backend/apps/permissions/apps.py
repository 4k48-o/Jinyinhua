"""
权限管理应用配置
"""
from apps.apps import BaseAppConfig


class PermissionsConfig(BaseAppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.permissions'
    label = 'apps_permissions'  # 明确指定应用标签
    verbose_name = '权限管理'

