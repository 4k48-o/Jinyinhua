"""
自定义异常类和异常处理器
定义业务异常和错误码体系，提供统一的异常处理
"""
import uuid
import logging
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response

logger = logging.getLogger('django.exception')


class BaseAPIException(APIException):
    """
    基础 API 异常类
    所有自定义异常都继承此类
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('服务器内部错误')
    default_code = 'E000000'
    
    def __init__(self, detail=None, code=None, status_code=None):
        """
        初始化异常
        
        Args:
            detail: 错误详情
            code: 业务错误码
            status_code: HTTP 状态码
        """
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = detail
        if code is not None:
            self.code = code
        else:
            self.code = self.default_code
        
        super().__init__(detail, code)


class ValidationException(BaseAPIException):
    """数据验证异常"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('数据验证失败')
    default_code = 'E001001'


class AuthenticationException(BaseAPIException):
    """认证异常"""
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('认证失败')
    default_code = 'E002001'


class PermissionException(BaseAPIException):
    """权限异常"""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('权限不足')
    default_code = 'E002002'


class NotFoundException(BaseAPIException):
    """资源未找到异常"""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('资源不存在')
    default_code = 'E003001'


class ConflictException(BaseAPIException):
    """资源冲突异常"""
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('资源冲突')
    default_code = 'E003002'


class BusinessException(BaseAPIException):
    """业务逻辑异常"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('业务处理失败')
    default_code = 'E004001'


class RateLimitException(BaseAPIException):
    """限流异常"""
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = _('请求过于频繁，请稍后重试')
    default_code = 'E005001'


class ServiceUnavailableException(BaseAPIException):
    """服务不可用异常"""
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = _('服务暂时不可用，请稍后重试')
    default_code = 'E006001'


def custom_exception_handler(exc, context):
    """
    自定义 DRF 异常处理器
    统一处理 DRF 异常，返回标准格式的错误响应
    
    Args:
        exc: 异常对象
        context: 异常上下文（包含 request, view 等）
    
    Returns:
        Response: 标准格式的错误响应
    """
    # 调用 DRF 默认异常处理器
    response = drf_exception_handler(exc, context)
    
    if response is not None:
        # 获取请求对象
        request = context.get('request')
        request_id = getattr(request, 'request_id', None) if request else None
        error_id = f'err_{uuid.uuid4().hex[:12]}'
        
        # 获取错误码
        if isinstance(exc, BaseAPIException):
            error_code = exc.code
        elif isinstance(exc, APIException):
            # DRF 标准异常，使用默认错误码
            error_code = getattr(exc, 'code', f'E{response.status_code:03d}000')
        else:
            error_code = f'E{response.status_code:03d}000'
        
        # 构建标准错误响应
        custom_response_data = {
            'success': False,
            'code': error_code,
            'message': str(exc.detail) if hasattr(exc, 'detail') else '操作失败',
            'error': str(exc.detail) if hasattr(exc, 'detail') else str(exc),
            'data': None,
            'request_id': request_id,
            'error_id': error_id,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
        }
        
        # 如果是验证错误，添加字段级错误详情
        if hasattr(exc, 'detail') and isinstance(exc.detail, dict):
            custom_response_data['errors'] = exc.detail
        
        # 记录异常日志（结构化日志）
        log_record = logging.LogRecord(
            name=logger.name,
            level=logging.ERROR,
            pathname='',
            lineno=0,
            msg=f"API Exception: {type(exc).__name__}: {str(exc)}",
            args=(),
            exc_info=None,
        )
        log_record.request_id = request_id
        log_record.error_id = error_id
        log_record.extra_data = {
            'exception_type': type(exc).__name__,
            'exception_message': str(exc),
            'path': request.path if request else 'unknown',
            'method': request.method if request else 'unknown',
            'error_code': error_code,
        }
        logger.handle(log_record)
        
        response.data = custom_response_data
    
    return response
