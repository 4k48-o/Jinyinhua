"""
自定义权限类
"""
from rest_framework import permissions
from django.utils.translation import gettext_lazy as _
from .utils import check_user_permission, check_user_role


class BasePermission(permissions.BasePermission):
    """
    基础权限类
    所有自定义权限类都继承此类
    """
    message = _('您没有执行此操作的权限')


class RolePermission(BasePermission):
    """
    角色权限类
    检查用户是否拥有指定角色
    """
    required_roles = []
    
    def __init__(self, required_roles=None):
        """
        初始化权限类
        
        Args:
            required_roles: 需要的角色代码列表，如：['admin', 'manager']
        """
        if required_roles is not None:
            self.required_roles = required_roles
    
    def has_permission(self, request, view):
        """
        检查是否有权限访问视图
        
        Args:
            request: 请求对象
            view: 视图对象
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # 超级管理员拥有所有权限
        if request.user.is_superuser:
            return True
        
        # 检查是否拥有所需角色
        if not self.required_roles:
            return True
        
        for role_code in self.required_roles:
            if check_user_role(request.user, role_code):
                return True
        
        return False


class PermissionRequired(BasePermission):
    """
    权限要求类
    检查用户是否拥有指定权限
    """
    required_permissions = []
    
    def __init__(self, required_permissions=None):
        """
        初始化权限类
        
        Args:
            required_permissions: 需要的权限代码列表，如：['user:create', 'user:update']
        """
        if required_permissions is not None:
            self.required_permissions = required_permissions
    
    def has_permission(self, request, view):
        """
        检查是否有权限访问视图
        
        Args:
            request: 请求对象
            view: 视图对象
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # 超级管理员拥有所有权限
        if request.user.is_superuser:
            return True
        
        # 检查是否拥有所需权限
        if not self.required_permissions:
            return True
        
        for permission_code in self.required_permissions:
            if check_user_permission(request.user, permission_code):
                return True
        
        return False

