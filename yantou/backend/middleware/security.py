"""
安全中间件
提供安全响应头、SQL 注入检查等功能
"""
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from utils.security import SQLInjectionChecker, XSSProtection


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    安全响应头中间件
    为所有响应添加安全相关的 HTTP 头
    """
    
    def process_response(self, request, response):
        """
        添加安全响应头
        
        Args:
            request: Django request 对象
            response: Django response 对象
            
        Returns:
            HttpResponse: 添加了安全头的响应
        """
        # X-Frame-Options: 防止点击劫持
        if not response.get('X-Frame-Options'):
            response['X-Frame-Options'] = getattr(settings, 'X_FRAME_OPTIONS', 'DENY')
        
        # X-Content-Type-Options: 防止 MIME 类型嗅探
        if not response.get('X-Content-Type-Options'):
            response['X-Content-Type-Options'] = 'nosniff'
        
        # X-XSS-Protection: XSS 保护
        if not response.get('X-XSS-Protection'):
            response['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer-Policy: 控制 referrer 信息
        if not response.get('Referrer-Policy'):
            referrer_policy = getattr(settings, 'SECURE_REFERRER_POLICY', 'strict-origin-when-cross-origin')
            response['Referrer-Policy'] = referrer_policy
        
        # Permissions-Policy: 控制浏览器功能
        if not response.get('Permissions-Policy'):
            permissions_policy = getattr(settings, 'SECURE_PERMISSIONS_POLICY', {})
            if permissions_policy:
                policy_parts = []
                for feature, allowlist in permissions_policy.items():
                    if allowlist:
                        policy_parts.append(f"{feature}=({' '.join(allowlist)})")
                    else:
                        policy_parts.append(f"{feature}=()")
                response['Permissions-Policy'] = ', '.join(policy_parts)
        
        # Content-Security-Policy (可选，需要根据实际情况配置)
        # if not response.get('Content-Security-Policy'):
        #     csp = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
        #     response['Content-Security-Policy'] = csp
        
        return response


class SQLInjectionProtectionMiddleware(MiddlewareMixin):
    """
    SQL 注入防护中间件
    检查请求参数中的潜在 SQL 注入代码
    """
    
    def process_request(self, request):
        """
        检查请求参数
        
        Args:
            request: Django request 对象
            
        Returns:
            None 或 HttpResponse: 如果检测到 SQL 注入，返回错误响应
        """
        # 只检查 GET 和 POST 参数
        if request.method in ['GET', 'POST']:
            # 检查 GET 参数
            for key, value in request.GET.items():
                if isinstance(value, str):
                    try:
                        SQLInjectionChecker.check_string(value)
                    except Exception:
                        from django.http import JsonResponse
                        from apps.common.response import APIResponse
                        from apps.common.response import APIResponse
                        from django.utils.translation import gettext_lazy as _
                        return APIResponse.error(
                            message=_('请求参数包含不安全的字符'),
                            code='E007001',
                            status_code=400,
                            request_id=getattr(request, 'request_id', None)
                        )
            
            # 检查 POST 参数
            if hasattr(request, 'POST'):
                for key, value in request.POST.items():
                    if isinstance(value, str):
                        try:
                            SQLInjectionChecker.check_string(value)
                        except Exception:
                            from apps.common.response import APIResponse
                            from django.utils.translation import gettext_lazy as _
                            return APIResponse.error(
                                message=_('请求参数包含不安全的字符'),
                                code='E007001',
                                status_code=400,
                                request_id=getattr(request, 'request_id', None)
                            )
        
        return None

