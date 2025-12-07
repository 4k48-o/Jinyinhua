"""
用户管理 API 测试
"""
import pytest
from django.contrib.auth.models import User
from rest_framework import status
from apps.users.models import UserProfile, Department


@pytest.mark.django_db
class TestUserViewSet:
    """用户视图集测试"""
    
    def test_list_users_as_admin(self, admin_client):
        """测试管理员查看用户列表"""
        # 创建测试用户
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='Test123!@#'
        )
        
        response = admin_client.get('/api/v1/users/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
        assert 'data' in data
    
    def test_list_users_as_user(self, authenticated_client):
        """测试普通用户查看用户列表（只能看到自己）"""
        response = authenticated_client.get('/api/v1/users/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True
    
    def test_create_user_as_admin(self, admin_client):
        """测试管理员创建用户"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'Test123!@#',
            'password_confirm': 'Test123!@#',
            'first_name': 'New',
            'last_name': 'User',
            'is_active': True
        }
        
        response = admin_client.post('/api/v1/users/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
        assert User.objects.filter(username='newuser').exists()
    
    def test_create_user_as_user(self, authenticated_client):
        """测试普通用户创建用户（应该被拒绝）"""
        data = {
            'username': 'newuser2',
            'email': 'newuser2@example.com',
            'password': 'Test123!@#',
            'password_confirm': 'Test123!@#',
        }
        
        response = authenticated_client.post('/api/v1/users/', data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_retrieve_user(self, admin_client, user):
        """测试获取用户详情"""
        response = admin_client.get(f'/api/v1/users/{user.id}/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
        assert data['data']['id'] == user.id
    
    def test_update_user(self, admin_client, user):
        """测试更新用户"""
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com'
        }
        
        response = admin_client.patch(f'/api/v1/users/{user.id}/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
        
        user.refresh_from_db()
        assert user.first_name == 'Updated'
    
    def test_delete_user(self, admin_client, user):
        """测试删除用户（软删除）"""
        response = admin_client.delete(f'/api/v1/users/{user.id}/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
        
        user.refresh_from_db()
        assert user.is_active is False
    
    def test_get_current_user(self, authenticated_client, user):
        """测试获取当前用户信息"""
        response = authenticated_client.get('/api/v1/users/me/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
        assert data['data']['id'] == user.id
    
    def test_update_current_user(self, authenticated_client, user):
        """测试更新当前用户信息"""
        data = {
            'first_name': 'My',
            'last_name': 'Name'
        }
        
        response = authenticated_client.put('/api/v1/users/me/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
        
        user.refresh_from_db()
        assert user.first_name == 'My'


@pytest.mark.django_db
class TestDepartmentViewSet:
    """部门视图集测试"""
    
    def test_list_departments(self, authenticated_client):
        """测试获取部门列表"""
        Department.objects.create(name='技术部', code='tech')
        Department.objects.create(name='市场部', code='market')
        
        response = authenticated_client.get('/api/v1/departments/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
    
    def test_create_department(self, authenticated_client):
        """测试创建部门"""
        data = {
            'name': '研发部',
            'code': 'rd',
            'description': '研发部门'
        }
        
        response = authenticated_client.post('/api/v1/departments/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
        assert Department.objects.filter(code='rd').exists()
    
    def test_retrieve_department(self, authenticated_client):
        """测试获取部门详情"""
        dept = Department.objects.create(name='技术部', code='tech')
        
        response = authenticated_client.get(f'/api/v1/departments/{dept.id}/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
        assert data['data']['name'] == '技术部'

