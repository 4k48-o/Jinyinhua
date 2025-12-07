"""
Django 设置模块
根据环境变量 DJANGO_SETTINGS_MODULE 加载对应的配置
"""
import os

# 从环境变量获取设置模块，默认为开发环境
settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'config.settings.development')

if settings_module == 'config.settings':
    # 兼容旧的方式，默认使用开发环境
    from .development import *
else:
    # 根据 settings_module 导入对应的配置
    if 'development' in settings_module:
        from .development import *
    elif 'production' in settings_module:
        from .production import *
    elif 'testing' in settings_module:
        from .testing import *
    else:
        from .development import *

