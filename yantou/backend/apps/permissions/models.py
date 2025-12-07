"""
权限管理模型
基于 RBAC（Role-Based Access Control）的权限管理系统
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Permission(models.Model):
    """
    权限模型
    存储权限信息，支持树形结构
    """
    name = models.CharField(_('权限名称'), max_length=100)
    code = models.CharField(_('权限代码'), max_length=100, unique=True, db_index=True, help_text=_('格式：资源类型:操作类型，如：user:create'))
    content_type = models.CharField(_('资源类型'), max_length=100, null=True, blank=True, db_index=True, help_text=_('如：user, role'))
    action = models.CharField(_('操作类型'), max_length=50, null=True, blank=True, help_text=_('如：create, read, update, delete'))
    description = models.TextField(_('权限描述'), null=True, blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('父权限'),
        db_index=True
    )
    sort_order = models.IntegerField(_('排序顺序'), default=0)
    is_active = models.BooleanField(_('是否激活'), default=True, db_index=True)
    is_system = models.BooleanField(_('是否系统权限'), default=False, help_text=_('系统权限不可删除'))
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        db_table = 'sys_permission'
        verbose_name = _('权限')
        verbose_name_plural = _('权限')
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Role(models.Model):
    """
    角色模型
    存储角色信息，用于 RBAC 权限控制
    """
    name = models.CharField(_('角色名称'), max_length=50, unique=True)
    code = models.CharField(_('角色代码'), max_length=50, unique=True, db_index=True, help_text=_('如：admin, user, guest'))
    description = models.TextField(_('角色描述'), null=True, blank=True)
    permissions = models.ManyToManyField(
        Permission,
        through='RolePermission',
        related_name='roles',
        verbose_name=_('权限'),
        blank=True
    )
    sort_order = models.IntegerField(_('排序顺序'), default=0)
    is_active = models.BooleanField(_('是否激活'), default=True, db_index=True)
    is_system = models.BooleanField(_('是否系统角色'), default=False, help_text=_('系统角色不可删除'))
    is_deleted = models.BooleanField(_('是否删除'), default=False, db_index=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    deleted_at = models.DateTimeField(_('删除时间'), null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_roles',
        verbose_name=_('创建人'),
        db_index=True
    )

    class Meta:
        db_table = 'sys_role'
        verbose_name = _('角色')
        verbose_name_plural = _('角色')
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.name


class UserRole(models.Model):
    """
    用户角色关联模型
    存储用户和角色的多对多关系
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_roles',
        verbose_name=_('用户'),
        db_index=True
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='user_roles',
        verbose_name=_('角色'),
        db_index=True
    )
    assigned_at = models.DateTimeField(_('分配时间'), auto_now_add=True)
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_user_roles',
        verbose_name=_('分配人'),
        db_index=True
    )
    is_active = models.BooleanField(_('是否激活'), default=True)
    expires_at = models.DateTimeField(_('过期时间'), null=True, blank=True, db_index=True, help_text=_('NULL 表示永久有效'))

    class Meta:
        db_table = 'sys_user_role'
        verbose_name = _('用户角色')
        verbose_name_plural = _('用户角色')
        unique_together = [['user', 'role']]
        ordering = ['-assigned_at']

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"

    @property
    def is_expired(self):
        """检查角色是否过期"""
        if self.expires_at is None:
            return False
        from django.utils import timezone
        return timezone.now() > self.expires_at


class RolePermission(models.Model):
    """
    角色权限关联模型
    存储角色和权限的多对多关系
    """
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='role_permissions',
        verbose_name=_('角色'),
        db_index=True
    )
    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE,
        related_name='role_permissions',
        verbose_name=_('权限'),
        db_index=True
    )
    granted_at = models.DateTimeField(_('授权时间'), auto_now_add=True)
    granted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='granted_role_permissions',
        verbose_name=_('授权人'),
        db_index=True
    )

    class Meta:
        db_table = 'sys_role_permission'
        verbose_name = _('角色权限')
        verbose_name_plural = _('角色权限')
        unique_together = [['role', 'permission']]
        ordering = ['-granted_at']

    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"

