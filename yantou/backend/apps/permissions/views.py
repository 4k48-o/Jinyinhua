"""
权限管理视图
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, OpenApiExample
from apps.common.response import APIResponse
from apps.common.exceptions import NotFoundException, PermissionException, ValidationException
from apps.common.pagination import CustomPageNumberPagination
from .models import Role, Permission, UserRole, RolePermission
from .serializers import (
    RoleListSerializer, RoleDetailSerializer, RoleCreateSerializer, RoleUpdateSerializer,
    PermissionSerializer, PermissionTreeSerializer, PermissionCreateSerializer, PermissionUpdateSerializer,
    UserRoleSerializer, UserRoleListSerializer
)
from .utils import get_user_permissions, get_user_roles, check_user_permission, check_user_role
import logging

logger = logging.getLogger('django.request')


class PermissionViewSet(viewsets.ModelViewSet):
    """
    权限管理视图集
    """
    queryset = Permission.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = CustomPageNumberPagination
    filterset_fields = ['content_type', 'action', 'parent', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['sort_order', 'created_at']
    ordering = ['sort_order', 'id']

    def get_serializer_class(self):
        """根据操作返回不同的序列化器"""
        if self.action == 'create':
            return PermissionCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return PermissionUpdateSerializer
        elif self.action == 'tree':
            return PermissionTreeSerializer
        else:
            return PermissionSerializer

    def get_queryset(self):
        """获取查询集"""
        queryset = Permission.objects.all()
        # 列表接口默认只显示激活的权限
        if self.action == 'list':
            queryset = queryset.filter(is_active=True)
        return queryset

    @extend_schema(
        tags=['权限'],
        summary='权限列表',
        description='获取权限列表，支持分页、过滤、搜索。只有管理员可以访问。'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        tags=['权限'],
        summary='权限详情',
        description='获取权限详细信息'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=['权限'],
        summary='创建权限',
        description='创建新权限，只有管理员可以创建。',
        request=PermissionCreateSerializer
    )
    def create(self, request, *args, **kwargs):
        """创建权限"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        permission = serializer.save()
        
        logger.info(f'权限创建成功: {permission.name}', extra={
            'permission_id': permission.id,
            'permission_code': permission.code,
            'created_by': request.user.id
        })
        
        return APIResponse.success(
            data=PermissionSerializer(permission).data,
            message=_('权限创建成功'),
            status_code=status.HTTP_201_CREATED
        )

    @extend_schema(
        tags=['权限'],
        summary='更新权限',
        description='更新权限信息，系统权限不可修改。'
    )
    def update(self, request, *args, **kwargs):
        """更新权限"""
        instance = self.get_object()
        
        # 系统权限不可修改
        if instance.is_system and not request.user.is_superuser:
            raise PermissionException(_('系统权限不可修改'))
        
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        permission = serializer.save()
        
        logger.info(f'权限更新成功: {permission.name}', extra={
            'permission_id': permission.id,
            'permission_code': permission.code,
            'updated_by': request.user.id
        })
        
        return APIResponse.success(
            data=PermissionSerializer(permission).data,
            message=_('权限更新成功')
        )

    @extend_schema(
        tags=['权限'],
        summary='删除权限',
        description='删除权限（软删除），系统权限不可删除。'
    )
    def destroy(self, request, *args, **kwargs):
        """删除权限（软删除）"""
        instance = self.get_object()
        
        # 系统权限不可删除
        if instance.is_system:
            raise PermissionException(_('系统权限不可删除'))
        
        # 检查是否有子权限
        if instance.children.filter(is_active=True).exists():
            raise ValidationException(_('该权限下存在子权限，无法删除'))
        
        # 检查是否有角色使用该权限
        from .models import RolePermission
        if RolePermission.objects.filter(permission=instance).exists():
            raise ValidationException(_('该权限已被角色使用，无法删除'))
        
        # 软删除：设置为非激活状态
        instance.is_active = False
        instance.save()
        
        logger.info(f'权限删除成功: {instance.name}', extra={
            'permission_id': instance.id,
            'permission_code': instance.code,
            'deleted_by': request.user.id
        })
        
        return APIResponse.success(message=_('权限删除成功'))

    @extend_schema(
        tags=['权限'],
        summary='权限树形结构',
        description='获取权限树形结构'
    )
    @action(detail=False, methods=['get'], serializer_class=PermissionTreeSerializer)
    def tree(self, request):
        """获取权限树形结构"""
        # 获取根权限（没有父权限的权限）
        root_permissions = Permission.objects.filter(
            parent__isnull=True,
            is_active=True
        ).order_by('sort_order', 'id')
        
        serializer = PermissionTreeSerializer(root_permissions, many=True)
        return APIResponse.success(data=serializer.data)


class RoleViewSet(viewsets.ModelViewSet):
    """
    角色管理视图集
    """
    queryset = Role.objects.filter(is_deleted=False)
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = CustomPageNumberPagination
    filterset_fields = ['is_active', 'is_system']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['sort_order', 'created_at']
    ordering = ['sort_order', 'id']

    def get_serializer_class(self):
        """根据操作返回不同的序列化器"""
        if self.action == 'list':
            return RoleListSerializer
        elif self.action == 'create':
            return RoleCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return RoleUpdateSerializer
        else:
            return RoleDetailSerializer

    @extend_schema(
        tags=['权限'],
        summary='角色列表',
        description='获取角色列表，支持分页、过滤、搜索。只有管理员可以访问。'
    )
    def list(self, request, *args, **kwargs):
        # 记录搜索参数用于调试
        search_param = request.query_params.get('search')
        if search_param:
            logger.info(f'角色列表搜索: {search_param}', extra={
                'user_id': request.user.id,
                'search': search_param
            })
        return super().list(request, *args, **kwargs)

    @extend_schema(
        tags=['权限'],
        summary='角色详情',
        description='获取角色详细信息，包括权限列表'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=['权限'],
        summary='创建角色',
        description='创建新角色，只有管理员可以创建。',
        request=RoleCreateSerializer
    )
    def create(self, request, *args, **kwargs):
        """创建角色"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 通过 context 传递 request，让 serializer 可以访问 user
        serializer.context['request'] = request
        role = serializer.save()
        
        logger.info(f'角色创建成功: {role.name}', extra={
            'role_id': role.id,
            'role_code': role.code,
            'created_by': request.user.id
        })
        
        return APIResponse.success(
            data=RoleDetailSerializer(role).data,
            message=_('角色创建成功'),
            status_code=status.HTTP_201_CREATED
        )

    @extend_schema(
        tags=['权限'],
        summary='更新角色',
        description='更新角色信息，系统角色不可修改。'
    )
    def update(self, request, *args, **kwargs):
        """更新角色"""
        instance = self.get_object()
        
        # 系统角色不可修改
        if instance.is_system and not request.user.is_superuser:
            raise PermissionException(_('系统角色不可修改'))
        
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        role = serializer.save()
        
        logger.info(f'角色更新成功: {role.name}', extra={
            'role_id': role.id,
            'role_code': role.code,
            'updated_by': request.user.id
        })
        
        return APIResponse.success(
            data=RoleDetailSerializer(role).data,
            message=_('角色更新成功')
        )

    @extend_schema(
        tags=['权限'],
        summary='删除角色',
        description='删除角色（软删除），系统角色不可删除。'
    )
    def destroy(self, request, *args, **kwargs):
        """删除角色（软删除）"""
        instance = self.get_object()
        
        # 系统角色不可删除
        if instance.is_system:
            raise PermissionException(_('系统角色不可删除'))
        
        instance.is_deleted = True
        instance.save()
        
        logger.info(f'角色删除成功: {instance.name}', extra={
            'role_id': instance.id,
            'role_code': instance.code,
            'deleted_by': request.user.id
        })
        
        return APIResponse.success(message=_('角色删除成功'))

    @extend_schema(
        tags=['权限'],
        summary='获取角色权限列表',
        description='获取指定角色的所有权限列表'
    )
    @action(detail=True, methods=['get'], url_path='permissions')
    def permissions(self, request, pk=None):
        """获取角色的权限列表"""
        role = self.get_object()
        permissions = role.permissions.filter(is_active=True).order_by('sort_order', 'id')
        serializer = PermissionSerializer(permissions, many=True)
        return APIResponse.success(data=serializer.data)

    @extend_schema(
        tags=['权限'],
        summary='批量添加权限',
        description='为角色批量添加权限（增量添加，不替换现有权限）',
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'permission_ids': {
                        'type': 'array',
                        'items': {'type': 'integer'},
                        'description': '权限 ID 列表'
                    }
                },
                'required': ['permission_ids']
            }
        }
    )
    @action(detail=True, methods=['post'], url_path='permissions/add')
    def add_permissions(self, request, pk=None):
        """批量添加权限到角色"""
        role = self.get_object()
        
        # 系统角色不可修改
        if role.is_system and not request.user.is_superuser:
            raise PermissionException(_('系统角色不可修改'))
        
        permission_ids = request.data.get('permission_ids', [])
        if not permission_ids:
            raise ValidationException(_('请提供权限 ID 列表'))
        
        # 获取现有权限 ID
        existing_permission_ids = set(
            role.role_permissions.values_list('permission_id', flat=True)
        )
        
        # 过滤出需要添加的权限
        permissions = Permission.objects.filter(
            id__in=permission_ids,
            is_active=True
        ).exclude(id__in=existing_permission_ids)
        
        added_count = 0
        for permission in permissions:
            RolePermission.objects.get_or_create(
                role=role,
                permission=permission,
                defaults={'granted_by': request.user}
            )
            added_count += 1
        
        logger.info(f'为角色 {role.name} 添加了 {added_count} 个权限', extra={
            'role_id': role.id,
            'added_count': added_count,
            'added_by': request.user.id
        })
        
        return APIResponse.success(
            data={'added_count': added_count},
            message=_('成功添加 {count} 个权限').format(count=added_count)
        )

    @extend_schema(
        tags=['权限'],
        summary='批量移除权限',
        description='从角色批量移除权限',
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'permission_ids': {
                        'type': 'array',
                        'items': {'type': 'integer'},
                        'description': '权限 ID 列表'
                    }
                },
                'required': ['permission_ids']
            }
        }
    )
    @action(detail=True, methods=['post'], url_path='permissions/remove')
    def remove_permissions(self, request, pk=None):
        """批量移除角色的权限"""
        role = self.get_object()
        
        # 系统角色不可修改
        if role.is_system and not request.user.is_superuser:
            raise PermissionException(_('系统角色不可修改'))
        
        permission_ids = request.data.get('permission_ids', [])
        if not permission_ids:
            raise ValidationException(_('请提供权限 ID 列表'))
        
        # 删除指定的权限关联
        deleted_count, _ = RolePermission.objects.filter(
            role=role,
            permission_id__in=permission_ids
        ).delete()
        
        logger.info(f'从角色 {role.name} 移除了 {deleted_count} 个权限', extra={
            'role_id': role.id,
            'removed_count': deleted_count,
            'removed_by': request.user.id
        })
        
        return APIResponse.success(
            data={'removed_count': deleted_count},
            message=_('成功移除 {count} 个权限').format(count=deleted_count)
        )

    @extend_schema(
        tags=['权限'],
        summary='替换角色权限',
        description='替换角色的所有权限（完全替换）',
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'permission_ids': {
                        'type': 'array',
                        'items': {'type': 'integer'},
                        'description': '权限 ID 列表'
                    }
                },
                'required': ['permission_ids']
            }
        }
    )
    @action(detail=True, methods=['post'], url_path='permissions/replace')
    def replace_permissions(self, request, pk=None):
        """替换角色的所有权限"""
        role = self.get_object()
        
        # 系统角色不可修改
        if role.is_system and not request.user.is_superuser:
            raise PermissionException(_('系统角色不可修改'))
        
        permission_ids = request.data.get('permission_ids', [])
        
        # 删除所有现有权限
        old_count = role.role_permissions.count()
        role.role_permissions.all().delete()
        
        # 添加新权限
        if permission_ids:
            permissions = Permission.objects.filter(id__in=permission_ids, is_active=True)
            for permission in permissions:
                RolePermission.objects.create(
                    role=role,
                    permission=permission,
                    granted_by=request.user
                )
        
        new_count = role.role_permissions.count()
        
        logger.info(f'替换角色 {role.name} 的权限: {old_count} -> {new_count}', extra={
            'role_id': role.id,
            'old_count': old_count,
            'new_count': new_count,
            'replaced_by': request.user.id
        })
        
        return APIResponse.success(
            data={'old_count': old_count, 'new_count': new_count},
            message=_('成功替换权限')
        )


class UserRoleViewSet(viewsets.ModelViewSet):
    """
    用户角色管理视图集
    """
    queryset = UserRole.objects.select_related('user', 'role', 'assigned_by').all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = CustomPageNumberPagination
    filterset_fields = ['user', 'role', 'is_active']
    ordering_fields = ['assigned_at']
    ordering = ['-assigned_at']

    @extend_schema(
        tags=['权限'],
        summary='用户角色列表',
        description='获取用户角色列表，支持分页、过滤。只有管理员可以访问。'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        tags=['权限'],
        summary='用户角色详情',
        description='获取用户角色详细信息'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=['权限'],
        summary='分配角色',
        description='为用户分配角色，只有管理员可以操作。',
        request=UserRoleSerializer
    )
    def create(self, request, *args, **kwargs):
        """为用户分配角色"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_role = serializer.save()
        
        logger.info(f'角色分配成功: {user_role.user.username} - {user_role.role.name}', extra={
            'user_id': user_role.user.id,
            'role_id': user_role.role.id,
            'assigned_by': request.user.id
        })
        
        return APIResponse.success(
            data=UserRoleSerializer(user_role).data,
            message=_('角色分配成功'),
            status_code=status.HTTP_201_CREATED
        )

    @extend_schema(
        tags=['权限'],
        summary='移除角色',
        description='移除用户的角色，只有管理员可以操作。'
    )
    def destroy(self, request, *args, **kwargs):
        """移除用户角色"""
        instance = self.get_object()
        user = instance.user
        role = instance.role
        
        instance.delete()
        
        logger.info(f'角色移除成功: {user.username} - {role.name}', extra={
            'user_id': user.id,
            'role_id': role.id,
            'removed_by': request.user.id
        })
        
        return APIResponse.success(message=_('角色移除成功'))

    @extend_schema(
        tags=['权限'],
        summary='获取用户的角色列表',
        description='获取指定用户的所有角色'
    )
    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def user_roles(self, request, user_id=None):
        """获取用户的角色列表"""
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise NotFoundException(_('用户不存在'))
        
        user_roles = UserRole.objects.filter(user=user, is_active=True)
        serializer = UserRoleListSerializer(user_roles, many=True)
        
        return APIResponse.success(data=serializer.data)


class PermissionCheckViewSet(viewsets.ViewSet):
    """
    权限检查视图集
    提供权限查询和检查接口
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['权限'],
        summary='获取当前用户的所有权限',
        description='获取当前登录用户的所有权限列表'
    )
    @action(detail=False, methods=['get'])
    def my_permissions(self, request):
        """获取当前用户的所有权限"""
        permissions = get_user_permissions(request.user)
        serializer = PermissionSerializer(permissions, many=True)
        return APIResponse.success(data=serializer.data)

    @extend_schema(
        tags=['权限'],
        summary='获取当前用户的所有角色',
        description='获取当前登录用户的所有角色列表'
    )
    @action(detail=False, methods=['get'])
    def my_roles(self, request):
        """获取当前用户的所有角色"""
        roles = get_user_roles(request.user)
        serializer = RoleListSerializer(roles, many=True)
        return APIResponse.success(data=serializer.data)

    @extend_schema(
        tags=['权限'],
        summary='检查权限',
        description='检查当前用户是否拥有指定权限',
        parameters=[
            {
                'name': 'permission_code',
                'in': 'query',
                'required': True,
                'description': '权限代码，如：user:create',
                'schema': {'type': 'string'}
            }
        ]
    )
    @action(detail=False, methods=['get'])
    def check_permission(self, request):
        """检查用户是否拥有指定权限"""
        permission_code = request.query_params.get('permission_code')
        if not permission_code:
            raise ValidationException(_('请提供权限代码'))
        
        has_permission = check_user_permission(request.user, permission_code)
        return APIResponse.success(data={
            'permission_code': permission_code,
            'has_permission': has_permission
        })

    @extend_schema(
        tags=['权限'],
        summary='检查角色',
        description='检查当前用户是否拥有指定角色',
        parameters=[
            {
                'name': 'role_code',
                'in': 'query',
                'required': True,
                'description': '角色代码，如：admin',
                'schema': {'type': 'string'}
            }
        ]
    )
    @action(detail=False, methods=['get'])
    def check_role(self, request):
        """检查用户是否拥有指定角色"""
        role_code = request.query_params.get('role_code')
        if not role_code:
            raise ValidationException(_('请提供角色代码'))
        
        has_role = check_user_role(request.user, role_code)
        return APIResponse.success(data={
            'role_code': role_code,
            'has_role': has_role
        })

