"""
工具函数单元测试
测试 utils/helpers.py 中的辅助函数
"""
import pytest
from datetime import datetime, timedelta
from django.utils import timezone
from utils.helpers import (
    generate_random_string,
    generate_code,
    md5_hash,
    sha256_hash,
    format_datetime,
    parse_datetime,
    get_time_range,
    mask_phone,
    mask_email,
    safe_int,
    safe_float,
    chunk_list,
    get_cache_key,
)


@pytest.mark.unit
class TestStringGeneration:
    """字符串生成函数测试"""
    
    def test_generate_random_string_default(self):
        """测试生成默认长度的随机字符串"""
        result = generate_random_string()
        assert isinstance(result, str)
        assert len(result) == 32
    
    def test_generate_random_string_custom_length(self):
        """测试生成指定长度的随机字符串"""
        result = generate_random_string(16)
        assert len(result) == 16
    
    def test_generate_random_string_with_special(self):
        """测试包含特殊字符的随机字符串"""
        result = generate_random_string(20, include_special=True)
        assert len(result) == 20
        # 验证包含特殊字符（至少有一个）
        has_special = any(c in result for c in '!@#$%^&*()')
        assert has_special
    
    def test_generate_code_default(self):
        """测试生成默认长度的验证码"""
        result = generate_code()
        assert isinstance(result, str)
        assert len(result) == 6
        assert result.isdigit()
    
    def test_generate_code_custom_length(self):
        """测试生成指定长度的验证码"""
        result = generate_code(4)
        assert len(result) == 4
        assert result.isdigit()


@pytest.mark.unit
class TestHashFunctions:
    """哈希函数测试"""
    
    def test_md5_hash(self):
        """测试 MD5 哈希"""
        text = "test"
        result = md5_hash(text)
        assert isinstance(result, str)
        assert len(result) == 32  # MD5 是 32 位十六进制
        assert result == "098f6bcd4621d373cade4e832627b4f6"
    
    def test_md5_hash_empty_string(self):
        """测试空字符串的 MD5 哈希"""
        result = md5_hash("")
        assert isinstance(result, str)
        assert len(result) == 32
    
    def test_sha256_hash(self):
        """测试 SHA256 哈希"""
        text = "test"
        result = sha256_hash(text)
        assert isinstance(result, str)
        assert len(result) == 64  # SHA256 是 64 位十六进制
    
    def test_sha256_hash_empty_string(self):
        """测试空字符串的 SHA256 哈希"""
        result = sha256_hash("")
        assert isinstance(result, str)
        assert len(result) == 64


@pytest.mark.unit
class TestDateTimeFunctions:
    """日期时间函数测试"""
    
    def test_format_datetime_default(self):
        """测试默认格式的日期时间格式化"""
        dt = datetime(2025, 12, 6, 15, 30, 45)
        result = format_datetime(dt)
        assert result == "2025-12-06 15:30:45"
    
    def test_format_datetime_custom_format(self):
        """测试自定义格式的日期时间格式化"""
        dt = datetime(2025, 12, 6, 15, 30, 45)
        result = format_datetime(dt, '%Y/%m/%d')
        assert result == "2025/12/06"
    
    def test_format_datetime_none(self):
        """测试 None 值的日期时间格式化"""
        result = format_datetime(None)
        assert result == ""
    
    def test_parse_datetime_success(self):
        """测试日期时间字符串解析成功"""
        result = parse_datetime("2025-12-06 15:30:45")
        assert isinstance(result, datetime)
        assert result.year == 2025
        assert result.month == 12
        assert result.day == 6
    
    def test_parse_datetime_invalid(self):
        """测试无效日期时间字符串解析"""
        result = parse_datetime("invalid")
        assert result is None
    
    def test_parse_datetime_custom_format(self):
        """测试自定义格式的日期时间解析"""
        result = parse_datetime("2025/12/06", '%Y/%m/%d')
        assert isinstance(result, datetime)
        assert result.year == 2025
    
    def test_get_time_range(self):
        """测试获取时间范围"""
        start, end = get_time_range(days=1, hours=2, minutes=30)
        assert isinstance(start, datetime)
        assert isinstance(end, datetime)
        assert end > start
        # 验证时间差大约为 1 天 2 小时 30 分钟
        diff = end - start
        assert diff >= timedelta(days=1, hours=2, minutes=29)
        assert diff <= timedelta(days=1, hours=2, minutes=31)


@pytest.mark.unit
class TestMaskFunctions:
    """掩码函数测试"""
    
    def test_mask_phone(self):
        """测试手机号掩码"""
        phone = "13812345678"
        result = mask_phone(phone)
        assert result == "138****5678"
        assert len(result) == len(phone)
    
    def test_mask_phone_short(self):
        """测试短手机号掩码"""
        phone = "1381234"
        result = mask_phone(phone)
        # 短号码可能不会正确掩码，但不应报错
        assert isinstance(result, str)
    
    def test_mask_email(self):
        """测试邮箱掩码"""
        email = "test@example.com"
        result = mask_email(email)
        assert "@" in result
        assert "example.com" in result
        assert result.startswith("tes")
    
    def test_mask_email_short_local(self):
        """测试短本地部分的邮箱掩码"""
        email = "ab@example.com"
        result = mask_email(email)
        assert "@" in result
        assert "example.com" in result


@pytest.mark.unit
class TestSafeConversion:
    """安全转换函数测试"""
    
    def test_safe_int_valid(self):
        """测试有效的整数转换"""
        assert safe_int("123") == 123
        assert safe_int(123) == 123
        assert safe_int(123.5) == 123
    
    def test_safe_int_invalid(self):
        """测试无效的整数转换"""
        assert safe_int("invalid") == 0
        assert safe_int(None) == 0
        assert safe_int([]) == 0
    
    def test_safe_int_default(self):
        """测试带默认值的整数转换"""
        assert safe_int("invalid", default=999) == 999
        assert safe_int(None, default=999) == 999
    
    def test_safe_float_valid(self):
        """测试有效的浮点数转换"""
        assert safe_float("123.45") == 123.45
        assert safe_float(123.45) == 123.45
        assert safe_float(123) == 123.0
    
    def test_safe_float_invalid(self):
        """测试无效的浮点数转换"""
        assert safe_float("invalid") == 0.0
        assert safe_float(None) == 0.0
    
    def test_safe_float_default(self):
        """测试带默认值的浮点数转换"""
        assert safe_float("invalid", default=99.9) == 99.9


@pytest.mark.unit
class TestListFunctions:
    """列表函数测试"""
    
    def test_chunk_list(self):
        """测试列表分块"""
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        result = chunk_list(lst, 3)
        assert len(result) == 3
        assert result[0] == [1, 2, 3]
        assert result[1] == [4, 5, 6]
        assert result[2] == [7, 8, 9]
    
    def test_chunk_list_uneven(self):
        """测试不均匀分块"""
        lst = [1, 2, 3, 4, 5]
        result = chunk_list(lst, 2)
        assert len(result) == 3
        assert result[0] == [1, 2]
        assert result[1] == [3, 4]
        assert result[2] == [5]
    
    def test_chunk_list_empty(self):
        """测试空列表分块"""
        result = chunk_list([], 3)
        assert result == []


@pytest.mark.unit
class TestCacheKey:
    """缓存键函数测试"""
    
    def test_get_cache_key_simple(self):
        """测试简单缓存键生成"""
        key = get_cache_key("prefix")
        assert key == "prefix"
    
    def test_get_cache_key_with_args(self):
        """测试带参数的缓存键生成"""
        key = get_cache_key("prefix", "arg1", "arg2")
        assert "prefix" in key
        assert "arg1" in key
        assert "arg2" in key
    
    def test_get_cache_key_with_kwargs(self):
        """测试带关键字参数的缓存键生成"""
        key = get_cache_key("prefix", key1="value1", key2="value2")
        assert "prefix" in key
        assert "key1:value1" in key
        assert "key2:value2" in key
    
    def test_get_cache_key_complex(self):
        """测试复杂缓存键生成"""
        key = get_cache_key("prefix", "arg1", key1="value1")
        assert "prefix" in key
        assert "arg1" in key
        assert "key1:value1" in key

