"""
pytest 配置文件
提供全局的 fixtures 和测试配置
"""
import pytest
import os
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

# 设置测试环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.testing')

User = get_user_model()


@pytest.fixture(scope='function')
def api_client():
    """
    API 客户端 Fixture
    提供未认证的 API 客户端
    """
    return APIClient()


@pytest.fixture(scope='function')
def user(db):
    """
    测试用户 Fixture
    创建一个普通测试用户
    """
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User',
        is_active=True,
    )


@pytest.fixture(scope='function')
def admin_user(db):
    """
    管理员用户 Fixture
    创建一个管理员用户
    """
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123',
        first_name='Admin',
        last_name='User',
    )


@pytest.fixture(scope='function')
def authenticated_client(api_client, user):
    """
    已认证的 API 客户端 Fixture
    使用 JWT Token 认证
    """
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.fixture(scope='function')
def admin_client(api_client, admin_user):
    """
    管理员 API 客户端 Fixture
    使用管理员 JWT Token 认证
    """
    refresh = RefreshToken.for_user(admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.fixture(scope='function')
def token_pair(user):
    """
    JWT Token 对 Fixture
    返回 access 和 refresh token
    """
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }


@pytest.fixture(scope='function')
def admin_token_pair(admin_user):
    """
    管理员 JWT Token 对 Fixture
    """
    refresh = RefreshToken.for_user(admin_user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    自动为所有测试启用数据库访问
    """
    pass


@pytest.fixture(scope='function')
def mock_redis(monkeypatch):
    """
    Mock Redis Fixture
    用于不需要真实 Redis 连接的测试
    """
    from unittest.mock import MagicMock
    
    mock_cache = MagicMock()
    mock_cache.get.return_value = None
    mock_cache.set.return_value = True
    mock_cache.delete.return_value = True
    mock_cache.has_key.return_value = False
    
    monkeypatch.setattr('django.core.cache.cache', mock_cache)
    return mock_cache

