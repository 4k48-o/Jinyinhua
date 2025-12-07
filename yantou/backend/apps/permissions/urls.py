"""
权限管理路由
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PermissionViewSet, RoleViewSet, UserRoleViewSet, PermissionCheckViewSet
)

router = DefaultRouter()
router.register(r'permissions', PermissionViewSet, basename='permission')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'user-roles', UserRoleViewSet, basename='user-role')
router.register(r'permission-check', PermissionCheckViewSet, basename='permission-check')

app_name = 'permissions'

urlpatterns = [
    path('', include(router.urls)),
]

