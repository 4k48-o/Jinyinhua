"""
请求日志中间件
记录所有 HTTP 请求的详细信息
支持结构化日志（JSON 格式）
同时记录操作日志（AuditLog）
"""
import time
import json
import logging
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

logger = logging.getLogger('django.request')


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    请求日志中间件
    记录请求的详细信息，包括：
    - 请求方法、路径、参数
    - 响应状态码
    - 执行时间
    - IP 地址
    - 用户信息
    """
    
    def process_request(self, request):
        """处理请求前"""
        # 记录请求开始时间
        request._start_time = time.time()
        return None
    
    def process_response(self, request, response):
        """处理响应后"""
        # 计算执行时间
        if hasattr(request, '_start_time'):
            execution_time = (time.time() - request._start_time) * 1000  # 转换为毫秒
        else:
            execution_time = 0
        
        # 获取请求信息
        method = request.method
        path = request.path
        query_params = request.GET.dict()
        status_code = response.status_code
        
        # 获取客户端 IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'unknown')
        
        # 获取用户信息
        user = getattr(request, 'user', None)
        username = user.username if user and user.is_authenticated else 'anonymous'
        
        # 获取请求 ID
        request_id = getattr(request, 'request_id', None)
        
        # 构建结构化日志数据
        log_data = {
            'request_id': request_id,
            'method': method,
            'path': path,
            'query_params': query_params,
            'status_code': status_code,
            'execution_time_ms': round(execution_time, 2),
            'ip': ip,
            'username': username,
        }
        
        # 创建日志记录，添加额外字段
        log_record = logging.LogRecord(
            name=logger.name,
            level=logging.INFO,
            pathname='',
            lineno=0,
            msg='HTTP Request',
            args=(),
            exc_info=None,
        )
        log_record.request_id = request_id
        log_record.extra_data = log_data
        
        # 根据状态码选择日志级别
        if status_code >= 500:
            log_record.levelno = logging.ERROR
            log_record.levelname = 'ERROR'
            logger.handle(log_record)
        elif status_code >= 400:
            log_record.levelno = logging.WARNING
            log_record.levelname = 'WARNING'
            logger.handle(log_record)
        else:
            logger.handle(log_record)
        
        # 记录操作日志（AuditLog）
        # 只记录 API 请求（排除静态文件、健康检查等）
        if self._should_log_audit(request, response):
            self._log_audit(request, response, execution_time)
        
        return response
    
    def _should_log_audit(self, request, response):
        """
        判断是否应该记录操作日志
        
        Args:
            request: Django request 对象
            response: Django response 对象
            
        Returns:
            bool: 是否应该记录
        """
        # 排除静态文件和媒体文件
        if request.path.startswith(('/static/', '/media/')):
            return False
        
        # 排除健康检查
        if request.path.startswith('/api/v1/health'):
            return False
        
        # 排除文档页面
        if request.path.startswith(('/api/docs/', '/api/redoc/', '/api/schema/')):
            return False
        
        # 只记录 API 请求
        if not request.path.startswith('/api/'):
            return False
        
        # 只记录需要认证的请求（有用户信息）
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return False
        
        return True
    
    def _log_audit(self, request, response, execution_time):
        """
        记录操作日志
        
        Args:
            request: Django request 对象
            response: Django response 对象
            execution_time: 执行时间（毫秒）
        """
        try:
            from apps.common.audit import log_audit
            
            # 确定操作类型
            method = request.method
            if method == 'GET':
                action = 'view'
            elif method == 'POST':
                action = 'create'
            elif method in ['PUT', 'PATCH']:
                action = 'update'
            elif method == 'DELETE':
                action = 'delete'
            else:
                action = 'other'
            
            # 从路径推断资源类型
            path_parts = request.path.strip('/').split('/')
            if len(path_parts) >= 3 and path_parts[0] == 'api' and path_parts[1] == 'v1':
                resource_type = path_parts[2]  # 例如: users, roles, permissions
            else:
                resource_type = 'unknown'
            
            # 确定操作状态
            status = 1 if 200 <= response.status_code < 400 else 0
            error_message = None
            if status == 0:
                # 尝试从响应中获取错误信息
                if hasattr(response, 'data') and isinstance(response.data, dict):
                    error_message = response.data.get('message') or response.data.get('error')
            
            # 获取资源 ID（从路径或响应中）
            resource_id = None
            resource_name = None
            if len(path_parts) >= 4:
                try:
                    resource_id = int(path_parts[3])
                except (ValueError, IndexError):
                    pass
            
            # 记录日志
            log_audit(
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                resource_name=resource_name,
                description=f"{method} {request.path}",
                request=request,
                status=status,
                error_message=error_message,
                execution_time=int(execution_time),
            )
        except Exception as e:
            # 操作日志记录失败不应该影响主业务
            logger.warning(f"Failed to log audit: {str(e)}")

