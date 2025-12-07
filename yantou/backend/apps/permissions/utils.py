"""
权限工具函数
提供权限检查、缓存等功能
"""
from django.core.cache import cache
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from .models import Role, Permission, UserRole, RolePermission


def get_user_roles(user, use_cache=True):
    """
    获取用户的所有角色
    
    Args:
        user: 用户对象
        use_cache: 是否使用缓存
        
    Returns:
        QuerySet: 角色查询集
    """
    if not user or not user.is_authenticated:
        return Role.objects.none()
    
    # 超级管理员拥有所有角色
    if user.is_superuser:
        return Role.objects.filter(is_active=True, is_deleted=False)
    
    cache_key = f'user_roles:{user.id}'
    
    if use_cache:
        cached_roles = cache.get(cache_key)
        if cached_roles is not None:
            return Role.objects.filter(id__in=cached_roles, is_active=True, is_deleted=False)
    
    # 从数据库查询
    now = timezone.now()
    user_roles = UserRole.objects.filter(
        user=user,
        is_active=True,
        role__is_active=True,
        role__is_deleted=False
    ).filter(
        models.Q(expires_at__isnull=True) | models.Q(expires_at__gt=now)
    ).select_related('role')
    
    role_ids = [ur.role_id for ur in user_roles]
    
    # 缓存结果（5分钟）
    if use_cache:
        cache.set(cache_key, role_ids, 300)
    
    return Role.objects.filter(id__in=role_ids, is_active=True, is_deleted=False)


def get_user_permissions(user, use_cache=True):
    """
    获取用户的所有权限
    
    Args:
        user: 用户对象
        use_cache: 是否使用缓存
        
    Returns:
        QuerySet: 权限查询集
    """
    if not user or not user.is_authenticated:
        return Permission.objects.none()
    
    # 超级管理员拥有所有权限
    if user.is_superuser:
        return Permission.objects.filter(is_active=True)
    
    cache_key = f'user_permissions:{user.id}'
    
    if use_cache:
        cached_permissions = cache.get(cache_key)
        if cached_permissions is not None:
            return Permission.objects.filter(id__in=cached_permissions, is_active=True)
    
    # 从用户角色获取权限
    roles = get_user_roles(user, use_cache=False)
    role_ids = list(roles.values_list('id', flat=True))
    
    if not role_ids:
        return Permission.objects.none()
    
    # 查询角色关联的权限
    permission_ids = RolePermission.objects.filter(
        role_id__in=role_ids
    ).values_list('permission_id', flat=True).distinct()
    
    permissions = Permission.objects.filter(
        id__in=permission_ids,
        is_active=True
    )
    
    permission_id_list = list(permissions.values_list('id', flat=True))
    
    # 缓存结果（5分钟）
    if use_cache:
        cache.set(cache_key, permission_id_list, 300)
    
    return permissions


def check_user_role(user, role_code, use_cache=True):
    """
    检查用户是否拥有指定角色
    
    Args:
        user: 用户对象
        role_code: 角色代码
        use_cache: 是否使用缓存
        
    Returns:
        bool: 是否拥有该角色
    """
    if not user or not user.is_authenticated:
        return False
    
    # 超级管理员拥有所有角色
    if user.is_superuser:
        return True
    
    roles = get_user_roles(user, use_cache=use_cache)
    return roles.filter(code=role_code).exists()


def check_user_permission(user, permission_code, use_cache=True):
    """
    检查用户是否拥有指定权限
    
    Args:
        user: 用户对象
        permission_code: 权限代码
        use_cache: 是否使用缓存
        
    Returns:
        bool: 是否拥有该权限
    """
    if not user or not user.is_authenticated:
        return False
    
    # 超级管理员拥有所有权限
    if user.is_superuser:
        return True
    
    permissions = get_user_permissions(user, use_cache=use_cache)
    return permissions.filter(code=permission_code).exists()


def clear_user_permission_cache(user):
    """
    清除用户的权限缓存
    
    Args:
        user: 用户对象
    """
    cache.delete(f'user_roles:{user.id}')
    cache.delete(f'user_permissions:{user.id}')


def clear_all_permission_cache():
    """
    清除所有权限缓存
    """
    # 这里可以扩展为清除所有用户权限缓存
    # 由于用户 ID 未知，可以通过设置缓存版本号来实现
    pass

