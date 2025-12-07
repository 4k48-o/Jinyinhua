"""
通用应用 Admin 配置
"""
from django.contrib import admin
from .models import AuditLog, LoginLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """
    操作日志管理
    """
    list_display = [
        'id', 'username', 'action', 'resource_type', 'resource_id',
        'status', 'ip_address', 'created_at'
    ]
    list_filter = [
        'action', 'resource_type', 'status', 'created_at'
    ]
    search_fields = [
        'username', 'resource_type', 'resource_name', 'description',
        'ip_address', 'request_path'
    ]
    readonly_fields = [
        'user_id', 'username', 'action', 'resource_type', 'resource_id',
        'resource_name', 'description', 'request_method', 'request_path',
        'request_params', 'ip_address', 'user_agent', 'status',
        'error_message', 'execution_time', 'created_at'
    ]
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    def has_add_permission(self, request):
        """禁止手动添加日志"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """禁止修改日志"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """允许删除日志（用于清理）"""
        return True


@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    """
    登录日志管理
    """
    list_display = [
        'id', 'username', 'login_type', 'status', 'ip_address',
        'device', 'browser', 'created_at'
    ]
    list_filter = [
        'login_type', 'status', 'created_at'
    ]
    search_fields = [
        'username', 'ip_address', 'device', 'browser', 'failure_reason'
    ]
    readonly_fields = [
        'user_id', 'username', 'login_type', 'ip_address', 'user_agent',
        'location', 'device', 'browser', 'os', 'status', 'failure_reason', 'created_at'
    ]
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    def has_add_permission(self, request):
        """禁止手动添加日志"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """禁止修改日志"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """允许删除日志（用于清理）"""
        return True

