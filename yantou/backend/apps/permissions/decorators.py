"""
权限装饰器
提供便捷的权限检查装饰器
"""
from functools import wraps
from rest_framework.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _
from .utils import check_user_permission, check_user_role


def require_role(*role_codes):
    """
    角色装饰器
    检查用户是否拥有指定角色
    
    Usage:
        @require_role('admin', 'manager')
        def my_view(request):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if not request.user or not request.user.is_authenticated:
                raise PermissionDenied(_('请先登录'))
            
            # 超级管理员拥有所有角色
            if request.user.is_superuser:
                return func(request, *args, **kwargs)
            
            # 检查是否拥有所需角色
            has_role = False
            for role_code in role_codes:
                if check_user_role(request.user, role_code):
                    has_role = True
                    break
            
            if not has_role:
                raise PermissionDenied(_('您没有执行此操作的权限'))
            
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_permission(*permission_codes):
    """
    权限装饰器
    检查用户是否拥有指定权限
    
    Usage:
        @require_permission('user:create', 'user:update')
        def my_view(request):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if not request.user or not request.user.is_authenticated:
                raise PermissionDenied(_('请先登录'))
            
            # 超级管理员拥有所有权限
            if request.user.is_superuser:
                return func(request, *args, **kwargs)
            
            # 检查是否拥有所需权限
            has_permission = False
            for permission_code in permission_codes:
                if check_user_permission(request.user, permission_code):
                    has_permission = True
                    break
            
            if not has_permission:
                raise PermissionDenied(_('您没有执行此操作的权限'))
            
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

