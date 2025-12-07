"""
认证安全增强模块
实现登录失败次数限制、IP 白名单/黑名单、验证码、设备指纹识别等功能
"""
import hashlib
import time
import random
import string
import base64
import io
from typing import Optional, Dict, Any, Tuple
from django.core.cache import cache
from django.conf import settings
from apps.common.exceptions import RateLimitException, AuthenticationException
from PIL import Image, ImageDraw, ImageFont
import logging

logger = logging.getLogger('django.request')


class LoginAttemptLimiter:
    """
    登录失败次数限制器
    使用 Redis 记录登录失败次数，防止暴力破解
    """
    
    def __init__(
        self,
        max_attempts: int = 5,
        lockout_duration: int = 900,  # 15 分钟
        window_duration: int = 3600,  # 1 小时
    ):
        """
        初始化登录限制器
        
        Args:
            max_attempts: 最大失败次数
            lockout_duration: 锁定持续时间（秒）
            window_duration: 时间窗口（秒）
        """
        self.max_attempts = max_attempts
        self.lockout_duration = lockout_duration
        self.window_duration = window_duration
    
    def get_cache_key(self, identifier: str) -> str:
        """
        获取缓存键
        
        Args:
            identifier: 标识符（用户名或 IP）
            
        Returns:
            str: 缓存键
        """
        return f'login_attempts:{identifier}'
    
    def record_failure(self, identifier: str) -> Dict[str, Any]:
        """
        记录登录失败
        
        Args:
            identifier: 标识符（用户名或 IP）
            
        Returns:
            dict: 包含失败次数和剩余锁定时间的信息
        """
        cache_key = self.get_cache_key(identifier)
        attempts_data = cache.get(cache_key, {'count': 0, 'first_attempt': time.time()})
        
        attempts_data['count'] += 1
        attempts_data['last_attempt'] = time.time()
        
        # 如果超过时间窗口，重置计数
        if time.time() - attempts_data['first_attempt'] > self.window_duration:
            attempts_data = {'count': 1, 'first_attempt': time.time(), 'last_attempt': time.time()}
        
        # 计算剩余锁定时间
        remaining_lockout = 0
        if attempts_data['count'] >= self.max_attempts:
            remaining_lockout = self.lockout_duration - (time.time() - attempts_data['last_attempt'])
            if remaining_lockout < 0:
                remaining_lockout = 0
        
        # 保存到缓存
        cache.set(cache_key, attempts_data, timeout=self.window_duration)
        
        return {
            'count': attempts_data['count'],
            'remaining_lockout': max(0, int(remaining_lockout)),
            'is_locked': attempts_data['count'] >= self.max_attempts,
        }
    
    def record_success(self, identifier: str):
        """
        记录登录成功，清除失败记录
        
        Args:
            identifier: 标识符（用户名或 IP）
        """
        cache_key = self.get_cache_key(identifier)
        cache.delete(cache_key)
    
    def check_lockout(self, identifier: str) -> bool:
        """
        检查是否被锁定
        
        Args:
            identifier: 标识符（用户名或 IP）
            
        Returns:
            bool: True 表示被锁定，False 表示未锁定
        """
        cache_key = self.get_cache_key(identifier)
        attempts_data = cache.get(cache_key)
        
        if not attempts_data:
            return False
        
        # 检查是否超过时间窗口
        if time.time() - attempts_data['first_attempt'] > self.window_duration:
            cache.delete(cache_key)
            return False
        
        # 检查是否达到最大失败次数
        if attempts_data['count'] >= self.max_attempts:
            # 检查锁定时间是否已过
            if time.time() - attempts_data['last_attempt'] < self.lockout_duration:
                return True
            else:
                # 锁定时间已过，清除记录
                cache.delete(cache_key)
                return False
        
        return False
    
    def get_remaining_attempts(self, identifier: str) -> int:
        """
        获取剩余尝试次数
        
        Args:
            identifier: 标识符（用户名或 IP）
            
        Returns:
            int: 剩余尝试次数
        """
        cache_key = self.get_cache_key(identifier)
        attempts_data = cache.get(cache_key)
        
        if not attempts_data:
            return self.max_attempts
        
        # 检查是否超过时间窗口
        if time.time() - attempts_data['first_attempt'] > self.window_duration:
            return self.max_attempts
        
        remaining = self.max_attempts - attempts_data['count']
        return max(0, remaining)


class IPWhitelistBlacklist:
    """
    IP 白名单/黑名单管理器
    """
    
    def __init__(self):
        """初始化 IP 管理器"""
        self.whitelist_key = 'ip_whitelist'
        self.blacklist_key = 'ip_blacklist'
    
    def get_client_ip(self, request) -> str:
        """
        获取客户端 IP 地址
        
        Args:
            request: Django 请求对象
            
        Returns:
            str: 客户端 IP 地址
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'unknown')
        return ip
    
    def is_whitelisted(self, ip: str) -> bool:
        """
        检查 IP 是否在白名单中
        
        Args:
            ip: IP 地址
            
        Returns:
            bool: True 表示在白名单中
        """
        whitelist = cache.get(self.whitelist_key, set())
        return ip in whitelist
    
    def is_blacklisted(self, ip: str) -> bool:
        """
        检查 IP 是否在黑名单中
        
        Args:
            ip: IP 地址
            
        Returns:
            bool: True 表示在黑名单中
        """
        blacklist = cache.get(self.blacklist_key, set())
        return ip in blacklist
    
    def add_to_whitelist(self, ip: str):
        """
        添加 IP 到白名单
        
        Args:
            ip: IP 地址
        """
        whitelist = cache.get(self.whitelist_key, set())
        whitelist.add(ip)
        cache.set(self.whitelist_key, whitelist, timeout=None)
    
    def add_to_blacklist(self, ip: str, duration: int = 3600):
        """
        添加 IP 到黑名单
        
        Args:
            ip: IP 地址
            duration: 黑名单持续时间（秒），None 表示永久
        """
        blacklist = cache.get(self.blacklist_key, set())
        blacklist.add(ip)
        if duration:
            cache.set(self.blacklist_key, blacklist, timeout=duration)
        else:
            cache.set(self.blacklist_key, blacklist, timeout=None)
    
    def remove_from_whitelist(self, ip: str):
        """
        从白名单中移除 IP
        
        Args:
            ip: IP 地址
        """
        whitelist = cache.get(self.whitelist_key, set())
        whitelist.discard(ip)
        cache.set(self.whitelist_key, whitelist, timeout=None)
    
    def remove_from_blacklist(self, ip: str):
        """
        从黑名单中移除 IP
        
        Args:
            ip: IP 地址
        """
        blacklist = cache.get(self.blacklist_key, set())
        blacklist.discard(ip)
        cache.set(self.blacklist_key, blacklist, timeout=None)


class CaptchaGenerator:
    """
    验证码生成器
    生成图片验证码（base64 格式）
    """
    
    @staticmethod
    def generate(length: int = 4) -> Tuple[str, str]:
        """
        生成验证码图片
        
        Args:
            length: 验证码长度
            
        Returns:
            tuple: (验证码字符串, base64 图片数据)
        """
        # 生成验证码字符串
        captcha_text = ''.join(random.choices(string.digits, k=length))
        
        # 创建图片
        width, height = 120, 40
        image = Image.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        # 尝试使用系统字体，如果失败则使用默认字体
        try:
            font = ImageFont.truetype('/System/Library/Fonts/Arial.ttf', 24)
        except:
            try:
                font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)
            except:
                font = ImageFont.load_default()
        
        # 绘制验证码文字
        text_width = draw.textlength(captcha_text, font=font)
        x = (width - text_width) / 2
        y = (height - 24) / 2
        
        # 添加一些干扰线
        for _ in range(3):
            start = (random.randint(0, width), random.randint(0, height))
            end = (random.randint(0, width), random.randint(0, height))
            draw.line([start, end], fill=(random.randint(100, 200), random.randint(100, 200), random.randint(100, 200)), width=1)
        
        # 绘制文字
        draw.text((x, y), captcha_text, fill=(0, 0, 0), font=font)
        
        # 添加一些干扰点
        for _ in range(20):
            x_point = random.randint(0, width)
            y_point = random.randint(0, height)
            draw.point((x_point, y_point), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        
        # 转换为 base64
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        image_data = buffer.getvalue()
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        return captcha_text, f'data:image/png;base64,{base64_image}'
    
    @staticmethod
    def store_captcha(captcha: str, identifier: str, duration: int = 300):
        """
        存储验证码到缓存
        
        Args:
            captcha: 验证码
            identifier: 标识符（IP 或用户名）
            duration: 过期时间（秒）
        """
        cache_key = f'captcha:{identifier}'
        cache.set(cache_key, captcha.lower(), timeout=duration)
    
    @staticmethod
    def verify_captcha(captcha: str, identifier: str) -> bool:
        """
        验证验证码
        
        Args:
            captcha: 用户输入的验证码
            identifier: 标识符（IP 或用户名）
            
        Returns:
            bool: True 表示验证通过
        """
        cache_key = f'captcha:{identifier}'
        stored_captcha = cache.get(cache_key)
        
        if not stored_captcha:
            return False
        
        # 验证后删除验证码（一次性使用）
        cache.delete(cache_key)
        
        return captcha.lower() == stored_captcha


class DeviceFingerprint:
    """
    设备指纹识别
    从请求头中提取设备信息并生成设备指纹
    """
    
    @staticmethod
    def get_device_info(request) -> Dict[str, Any]:
        """
        获取设备信息
        
        Args:
            request: Django 请求对象
            
        Returns:
            dict: 设备信息
        """
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
        accept_encoding = request.META.get('HTTP_ACCEPT_ENCODING', '')
        
        # 获取 IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'unknown')
        
        return {
            'user_agent': user_agent,
            'accept_language': accept_language,
            'accept_encoding': accept_encoding,
            'ip': ip,
        }
    
    @staticmethod
    def generate_fingerprint(request) -> str:
        """
        生成设备指纹
        
        Args:
            request: Django 请求对象
            
        Returns:
            str: 设备指纹（MD5 哈希）
        """
        device_info = DeviceFingerprint.get_device_info(request)
        
        # 组合设备信息
        fingerprint_string = (
            f"{device_info['user_agent']}"
            f"|{device_info['accept_language']}"
            f"|{device_info['accept_encoding']}"
        )
        
        # 生成 MD5 哈希
        fingerprint = hashlib.md5(fingerprint_string.encode()).hexdigest()
        
        return fingerprint
    
    @staticmethod
    def store_device_fingerprint(user_id: int, fingerprint: str):
        """
        存储用户设备指纹
        
        Args:
            user_id: 用户 ID
            fingerprint: 设备指纹
        """
        cache_key = f'user_device:{user_id}'
        devices = cache.get(cache_key, set())
        devices.add(fingerprint)
        # 最多保存 10 个设备
        if len(devices) > 10:
            devices = set(list(devices)[-10:])
        cache.set(cache_key, devices, timeout=86400 * 30)  # 30 天
    
    @staticmethod
    def is_known_device(user_id: int, fingerprint: str) -> bool:
        """
        检查设备是否为已知设备
        
        Args:
            user_id: 用户 ID
            fingerprint: 设备指纹
            
        Returns:
            bool: True 表示是已知设备
        """
        cache_key = f'user_device:{user_id}'
        devices = cache.get(cache_key, set())
        return fingerprint in devices

