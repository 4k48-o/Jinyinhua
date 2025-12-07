"""
辅助函数
提供常用的辅助工具函数
"""
import hashlib
import random
import string
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from django.utils import timezone
from django.core.cache import cache


def generate_random_string(length: int = 32, include_special: bool = False) -> str:
    """
    生成随机字符串
    
    Args:
        length: 字符串长度
        include_special: 是否包含特殊字符
        
    Returns:
        str: 随机字符串
    """
    chars = string.ascii_letters + string.digits
    if include_special:
        chars += string.punctuation
    
    return ''.join(random.choice(chars) for _ in range(length))


def generate_code(length: int = 6) -> str:
    """
    生成数字验证码
    
    Args:
        length: 验证码长度
        
    Returns:
        str: 数字验证码
    """
    return ''.join(random.choice(string.digits) for _ in range(length))


def md5_hash(text: str) -> str:
    """
    计算字符串的 MD5 哈希值
    
    Args:
        text: 要哈希的字符串
        
    Returns:
        str: MD5 哈希值（32位十六进制字符串）
    """
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def sha256_hash(text: str) -> str:
    """
    计算字符串的 SHA256 哈希值
    
    Args:
        text: 要哈希的字符串
        
    Returns:
        str: SHA256 哈希值（64位十六进制字符串）
    """
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def format_datetime(dt: datetime, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    格式化日期时间
    
    Args:
        dt: datetime 对象
        format_str: 格式字符串
        
    Returns:
        str: 格式化后的日期时间字符串
    """
    if dt is None:
        return ''
    if timezone.is_aware(dt):
        dt = timezone.localtime(dt)
    return dt.strftime(format_str)


def parse_datetime(dt_str: str, format_str: str = '%Y-%m-%d %H:%M:%S') -> Optional[datetime]:
    """
    解析日期时间字符串
    
    Args:
        dt_str: 日期时间字符串
        format_str: 格式字符串
        
    Returns:
        datetime 对象，如果解析失败则返回 None
    """
    try:
        return datetime.strptime(dt_str, format_str)
    except (ValueError, TypeError):
        return None


def get_time_range(days: int = 0, hours: int = 0, minutes: int = 0) -> tuple:
    """
    获取时间范围（开始时间和结束时间）
    
    Args:
        days: 天数偏移
        hours: 小时偏移
        minutes: 分钟偏移
        
    Returns:
        tuple: (start_time, end_time) datetime 对象元组
    """
    now = timezone.now()
    start = now - timedelta(days=days, hours=hours, minutes=minutes)
    end = now
    return start, end


def paginate_queryset(queryset, page: int = 1, page_size: int = 20):
    """
    分页查询集（简单实现）
    
    Args:
        queryset: Django QuerySet
        page: 页码（从1开始）
        page_size: 每页数量
        
    Returns:
        dict: 包含分页信息的字典
        {
            'results': [...],  # 当前页数据
            'count': 100,      # 总数量
            'page': 1,         # 当前页码
            'page_size': 20,   # 每页数量
            'total_pages': 5   # 总页数
        }
    """
    count = queryset.count()
    total_pages = (count + page_size - 1) // page_size if count > 0 else 0
    offset = (page - 1) * page_size
    
    results = list(queryset[offset:offset + page_size])
    
    return {
        'results': results,
        'count': count,
        'page': page,
        'page_size': page_size,
        'total_pages': total_pages,
    }


def get_client_ip(request) -> str:
    """
    获取客户端 IP 地址
    
    Args:
        request: Django Request 对象
        
    Returns:
        str: IP 地址
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', 'unknown')
    return ip


def mask_sensitive_data(data: str, start: int = 0, end: int = 4, mask_char: str = '*') -> str:
    """
    掩码敏感数据（如手机号、身份证号等）
    
    Args:
        data: 原始数据
        start: 保留开始位数
        end: 保留结束位数
        mask_char: 掩码字符
        
    Returns:
        str: 掩码后的数据
    """
    if not data or len(data) <= start + end:
        return data
    
    return data[:start] + mask_char * (len(data) - start - end) + data[-end:]


def mask_phone(phone: str) -> str:
    """
    掩码手机号（显示前3位和后4位）
    
    Args:
        phone: 手机号
        
    Returns:
        str: 掩码后的手机号，如：138****5678
    """
    return mask_sensitive_data(phone, start=3, end=4)


def mask_email(email: str) -> str:
    """
    掩码邮箱（显示@前的前3位和@后的域名）
    
    Args:
        email: 邮箱地址
        
    Returns:
        str: 掩码后的邮箱，如：abc***@example.com
    """
    if '@' not in email:
        return email
    
    local, domain = email.split('@', 1)
    if len(local) <= 3:
        masked_local = local[0] + '*' * (len(local) - 1)
    else:
        masked_local = local[:3] + '*' * (len(local) - 3)
    
    return f'{masked_local}@{domain}'


def safe_int(value: Any, default: int = 0) -> int:
    """
    安全转换为整数
    
    Args:
        value: 要转换的值
        default: 转换失败时的默认值
        
    Returns:
        int: 转换后的整数
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value: Any, default: float = 0.0) -> float:
    """
    安全转换为浮点数
    
    Args:
        value: 要转换的值
        default: 转换失败时的默认值
        
    Returns:
        float: 转换后的浮点数
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """
    将列表分割成指定大小的块
    
    Args:
        lst: 要分割的列表
        chunk_size: 每块的大小
        
    Returns:
        List[List]: 分割后的列表
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def get_cache_key(prefix: str, *args, **kwargs) -> str:
    """
    生成缓存键
    
    Args:
        prefix: 前缀
        *args: 位置参数
        **kwargs: 关键字参数
        
    Returns:
        str: 缓存键
    """
    key_parts = [prefix]
    key_parts.extend(str(arg) for arg in args)
    key_parts.extend(f'{k}:{v}' for k, v in sorted(kwargs.items()))
    return ':'.join(key_parts)

