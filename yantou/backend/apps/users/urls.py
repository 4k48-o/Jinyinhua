"""
用户管理路由
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, DepartmentViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'departments', DepartmentViewSet, basename='department')

app_name = 'users'

urlpatterns = [
    path('', include(router.urls)),
]

