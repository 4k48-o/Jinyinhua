"""
通用工具函数
整合日期时间、字符串处理、数据验证、文件处理等工具函数
"""
import os
import re
import hashlib
import random
import string
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from io import BytesIO
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from PIL import Image


# ==================== 日期时间工具函数 ====================

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


def get_today_range() -> tuple:
    """
    获取今天的时间范围（00:00:00 到 23:59:59）
    
    Returns:
        tuple: (start_time, end_time) datetime 对象元组
    """
    today = timezone.now().date()
    start = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    end = timezone.make_aware(datetime.combine(today, datetime.max.time()))
    return start, end


def get_week_range() -> tuple:
    """
    获取本周的时间范围（周一到周日）
    
    Returns:
        tuple: (start_time, end_time) datetime 对象元组
    """
    today = timezone.now().date()
    # 获取本周一
    days_since_monday = today.weekday()
    monday = today - timedelta(days=days_since_monday)
    # 获取本周日
    sunday = monday + timedelta(days=6)
    
    start = timezone.make_aware(datetime.combine(monday, datetime.min.time()))
    end = timezone.make_aware(datetime.combine(sunday, datetime.max.time()))
    return start, end


def get_month_range() -> tuple:
    """
    获取本月的时间范围（1号到月末）
    
    Returns:
        tuple: (start_time, end_time) datetime 对象元组
    """
    now = timezone.now()
    # 获取本月第一天
    first_day = datetime(now.year, now.month, 1)
    # 获取下个月第一天，然后减一天得到本月最后一天
    if now.month == 12:
        next_month = datetime(now.year + 1, 1, 1)
    else:
        next_month = datetime(now.year, now.month + 1, 1)
    last_day = next_month - timedelta(days=1)
    
    start = timezone.make_aware(datetime.combine(first_day.date(), datetime.min.time()))
    end = timezone.make_aware(datetime.combine(last_day.date(), datetime.max.time()))
    return start, end


# ==================== 字符串处理工具函数 ====================

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


def truncate_string(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """
    截断字符串
    
    Args:
        text: 原始字符串
        max_length: 最大长度
        suffix: 截断后的后缀
        
    Returns:
        str: 截断后的字符串
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


# ==================== 哈希工具函数 ====================

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


def file_md5(file_path: str) -> str:
    """
    计算文件的 MD5 哈希值
    
    Args:
        file_path: 文件路径
        
    Returns:
        str: MD5 哈希值
    """
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


# ==================== 数据验证工具函数 ====================

def validate_phone(phone: str) -> bool:
    """
    验证手机号格式
    
    Args:
        phone: 手机号字符串
        
    Returns:
        bool: True 表示格式正确
        
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


# ==================== 文件处理工具函数 ====================

def validate_image_file(file, max_size: int = 5 * 1024 * 1024, allowed_types: List[str] = None):
    """
    验证图片文件
    
    Args:
        file: 上传的文件对象
        max_size: 最大文件大小（字节），默认 5MB
        allowed_types: 允许的文件类型列表
        
    Raises:
        ValidationError: 如果文件不符合要求
    """
    if allowed_types is None:
        allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    
    # 检查文件大小
    if file.size > max_size:
        raise ValidationError(_('图片大小不能超过 {}MB').format(max_size // (1024 * 1024)))
    
    # 检查文件类型
    if file.content_type not in allowed_types:
        raise ValidationError(_('只支持 JPEG、PNG、GIF、WebP 格式的图片'))
    
    # 检查文件扩展名
    ext = os.path.splitext(file.name)[1].lower()
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    if ext not in allowed_extensions:
        raise ValidationError(_('只支持 .jpg、.jpeg、.png、.gif、.webp 格式的图片'))


def compress_image(image_file, max_size=(800, 800), quality=85):
    """
    压缩图片
    
    Args:
        image_file: 图片文件对象
        max_size: 最大尺寸 (width, height)
        quality: JPEG 质量 (1-100)
        
    Returns:
        BytesIO: 压缩后的图片数据
        
    Raises:
        ValidationError: 如果处理失败
    """
    try:
        # 打开图片
        img = Image.open(image_file)
        
        # 转换为 RGB（如果是 RGBA）
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # 调整尺寸
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # 保存到内存
        output = BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        
        return output
    except Exception as e:
        raise ValidationError(_('图片处理失败: {}').format(str(e)))


def generate_thumbnail(image_file, size=(200, 200), quality=75):
    """
    生成缩略图
    
    Args:
        image_file: 图片文件对象
        size: 缩略图尺寸 (width, height)
        quality: JPEG 质量 (1-100)
        
    Returns:
        BytesIO: 缩略图数据
        
    Raises:
        ValidationError: 如果处理失败
    """
    try:
        img = Image.open(image_file)
        
        # 转换为 RGB
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # 生成缩略图（保持宽高比）
        img.thumbnail(size, Image.Resampling.LANCZOS)
        
        # 保存到内存
        output = BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        
        return output
    except Exception as e:
        raise ValidationError(_('缩略图生成失败: {}').format(str(e)))


def get_file_extension(filename: str) -> str:
    """
    获取文件扩展名
    
    Args:
        filename: 文件名
        
    Returns:
        str: 文件扩展名（包含点号，如 .jpg）
    """
    return os.path.splitext(filename)[1].lower()


def get_file_size_mb(file_path: str) -> float:
    """
    获取文件大小（MB）
    
    Args:
        file_path: 文件路径
        
    Returns:
        float: 文件大小（MB）
    """
    size_bytes = os.path.getsize(file_path)
    return size_bytes / (1024 * 1024)


def generate_unique_filename(original_filename: str, prefix: str = '') -> str:
    """
    生成唯一文件名
    
    Args:
        original_filename: 原始文件名
        prefix: 文件名前缀
        
    Returns:
        str: 唯一文件名
    """
    ext = get_file_extension(original_filename)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_str = generate_random_string(8)
    filename = f'{prefix}{timestamp}_{random_str}{ext}' if prefix else f'{timestamp}_{random_str}{ext}'
    return filename


# ==================== 其他工具函数 ====================

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

