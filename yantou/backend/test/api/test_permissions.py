"""
权限管理 API 测试
"""
import pytest
from django.contrib.auth.models import User
from rest_framework import status
from apps.permissions.models import Role, Permission, UserRole, RolePermission


@pytest.mark.django_db
class TestRoleViewSet:
    """角色视图集测试"""
    
    def test_list_roles_as_admin(self, admin_client):
        """测试管理员查看角色列表"""
        Role.objects.create(name='测试角色', code='test_role', description='测试')
        
        response = admin_client.get('/api/v1/roles/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
    
    def test_list_roles_as_user(self, authenticated_client):
        """测试普通用户查看角色列表（应该被拒绝）"""
        response = authenticated_client.get('/api/v1/roles/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_create_role(self, admin_client):
        """测试创建角色"""
        permission = Permission.objects.create(
            name='测试权限',
            code='test:permission',
            content_type='test',
            action='read'
        )
        
        data = {
            'name': '新角色',
            'code': 'new_role',
            'description': '新角色描述',
            'permission_ids': [permission.id]
        }
        
        response = admin_client.post('/api/v1/roles/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
        assert Role.objects.filter(code='new_role').exists()
    
    def test_retrieve_role(self, admin_client):
        """测试获取角色详情"""
        role = Role.objects.create(name='测试角色', code='test_role')
        
        response = admin_client.get(f'/api/v1/roles/{role.id}/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
        assert data['data']['name'] == '测试角色'
    
    def test_update_role(self, admin_client):
        """测试更新角色"""
        role = Role.objects.create(name='测试角色', code='test_role')
        
        data = {
            'name': '更新后的角色',
            'description': '更新描述'
        }
        
        response = admin_client.patch(f'/api/v1/roles/{role.id}/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
        
        role.refresh_from_db()
        assert role.name == '更新后的角色'
    
    def test_delete_role(self, admin_client):
        """测试删除角色（软删除）"""
        role = Role.objects.create(name='测试角色', code='test_role', is_system=False)
        
        response = admin_client.delete(f'/api/v1/roles/{role.id}/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
        
        role.refresh_from_db()
        assert role.is_deleted is True
    
    def test_delete_system_role(self, admin_client):
        """测试删除系统角色（应该被拒绝）"""
        role = Role.objects.create(name='系统角色', code='system_role', is_system=True)
        
        response = admin_client.delete(f'/api/v1/roles/{role.id}/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserRoleViewSet:
    """用户角色管理视图集测试"""
    
    def test_assign_role(self, admin_client, user):
        """测试分配角色"""
        role = Role.objects.create(name='测试角色', code='test_role')
        
        data = {
            'user': user.id,
            'role': role.id
        }
        
        response = admin_client.post('/api/v1/user-roles/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
        assert UserRole.objects.filter(user=user, role=role).exists()
    
    def test_list_user_roles(self, admin_client, user):
        """测试获取用户角色列表"""
        role = Role.objects.create(name='测试角色', code='test_role')
        UserRole.objects.create(user=user, role=role)
        
        response = admin_client.get('/api/v1/user-roles/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
    
    def test_remove_role(self, admin_client, user):
        """测试移除角色"""
        role = Role.objects.create(name='测试角色', code='test_role')
        user_role = UserRole.objects.create(user=user, role=role)
        
        response = admin_client.delete(f'/api/v1/user-roles/{user_role.id}/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
        assert not UserRole.objects.filter(id=user_role.id).exists()
    
    def test_get_user_roles(self, admin_client, user):
        """测试获取指定用户的角色列表"""
        role = Role.objects.create(name='测试角色', code='test_role')
        UserRole.objects.create(user=user, role=role)
        
        response = admin_client.get(f'/api/v1/user-roles/user/{user.id}/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
        assert len(data['data']) > 0


@pytest.mark.django_db
class TestPermissionViewSet:
    """权限视图集测试"""
    
    def test_list_permissions(self, authenticated_client):
        """测试获取权限列表"""
        Permission.objects.create(
            name='测试权限',
            code='test:permission',
            content_type='test',
            action='read'
        )
        
        response = authenticated_client.get('/api/v1/permissions/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
    
    def test_permission_tree(self, authenticated_client):
        """测试获取权限树形结构"""
        parent = Permission.objects.create(
            name='父权限',
            code='parent:permission',
            content_type='test',
            action='read'
        )
        Permission.objects.create(
            name='子权限',
            code='child:permission',
            content_type='test',
            action='read',
            parent=parent
        )
        
        response = authenticated_client.get('/api/v1/permissions/tree/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True


@pytest.mark.django_db
class TestPermissionCheckViewSet:
    """权限检查视图集测试"""
    
    def test_my_permissions(self, authenticated_client, user):
        """测试获取当前用户权限"""
        permission = Permission.objects.create(
            name='测试权限',
            code='test:permission',
            content_type='test',
            action='read'
        )
        role = Role.objects.create(name='测试角色', code='test_role')
        RolePermission.objects.create(role=role, permission=permission)
        UserRole.objects.create(user=user, role=role)
        
        response = authenticated_client.get('/api/v1/permission-check/my_permissions/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
    
    def test_my_roles(self, authenticated_client, user):
        """测试获取当前用户角色"""
        role = Role.objects.create(name='测试角色', code='test_role')
        UserRole.objects.create(user=user, role=role)
        
        response = authenticated_client.get('/api/v1/permission-check/my_roles/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
    
    def test_check_permission(self, authenticated_client, user):
        """测试检查权限"""
        permission = Permission.objects.create(
            name='测试权限',
            code='test:permission',
            content_type='test',
            action='read'
        )
        role = Role.objects.create(name='测试角色', code='test_role')
        RolePermission.objects.create(role=role, permission=permission)
        UserRole.objects.create(user=user, role=role)
        
        response = authenticated_client.get('/api/v1/permission-check/check_permission/?permission_code=test:permission')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
        assert data['data']['has_permission'] is True
    
    def test_check_role(self, authenticated_client, user):
        """测试检查角色"""
        role = Role.objects.create(name='测试角色', code='test_role')
        UserRole.objects.create(user=user, role=role)
        
        response = authenticated_client.get('/api/v1/permission-check/check_role/?role_code=test_role')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
        assert data['data']['has_role'] is True

