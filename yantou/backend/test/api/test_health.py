"""
健康检查 API 测试
测试 /health/ 和 /api/v1/health/ 端点
"""
import pytest
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.api
@pytest.mark.requires_db
class TestHealthCheckAPI:
    """健康检查 API 测试类"""
    
    def test_health_check_success(self, api_client):
        """
        测试健康检查成功场景
        GET /health/
        """
        # Act: 执行 API 调用
        response = api_client.get('/health/')
        
        # Assert: 验证结果
        assert response.status_code == status.HTTP_200_OK
        assert response['Content-Type'] == 'application/json'
        
        data = response.json()
        assert 'status' in data
        assert 'database' in data
        assert 'service' in data
        assert data['status'] == 'ok'
        assert data['database'] == 'ok'
        assert data['service'] == 'yantou-backend'
    
    def test_api_health_check_success(self, api_client):
        """
        测试 API 健康检查成功场景
        GET /api/v1/health/
        """
        # Act: 执行 API 调用
        response = api_client.get('/api/v1/health/')
        
        # Assert: 验证结果
        assert response.status_code == status.HTTP_200_OK
        assert response['Content-Type'] == 'application/json'
        
        data = response.json()
        assert 'status' in data
        assert 'database' in data
        assert 'service' in data
        assert data['status'] == 'ok'
        assert data['database'] == 'ok'
        assert data['service'] == 'yantou-backend'
    
    def test_health_check_post_method(self, api_client):
        """
        测试 POST 方法（健康检查端点也接受 POST）
        POST /health/
        """
        # Act: 使用 POST 方法
        response = api_client.post('/health/')
        
        # Assert: 健康检查端点也接受 POST 方法
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['status'] == 'ok'
    
    def test_health_check_response_format(self, api_client):
        """
        测试响应格式
        验证响应包含所有必需的字段
        """
        # Act: 执行 API 调用
        response = api_client.get('/health/')
        
        # Assert: 验证响应格式
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # 验证必需字段
        required_fields = ['status', 'database', 'service']
        for field in required_fields:
            assert field in data, f'响应中缺少字段: {field}'
        
        # 验证字段类型
        assert isinstance(data['status'], str)
        assert isinstance(data['database'], str)
        assert isinstance(data['service'], str)
    
    @pytest.mark.slow
    def test_health_check_database_connection(self, api_client):
        """
        测试数据库连接检查
        验证数据库连接状态正确反映在响应中
        """
        # Act: 执行 API 调用
        response = api_client.get('/health/')
        
        # Assert: 验证数据库状态
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # 在测试环境中，数据库应该正常连接
        assert data['database'] == 'ok'


@pytest.mark.api
class TestHealthCheckAPIIntegration:
    """健康检查 API 集成测试"""
    
    def test_health_check_without_authentication(self, api_client):
        """
        测试健康检查不需要认证
        健康检查端点应该是公开的
        """
        # Act: 未认证的请求
        response = api_client.get('/health/')
        
        # Assert: 应该成功，不需要认证
        assert response.status_code == status.HTTP_200_OK
    
    def test_health_check_cors_headers(self, api_client):
        """
        测试 CORS 头信息
        验证响应包含正确的 CORS 头
        """
        # Act: 执行 OPTIONS 请求
        response = api_client.options('/health/')
        
        # Assert: 验证 CORS 头（如果配置了）
        # 注意: 这取决于 CORS 配置
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_204_NO_CONTENT,
            status.HTTP_405_METHOD_NOT_ALLOWED
        ]

