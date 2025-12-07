"""
通用模型
包含基础模型和审计日志模型
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import json

User = get_user_model()


class BaseModel(models.Model):
    """
    基础模型
    提供通用字段：创建时间、更新时间、软删除
    """
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    is_deleted = models.BooleanField(_('是否删除'), default=False, db_index=True)
    deleted_at = models.DateTimeField(_('删除时间'), null=True, blank=True)
    
    class Meta:
        abstract = True
        ordering = ['-created_at']


class AuditLog(models.Model):
    """
    操作日志模型
    记录用户的所有重要操作，用于审计和追踪
    """
    ACTION_CHOICES = [
        ('create', _('创建')),
        ('update', _('更新')),
        ('delete', _('删除')),
        ('view', _('查看')),
        ('login', _('登录')),
        ('logout', _('登出')),
        ('export', _('导出')),
        ('import', _('导入')),
        ('other', _('其他')),
    ]
    
    STATUS_CHOICES = [
        (1, _('成功')),
        (0, _('失败')),
    ]
    
    user_id = models.BigIntegerField(_('用户 ID'), null=True, blank=True, db_index=True)
    username = models.CharField(_('用户名'), max_length=150, null=True, blank=True, db_index=True)
    action = models.CharField(_('操作类型'), max_length=50, choices=ACTION_CHOICES, db_index=True)
    resource_type = models.CharField(_('资源类型'), max_length=100, db_index=True)
    resource_id = models.BigIntegerField(_('资源 ID'), null=True, blank=True, db_index=True)
    resource_name = models.CharField(_('资源名称'), max_length=200, null=True, blank=True)
    description = models.TextField(_('操作描述'), null=True, blank=True)
    request_method = models.CharField(_('HTTP 方法'), max_length=10, null=True, blank=True)
    request_path = models.CharField(_('请求路径'), max_length=500, null=True, blank=True)
    request_params = models.TextField(_('请求参数'), null=True, blank=True)  # JSON 格式
    ip_address = models.CharField(_('IP 地址'), max_length=50, null=True, blank=True, db_index=True)
    user_agent = models.CharField(_('用户代理'), max_length=500, null=True, blank=True)
    status = models.SmallIntegerField(_('操作状态'), choices=STATUS_CHOICES, default=1, db_index=True)
    error_message = models.TextField(_('错误信息'), null=True, blank=True)
    execution_time = models.IntegerField(_('执行时间（毫秒）'), null=True, blank=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True, db_index=True)
    
    class Meta:
        db_table = 'sys_audit_log'
        verbose_name = _('操作日志')
        verbose_name_plural = _('操作日志')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id', 'created_at']),
            models.Index(fields=['action', 'resource_type']),
            models.Index(fields=['status', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.username} - {self.get_action_display()} - {self.resource_type} - {self.created_at}"
    
    def set_request_params(self, params):
        """
        设置请求参数（自动转换为 JSON）
        
        Args:
            params: 字典或可序列化的对象
        """
        if params is not None:
            try:
                self.request_params = json.dumps(params, ensure_ascii=False)
            except (TypeError, ValueError):
                self.request_params = str(params)
    
    def get_request_params(self):
        """
        获取请求参数（自动解析 JSON）
        
        Returns:
            dict: 请求参数字典
        """
        if self.request_params:
            try:
                return json.loads(self.request_params)
            except (TypeError, ValueError):
                return {}
        return {}


class LoginLog(models.Model):
    """
    登录日志模型
    记录用户登录/退出日志，用于审计和追踪
    """
    LOGIN_TYPE_CHOICES = [
        ('password', _('密码登录')),
        ('token', _('Token登录')),
        ('sso', _('单点登录')),
        ('other', _('其他')),
    ]
    
    STATUS_CHOICES = [
        (1, _('成功')),
        (0, _('失败')),
    ]
    
    user_id = models.BigIntegerField(_('用户 ID'), null=True, blank=True, db_index=True)
    username = models.CharField(_('用户名'), max_length=150, null=True, blank=True, db_index=True)
    login_type = models.CharField(_('登录类型'), max_length=20, choices=LOGIN_TYPE_CHOICES, default='password', db_index=True)
    ip_address = models.CharField(_('IP 地址'), max_length=50, null=True, blank=True, db_index=True)
    user_agent = models.CharField(_('用户代理'), max_length=500, null=True, blank=True)
    location = models.CharField(_('登录地点'), max_length=200, null=True, blank=True)
    device = models.CharField(_('设备信息'), max_length=100, null=True, blank=True)
    browser = models.CharField(_('浏览器信息'), max_length=100, null=True, blank=True)
    os = models.CharField(_('操作系统'), max_length=100, null=True, blank=True)
    status = models.SmallIntegerField(_('登录状态'), choices=STATUS_CHOICES, default=1, db_index=True)
    failure_reason = models.CharField(_('失败原因'), max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(_('登录时间'), auto_now_add=True, db_index=True)
    
    class Meta:
        db_table = 'sys_login_log'
        verbose_name = _('登录日志')
        verbose_name_plural = _('登录日志')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id', 'created_at']),
            models.Index(fields=['username', 'created_at']),
            models.Index(fields=['ip_address', 'created_at']),
            models.Index(fields=['status', 'created_at']),
        ]
    
    def __str__(self):
        status_display = '成功' if self.status == 1 else '失败'
        return f"{self.username} - {status_display} - {self.created_at}"

