"""
CORS 中间件配置
使用 django-cors-headers，这里提供额外的配置说明
"""
# CORS 中间件使用 django-cors-headers 提供的 CorsMiddleware
# 配置在 settings.py 中的 CORS_ALLOWED_ORIGINS 等设置中

# 如果需要自定义 CORS 行为，可以继承 CorsMiddleware
# 示例：
# from corsheaders.middleware import CorsMiddleware
# 
# class CustomCorsMiddleware(CorsMiddleware):
#     def process_response(self, request, response):
#         response = super().process_response(request, response)
#         # 添加自定义 CORS 头
#         response['X-Custom-Header'] = 'value'
#         return response

