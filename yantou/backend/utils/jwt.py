"""
JWT 工具函数
提供 JWT Token 相关的工具函数
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import get_user_model

User = get_user_model()


def create_token_pair(user) -> Dict[str, str]:
    """
    为用户创建 JWT Token 对（Access Token 和 Refresh Token）
    
    Args:
        user: 用户对象
        
    Returns:
        dict: 包含 access 和 refresh token 的字典
        {
            'access': 'access_token_string',
            'refresh': 'refresh_token_string'
        }
    """
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }


def get_user_from_token(token: str) -> Optional[User]:
    """
    从 Access Token 中获取用户对象
    
    Args:
        token: Access Token 字符串
        
    Returns:
        User 对象，如果 token 无效则返回 None
    """
    try:
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        return User.objects.get(id=user_id)
    except (TokenError, User.DoesNotExist, KeyError):
        return None


def refresh_access_token(refresh_token: str) -> Optional[Dict[str, str]]:
    """
    使用 Refresh Token 刷新 Access Token
    
    Args:
        refresh_token: Refresh Token 字符串
        
    Returns:
        dict: 包含新的 access token 的字典，如果 token 无效则返回 None
        {
            'access': 'new_access_token_string'
        }
    """
    try:
        refresh = RefreshToken(refresh_token)
        return {
            'access': str(refresh.access_token),
        }
    except TokenError:
        return None


def blacklist_token(refresh_token: str) -> bool:
    """
    将 Refresh Token 加入黑名单（登出时使用）
    
    Args:
        refresh_token: Refresh Token 字符串
        
    Returns:
        bool: 是否成功加入黑名单
    """
    try:
        refresh = RefreshToken(refresh_token)
        refresh.blacklist()
        return True
    except TokenError:
        return False


def get_token_payload(token: str) -> Optional[Dict[str, Any]]:
    """
    获取 Token 的载荷信息（不验证 token 有效性）
    
    Args:
        token: Token 字符串
        
    Returns:
        dict: Token 载荷信息，如果解析失败则返回 None
    """
    try:
        access_token = AccessToken(token)
        return {
            'user_id': access_token.get('user_id'),
            'exp': access_token.get('exp'),
            'iat': access_token.get('iat'),
            'jti': access_token.get('jti'),
        }
    except TokenError:
        return None


def is_token_expired(token: str) -> bool:
    """
    检查 Token 是否已过期
    
    Args:
        token: Token 字符串
        
    Returns:
        bool: True 表示已过期，False 表示未过期或无效
    """
    try:
        access_token = AccessToken(token)
        exp = access_token.get('exp')
        if exp:
            exp_datetime = datetime.fromtimestamp(exp)
            return datetime.now() > exp_datetime
        return True
    except TokenError:
        return True

