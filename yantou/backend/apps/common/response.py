"""
统一响应格式
提供标准的 API 响应格式
"""
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext_lazy as _
import uuid
from datetime import datetime


class APIResponse(Response):
    """
    统一 API 响应格式
    
    成功响应格式:
    {
        "success": true,
        "code": 200,
        "message": "操作成功",
        "data": {...},
        "request_id": "req_xxx",
        "timestamp": "2025-12-06T16:00:00Z"
    }
    
    错误响应格式:
    {
        "success": false,
        "code": "E001001",
        "message": "错误描述",
        "error": "详细错误信息",
        "errors": {...},  // 字段级错误
        "data": null,
        "request_id": "req_xxx",
        "error_id": "err_xxx",
        "timestamp": "2025-12-06T16:00:00Z"
    }
    """
    
    def __init__(
        self,
        data=None,
        message=None,
        code=None,
        status_code=status.HTTP_200_OK,
        request_id=None,
        error_id=None,
        errors=None,
        **kwargs
    ):
        """
        初始化响应
        
        Args:
            data: 响应数据
            message: 响应消息
            code: 业务错误码（成功时为 HTTP 状态码，错误时为业务错误码）
            status_code: HTTP 状态码
            request_id: 请求 ID
            error_id: 错误 ID（仅错误响应）
            errors: 字段级错误详情（仅验证错误）
        """
        success = 200 <= status_code < 400
        
        # 获取消息（支持国际化）
        if message is None:
            message = str(_('操作成功')) if success else str(_('操作失败'))
        else:
            # 如果消息是翻译对象，获取翻译后的文本
            if hasattr(message, '__class__') and 'translation' in str(type(message)):
                from django.utils.translation import gettext
                message = str(gettext(message))
            message = str(message)
        
        response_data = {
            'success': success,
            'code': code if code is not None else status_code,
            'message': message,
            'data': data,
            'request_id': request_id,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
        }
        
        # 错误响应添加额外字段
        if not success:
            if error_id:
                response_data['error_id'] = error_id
            if errors:
                response_data['errors'] = errors
            if 'error' in kwargs:
                response_data['error'] = kwargs.pop('error')
        
        super().__init__(data=response_data, status=status_code, **kwargs)
    
    @classmethod
    def success(cls, data=None, message=None, request_id=None, status_code=status.HTTP_200_OK, **kwargs):
        """
        成功响应
        
        Args:
            data: 响应数据
            message: 成功消息（如果为 None，则使用默认消息）
            request_id: 请求 ID
            status_code: HTTP 状态码（默认 200）
        """
        if message is None:
            message = _('操作成功')
        return cls(
            data=data,
            message=message,
            status_code=status_code,
            request_id=request_id,
            **kwargs
        )
    
    @classmethod
    def error(
        cls,
        message=None,
        code='E000000',
        status_code=status.HTTP_400_BAD_REQUEST,
        error=None,
        errors=None,
        request_id=None,
        error_id=None,
        **kwargs
    ):
        """
        错误响应
        
        Args:
            message: 错误消息（如果为 None，则使用默认消息）
            code: 业务错误码
            status_code: HTTP 状态码
            error: 详细错误信息
            errors: 字段级错误
            request_id: 请求 ID
            error_id: 错误 ID
        """
        if message is None:
            message = _('操作失败')
        if error_id is None:
            error_id = f'err_{uuid.uuid4().hex[:12]}'
        
        return cls(
            data=None,
            message=message,
            code=code,
            status_code=status_code,
            error=error,
            errors=errors,
            request_id=request_id,
            error_id=error_id,
            **kwargs
        )
