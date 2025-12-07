"""
认证序列化器
处理用户注册、登录、Token 刷新等操作
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from apps.common.exceptions import ValidationException, AuthenticationException, RateLimitException
from utils.validators import validate_username, validate_password_strength

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    """
    用户注册序列化器
    前期只支持用户名和密码注册，不包含邮箱和手机号
    """
    username = serializers.CharField(
        max_length=150,
        min_length=3,
        help_text=_('用户名，3-150个字符')
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text=_('密码，至少8个字符')
    )
    password_confirm = serializers.CharField(
        write_only=True,
        help_text=_('确认密码')
    )
    
    def validate_username(self, value):
        """
        验证用户名
        
        Args:
            value: 用户名
            
        Returns:
            str: 验证后的用户名
            
        Raises:
            ValidationException: 如果用户名不符合要求
        """
        # 使用工具函数验证用户名格式
        try:
            validate_username(value)
        except Exception as e:
            raise ValidationException(str(e), code='E001001')
        
        # 检查用户名是否已存在
        if User.objects.filter(username=value).exists():
            raise ValidationException(_('用户名已存在'), code='E030601')
        
        return value
    
    def validate_password(self, value):
        """
        验证密码强度
        
        Args:
            value: 密码
            
        Returns:
            str: 验证后的密码
            
        Raises:
            ValidationException: 如果密码不符合要求
        """
        # 使用 Django 内置密码验证器
        try:
            validate_password(value)
        except Exception as e:
            error_messages = [str(msg) for msg in e.messages]
            raise ValidationException('; '.join(error_messages), code='E001001')
        
        # 使用自定义密码强度验证
        try:
            validate_password_strength(value)
        except Exception as e:
            raise ValidationException(str(e), code='E001001')
        
        return value
    
    def validate(self, attrs):
        """
        验证密码确认
        
        Args:
            attrs: 序列化器数据
            
        Returns:
            dict: 验证后的数据
            
        Raises:
            ValidationException: 如果密码不匹配
        """
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        
        if password != password_confirm:
            raise ValidationException(_('两次输入的密码不一致'), code='E001001')
        
        return attrs
    
    def create(self, validated_data):
        """
        创建用户
        
        Args:
            validated_data: 验证后的数据
            
        Returns:
            User: 创建的用户对象
        """
        username = validated_data['username']
        password = validated_data['password']
        
        # 创建用户
        user = User.objects.create_user(
            username=username,
            password=password,
            is_active=True,  # 前期不需要邮箱激活，直接激活
        )
        
        return user


class LoginSerializer(serializers.Serializer):
    """
    用户登录序列化器
    前期只支持用户名登录，不包含邮箱和手机号
    """
    username = serializers.CharField(
        help_text=_('用户名')
    )
    password = serializers.CharField(
        write_only=True,
        help_text=_('密码')
    )
    captcha = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text=_('验证码（登录失败次数过多时需要）')
    )
    
    def validate(self, attrs):
        """
        验证用户登录信息
        
        Args:
            attrs: 序列化器数据
            
        Returns:
            dict: 验证后的数据，包含 user 对象
            
        Raises:
            AuthenticationException: 如果认证失败
        """
        from .security import LoginAttemptLimiter, IPWhitelistBlacklist, CaptchaGenerator
        
        username = attrs.get('username')
        password = attrs.get('password')
        captcha = attrs.get('captcha', '')
        request = self.context.get('request')
        
        if not username or not password:
            raise AuthenticationException(_('用户名和密码不能为空'), code='E002001')
        
        # 获取客户端 IP
        ip_manager = IPWhitelistBlacklist()
        client_ip = ip_manager.get_client_ip(request)
        
        # 检查 IP 黑名单
        if ip_manager.is_blacklisted(client_ip):
            raise AuthenticationException(_('IP 地址已被封禁'), code='E002001')
        
        # 检查登录失败次数限制
        limiter = LoginAttemptLimiter()
        identifier = f"{client_ip}:{username}"  # 使用 IP+用户名作为标识符
        
        # 检查是否被锁定
        if limiter.check_lockout(identifier):
            remaining_lockout = limiter.get_remaining_attempts(identifier)
            raise RateLimitException(
                _('登录失败次数过多，账户已被锁定，请 {minutes} 分钟后重试').format(minutes=remaining_lockout // 60),
                code='E005001'
            )
        
        # 如果失败次数较多，需要验证码
        remaining_attempts = limiter.get_remaining_attempts(identifier)
        if remaining_attempts <= 2:  # 剩余 2 次或更少时需要验证码
            if not captcha:
                raise AuthenticationException(_('登录失败次数过多，请输入验证码'), code='E002001')
            
            # 验证验证码
            captcha_gen = CaptchaGenerator()
            if not captcha_gen.verify_captcha(captcha, client_ip):
                limiter.record_failure(identifier)
                raise AuthenticationException(_('验证码错误'), code='E002001')
        
        # 尝试认证用户
        user = authenticate(
            request=request,
            username=username,
            password=password
        )
        
        if not user:
            # 记录登录失败
            attempt_info = limiter.record_failure(identifier)
            remaining_attempts = limiter.get_remaining_attempts(identifier)
            
            # 如果失败次数过多，自动加入黑名单（可选）
            if attempt_info['count'] >= 10:  # 10 次失败后加入黑名单
                ip_manager.add_to_blacklist(client_ip, duration=3600)  # 1 小时
            
            if remaining_attempts <= 2:
                error_msg = _('用户名或密码错误，剩余尝试次数：{count}，需要验证码').format(count=remaining_attempts)
            else:
                error_msg = _('用户名或密码错误，剩余尝试次数：{count}').format(count=remaining_attempts)
            
            raise AuthenticationException(error_msg, code='E002001')
        
        # 检查用户是否激活
        if not user.is_active:
            raise AuthenticationException(_('用户已被禁用，请联系管理员'), code='E002001')
        
        # 登录成功，清除失败记录
        limiter.record_success(identifier)
        
        attrs['user'] = user
        return attrs


class TokenRefreshSerializer(serializers.Serializer):
    """
    Token 刷新序列化器
    使用 DRF SimpleJWT 提供的序列化器
    """
    refresh = serializers.CharField(help_text='Refresh Token')
    
    def validate_refresh(self, value):
        """
        验证 Refresh Token
        
        Args:
            value: Refresh Token 字符串
            
        Returns:
            str: 验证后的 Token
            
        Raises:
            ValidationException: 如果 Token 无效
        """
        try:
            refresh = RefreshToken(value)
        except Exception as e:
            raise ValidationException(_('无效的 Refresh Token'), code='E010303')
        
        return value

