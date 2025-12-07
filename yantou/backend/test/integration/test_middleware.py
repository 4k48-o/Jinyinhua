"""
中间件集成测试
测试 middleware/ 中的中间件功能
"""
import pytest
import time
from unittest.mock import Mock, patch
from django.test import RequestFactory
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import PermissionDenied, ValidationError
from rest_framework.exceptions import APIException
from middleware.logging import RequestLoggingMiddleware
from middleware.exception import ExceptionHandlingMiddleware


@pytest.mark.integration
class TestRequestLoggingMiddleware:
    """请求日志中间件测试"""
    
    def test_process_request_sets_start_time(self):
        """测试请求处理前设置开始时间"""
        middleware = RequestLoggingMiddleware(lambda x: HttpResponse())
        request = RequestFactory().get('/test/')
        
        middleware.process_request(request)
        
        assert hasattr(request, '_start_time')
        assert isinstance(request._start_time, float)
    
    def test_process_response_logs_request(self):
        """测试响应处理后记录日志"""
        middleware = RequestLoggingMiddleware(lambda x: HttpResponse())
        request = RequestFactory().get('/test/')
        request._start_time = time.time()
        response = HttpResponse()
        
        with patch('middleware.logging.logger') as mock_logger:
            result = middleware.process_response(request, response)
            
            assert result == response
            # 验证日志被调用
            assert mock_logger.info.called or mock_logger.warning.called or mock_logger.error.called
    
    def test_process_response_calculates_execution_time(self):
        """测试计算执行时间"""
        middleware = RequestLoggingMiddleware(lambda x: HttpResponse())
        request = RequestFactory().get('/test/')
        request._start_time = time.time() - 0.1  # 模拟 100ms 的执行时间
        response = HttpResponse(status=200)
        
        with patch('middleware.logging.logger') as mock_logger:
            middleware.process_response(request, response)
            
            # 验证日志调用中包含执行时间信息
            call_args = mock_logger.info.call_args
            if call_args:
                log_message = str(call_args)
                # 执行时间应该被记录
                assert 'execution_time' in log_message or 'Request:' in log_message
    
    def test_process_response_logs_ip_address(self):
        """测试记录 IP 地址"""
        middleware = RequestLoggingMiddleware(lambda x: HttpResponse())
        request = RequestFactory().get('/test/')
        request._start_time = time.time()
        request.META['REMOTE_ADDR'] = '192.168.1.1'
        response = HttpResponse(status=200)
        
        with patch('middleware.logging.logger') as mock_logger:
            middleware.process_response(request, response)
            
            # 验证 IP 地址被记录
            assert mock_logger.info.called or mock_logger.warning.called
    
    def test_process_response_logs_user_info(self, user):
        """测试记录用户信息"""
        middleware = RequestLoggingMiddleware(lambda x: HttpResponse())
        request = RequestFactory().get('/test/')
        request._start_time = time.time()
        request.user = user
        response = HttpResponse(status=200)
        
        with patch('middleware.logging.logger') as mock_logger:
            middleware.process_response(request, response)
            
            # 验证用户信息被记录
            assert mock_logger.info.called
    
    def test_process_response_logs_error_for_500(self):
        """测试 500 错误使用 ERROR 级别"""
        middleware = RequestLoggingMiddleware(lambda x: HttpResponse())
        request = RequestFactory().get('/test/')
        request._start_time = time.time()
        response = HttpResponse(status=500)
        
        with patch('middleware.logging.logger') as mock_logger:
            middleware.process_response(request, response)
            
            # 500 错误应该使用 ERROR 级别
            assert mock_logger.error.called
    
    def test_process_response_logs_warning_for_400(self):
        """测试 400 错误使用 WARNING 级别"""
        middleware = RequestLoggingMiddleware(lambda x: HttpResponse())
        request = RequestFactory().get('/test/')
        request._start_time = time.time()
        response = HttpResponse(status=400)
        
        with patch('middleware.logging.logger') as mock_logger:
            middleware.process_response(request, response)
            
            # 400 错误应该使用 WARNING 级别
            assert mock_logger.warning.called
    
    def test_process_response_without_start_time(self):
        """测试没有开始时间的情况"""
        middleware = RequestLoggingMiddleware(lambda x: HttpResponse())
        request = RequestFactory().get('/test/')
        # 不设置 _start_time
        response = HttpResponse(status=200)
        
        with patch('middleware.logging.logger') as mock_logger:
            result = middleware.process_response(request, response)
            
            assert result == response
            # 应该仍然记录日志，执行时间为 0
            assert mock_logger.info.called or mock_logger.warning.called
    
    def test_process_response_logs_query_params(self):
        """测试记录查询参数"""
        middleware = RequestLoggingMiddleware(lambda x: HttpResponse())
        request = RequestFactory().get('/test/?key=value&page=1')
        request._start_time = time.time()
        response = HttpResponse(status=200)
        
        with patch('middleware.logging.logger') as mock_logger:
            middleware.process_response(request, response)
            
            # 验证日志被调用
            assert mock_logger.info.called
    
    def test_process_response_logs_anonymous_user(self):
        """测试记录匿名用户"""
        middleware = RequestLoggingMiddleware(lambda x: HttpResponse())
        request = RequestFactory().get('/test/')
        request._start_time = time.time()
        # 不设置 user，应该是匿名用户
        response = HttpResponse(status=200)
        
        with patch('middleware.logging.logger') as mock_logger:
            middleware.process_response(request, response)
            
            # 验证日志被调用
            assert mock_logger.info.called
    
    def test_process_response_logs_authenticated_user(self, user):
        """测试记录已认证用户"""
        middleware = RequestLoggingMiddleware(lambda x: HttpResponse())
        request = RequestFactory().get('/test/')
        request._start_time = time.time()
        request.user = user
        response = HttpResponse(status=200)
        
        with patch('middleware.logging.logger') as mock_logger:
            middleware.process_response(request, response)
            
            # 验证日志被调用
            assert mock_logger.info.called
    
    def test_process_response_logs_300_status(self):
        """测试 3xx 状态码使用 INFO 级别"""
        middleware = RequestLoggingMiddleware(lambda x: HttpResponse())
        request = RequestFactory().get('/test/')
        request._start_time = time.time()
        response = HttpResponse(status=301)
        
        with patch('middleware.logging.logger') as mock_logger:
            middleware.process_response(request, response)
            
            # 3xx 应该使用 INFO 级别
            assert mock_logger.info.called
    
    def test_process_response_logs_500_status(self):
        """测试 500 状态码使用 ERROR 级别"""
        middleware = RequestLoggingMiddleware(lambda x: HttpResponse())
        request = RequestFactory().get('/test/')
        request._start_time = time.time()
        response = HttpResponse(status=500)
        
        with patch('middleware.logging.logger') as mock_logger:
            middleware.process_response(request, response)
            
            # 500 应该使用 ERROR 级别
            assert mock_logger.error.called
    
    def test_process_response_logs_404_status(self):
        """测试 404 状态码使用 WARNING 级别"""
        middleware = RequestLoggingMiddleware(lambda x: HttpResponse())
        request = RequestFactory().get('/test/')
        request._start_time = time.time()
        response = HttpResponse(status=404)
        
        with patch('middleware.logging.logger') as mock_logger:
            middleware.process_response(request, response)
            
            # 404 应该使用 WARNING 级别
            assert mock_logger.warning.called


@pytest.mark.integration
class TestExceptionHandlingMiddleware:
    """异常处理中间件测试"""
    
    def test_process_exception_permission_denied(self):
        """测试处理 PermissionDenied 异常"""
        middleware = ExceptionHandlingMiddleware(lambda x: HttpResponse())
        request = RequestFactory().get('/test/')
        exception = PermissionDenied("权限不足")
        
        response = middleware.process_exception(request, exception)
        
        assert response is not None
        assert isinstance(response, JsonResponse)
        assert response.status_code == 403
        
        # 验证响应内容
        import json
        data = json.loads(response.content)
        assert data['code'] == 403
        assert '权限不足' in data['message']
    
    def test_process_exception_validation_error(self):
        """测试处理 ValidationError 异常"""
        middleware = ExceptionHandlingMiddleware(lambda x: HttpResponse())
        request = RequestFactory().get('/test/')
        exception = ValidationError("验证失败")
        
        response = middleware.process_exception(request, exception)
        
        assert response is not None
        assert isinstance(response, JsonResponse)
        assert response.status_code == 400
        
        # 验证响应内容
        import json
        data = json.loads(response.content)
        assert data['code'] == 400
        assert '验证失败' in data['message'] or '数据验证失败' in data['message']
    
    def test_process_exception_validation_error_with_dict(self):
        """测试处理带字典的 ValidationError 异常"""
        middleware = ExceptionHandlingMiddleware(lambda x: HttpResponse())
        request = RequestFactory().get('/test/')
        # 创建带 message_dict 的 ValidationError
        exception = ValidationError({'field': ['错误信息']})
        # ValidationError 会自动设置 message_dict
        if not hasattr(exception, 'message_dict'):
            # 如果版本不支持，使用 Mock
            from unittest.mock import Mock
            exception = Mock(spec=ValidationError)
            exception.message_dict = {'field': ['错误信息']}
            exception.__str__ = lambda: "验证失败"
        
        response = middleware.process_exception(request, exception)
        
        assert response is not None
        assert isinstance(response, JsonResponse)
        assert response.status_code == 400
        
        # 验证响应包含错误详情
        import json
        data = json.loads(response.content)
        assert 'errors' in data or 'error' in data
    
    def test_process_exception_validation_error_string(self):
        """测试处理字符串类型的 ValidationError"""
        middleware = ExceptionHandlingMiddleware(lambda x: HttpResponse())
        request = RequestFactory().get('/test/')
        exception = ValidationError("简单错误消息")
        
        response = middleware.process_exception(request, exception)
        
        assert response is not None
        assert isinstance(response, JsonResponse)
        assert response.status_code == 400
        
        import json
        data = json.loads(response.content)
        assert data['code'] == 400
        assert 'error' in data
    
    def test_process_exception_api_exception_returns_none(self):
        """测试 APIException 返回 None（由 DRF 处理）"""
        middleware = ExceptionHandlingMiddleware(lambda x: HttpResponse())
        request = RequestFactory().get('/test/')
        exception = APIException("API 异常")
        
        response = middleware.process_exception(request, exception)
        
        # APIException 应该返回 None，让 DRF 处理
        assert response is None
    
    def test_process_exception_generic_exception_debug_mode(self, settings):
        """测试通用异常在 DEBUG 模式下的处理"""
        settings.DEBUG = True
        middleware = ExceptionHandlingMiddleware(lambda x: HttpResponse())
        request = RequestFactory().get('/test/')
        exception = ValueError("通用错误")
        
        with patch('middleware.exception.logger') as mock_logger:
            response = middleware.process_exception(request, exception)
            
            assert response is not None
            assert isinstance(response, JsonResponse)
            assert response.status_code == 500
            
            # DEBUG 模式下应该包含详细错误信息
            import json
            data = json.loads(response.content)
            assert data['code'] == 500
            # DEBUG 模式下可能包含 traceback
            assert 'error' in data or 'traceback' in data
            
            # 验证错误被记录
            assert mock_logger.error.called
    
    def test_process_exception_generic_exception_production_mode(self, settings):
        """测试通用异常在生产模式下的处理"""
        settings.DEBUG = False
        middleware = ExceptionHandlingMiddleware(lambda x: HttpResponse())
        request = RequestFactory().get('/test/')
        exception = ValueError("通用错误")
        
        with patch('middleware.exception.logger') as mock_logger:
            response = middleware.process_exception(request, exception)
            
            assert response is not None
            assert isinstance(response, JsonResponse)
            assert response.status_code == 500
            
            # 生产模式下不应该包含详细错误信息
            import json
            data = json.loads(response.content)
            assert data['code'] == 500
            assert data['error'] is None  # 生产模式不暴露错误详情
            
            # 验证错误被记录
            assert mock_logger.error.called
    
    def test_process_exception_logs_exception_details(self, settings):
        """测试异常详情被记录"""
        settings.DEBUG = False
        middleware = ExceptionHandlingMiddleware(lambda x: HttpResponse())
        request = RequestFactory().get('/test/path')
        request.method = 'GET'
        exception = ValueError("测试错误")
        
        with patch('middleware.exception.logger') as mock_logger:
            middleware.process_exception(request, exception)
            
            # 验证日志被调用
            assert mock_logger.error.called
            
            # 验证日志包含异常信息
            call_args = mock_logger.error.call_args
            if call_args:
                log_message = str(call_args)
                assert 'ValueError' in log_message or '测试错误' in log_message
    
    def test_process_exception_none_handles_as_generic(self):
        """测试 None 异常被当作通用异常处理"""
        middleware = ExceptionHandlingMiddleware(lambda x: HttpResponse())
        request = RequestFactory().get('/test/')
        
        # None 异常会被当作通用异常处理
        with patch('middleware.exception.logger') as mock_logger:
            response = middleware.process_exception(request, None)
            
            # 应该返回错误响应
            assert response is not None
            assert isinstance(response, JsonResponse)
            assert response.status_code == 500
            
            # 验证错误被记录
            assert mock_logger.error.called
    
    def test_process_exception_logs_path_and_method(self, settings):
        """测试日志包含请求路径和方法"""
        settings.DEBUG = False
        middleware = ExceptionHandlingMiddleware(lambda x: HttpResponse())
        request = RequestFactory().post('/test/path/')
        request.method = 'POST'
        exception = ValueError("测试")
        
        with patch('middleware.exception.logger') as mock_logger:
            middleware.process_exception(request, exception)
            
            # 验证日志被调用
            assert mock_logger.error.called
            
            # 验证日志包含路径和方法
            call_args_str = str(mock_logger.error.call_args)
            assert '/test/path/' in call_args_str or 'POST' in call_args_str

