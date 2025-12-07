"""
请求 ID 中间件
为每个请求生成唯一的请求 ID，用于追踪和日志关联
"""
import uuid
from django.utils.deprecation import MiddlewareMixin


class RequestIDMiddleware(MiddlewareMixin):
    """
    请求 ID 中间件
    为每个请求生成唯一的请求 ID，并添加到响应头中
    """
    
    def process_request(self, request):
        """处理请求前，生成请求 ID"""
        # 从请求头获取请求 ID，如果没有则生成新的
        request_id = request.META.get('HTTP_X_REQUEST_ID')
        if not request_id:
            request_id = f'req_{uuid.uuid4().hex[:12]}'
        
        # 将请求 ID 存储到 request 对象中
        request.request_id = request_id
        return None
    
    def process_response(self, request, response):
        """处理响应后，添加请求 ID 到响应头"""
        if hasattr(request, 'request_id'):
            response['X-Request-ID'] = request.request_id
        return response

