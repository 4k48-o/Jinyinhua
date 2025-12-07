"""
认证视图
处理用户注册、登录、Token 刷新、登出等操作
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from django.utils.translation import gettext_lazy as _
from apps.common.response import APIResponse
from apps.common.exceptions import ValidationException, AuthenticationException
from apps.common.audit import log_login, log_logout
from .serializers import RegisterSerializer, LoginSerializer, TokenRefreshSerializer
from .security import LoginAttemptLimiter, IPWhitelistBlacklist, CaptchaGenerator, DeviceFingerprint
import logging

logger = logging.getLogger('django.request')


class RegisterView(APIView):
    """
    用户注册视图
    允许匿名用户注册
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        tags=['认证'],
        summary='用户注册',
        description='新用户注册，注册成功后自动返回 JWT Token',
        request=RegisterSerializer,
        responses={
            200: {
                'description': '注册成功',
                'examples': [
                    OpenApiExample(
                        '成功响应',
                        value={
                            'success': True,
                            'code': 200,
                            'message': '注册成功',
                            'data': {
                                'access': 'eyJ0eXAiOiJKV1QiLCJhbGc...',
                                'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGc...',
                                'user': {
                                    'id': 1,
                                    'username': 'testuser'
                                }
                            },
                            'request_id': 'req_abc123',
                            'timestamp': '2025-12-06T16:00:00Z'
                        }
                    )
                ]
            },
            400: {
                'description': '注册失败，数据验证错误',
                'examples': [
                    OpenApiExample(
                        '验证错误',
                        value={
                            'success': False,
                            'code': 'E001001',
                            'message': '数据验证失败',
                            'errors': {
                                'username': ['用户名已存在'],
                                'password': ['密码强度不足']
                            }
                        }
                    )
                ]
            }
        },
        examples=[
            OpenApiExample(
                '注册请求',
                value={
                    'username': 'testuser',
                    'password': 'password123',
                    'password_confirm': 'password123'
                }
            )
        ]
    )
    def post(self, request):
        """
        用户注册
        
        Request Body:
        {
            "username": "testuser",
            "password": "password123",
            "password_confirm": "password123"
        }
        
        Returns:
            APIResponse: 包含 Token 的响应
        """
        serializer = RegisterSerializer(data=request.data)
        
        if not serializer.is_valid():
            # 提取验证错误
            errors = serializer.errors
            error_message = '注册失败'
            if 'username' in errors:
                error_message = errors['username'][0] if isinstance(errors['username'], list) else str(errors['username'])
            elif 'password' in errors:
                error_message = errors['password'][0] if isinstance(errors['password'], list) else str(errors['password'])
            elif 'password_confirm' in errors:
                error_message = errors['password_confirm'][0] if isinstance(errors['password_confirm'], list) else str(errors['password_confirm'])
            elif 'non_field_errors' in errors:
                error_message = errors['non_field_errors'][0] if isinstance(errors['non_field_errors'], list) else str(errors['non_field_errors'])
            
            return APIResponse.error(
                message=error_message,
                code='E001001',
                status_code=status.HTTP_400_BAD_REQUEST,
                errors=errors,
                request_id=getattr(request, 'request_id', None)
            )
        
        try:
            # 检查 IP 黑名单
            ip_manager = IPWhitelistBlacklist()
            client_ip = ip_manager.get_client_ip(request)
            if ip_manager.is_blacklisted(client_ip):
                return APIResponse.error(
                    message=_('IP 地址已被封禁，无法注册'),
                    code='E002001',
                    status_code=status.HTTP_403_FORBIDDEN,
                    request_id=getattr(request, 'request_id', None)
                )
            
            # 创建用户
            user = serializer.save()
            
            # 生成 Token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            # 设备指纹识别
            device_fingerprint = DeviceFingerprint.generate_fingerprint(request)
            DeviceFingerprint.store_device_fingerprint(user.id, device_fingerprint)
            
            # 记录注册日志
            device_info = DeviceFingerprint.get_device_info(request)
            logger.info(
                f"User registered: {user.username}",
                extra={
                    'request_id': getattr(request, 'request_id', None),
                    'user_id': user.id,
                    'username': user.username,
                    'device_fingerprint': device_fingerprint,
                    'ip': device_info.get('ip'),
                }
            )
            
            return APIResponse.success(
                data={
                    'access': access_token,
                    'refresh': refresh_token,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                    }
                },
                message=_('注册成功'),
                request_id=getattr(request, 'request_id', None)
            )
        except Exception as e:
            logger.error(
                f"Registration failed: {str(e)}",
                extra={
                    'request_id': getattr(request, 'request_id', None),
                    'error': str(e),
                }
            )
            return APIResponse.error(
                message=_('注册失败，请稍后重试'),
                code='E000000',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error=str(e),
                request_id=getattr(request, 'request_id', None)
            )


class LoginView(APIView):
    """
    用户登录视图
    允许匿名用户登录
    支持登录失败次数限制、验证码、设备指纹识别
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        tags=['认证'],
        summary='用户登录',
        description='用户登录，登录成功后返回 JWT Token。登录失败次数过多时需要验证码。',
        request=LoginSerializer,
        responses={
            200: {
                'description': '登录成功',
                'examples': [
                    OpenApiExample(
                        '成功响应',
                        value={
                            'success': True,
                            'code': 200,
                            'message': '登录成功',
                            'data': {
                                'access': 'eyJ0eXAiOiJKV1QiLCJhbGc...',
                                'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGc...',
                                'user': {
                                    'id': 1,
                                    'username': 'testuser'
                                }
                            },
                            'request_id': 'req_abc123',
                            'timestamp': '2025-12-06T16:00:00Z'
                        }
                    )
                ]
            },
            401: {
                'description': '登录失败',
                'examples': [
                    OpenApiExample(
                        '认证失败',
                        value={
                            'success': False,
                            'code': 'E002001',
                            'message': '用户名或密码错误，剩余尝试次数：3',
                            'request_id': 'req_abc123',
                            'error_id': 'err_xyz789'
                        }
                    )
                ]
            },
            429: {
                'description': '登录失败次数过多，账户被锁定',
            }
        },
        examples=[
            OpenApiExample(
                '普通登录',
                value={
                    'username': 'testuser',
                    'password': 'password123'
                }
            ),
            OpenApiExample(
                '需要验证码的登录',
                value={
                    'username': 'testuser',
                    'password': 'password123',
                    'captcha': '1234'
                }
            )
        ]
    )
    def post(self, request):
        """
        用户登录
        
        Request Body:
        {
            "username": "testuser",
            "password": "password123",
            "captcha": "1234"  // 可选，登录失败次数过多时需要
        }
        
        Returns:
            APIResponse: 包含 Token 的响应
        """
        serializer = LoginSerializer(data=request.data, context={'request': request})
        
        if not serializer.is_valid():
            # 提取验证错误
            errors = serializer.errors
            error_message = '登录失败'
            if 'username' in errors:
                error_message = errors['username'][0] if isinstance(errors['username'], list) else str(errors['username'])
            elif 'password' in errors:
                error_message = errors['password'][0] if isinstance(errors['password'], list) else str(errors['password'])
            elif 'non_field_errors' in errors:
                error_message = errors['non_field_errors'][0] if isinstance(errors['non_field_errors'], list) else str(errors['non_field_errors'])
            
            # 获取用户名（用于记录登录失败日志）
            username = request.data.get('username', 'unknown')
            
            # 记录登录失败日志到数据库（审计日志）
            device_info = DeviceFingerprint.get_device_info(request)
            log_login(
                username=username,
                login_type='password',
                request=request,
                status=0,
                failure_reason=error_message,
                device_info=device_info,
            )
            
            # 记录业务日志到文件
            logger.warning(
                f"Login failed: {username} - {error_message}",
                extra={
                    'request_id': getattr(request, 'request_id', None),
                    'username': username,
                    'error': error_message,
                }
            )
            
            return APIResponse.error(
                message=error_message,
                code='E002001',
                status_code=status.HTTP_401_UNAUTHORIZED,
                errors=errors,
                request_id=getattr(request, 'request_id', None)
            )
        
        try:
            user = serializer.validated_data['user']
            
            # 设备指纹识别
            device_fingerprint = DeviceFingerprint.generate_fingerprint(request)
            DeviceFingerprint.store_device_fingerprint(user.id, device_fingerprint)
            
            # 生成 Token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            # 获取设备信息
            device_info = DeviceFingerprint.get_device_info(request)
            
            # 记录登录日志到数据库（审计日志）
            log_login(
                user=user,
                login_type='password',
                request=request,
                status=1,
                device_info=device_info,
            )
            
            # 记录业务日志到文件
            logger.info(
                f"User logged in: {user.username}",
                extra={
                    'request_id': getattr(request, 'request_id', None),
                    'user_id': user.id,
                    'username': user.username,
                    'device_fingerprint': device_fingerprint,
                    'ip': device_info.get('ip'),
                    'user_agent': device_info.get('user_agent'),
                }
            )
            
            return APIResponse.success(
                data={
                    'access': access_token,
                    'refresh': refresh_token,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                    }
                },
                message=_('登录成功'),
                request_id=getattr(request, 'request_id', None)
            )
        except Exception as e:
            # 获取用户名（用于记录登录失败日志）
            username = request.data.get('username', 'unknown')
            
            # 记录登录失败日志到数据库（审计日志）
            device_info = DeviceFingerprint.get_device_info(request)
            log_login(
                username=username,
                login_type='password',
                request=request,
                status=0,
                failure_reason=str(e),
                device_info=device_info,
            )
            
            # 记录业务日志到文件
            logger.error(
                f"Login failed: {username} - {str(e)}",
                extra={
                    'request_id': getattr(request, 'request_id', None),
                    'username': username,
                    'error': str(e),
                }
            )
            
            return APIResponse.error(
                message=_('登录失败，请稍后重试'),
                code='E000000',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error=str(e),
                request_id=getattr(request, 'request_id', None)
            )


class CaptchaView(APIView):
    """
    验证码视图
    获取登录验证码（当登录失败次数过多时）
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        tags=['认证'],
        summary='获取验证码',
        description='获取登录验证码，当登录失败次数过多时需要验证码',
        responses={
            200: {
                'description': '验证码获取成功',
                'examples': [
                    OpenApiExample(
                        '成功响应',
                        value={
                            'success': True,
                            'code': 200,
                            'message': '验证码获取成功',
                            'data': {
                                'captcha': '1234'
                            },
                            'request_id': 'req_abc123',
                            'timestamp': '2025-12-06T16:00:00Z'
                        }
                    )
                ]
            }
        }
    )
    def get(self, request):
        """
        获取验证码
        
        Returns:
            APIResponse: 包含验证码图片的响应
        """
        ip_manager = IPWhitelistBlacklist()
        client_ip = ip_manager.get_client_ip(request)
        
        # 生成验证码（返回验证码字符串和 base64 图片）
        captcha_text, captcha_image = CaptchaGenerator.generate()
        
        # 存储验证码（只存储文本，用于验证）
        CaptchaGenerator.store_captcha(captcha_text, client_ip)
        
        return APIResponse.success(
            data={
                'image': captcha_image,  # base64 图片数据
                'key': client_ip,  # 用于标识验证码的 key（IP 地址）
            },
            message=_('验证码获取成功'),
            request_id=getattr(request, 'request_id', None)
        )


class TokenRefreshView(APIView):
    """
    Token 刷新视图
    使用 Refresh Token 获取新的 Access Token
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        tags=['认证'],
        summary='刷新 Token',
        description='使用 Refresh Token 获取新的 Access Token',
        request=TokenRefreshSerializer,
        responses={
            200: {
                'description': 'Token 刷新成功',
                'examples': [
                    OpenApiExample(
                        '成功响应',
                        value={
                            'success': True,
                            'code': 200,
                            'message': 'Token 刷新成功',
                            'data': {
                                'access': 'eyJ0eXAiOiJKV1QiLCJhbGc...',
                                'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGc...'  # 如果启用了 Token 旋转
                            }
                        }
                    )
                ]
            },
            400: {
                'description': 'Refresh Token 无效或过期',
            }
        },
        examples=[
            OpenApiExample(
                '刷新请求',
                value={
                    'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGc...'
                }
            )
        ]
    )
    def post(self, request):
        """
        刷新 Token
        
        Request Body:
        {
            "refresh": "refresh_token_string"
        }
        
        Returns:
            APIResponse: 包含新 Token 的响应
        """
        serializer = TokenRefreshSerializer(data=request.data)
        
        if not serializer.is_valid():
            errors = serializer.errors
            error_message = 'Token 刷新失败'
            if 'refresh' in errors:
                error_message = errors['refresh'][0] if isinstance(errors['refresh'], list) else str(errors['refresh'])
            
            return APIResponse.error(
                message=error_message,
                code='E010303',
                status_code=status.HTTP_400_BAD_REQUEST,
                errors=errors,
                request_id=getattr(request, 'request_id', None)
            )
        
        try:
            refresh_token = serializer.validated_data['refresh']
            refresh = RefreshToken(refresh_token)
            
            # 生成新的 Access Token
            access_token = str(refresh.access_token)
            
            # 如果配置了 Token 旋转，返回新的 Refresh Token
            from django.conf import settings
            if settings.SIMPLE_JWT.get('ROTATE_REFRESH_TOKENS', False):
                # 将旧的 Refresh Token 加入黑名单
                refresh.blacklist()
                # 生成新的 Refresh Token
                new_refresh = RefreshToken.for_user(refresh.user)
                refresh_token = str(new_refresh)
            
            return APIResponse.success(
                data={
                    'access': access_token,
                    'refresh': refresh_token if settings.SIMPLE_JWT.get('ROTATE_REFRESH_TOKENS', False) else None,
                },
                message=_('Token 刷新成功'),
                request_id=getattr(request, 'request_id', None)
            )
        except TokenError as e:
            logger.warning(
                f"Token refresh failed: {str(e)}",
                extra={
                    'request_id': getattr(request, 'request_id', None),
                    'error': str(e),
                }
            )
            return APIResponse.error(
                message=_('无效的 Refresh Token'),
                code='E010303',
                status_code=status.HTTP_401_UNAUTHORIZED,
                error=str(e),
                request_id=getattr(request, 'request_id', None)
            )
        except Exception as e:
            logger.error(
                f"Token refresh error: {str(e)}",
                extra={
                    'request_id': getattr(request, 'request_id', None),
                    'error': str(e),
                }
            )
            return APIResponse.error(
                message=_('Token 刷新失败，请稍后重试'),
                code='E000000',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error=str(e),
                request_id=getattr(request, 'request_id', None)
            )


class LogoutView(APIView):
    """
    用户登出视图
    将 Refresh Token 加入黑名单
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        tags=['认证'],
        summary='用户登出',
        description='用户登出，将 Refresh Token 加入黑名单',
        request={
            'type': 'object',
            'properties': {
                'refresh': {
                    'type': 'string',
                    'description': 'Refresh Token'
                }
            },
            'required': ['refresh']
        },
        responses={
            200: {
                'description': '登出成功',
                'examples': [
                    OpenApiExample(
                        '成功响应',
                        value={
                            'success': True,
                            'code': 200,
                            'message': '登出成功',
                            'request_id': 'req_abc123',
                            'timestamp': '2025-12-06T16:00:00Z'
                        }
                    )
                ]
            },
            400: {
                'description': 'Refresh Token 无效',
            }
        },
        examples=[
            OpenApiExample(
                '登出请求',
                value={
                    'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGc...'
                }
            )
        ]
    )
    def post(self, request):
        """
        用户登出
        
        Request Body:
        {
            "refresh": "refresh_token_string"
        }
        
        Returns:
            APIResponse: 登出成功响应
        """
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return APIResponse.error(
                message=_('Refresh Token 不能为空'),
                code='E001001',
                status_code=status.HTTP_400_BAD_REQUEST,
                request_id=getattr(request, 'request_id', None)
            )
        
        try:
            refresh = RefreshToken(refresh_token)
            # 将 Token 加入黑名单
            refresh.blacklist()
            
            # 记录退出日志到数据库（审计日志）
            log_logout(
                user=request.user,
                request=request,
                status=1,
            )
            
            # 记录业务日志到文件
            logger.info(
                f"User logged out: {request.user.username}",
                extra={
                    'request_id': getattr(request, 'request_id', None),
                    'user_id': request.user.id,
                    'username': request.user.username,
                }
            )
            
            return APIResponse.success(
                message=_('登出成功'),
                request_id=getattr(request, 'request_id', None)
            )
        except TokenError as e:
            logger.warning(
                f"Logout failed: {str(e)}",
                extra={
                    'request_id': getattr(request, 'request_id', None),
                    'error': str(e),
                }
            )
            return APIResponse.error(
                message=_('无效的 Refresh Token'),
                code='E010303',
                status_code=status.HTTP_400_BAD_REQUEST,
                error=str(e),
                request_id=getattr(request, 'request_id', None)
            )
        except Exception as e:
            logger.error(
                f"Logout error: {str(e)}",
                extra={
                    'request_id': getattr(request, 'request_id', None),
                    'error': str(e),
                }
            )
            return APIResponse.error(
                message=_('登出失败，请稍后重试'),
                code='E000000',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error=str(e),
                request_id=getattr(request, 'request_id', None)
            )
