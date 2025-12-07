"""
权限管理 Admin 配置
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Role, Permission, UserRole, RolePermission


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """权限管理"""
    list_display = ['name', 'code', 'content_type', 'action', 'parent', 'is_active', 'sort_order', 'created_at']
    list_filter = ['is_active', 'is_system', 'content_type', 'action']
    search_fields = ['name', 'code', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (_('基本信息'), {
            'fields': ('name', 'code', 'content_type', 'action', 'description')
        }),
        (_('层级关系'), {
            'fields': ('parent', 'sort_order')
        }),
        (_('状态信息'), {
            'fields': ('is_active', 'is_system')
        }),
        (_('时间信息'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class RolePermissionInline(admin.TabularInline):
    """角色权限内联"""
    model = RolePermission
    extra = 1
    verbose_name_plural = _('权限')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """角色管理"""
    list_display = ['name', 'code', 'is_active', 'is_system', 'sort_order', 'created_at', 'created_by']
    list_filter = ['is_active', 'is_system', 'is_deleted']
    search_fields = ['name', 'code', 'description']
    readonly_fields = ['created_at', 'updated_at', 'deleted_at']
    inlines = [RolePermissionInline]
    fieldsets = (
        (_('基本信息'), {
            'fields': ('name', 'code', 'description')
        }),
        (_('状态信息'), {
            'fields': ('is_active', 'is_system', 'is_deleted', 'sort_order')
        }),
        (_('创建信息'), {
            'fields': ('created_by', 'created_at', 'updated_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    """用户角色管理"""
    list_display = ['user', 'role', 'is_active', 'assigned_at', 'assigned_by', 'expires_at']
    list_filter = ['is_active', 'role', 'assigned_at']
    search_fields = ['user__username', 'role__name']
    readonly_fields = ['assigned_at']
    fieldsets = (
        (_('关联信息'), {
            'fields': ('user', 'role', 'assigned_by')
        }),
        (_('状态信息'), {
            'fields': ('is_active', 'expires_at', 'assigned_at')
        }),
    )


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    """角色权限管理"""
    list_display = ['role', 'permission', 'granted_at', 'granted_by']
    list_filter = ['role', 'permission', 'granted_at']
    search_fields = ['role__name', 'permission__name']
    readonly_fields = ['granted_at']

