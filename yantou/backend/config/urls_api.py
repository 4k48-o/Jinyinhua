"""
API URL 配置
所有 API 路由都在这里配置，使用版本控制 /api/v1/
"""
from django.urls import path, include

urlpatterns = [
    # 认证相关路由
    path('auth/', include('apps.auth.urls')),
    
    # 用户管理路由
    path('', include('apps.users.urls')),
    
    # 权限管理路由
    path('', include('apps.permissions.urls')),
    
    # 健康检查
    path('health/', include('config.urls_health')),
]
