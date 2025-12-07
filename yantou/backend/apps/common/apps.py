"""
通用应用配置
"""
from apps.apps import BaseAppConfig


class CommonConfig(BaseAppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.common'
    label = 'apps_common'  # 明确指定应用标签
    verbose_name = '通用功能'

