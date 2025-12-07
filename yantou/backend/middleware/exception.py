"""
异常处理中间件
统一处理应用异常，返回标准格式的错误响应
"""
import logging
import traceback
import uuid
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import PermissionDenied, ValidationError
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

logger = logging.getLogger('django.exception')


class ExceptionHandlingMiddleware(MiddlewareMixin):
    """
    异常处理中间件
    捕获并统一处理应用异常，返回标准格式的 JSON 响应
    """
    
    def process_exception(self, request, exception):
        """
        处理异常
        返回统一的错误响应格式
        """
        # DRF 异常由 DRF 的异常处理器处理
        if isinstance(exception, APIException):
            return None
        
        # 获取请求 ID
        request_id = getattr(request, 'request_id', None)
        error_id = f'err_{uuid.uuid4().hex[:12]}'
        
        # Django 权限异常
        if isinstance(exception, PermissionDenied):
            response_data = {
                'success': False,
                'code': 'E002002',
                'message': str(_('权限不足')),
                'error': str(exception),
                'data': None,
                'request_id': request_id,
                'error_id': error_id,
                'timestamp': self._get_timestamp(),
            }
            return JsonResponse(response_data, status=403)
        
        # Django 验证异常
        if isinstance(exception, ValidationError):
            response_data = {
                'success': False,
                'code': 'E001001',
                'message': str(_('数据验证失败')),
                'error': str(exception),
                'errors': exception.message_dict if hasattr(exception, 'message_dict') else None,
                'data': None,
                'request_id': request_id,
                'error_id': error_id,
                'timestamp': self._get_timestamp(),
            }
            return JsonResponse(response_data, status=400)
        
        # 其他未处理的异常
        # 记录详细错误信息
        error_traceback = traceback.format_exc()
        logger.error(
            f"Unhandled exception: {type(exception).__name__}: {str(exception)}\n"
            f"Request ID: {request_id}\n"
            f"Error ID: {error_id}\n"
            f"Path: {request.path}\n"
            f"Method: {request.method}\n"
            f"Traceback:\n{error_traceback}"
        )
        
        # 根据 DEBUG 模式返回不同的错误信息
        from django.conf import settings
        if settings.DEBUG:
            # 开发环境返回详细错误信息
            response_data = {
                'success': False,
                'code': 'E000000',
                'message': str(_('服务器内部错误')),
                'error': str(exception),
                'traceback': error_traceback.split('\n'),
                'data': None,
                'request_id': request_id,
                'error_id': error_id,
                'timestamp': self._get_timestamp(),
            }
            return JsonResponse(response_data, status=500)
        else:
            # 生产环境返回通用错误信息
            response_data = {
                'success': False,
                'code': 'E000000',
                'message': str(_('服务器内部错误，请稍后重试')),
                'error': None,
                'data': None,
                'request_id': request_id,
                'error_id': error_id,
                'timestamp': self._get_timestamp(),
            }
            return JsonResponse(response_data, status=500)
    
    def _get_timestamp(self):
        """获取当前时间戳（ISO 格式）"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + 'Z'

