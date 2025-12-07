"""
自定义验证器
提供常用的数据验证函数
"""
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_phone(phone: str) -> bool:
    """
    验证手机号格式
    
    Args:
        phone: 手机号字符串
        
    Returns:
        bool: True 表示格式正确，False 表示格式错误
        
    Raises:
        ValidationError: 如果格式不正确
    """
    # 中国手机号正则：1开头，第二位是3-9，共11位
    pattern = r'^1[3-9]\d{9}$'
    if not re.match(pattern, phone):
        raise ValidationError(_('手机号格式不正确，请输入11位有效手机号'))
    return True


def validate_email(email: str) -> bool:
    """
    验证邮箱格式
    
    Args:
        email: 邮箱字符串
        
    Returns:
        bool: True 表示格式正确
        
    Raises:
        ValidationError: 如果格式不正确
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError(_('邮箱格式不正确'))
    return True


def validate_password_strength(password: str) -> bool:
    """
    验证密码强度
    要求：至少8位，包含大小写字母、数字和特殊字符
    
    Args:
        password: 密码字符串
        
    Returns:
        bool: True 表示密码强度符合要求
        
    Raises:
        ValidationError: 如果密码强度不符合要求
    """
    if len(password) < 8:
        raise ValidationError(_('密码长度至少为8位'))
    
    if not re.search(r'[a-z]', password):
        raise ValidationError(_('密码必须包含小写字母'))
    
    if not re.search(r'[A-Z]', password):
        raise ValidationError(_('密码必须包含大写字母'))
    
    if not re.search(r'\d', password):
        raise ValidationError(_('密码必须包含数字'))
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError(_('密码必须包含特殊字符'))
    
    return True


def validate_username(username: str) -> bool:
    """
    验证用户名格式
    要求：3-20位，只能包含字母、数字、下划线和连字符
    
    Args:
        username: 用户名字符串
        
    Returns:
        bool: True 表示格式正确
        
    Raises:
        ValidationError: 如果格式不正确
    """
    if len(username) < 3 or len(username) > 20:
        raise ValidationError(_('用户名长度必须在3-20位之间'))
    
    pattern = r'^[a-zA-Z0-9_-]+$'
    if not re.match(pattern, username):
        raise ValidationError(_('用户名只能包含字母、数字、下划线和连字符'))
    
    return True


def validate_chinese_name(name: str) -> bool:
    """
    验证中文姓名
    要求：2-10个汉字
    
    Args:
        name: 姓名字符串
        
    Returns:
        bool: True 表示格式正确
        
    Raises:
        ValidationError: 如果格式不正确
    """
    pattern = r'^[\u4e00-\u9fa5]{2,10}$'
    if not re.match(pattern, name):
        raise ValidationError(_('姓名必须是2-10个汉字'))
    return True


def validate_id_card(id_card: str) -> bool:
    """
    验证身份证号格式（18位）
    
    Args:
        id_card: 身份证号字符串
        
    Returns:
        bool: True 表示格式正确
        
    Raises:
        ValidationError: 如果格式不正确
    """
    pattern = r'^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$'
    if not re.match(pattern, id_card):
        raise ValidationError(_('身份证号格式不正确'))
    return True


def validate_url(url: str) -> bool:
    """
    验证 URL 格式
    
    Args:
        url: URL 字符串
        
    Returns:
        bool: True 表示格式正确
        
    Raises:
        ValidationError: 如果格式不正确
    """
    pattern = r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*)?(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?$'
    if not re.match(pattern, url):
        raise ValidationError(_('URL 格式不正确'))
    return True

