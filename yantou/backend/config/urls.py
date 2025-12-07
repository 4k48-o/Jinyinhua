"""
URL configuration for config project.

主 URL 路由配置，包含：
- Admin 后台路由
- API 版本路由
- 静态文件和媒体文件路由（开发环境）
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Admin 后台配置
admin.site.site_header = '企业级应用管理系统'
admin.site.site_title = '管理系统'
admin.site.index_title = '欢迎使用管理系统'

urlpatterns = [
    # Admin 后台路由
    path('admin/', admin.site.urls),
    
    # API 版本路由
    path('api/v1/', include('config.urls_api')),
    
    # 健康检查路由（可选）
    path('health/', include('config.urls_health')),
]

# 静态文件和媒体文件路由（仅开发环境）
if settings.DEBUG:
    # 静态文件路由
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
    
    # 媒体文件路由
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    
    # API 文档路由（开发环境）
    try:
        from drf_spectacular.views import (
            SpectacularAPIView,
            SpectacularRedocView,
            SpectacularSwaggerView,
        )
        urlpatterns += [
            path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
            path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
            path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
        ]
    except ImportError:
        # drf-spectacular 未安装时跳过
        pass

