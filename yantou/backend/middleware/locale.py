"""
语言检测中间件
从请求头中检测用户语言偏好，并设置 Django 语言环境
"""
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class LocaleMiddleware(MiddlewareMixin):
    """
    语言检测中间件
    从请求头 Accept-Language 或自定义头 X-Language 中检测语言
    优先级：X-Language > Accept-Language > 默认语言
    """
    
    def process_request(self, request):
        """处理请求前，检测并设置语言"""
        # 优先从自定义请求头获取语言
        language = request.META.get('HTTP_X_LANGUAGE')
        
        # 如果没有自定义头，从 Accept-Language 获取
        if not language:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
            if language:
                # 解析 Accept-Language 头（格式：en-US,en;q=0.9,zh-CN;q=0.8）
                languages = [lang.strip().split(';')[0] for lang in language.split(',')]
                if languages:
                    # 尝试匹配支持的语言
                    for lang in languages:
                        # 处理语言代码（如 zh-CN -> zh-hans, en-US -> en）
                        lang_code = self._normalize_language_code(lang)
                        if lang_code in dict(settings.LANGUAGES):
                            language = lang_code
                            break
                    else:
                        # 如果没有匹配，使用第一个语言的基础代码
                        base_lang = languages[0].split('-')[0].lower()
                        if base_lang in dict(settings.LANGUAGES):
                            language = base_lang
        
        # 如果还是没有，使用默认语言
        if not language or language not in dict(settings.LANGUAGES):
            language = settings.LANGUAGE_CODE
        
        # 激活语言
        translation.activate(language)
        request.LANGUAGE_CODE = language
        
        return None
    
    def process_response(self, request, response):
        """处理响应后，清理语言环境"""
        translation.deactivate()
        return response
    
    def _normalize_language_code(self, lang_code):
        """
        标准化语言代码
        
        Args:
            lang_code: 原始语言代码（如 zh-CN, en-US）
            
        Returns:
            str: 标准化后的语言代码（如 zh-hans, en）
        """
        lang_code = lang_code.lower().strip()
        
        # 语言代码映射
        lang_map = {
            'zh-cn': 'zh-hans',
            'zh-hans-cn': 'zh-hans',
            'zh-tw': 'zh-hant',
            'zh-hant-tw': 'zh-hant',
            'zh-hk': 'zh-hant',
            'zh-hant-hk': 'zh-hant',
            'en-us': 'en',
            'en-gb': 'en',
        }
        
        # 先尝试完整匹配
        if lang_code in lang_map:
            return lang_map[lang_code]
        
        # 尝试基础代码匹配
        base_code = lang_code.split('-')[0]
        if base_code in dict(settings.LANGUAGES):
            return base_code
        
        # 返回原始代码
        return lang_code

