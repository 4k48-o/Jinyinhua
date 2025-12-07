"""
权限管理序列化器
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Role, Permission, UserRole, RolePermission
from apps.common.exceptions import ValidationException


class PermissionSerializer(serializers.ModelSerializer):
    """权限序列化器"""
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    children_count = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = [
            'id', 'name', 'code', 'content_type', 'action', 'description',
            'parent', 'parent_name', 'sort_order', 'is_active', 'is_system',
            'children_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_system']

    def get_children_count(self, obj):
        """获取子权限数量"""
        return obj.children.filter(is_active=True).count()


class PermissionCreateSerializer(serializers.ModelSerializer):
    """权限创建序列化器"""
    
    class Meta:
        model = Permission
        fields = [
            'name', 'code', 'content_type', 'action', 'description',
            'parent', 'sort_order', 'is_active'
        ]
    
    def validate_code(self, value):
        """验证权限代码"""
        if Permission.objects.filter(code=value).exists():
            raise ValidationException(_('权限代码已存在'))
        return value
    
    def validate_parent(self, value):
        """验证父权限"""
        if value and not value.is_active:
            raise ValidationException(_('父权限必须是激活状态'))
        return value


class PermissionUpdateSerializer(serializers.ModelSerializer):
    """权限更新序列化器"""
    
    class Meta:
        model = Permission
        fields = [
            'name', 'code', 'content_type', 'action', 'description',
            'parent', 'sort_order', 'is_active'
        ]
    
    def validate_code(self, value):
        """验证权限代码"""
        if self.instance and Permission.objects.filter(code=value).exclude(pk=self.instance.pk).exists():
            raise ValidationException(_('权限代码已存在'))
        return value
    
    def validate_parent(self, value):
        """验证父权限"""
        if value:
            if not value.is_active:
                raise ValidationException(_('父权限必须是激活状态'))
            # 防止将权限设置为自己的子权限（避免循环引用）
            if self.instance and value.id == self.instance.id:
                raise ValidationException(_('不能将权限设置为自己的父权限'))
            # 检查是否会导致循环引用
            if self.instance:
                current = value
                while current:
                    if current.id == self.instance.id:
                        raise ValidationException(_('不能将权限设置为自己的子权限（会导致循环引用）'))
                    current = current.parent
        return value


class PermissionTreeSerializer(serializers.ModelSerializer):
    """权限树形结构序列化器"""
    children = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = [
            'id', 'name', 'code', 'content_type', 'action', 'description',
            'sort_order', 'is_active', 'children'
        ]

    def get_children(self, obj):
        """获取子权限"""
        children = obj.children.filter(is_active=True).order_by('sort_order', 'id')
        return PermissionTreeSerializer(children, many=True).data


class RoleListSerializer(serializers.ModelSerializer):
    """角色列表序列化器"""
    permissions_count = serializers.SerializerMethodField()
    users_count = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = [
            'id', 'name', 'code', 'description', 'is_active', 'is_system',
            'sort_order', 'permissions_count', 'users_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_permissions_count(self, obj):
        """获取权限数量"""
        return obj.permissions.filter(is_active=True).count()

    def get_users_count(self, obj):
        """获取用户数量"""
        return obj.user_roles.filter(is_active=True).count()


class RoleDetailSerializer(serializers.ModelSerializer):
    """角色详情序列化器"""
    permissions = PermissionSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Role
        fields = [
            'id', 'name', 'code', 'description', 'permissions', 'is_active',
            'is_system', 'sort_order', 'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RoleCreateSerializer(serializers.ModelSerializer):
    """角色创建序列化器"""
    permission_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        write_only=True,
        help_text=_('权限 ID 列表')
    )

    class Meta:
        model = Role
        fields = [
            'name', 'code', 'description', 'permission_ids',
            'is_active', 'sort_order'
        ]

    def validate_code(self, value):
        """验证角色代码"""
        if Role.objects.filter(code=value).exists():
            raise ValidationException(_('角色代码已存在'))
        return value

    def create(self, validated_data):
        """创建角色"""
        permission_ids = validated_data.pop('permission_ids', [])
        # 从 context 中获取 request 和 user
        request = self.context.get('request')
        created_by = request.user if request else None
        
        # 创建角色
        role = Role.objects.create(
            **validated_data,
            created_by=created_by
        )
        
        # 分配权限
        if permission_ids:
            permissions = Permission.objects.filter(id__in=permission_ids, is_active=True)
            for permission in permissions:
                RolePermission.objects.create(
                    role=role,
                    permission=permission,
                    granted_by=created_by
                )
        
        return role


class RoleUpdateSerializer(serializers.ModelSerializer):
    """角色更新序列化器"""
    permission_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        write_only=True,
        help_text=_('权限 ID 列表')
    )

    class Meta:
        model = Role
        fields = [
            'name', 'code', 'description', 'permission_ids',
            'is_active', 'sort_order'
        ]

    def validate_code(self, value):
        """验证角色代码"""
        if Role.objects.filter(code=value).exclude(pk=self.instance.pk).exists():
            raise ValidationException(_('角色代码已存在'))
        return value

    def update(self, instance, validated_data):
        """更新角色"""
        permission_ids = validated_data.pop('permission_ids', None)
        
        # 更新角色基本信息
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # 更新权限
        if permission_ids is not None:
            # 删除旧权限
            instance.role_permissions.all().delete()
            # 添加新权限
            permissions = Permission.objects.filter(id__in=permission_ids, is_active=True)
            for permission in permissions:
                RolePermission.objects.create(
                    role=instance,
                    permission=permission,
                    granted_by=self.context['request'].user
                )
        
        return instance


class UserRoleSerializer(serializers.ModelSerializer):
    """用户角色序列化器"""
    role_name = serializers.CharField(source='role.name', read_only=True)
    role_code = serializers.CharField(source='role.code', read_only=True)
    assigned_by_name = serializers.CharField(source='assigned_by.username', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)

    class Meta:
        model = UserRole
        fields = [
            'id', 'user', 'role', 'role_name', 'role_code',
            'assigned_at', 'assigned_by', 'assigned_by_name',
            'is_active', 'expires_at', 'is_expired'
        ]
        read_only_fields = ['id', 'assigned_at']

    def validate(self, attrs):
        """验证数据"""
        user = attrs.get('user')
        role = attrs.get('role')
        
        if user and role:
            # 检查是否已存在
            if UserRole.objects.filter(user=user, role=role).exclude(pk=self.instance.pk if self.instance else None).exists():
                raise ValidationException(_('该用户已拥有此角色'))
        
        return attrs

    def create(self, validated_data):
        """创建用户角色"""
        validated_data['assigned_by'] = self.context['request'].user
        return super().create(validated_data)


class UserRoleListSerializer(serializers.ModelSerializer):
    """用户角色列表序列化器（简化版）"""
    role_name = serializers.CharField(source='role.name', read_only=True)
    role_code = serializers.CharField(source='role.code', read_only=True)

    class Meta:
        model = UserRole
        fields = [
            'id', 'role', 'role_name', 'role_code',
            'is_active', 'assigned_at', 'expires_at', 'is_expired'
        ]

