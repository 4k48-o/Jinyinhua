"""
用户权限控制
"""
from rest_framework import permissions
from django.utils.translation import gettext_lazy as _


class UserPermission(permissions.BasePermission):
    """
    用户权限控制类
    
    权限规则：
    1. 用户可以查看自己的信息
    2. 用户可以更新自己的信息
    3. 只有管理员可以创建/删除用户
    4. 只有管理员可以查看所有用户列表
    """
    
    def has_permission(self, request, view):
        """
        检查是否有权限访问视图
        """
        # 未认证用户无权限
        if not request.user or not request.user.is_authenticated:
            return False
        
        # 管理员拥有所有权限
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # 允许查看和更新自己的信息
        if view.action in ['retrieve', 'update', 'partial_update']:
            return True
        
        # 允许获取当前用户信息
        if view.action in ['me', 'update_me']:
            return True
        
        # 其他操作需要管理员权限
        return False
    
    def has_object_permission(self, request, view, obj):
        """
        检查是否有权限访问特定对象
        
        Args:
            request: 请求对象
            view: 视图对象
            obj: 用户对象
        """
        # 管理员拥有所有权限
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # 用户可以查看和更新自己的信息
        if obj == request.user:
            return True
        
        # 其他情况无权限
        return False

