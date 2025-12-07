"""
用户管理序列化器
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from .models import UserProfile, Department
from utils.validators import validate_phone, validate_password_strength
from apps.common.exceptions import ValidationException


class DepartmentSerializer(serializers.ModelSerializer):
    """部门序列化器"""
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    manager_name = serializers.CharField(source='manager.username', read_only=True)
    children_count = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = [
            'id', 'name', 'code', 'parent', 'parent_name', 'level', 'path',
            'manager', 'manager_name', 'description', 'sort_order', 'is_active',
            'children_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'level', 'path', 'created_at', 'updated_at']

    def get_children_count(self, obj):
        """获取子部门数量"""
        return obj.children.filter(is_deleted=False).count()


class DepartmentCreateSerializer(serializers.ModelSerializer):
    """部门创建序列化器"""
    class Meta:
        model = Department
        fields = [
            'name', 'code', 'parent', 'manager', 'description', 'sort_order', 'is_active'
        ]

    def validate_code(self, value):
        """验证部门代码唯一性"""
        if value:
            if Department.objects.filter(code=value, is_deleted=False).exists():
                raise serializers.ValidationError(_('部门代码已存在'))
        return value

    def validate_parent(self, value):
        """验证父部门"""
        if value:
            if value.is_deleted:
                raise serializers.ValidationError(_('父部门已被删除'))
            if not value.is_active:
                raise serializers.ValidationError(_('父部门未激活'))
        return value


class DepartmentUpdateSerializer(serializers.ModelSerializer):
    """部门更新序列化器"""
    class Meta:
        model = Department
        fields = [
            'name', 'code', 'parent', 'manager', 'description', 'sort_order', 'is_active'
        ]

    def validate_code(self, value):
        """验证部门代码唯一性"""
        if value:
            queryset = Department.objects.filter(code=value, is_deleted=False)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError(_('部门代码已存在'))
        return value

    def validate_parent(self, value):
        """验证父部门（包括循环引用检查）"""
        if value:
            if value.is_deleted:
                raise serializers.ValidationError(_('父部门已被删除'))
            if not value.is_active:
                raise serializers.ValidationError(_('父部门未激活'))
            
            # 检查循环引用：不能将部门设置为其子部门的子部门
            if self.instance:
                current = value
                while current:
                    if current.id == self.instance.id:
                        raise serializers.ValidationError(_('不能将部门设置为其子部门的子部门'))
                    current = current.parent
        return value


class DepartmentTreeSerializer(serializers.ModelSerializer):
    """部门树形结构序列化器"""
    children = serializers.SerializerMethodField()
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    manager_name = serializers.CharField(source='manager.username', read_only=True)
    children_count = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = [
            'id', 'name', 'code', 'parent', 'parent_name', 'level', 'path',
            'manager', 'manager_name', 'description', 'sort_order', 'is_active',
            'children_count', 'children'
        ]

    def get_children(self, obj):
        """获取子部门"""
        children = obj.children.filter(is_deleted=False, is_active=True).order_by('sort_order', 'id')
        return DepartmentTreeSerializer(children, many=True).data

    def get_children_count(self, obj):
        """获取子部门数量"""
        return obj.children.filter(is_deleted=False).count()


class UserProfileSerializer(serializers.ModelSerializer):
    """用户扩展信息序列化器"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    phone = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=20,
        validators=[validate_phone],
        help_text=_('手机号')
    )

    class Meta:
        model = UserProfile
        fields = [
            'id', 'phone', 'avatar', 'gender', 'gender_display', 'birthday', 'address',
            'bio', 'department', 'department_name', 'position', 'employee_no',
            'join_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_phone(self, value):
        """验证手机号"""
        if value:
            value = value.strip()
            if not value:
                return None
        return value

    def validate_employee_no(self, value):
        """验证工号唯一性"""
        if value:
            value = value.strip()
            if not value:
                return None
            queryset = UserProfile.objects.filter(employee_no=value)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError(_('工号已存在'))
        return value


class UserListSerializer(serializers.ModelSerializer):
    """用户列表序列化器"""
    profile = UserProfileSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'phone', 'first_name', 'last_name',
            'full_name', 'is_active', 'is_staff', 'is_superuser',
            'last_login', 'date_joined', 'profile'
        ]
        read_only_fields = ['id', 'last_login', 'date_joined']

    def get_full_name(self, obj):
        """获取全名"""
        if obj.first_name or obj.last_name:
            return f"{obj.first_name} {obj.last_name}".strip()
        return obj.username

    def get_phone(self, obj):
        """获取手机号（从 profile）"""
        if hasattr(obj, 'profile') and obj.profile:
            return obj.profile.phone
        return None


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详情序列化器"""
    profile = UserProfileSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'phone', 'first_name', 'last_name',
            'full_name', 'is_active', 'is_staff', 'is_superuser',
            'last_login', 'date_joined', 'profile'
        ]
        read_only_fields = ['id', 'username', 'last_login', 'date_joined']

    def get_full_name(self, obj):
        """获取全名"""
        if obj.first_name or obj.last_name:
            return f"{obj.first_name} {obj.last_name}".strip()
        return obj.username

    def get_phone(self, obj):
        """获取手机号（从 profile）"""
        if hasattr(obj, 'profile') and obj.profile:
            return obj.profile.phone
        return None


class UserCreateSerializer(serializers.ModelSerializer):
    """用户创建序列化器"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password_strength],
        help_text=_('密码')
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        help_text=_('确认密码')
    )
    phone = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=20,
        validators=[validate_phone],
        help_text=_('手机号')
    )
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'phone', 'password', 'password_confirm',
            'first_name', 'last_name', 'is_active', 'is_staff', 'profile'
        ]

    def validate(self, attrs):
        """验证数据"""
        if attrs.get('password') != attrs.get('password_confirm'):
            raise ValidationException(_('两次输入的密码不一致'))
        return attrs

    def validate_username(self, value):
        """验证用户名"""
        from utils.validators import validate_username as _validate_username
        _validate_username(value)
        if User.objects.filter(username=value).exists():
            raise ValidationException(_('用户名已存在'))
        return value

    def validate_email(self, value):
        """验证邮箱"""
        if value and User.objects.filter(email=value).exists():
            raise ValidationException(_('邮箱已被使用'))
        return value

    def create(self, validated_data):
        """创建用户"""
        password = validated_data.pop('password')
        password_confirm = validated_data.pop('password_confirm')
        phone = validated_data.pop('phone', None)
        profile_data = validated_data.pop('profile', {})

        # 处理 phone：如果 phone 是空字符串，设置为 None
        if phone is not None:
            phone = phone.strip() if phone else None
            if phone:
                profile_data['phone'] = phone
            # 如果 phone 是空字符串，不添加到 profile_data（使用默认值 None）
        elif 'phone' in profile_data:
            # 如果 profile_data 中有 phone 字段，确保空字符串转换为 None
            profile_phone = profile_data.get('phone')
            if profile_phone is not None:
                profile_phone = profile_phone.strip() if profile_phone else None
                if profile_phone:
                    profile_data['phone'] = profile_phone
                else:
                    # 空字符串不设置，使用默认值 None
                    profile_data.pop('phone', None)
        
        # 清理空字符串，转换为 None 或移除
        cleaned_profile_data = {}
        for key, value in profile_data.items():
            if value is not None and isinstance(value, str) and not value.strip():
                # 空字符串不添加到 cleaned_profile_data（使用模型默认值）
                continue
            else:
                cleaned_profile_data[key] = value

        # 创建用户
        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        # 创建用户扩展信息
        if cleaned_profile_data:
            UserProfile.objects.create(
                user=user,
                **cleaned_profile_data
            )

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """用户更新序列化器"""
    profile = UserProfileSerializer(required=False)
    phone = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=20,
        validators=[validate_phone],
        help_text=_('手机号')
    )

    class Meta:
        model = User
        fields = [
            'email', 'phone', 'first_name', 'last_name',
            'is_active', 'is_staff', 'profile'
        ]

    def validate_email(self, value):
        """验证邮箱"""
        if value and User.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
            raise ValidationException(_('邮箱已被使用'))
        return value

    def update(self, instance, validated_data):
        """更新用户"""
        profile_data = validated_data.pop('profile', {})
        phone = validated_data.pop('phone', None)

        # 更新用户基本信息
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # 更新用户扩展信息
        # 处理 phone：如果 phone 是空字符串，设置为 None
        if phone is not None:
            phone = phone.strip() if phone else None
            if phone:
                profile_data['phone'] = phone
            else:
                # 如果 phone 是空字符串，设置为 None 以清空字段
                profile_data['phone'] = None
        elif 'phone' in profile_data:
            # 如果 profile_data 中有 phone 字段，确保空字符串转换为 None
            profile_phone = profile_data.get('phone')
            if profile_phone is not None:
                profile_phone = profile_phone.strip() if profile_phone else None
                profile_data['phone'] = profile_phone
        
        # 清理空字符串，转换为 None
        cleaned_profile_data = {}
        for key, value in profile_data.items():
            if value is not None and isinstance(value, str) and not value.strip():
                cleaned_profile_data[key] = None
            else:
                cleaned_profile_data[key] = value
        
        if cleaned_profile_data:
            profile, created = UserProfile.objects.get_or_create(user=instance)
            for attr, value in cleaned_profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance


class CurrentUserSerializer(serializers.ModelSerializer):
    """当前用户信息序列化器"""
    profile = UserProfileSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'phone', 'first_name', 'last_name',
            'full_name', 'is_active', 'is_staff', 'is_superuser',
            'last_login', 'date_joined', 'profile', 'permissions', 'roles'
        ]
        read_only_fields = ['id', 'username', 'is_staff', 'is_superuser', 'last_login', 'date_joined']

    def get_full_name(self, obj):
        """获取全名"""
        if obj.first_name or obj.last_name:
            return f"{obj.first_name} {obj.last_name}".strip()
        return obj.username

    def get_phone(self, obj):
        """获取手机号（从 profile）"""
        if hasattr(obj, 'profile') and obj.profile:
            return obj.profile.phone
        return None

    def get_permissions(self, obj):
        """获取用户权限列表（权限代码）"""
        from apps.permissions.utils import get_user_permissions
        permissions = get_user_permissions(obj)
        return [p.code for p in permissions]

    def get_roles(self, obj):
        """获取用户角色列表（角色代码）"""
        from apps.permissions.utils import get_user_roles
        roles = get_user_roles(obj)
        return [r.code for r in roles]



