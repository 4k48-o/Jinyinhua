"""
用户管理视图
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from apps.common.response import APIResponse
from apps.common.exceptions import NotFoundException, PermissionException, ValidationException
from apps.permissions.permissions import PermissionRequired
from apps.common.pagination import CustomPageNumberPagination
from .models import UserProfile, Department
from .serializers import (
    UserListSerializer, UserDetailSerializer, UserCreateSerializer,
    UserUpdateSerializer, CurrentUserSerializer, DepartmentSerializer,
    DepartmentCreateSerializer, DepartmentUpdateSerializer, DepartmentTreeSerializer
)
from .filters import UserFilter
from .permissions import UserPermission
from .utils import validate_image_file, compress_image
from django.core.files.base import ContentFile
import logging
import os

logger = logging.getLogger('django.request')


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    部门管理视图集
    """
    queryset = Department.objects.filter(is_deleted=False)
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, PermissionRequired]
    required_permissions = ['department:read']
    pagination_class = CustomPageNumberPagination
    filterset_fields = ['parent', 'level', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['sort_order', 'created_at']
    ordering = ['sort_order', 'id']

    def get_serializer_class(self):
        """根据操作返回不同的序列化器"""
        if self.action == 'create':
            return DepartmentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return DepartmentUpdateSerializer
        elif self.action == 'tree':
            return DepartmentTreeSerializer
        else:
            return DepartmentSerializer

    def get_permissions(self):
        """根据操作返回不同的权限要求"""
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'tree':
            return [IsAuthenticated(), PermissionRequired(['department:read'])]
        elif self.action == 'create':
            return [IsAuthenticated(), PermissionRequired(['department:create'])]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), PermissionRequired(['department:update'])]
        elif self.action == 'destroy':
            return [IsAuthenticated(), PermissionRequired(['department:delete'])]
        return super().get_permissions()

    @extend_schema(
        tags=['用户'],
        summary='部门列表',
        description='获取部门列表，支持分页、过滤、搜索'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        tags=['用户'],
        summary='部门详情',
        description='获取部门详细信息'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=['用户'],
        summary='创建部门',
        description='创建新部门，需要 department:create 权限'
    )
    def create(self, request, *args, **kwargs):
        """创建部门"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        department = serializer.save()
        
        logger.info(f'部门创建成功: {department.name}', extra={
            'department_id': department.id,
            'department_code': department.code,
            'created_by': request.user.id
        })
        
        return APIResponse.success(
            data=DepartmentSerializer(department).data,
            message=_('部门创建成功'),
            status_code=status.HTTP_201_CREATED
        )

    @extend_schema(
        tags=['用户'],
        summary='更新部门',
        description='更新部门信息，需要 department:update 权限'
    )
    def update(self, request, *args, **kwargs):
        """更新部门"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        department = serializer.save()
        
        logger.info(f'部门更新成功: {department.name}', extra={
            'department_id': department.id,
            'department_code': department.code,
            'updated_by': request.user.id
        })
        
        return APIResponse.success(
            data=DepartmentSerializer(department).data,
            message=_('部门更新成功')
        )

    @extend_schema(
        tags=['用户'],
        summary='部分更新部门',
        description='部分更新部门信息，需要 department:update 权限'
    )
    def partial_update(self, request, *args, **kwargs):
        """部分更新部门"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @extend_schema(
        tags=['用户'],
        summary='删除部门',
        description='软删除部门，需要 department:delete 权限。如果部门下有子部门或用户，则无法删除。'
    )
    def destroy(self, request, *args, **kwargs):
        """删除部门（软删除）"""
        instance = self.get_object()
        
        # 检查是否有子部门
        if instance.children.filter(is_deleted=False).exists():
            raise ValidationException(_('该部门下存在子部门，无法删除'))
        
        # 检查是否有用户
        if instance.members.filter(user__is_active=True).exists():
            raise ValidationException(_('该部门下存在用户，无法删除'))
        
        # 软删除
        instance.is_deleted = True
        instance.save()
        
        logger.info(f'部门删除成功: {instance.name}', extra={
            'department_id': instance.id,
            'department_code': instance.code,
            'deleted_by': request.user.id
        })
        
        return APIResponse.success(message=_('部门删除成功'))

    @extend_schema(
        tags=['用户'],
        summary='部门树形结构',
        description='获取部门树形结构，只返回激活的部门'
    )
    @action(detail=False, methods=['get'], serializer_class=DepartmentTreeSerializer)
    def tree(self, request):
        """获取部门树形结构"""
        # 获取根部门（没有父部门的部门）
        root_departments = Department.objects.filter(
            parent__isnull=True,
            is_deleted=False,
            is_active=True
        ).order_by('sort_order', 'id')
        
        serializer = DepartmentTreeSerializer(root_departments, many=True)
        return APIResponse.success(data=serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    """
    用户管理视图集
    支持用户 CRUD 操作、分页、过滤、搜索
    """
    queryset = User.objects.select_related('profile', 'profile__department').all()
    permission_classes = [IsAuthenticated, UserPermission]
    pagination_class = CustomPageNumberPagination
    filterset_class = UserFilter
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'last_login', 'username']
    ordering = ['-date_joined']

    def get_serializer_class(self):
        """根据操作返回不同的序列化器"""
        if self.action == 'list':
            return UserListSerializer
        elif self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        else:
            return UserDetailSerializer

    def get_queryset(self):
        """获取查询集"""
        queryset = super().get_queryset()
        
        # 非管理员只能看到自己的信息
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            queryset = queryset.filter(pk=self.request.user.pk)
        
        return queryset

    @extend_schema(
        tags=['用户'],
        summary='用户列表',
        description='获取用户列表，支持分页、过滤、搜索。管理员可以看到所有用户，普通用户只能看到自己。',
        responses={
            200: {
                'description': '成功',
                'examples': [
                    OpenApiExample(
                        '成功响应',
                        value={
                            'success': True,
                            'code': 200,
                            'message': '操作成功',
                            'data': {
                                'results': [],
                                'pagination': {
                                    'count': 100,
                                    'page': 1,
                                    'page_size': 20,
                                    'pages': 5
                                }
                            }
                        }
                    )
                ]
            }
        }
    )
    def list(self, request, *args, **kwargs):
        """用户列表"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return APIResponse.success(data=serializer.data)

    @extend_schema(
        tags=['用户'],
        summary='用户详情',
        description='获取用户详细信息。用户可以查看自己的信息，管理员可以查看所有用户信息。'
    )
    def retrieve(self, request, *args, **kwargs):
        """用户详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return APIResponse.success(data=serializer.data)

    @extend_schema(
        tags=['用户'],
        summary='创建用户',
        description='创建新用户。只有管理员可以创建用户。',
        request=UserCreateSerializer,
        responses={
            201: {
                'description': '创建成功',
                'examples': [
                    OpenApiExample(
                        '成功响应',
                        value={
                            'success': True,
                            'code': 201,
                            'message': '用户创建成功',
                            'data': {
                                'id': 1,
                                'username': 'testuser'
                            }
                        }
                    )
                ]
            }
        }
    )
    def create(self, request, *args, **kwargs):
        """创建用户（仅管理员）"""
        if not (request.user.is_staff or request.user.is_superuser):
            raise PermissionException(_('只有管理员可以创建用户'))
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        logger.info(f'用户创建成功: {user.username}', extra={
            'user_id': user.id,
            'username': user.username,
            'created_by': request.user.id
        })
        
        return APIResponse.success(
            data=UserDetailSerializer(user).data,
            message=_('用户创建成功'),
            status_code=status.HTTP_201_CREATED
        )

    @extend_schema(
        tags=['用户'],
        summary='更新用户',
        description='更新用户信息。用户可以更新自己的信息，管理员可以更新所有用户信息。',
        request=UserUpdateSerializer
    )
    def update(self, request, *args, **kwargs):
        """更新用户"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        logger.info(f'用户更新成功: {user.username}', extra={
            'user_id': user.id,
            'username': user.username,
            'updated_by': request.user.id
        })
        
        return APIResponse.success(
            data=UserDetailSerializer(user).data,
            message=_('用户更新成功')
        )

    @extend_schema(
        tags=['用户'],
        summary='部分更新用户',
        description='部分更新用户信息'
    )
    def partial_update(self, request, *args, **kwargs):
        """部分更新用户"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @extend_schema(
        tags=['用户'],
        summary='删除用户',
        description='软删除用户。只有管理员可以删除用户。'
    )
    def destroy(self, request, *args, **kwargs):
        """删除用户（软删除，仅管理员）"""
        if not (request.user.is_staff or request.user.is_superuser):
            raise PermissionException(_('只有管理员可以删除用户'))
        
        instance = self.get_object()
        username = instance.username
        
        # 软删除：设置 is_active=False
        instance.is_active = False
        instance.save()
        
        logger.info(f'用户删除成功: {username}', extra={
            'user_id': instance.id,
            'username': username,
            'deleted_by': request.user.id
        })
        
        return APIResponse.success(message=_('用户删除成功'))

    @extend_schema(
        tags=['用户'],
        summary='获取当前用户信息',
        description='获取当前登录用户的详细信息',
        responses={
            200: {
                'description': '成功',
                'examples': [
                    OpenApiExample(
                        '成功响应',
                        value={
                            'success': True,
                            'code': 200,
                            'message': '操作成功',
                            'data': {
                                'id': 1,
                                'username': 'testuser',
                                'email': 'test@example.com',
                                'profile': {}
                            }
                        }
                    )
                ]
            }
        }
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """获取当前用户信息"""
        serializer = CurrentUserSerializer(request.user)
        return APIResponse.success(data=serializer.data)

    @extend_schema(
        tags=['用户'],
        summary='更新当前用户信息',
        description='更新当前登录用户的信息',
        request=UserUpdateSerializer
    )
    @action(detail=False, methods=['put', 'patch'], permission_classes=[IsAuthenticated])
    def update_me(self, request):
        """更新当前用户信息"""
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        logger.info(f'当前用户更新成功: {user.username}', extra={
            'user_id': user.id,
            'username': user.username
        })
        
        return APIResponse.success(
            data=CurrentUserSerializer(user).data,
            message=_('用户信息更新成功')
        )

    @extend_schema(
        tags=['用户'],
        summary='上传头像',
        description='上传用户头像，支持图片压缩和格式转换',
        request={
            'type': 'object',
            'properties': {
                'avatar': {
                    'type': 'string',
                    'format': 'binary',
                    'description': '头像图片文件'
                }
            },
            'required': ['avatar']
        }
    )
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def upload_avatar(self, request):
        """上传头像"""
        if 'avatar' not in request.FILES:
            from apps.common.exceptions import ValidationException
            raise ValidationException(_('请选择要上传的头像文件'))
        
        avatar_file = request.FILES['avatar']
        
        # 验证文件
        validate_image_file(avatar_file)
        
        # 压缩图片
        compressed_image = compress_image(avatar_file, max_size=(800, 800), quality=85)
        
        # 获取或创建用户扩展信息
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        # 删除旧头像
        if profile.avatar:
            try:
                os.remove(profile.avatar.path)
            except:
                pass
        
        # 保存新头像
        file_name = f"avatar_{request.user.id}_{avatar_file.name}"
        profile.avatar.save(file_name, ContentFile(compressed_image.read()), save=True)
        
        logger.info(f'用户头像上传成功: {request.user.username}', extra={
            'user_id': request.user.id,
            'username': request.user.username,
            'avatar': profile.avatar.name
        })
        
        return APIResponse.success(
            data={'avatar': profile.avatar.url if profile.avatar else None},
            message=_('头像上传成功')
        )

    @extend_schema(
        tags=['用户'],
        summary='激活/禁用用户',
        description='激活或禁用用户。只有管理员可以操作。'
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def toggle_active(self, request, pk=None):
        """激活/禁用用户"""
        if not (request.user.is_staff or request.user.is_superuser):
            raise PermissionException(_('只有管理员可以激活/禁用用户'))
        
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        
        action = _('激活') if user.is_active else _('禁用')
        logger.info(f'用户{action}成功: {user.username}', extra={
            'user_id': user.id,
            'username': user.username,
            'is_active': user.is_active,
            'updated_by': request.user.id
        })
        
        return APIResponse.success(
            data={'is_active': user.is_active},
            message=_('用户{action}成功').format(action=action)
        )

