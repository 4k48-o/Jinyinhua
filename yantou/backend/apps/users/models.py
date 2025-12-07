"""
用户管理模型
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Department(models.Model):
    """
    部门模型
    支持树形结构，通过 parent_id 建立层级关系
    """
    name = models.CharField(_('部门名称'), max_length=100, db_index=True)
    code = models.CharField(_('部门代码'), max_length=50, unique=True, null=True, blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('父部门'),
        db_index=True
    )
    level = models.IntegerField(_('部门层级'), default=1, db_index=True)
    path = models.CharField(_('部门路径'), max_length=500, null=True, blank=True, help_text=_('如：1/2/3'))
    manager = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_departments',
        verbose_name=_('部门负责人'),
        db_index=True
    )
    description = models.TextField(_('部门描述'), null=True, blank=True)
    sort_order = models.IntegerField(_('排序顺序'), default=0)
    is_active = models.BooleanField(_('是否激活'), default=True, db_index=True)
    is_deleted = models.BooleanField(_('是否删除'), default=False, db_index=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    deleted_at = models.DateTimeField(_('删除时间'), null=True, blank=True)

    class Meta:
        db_table = 'sys_department'
        verbose_name = _('部门')
        verbose_name_plural = _('部门')
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """保存时自动计算层级和路径"""
        if self.parent:
            self.level = self.parent.level + 1
            self.path = f"{self.parent.path}/{self.id}" if self.parent.path else str(self.id)
        else:
            self.level = 1
            self.path = str(self.id) if self.id else None
        
        super().save(*args, **kwargs)
        # 保存后更新路径（因为需要 id）
        if not self.path:
            self.path = str(self.id)
            super().save(update_fields=['path'])


class UserProfile(models.Model):
    """
    用户扩展信息模型
    与 Django User 模型一对一关系
    """
    GENDER_CHOICES = [
        (0, _('未知')),
        (1, _('男')),
        (2, _('女')),
    ]

    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('用户'),
        db_index=True
    )
    phone = models.CharField(_('手机号'), max_length=20, null=True, blank=True, db_index=True)
    avatar = models.ImageField(
        _('头像'),
        upload_to='avatars/%Y/%m/%d/',
        null=True,
        blank=True,
        max_length=500
    )
    gender = models.IntegerField(_('性别'), choices=GENDER_CHOICES, null=True, blank=True)
    birthday = models.DateField(_('生日'), null=True, blank=True)
    address = models.CharField(_('地址'), max_length=500, null=True, blank=True)
    bio = models.TextField(_('个人简介'), null=True, blank=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members',
        verbose_name=_('部门'),
        db_index=True
    )
    position = models.CharField(_('职位'), max_length=100, null=True, blank=True)
    employee_no = models.CharField(_('工号'), max_length=50, unique=True, null=True, blank=True)
    join_date = models.DateField(_('入职日期'), null=True, blank=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        db_table = 'sys_user_profile'
        verbose_name = _('用户扩展信息')
        verbose_name_plural = _('用户扩展信息')

    def __str__(self):
        return f"{self.user.username} - Profile"

