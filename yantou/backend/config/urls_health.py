"""
健康检查路由
用于监控系统状态
"""
from django.http import JsonResponse
from django.urls import path
from django.db import connection
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes

@extend_schema(
    tags=['系统'],
    summary='健康检查',
    description='检查系统健康状态和数据库连接',
    responses={
        200: {
            'description': '系统正常',
            'examples': [
                {
                    'status': 'ok',
                    'database': 'ok',
                    'service': 'yantou-backend'
                }
            ]
        },
        503: {
            'description': '系统异常',
        }
    }
)
def health_check(request):
    """
    健康检查接口
    检查数据库连接状态
    """
    try:
        # 检查数据库连接
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "ok"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    status_code = 200 if db_status == "ok" else 503
    
    return JsonResponse({
        'status': 'ok' if db_status == "ok" else 'error',
        'database': db_status,
        'service': 'yantou-backend',
    }, status=status_code)


urlpatterns = [
    path('', health_check, name='health-check'),
]

