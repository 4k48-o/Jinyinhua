"""
JWT 工具函数测试
测试 utils/jwt.py 中的 JWT 相关函数
"""
import pytest
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from utils.jwt import (
    create_token_pair,
    get_user_from_token,
    refresh_access_token,
    blacklist_token,
    get_token_payload,
    is_token_expired,
)

User = get_user_model()


@pytest.mark.unit
@pytest.mark.requires_db
class TestCreateTokenPair:
    """创建 Token 对测试"""
    
    def test_create_token_pair_success(self, user):
        """测试成功创建 Token 对"""
        tokens = create_token_pair(user)
        
        assert isinstance(tokens, dict)
        assert 'access' in tokens
        assert 'refresh' in tokens
        assert isinstance(tokens['access'], str)
        assert isinstance(tokens['refresh'], str)
        assert len(tokens['access']) > 0
        assert len(tokens['refresh']) > 0
    
    def test_create_token_pair_different_tokens(self, user):
        """测试每次创建的 Token 不同"""
        tokens1 = create_token_pair(user)
        tokens2 = create_token_pair(user)
        
        # Access Token 应该不同
        assert tokens1['access'] != tokens2['access']
        # Refresh Token 应该不同
        assert tokens1['refresh'] != tokens2['refresh']


@pytest.mark.unit
@pytest.mark.requires_db
class TestGetUserFromToken:
    """从 Token 获取用户测试"""
    
    def test_get_user_from_token_success(self, user):
        """测试成功从 Token 获取用户"""
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        result = get_user_from_token(access_token)
        
        assert result is not None
        assert isinstance(result, User)
        assert result.id == user.id
        assert result.username == user.username
    
    def test_get_user_from_token_invalid(self):
        """测试无效 Token"""
        invalid_token = "invalid.token.here"
        
        result = get_user_from_token(invalid_token)
        
        assert result is None
    
    def test_get_user_from_token_expired(self, user):
        """测试过期 Token"""
        # 创建一个过期的 Token（需要手动设置过期时间）
        # 注意：这在实际中很难测试，因为 Token 过期时间由 SIMPLE_JWT 配置控制
        # 这里主要测试函数能正确处理异常
        invalid_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.invalid.signature"
        
        result = get_user_from_token(invalid_token)
        
        # 应该返回 None 而不是抛出异常
        assert result is None
    
    def test_get_user_from_token_nonexistent_user(self, user):
        """测试 Token 中的用户不存在"""
        # 创建一个 Token，然后删除用户
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        user_id = user.id
        user.delete()
        
        result = get_user_from_token(access_token)
        
        # 用户不存在时应该返回 None
        assert result is None


@pytest.mark.unit
@pytest.mark.requires_db
class TestRefreshAccessToken:
    """刷新 Access Token 测试"""
    
    def test_refresh_access_token_success(self, user):
        """测试成功刷新 Access Token"""
        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        
        result = refresh_access_token(refresh_token)
        
        assert result is not None
        assert isinstance(result, dict)
        assert 'access' in result
        assert isinstance(result['access'], str)
        assert len(result['access']) > 0
    
    def test_refresh_access_token_invalid(self):
        """测试无效的 Refresh Token"""
        invalid_token = "invalid.refresh.token"
        
        result = refresh_access_token(invalid_token)
        
        assert result is None
    
    def test_refresh_access_token_different_access(self, user):
        """测试刷新后 Access Token 不同"""
        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        original_access = str(refresh.access_token)
        
        result = refresh_access_token(refresh_token)
        
        # 新的 Access Token 应该不同
        assert result['access'] != original_access


@pytest.mark.unit
@pytest.mark.requires_db
class TestBlacklistToken:
    """Token 黑名单测试"""
    
    def test_blacklist_token_success(self, user):
        """测试成功将 Token 加入黑名单"""
        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        
        result = blacklist_token(refresh_token)
        
        assert result is True
    
    def test_blacklist_token_invalid(self):
        """测试无效 Token 加入黑名单"""
        invalid_token = "invalid.token"
        
        result = blacklist_token(invalid_token)
        
        # 无效 Token 应该返回 False
        assert result is False
    
    def test_blacklist_token_twice(self, user):
        """测试重复加入黑名单"""
        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        
        # 第一次加入黑名单
        result1 = blacklist_token(refresh_token)
        assert result1 is True
        
        # 第二次加入黑名单（应该失败，因为已经在黑名单中）
        result2 = blacklist_token(refresh_token)
        # 注意：这取决于 rest_framework_simplejwt 的实现
        # 可能返回 True 或 False


@pytest.mark.unit
@pytest.mark.requires_db
class TestGetTokenPayload:
    """获取 Token 载荷测试"""
    
    def test_get_token_payload_success(self, user):
        """测试成功获取 Token 载荷"""
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        payload = get_token_payload(access_token)
        
        assert payload is not None
        assert isinstance(payload, dict)
        assert 'user_id' in payload
        assert payload['user_id'] == user.id
        assert 'exp' in payload
        assert 'iat' in payload
        assert 'jti' in payload
    
    def test_get_token_payload_invalid(self):
        """测试无效 Token 的载荷"""
        invalid_token = "invalid.token"
        
        payload = get_token_payload(invalid_token)
        
        assert payload is None
    
    def test_get_token_payload_user_id(self, user):
        """测试 Token 载荷中的用户 ID"""
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        payload = get_token_payload(access_token)
        
        assert payload['user_id'] == user.id


@pytest.mark.unit
@pytest.mark.requires_db
class TestIsTokenExpired:
    """Token 过期检查测试"""
    
    def test_is_token_expired_valid(self, user):
        """测试有效 Token 未过期"""
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        result = is_token_expired(access_token)
        
        # 新创建的 Token 应该未过期
        assert result is False
    
    def test_is_token_expired_invalid(self):
        """测试无效 Token"""
        invalid_token = "invalid.token"
        
        result = is_token_expired(invalid_token)
        
        # 无效 Token 应该被视为已过期
        assert result is True

