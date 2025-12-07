"""
认证 API 测试
"""
import pytest
from django.contrib.auth.models import User
from rest_framework import status


@pytest.mark.django_db
class TestAuthAPI:
    """认证 API 测试"""
    
    def test_register(self, api_client):
        """测试用户注册"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'Test123!@#',
            'password_confirm': 'Test123!@#'
        }
        
        response = api_client.post('/api/v1/auth/register/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
        assert 'access' in data['data']
        assert User.objects.filter(username='newuser').exists()
    
    def test_login(self, api_client, user):
        """测试用户登录"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = api_client.post('/api/v1/auth/login/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
        assert 'access' in data['data']
    
    def test_login_invalid_credentials(self, api_client):
        """测试登录失败（无效凭据）"""
        data = {
            'username': 'nonexistent',
            'password': 'wrongpass'
        }
        
        response = api_client.post('/api/v1/auth/login/', data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is False
    
    def test_refresh_token(self, api_client, token_pair):
        """测试刷新 Token"""
        data = {
            'refresh': token_pair['refresh']
        }
        
        response = api_client.post('/api/v1/auth/refresh/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
        assert 'access' in data['data']
    
    def test_logout(self, authenticated_client, token_pair):
        """测试用户登出"""
        data = {
            'refresh': token_pair['refresh']
        }
        
        response = authenticated_client.post('/api/v1/auth/logout/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
    
    def test_get_captcha(self, api_client):
        """测试获取验证码"""
        response = api_client.get('/api/v1/auth/captcha/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json() if hasattr(response, 'json') else response.data
        assert data['success'] is True
        assert 'captcha' in data['data']

