"""
安全工具函数
提供 SQL 注入检查、安全验证等功能
"""
import re
from typing import List, Optional
from django.db import connection
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class SQLInjectionChecker:
    """
    SQL 注入检查器
    用于检测潜在的 SQL 注入攻击
    """
    
    # SQL 注入常见模式
    SQL_INJECTION_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE|UNION|SCRIPT)\b)",
        r"(--|#|\/\*|\*\/)",  # SQL 注释
        r"(\b(OR|AND)\s+\d+\s*=\s*\d+)",  # OR/AND 注入
        r"(\b(OR|AND)\s+['\"]?\w+['\"]?\s*=\s*['\"]?\w+['\"]?)",
        r"(\bUNION\s+SELECT\b)",
        r"(\bEXEC\s*\()",
        r"(\bEXECUTE\s*\()",
        r"('|(\\')|(;)|(--)|(/\*)|(\*/)|(\+)|(\%)|(\[)|(\]))",  # 特殊字符
        r"(\bWAITFOR\s+DELAY\b)",
        r"(\bCHAR\s*\()",
        r"(\bCONVERT\s*\()",
        r"(\bCAST\s*\()",
    ]
    
    @classmethod
    def check_string(cls, value: str) -> bool:
        """
        检查字符串是否包含潜在的 SQL 注入代码
        
        Args:
            value: 要检查的字符串
            
        Returns:
            bool: True 表示安全，False 表示可能包含 SQL 注入
            
        Raises:
            ValidationError: 如果检测到 SQL 注入模式
        """
        if not value or not isinstance(value, str):
            return True
        
        value_upper = value.upper()
        
        for pattern in cls.SQL_INJECTION_PATTERNS:
            if re.search(pattern, value_upper, re.IGNORECASE):
                raise ValidationError(_('输入包含不安全的字符，可能存在 SQL 注入风险'))
        
        return True
    
    @classmethod
    def check_dict(cls, data: dict) -> List[str]:
        """
        检查字典中的所有字符串值
        
        Args:
            data: 要检查的字典
            
        Returns:
            List[str]: 包含潜在 SQL 注入的字段列表
        """
        suspicious_fields = []
        
        for key, value in data.items():
            if isinstance(value, str):
                try:
                    cls.check_string(value)
                except ValidationError:
                    suspicious_fields.append(key)
            elif isinstance(value, dict):
                nested_fields = cls.check_dict(value)
                suspicious_fields.extend([f"{key}.{f}" for f in nested_fields])
            elif isinstance(value, list):
                for idx, item in enumerate(value):
                    if isinstance(item, str):
                        try:
                            cls.check_string(item)
                        except ValidationError:
                            suspicious_fields.append(f"{key}[{idx}]")
        
        return suspicious_fields
    
    @classmethod
    def sanitize_string(cls, value: str) -> str:
        """
        清理字符串，移除潜在的 SQL 注入字符
        
        Args:
            value: 要清理的字符串
            
        Returns:
            str: 清理后的字符串
        """
        if not value:
            return value
        
        # 移除 SQL 注释
        value = re.sub(r'--.*', '', value)
        value = re.sub(r'/\*.*?\*/', '', value, flags=re.DOTALL)
        
        # 转义单引号
        value = value.replace("'", "''")
        
        return value


class XSSProtection:
    """
    XSS 防护工具
    用于检测和清理潜在的 XSS 攻击
    """
    
    # XSS 常见模式
    XSS_PATTERNS = [
        r'<script[^>]*>.*?</script>',
        r'<iframe[^>]*>.*?</iframe>',
        r'javascript:',
        r'on\w+\s*=',
        r'<img[^>]*src\s*=\s*["\']?javascript:',
        r'<svg[^>]*onload\s*=',
        r'<body[^>]*onload\s*=',
        r'<input[^>]*onfocus\s*=',
        r'<select[^>]*onchange\s*=',
        r'<textarea[^>]*onfocus\s*=',
        r'<form[^>]*on submit\s*=',
        r'<link[^>]*href\s*=\s*["\']?javascript:',
        r'<meta[^>]*http-equiv\s*=\s*["\']?refresh',
    ]
    
    @classmethod
    def check_string(cls, value: str) -> bool:
        """
        检查字符串是否包含潜在的 XSS 代码
        
        Args:
            value: 要检查的字符串
            
        Returns:
            bool: True 表示安全，False 表示可能包含 XSS
            
        Raises:
            ValidationError: 如果检测到 XSS 模式
        """
        if not value or not isinstance(value, str):
            return True
        
        for pattern in cls.XSS_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE | re.DOTALL):
                raise ValidationError(_('输入包含不安全的字符，可能存在 XSS 攻击风险'))
        
        return True
    
    @classmethod
    def sanitize_string(cls, value: str) -> str:
        """
        清理字符串，移除潜在的 XSS 代码
        
        Args:
            value: 要清理的字符串
            
        Returns:
            str: 清理后的字符串
        """
        if not value:
            return value
        
        # 移除 script 标签
        value = re.sub(r'<script[^>]*>.*?</script>', '', value, flags=re.IGNORECASE | re.DOTALL)
        
        # 移除 iframe 标签
        value = re.sub(r'<iframe[^>]*>.*?</iframe>', '', value, flags=re.IGNORECASE | re.DOTALL)
        
        # 移除 javascript: 协议
        value = re.sub(r'javascript:', '', value, flags=re.IGNORECASE)
        
        # 移除事件处理器
        value = re.sub(r'on\w+\s*=', '', value, flags=re.IGNORECASE)
        
        # HTML 转义（基本）
        value = value.replace('<', '&lt;')
        value = value.replace('>', '&gt;')
        value = value.replace('"', '&quot;')
        value = value.replace("'", '&#x27;')
        value = value.replace('/', '&#x2F;')
        
        return value


def check_sql_injection(value: str) -> bool:
    """
    检查 SQL 注入（便捷函数）
    
    Args:
        value: 要检查的字符串
        
    Returns:
        bool: True 表示安全
        
    Raises:
        ValidationError: 如果检测到 SQL 注入
    """
    return SQLInjectionChecker.check_string(value)


def check_xss(value: str) -> bool:
    """
    检查 XSS（便捷函数）
    
    Args:
        value: 要检查的字符串
        
    Returns:
        bool: True 表示安全
        
    Raises:
        ValidationError: 如果检测到 XSS
    """
    return XSSProtection.check_string(value)


def sanitize_user_input(value: str) -> str:
    """
    清理用户输入（同时检查 SQL 注入和 XSS）
    
    Args:
        value: 要清理的字符串
        
    Returns:
        str: 清理后的字符串
    """
    if not value:
        return value
    
    # 先检查
    SQLInjectionChecker.check_string(value)
    XSSProtection.check_string(value)
    
    # 再清理
    value = SQLInjectionChecker.sanitize_string(value)
    value = XSSProtection.sanitize_string(value)
    
    return value

