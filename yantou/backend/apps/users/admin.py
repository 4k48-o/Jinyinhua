"""
用户管理 Admin 配置
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import UserProfile, Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """部门管理"""
    list_display = ['name', 'code', 'parent', 'level', 'manager', 'is_active', 'sort_order', 'created_at']
    list_filter = ['is_active', 'is_deleted', 'level']
    search_fields = ['name', 'code', 'description']
    readonly_fields = ['created_at', 'updated_at', 'deleted_at']
    fieldsets = (
        (_('基本信息'), {
            'fields': ('name', 'code', 'parent', 'level', 'path', 'description')
        }),
        (_('管理信息'), {
            'fields': ('manager', 'sort_order', 'is_active', 'is_deleted')
        }),
        (_('时间信息'), {
            'fields': ('created_at', 'updated_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )


class UserProfileInline(admin.StackedInline):
    """用户扩展信息内联"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = _('用户扩展信息')
    fields = ('avatar', 'gender', 'birthday', 'address', 'bio', 'department', 'position', 'employee_no', 'join_date')


class CustomUserAdmin(BaseUserAdmin):
    """自定义用户管理"""
    inlines = (UserProfileInline,)
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']


# 重新注册 User Admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

