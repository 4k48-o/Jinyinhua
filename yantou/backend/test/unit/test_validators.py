"""
验证器单元测试
测试 utils/validators.py 中的验证函数
"""
import pytest
from django.core.exceptions import ValidationError
from utils.validators import (
    validate_phone,
    validate_email,
    validate_password_strength,
    validate_username,
    validate_chinese_name,
    validate_id_card,
    validate_url,
)


@pytest.mark.unit
class TestPhoneValidator:
    """手机号验证器测试"""
    
    def test_valid_phone(self):
        """测试有效的手机号"""
        assert validate_phone("13812345678") is True
        assert validate_phone("15912345678") is True
        assert validate_phone("18612345678") is True
    
    def test_invalid_phone_short(self):
        """测试过短的手机号"""
        with pytest.raises(ValidationError):
            validate_phone("1381234567")
    
    def test_invalid_phone_long(self):
        """测试过长的手机号"""
        with pytest.raises(ValidationError):
            validate_phone("138123456789")
    
    def test_invalid_phone_wrong_start(self):
        """测试错误开头的手机号"""
        with pytest.raises(ValidationError):
            validate_phone("12812345678")  # 第二位不是 3-9
    
    def test_invalid_phone_contains_letters(self):
        """测试包含字母的手机号"""
        with pytest.raises(ValidationError):
            validate_phone("1381234567a")


@pytest.mark.unit
class TestEmailValidator:
    """邮箱验证器测试"""
    
    def test_valid_email(self):
        """测试有效的邮箱"""
        assert validate_email("test@example.com") is True
        assert validate_email("user.name@example.co.uk") is True
        assert validate_email("test+tag@example.com") is True
    
    def test_invalid_email_no_at(self):
        """测试没有 @ 的邮箱"""
        with pytest.raises(ValidationError):
            validate_email("testexample.com")
    
    def test_invalid_email_no_domain(self):
        """测试没有域名的邮箱"""
        with pytest.raises(ValidationError):
            validate_email("test@")
    
    def test_invalid_email_no_tld(self):
        """测试没有顶级域名的邮箱"""
        with pytest.raises(ValidationError):
            validate_email("test@example")


@pytest.mark.unit
class TestPasswordStrengthValidator:
    """密码强度验证器测试"""
    
    def test_valid_password(self):
        """测试符合要求的密码"""
        assert validate_password_strength("Test123!") is True
        assert validate_password_strength("MyP@ssw0rd") is True
    
    def test_invalid_password_too_short(self):
        """测试过短的密码"""
        with pytest.raises(ValidationError, match="至少为8位"):
            validate_password_strength("Test1!")
    
    def test_invalid_password_no_lowercase(self):
        """测试没有小写字母的密码"""
        with pytest.raises(ValidationError, match="小写字母"):
            validate_password_strength("TEST123!")
    
    def test_invalid_password_no_uppercase(self):
        """测试没有大写字母的密码"""
        with pytest.raises(ValidationError, match="大写字母"):
            validate_password_strength("test123!")
    
    def test_invalid_password_no_digit(self):
        """测试没有数字的密码"""
        with pytest.raises(ValidationError, match="数字"):
            validate_password_strength("TestPass!")
    
    def test_invalid_password_no_special(self):
        """测试没有特殊字符的密码"""
        with pytest.raises(ValidationError, match="特殊字符"):
            validate_password_strength("Test1234")


@pytest.mark.unit
class TestUsernameValidator:
    """用户名验证器测试"""
    
    def test_valid_username(self):
        """测试有效的用户名"""
        assert validate_username("testuser") is True
        assert validate_username("test_user") is True
        assert validate_username("test-user") is True
        assert validate_username("test123") is True
    
    def test_invalid_username_too_short(self):
        """测试过短的用户名"""
        with pytest.raises(ValidationError, match="3-20位"):
            validate_username("ab")
    
    def test_invalid_username_too_long(self):
        """测试过长的用户名"""
        with pytest.raises(ValidationError, match="3-20位"):
            validate_username("a" * 21)
    
    def test_invalid_username_special_chars(self):
        """测试包含不允许字符的用户名"""
        with pytest.raises(ValidationError):
            validate_username("test@user")
        with pytest.raises(ValidationError):
            validate_username("test user")


@pytest.mark.unit
class TestChineseNameValidator:
    """中文姓名验证器测试"""
    
    def test_valid_chinese_name(self):
        """测试有效的中文姓名"""
        assert validate_chinese_name("张三") is True
        assert validate_chinese_name("李四") is True
        assert validate_chinese_name("王五") is True
        assert validate_chinese_name("欧阳修") is True
    
    def test_invalid_chinese_name_too_short(self):
        """测试过短的中文姓名"""
        with pytest.raises(ValidationError):
            validate_chinese_name("张")
    
    def test_invalid_chinese_name_too_long(self):
        """测试过长的中文姓名"""
        with pytest.raises(ValidationError):
            validate_chinese_name("张" * 11)
    
    def test_invalid_chinese_name_contains_english(self):
        """测试包含英文字母的中文姓名"""
        with pytest.raises(ValidationError):
            validate_chinese_name("张a")


@pytest.mark.unit
class TestIdCardValidator:
    """身份证号验证器测试"""
    
    def test_valid_id_card(self):
        """测试有效的身份证号"""
        # 注意：这里只是格式验证，不验证校验位
        assert validate_id_card("110101199003075678") is True
    
    def test_invalid_id_card_short(self):
        """测试过短的身份证号"""
        with pytest.raises(ValidationError):
            validate_id_card("11010119900307567")
    
    def test_invalid_id_card_long(self):
        """测试过长的身份证号"""
        with pytest.raises(ValidationError):
            validate_id_card("1101011990030756789")
    
    def test_invalid_id_card_wrong_format(self):
        """测试格式错误的身份证号"""
        with pytest.raises(ValidationError):
            validate_id_card("123456789012345678")


@pytest.mark.unit
class TestUrlValidator:
    """URL 验证器测试"""
    
    def test_valid_url_http(self):
        """测试有效的 HTTP URL"""
        assert validate_url("http://example.com") is True
        assert validate_url("http://example.com/path") is True
    
    def test_valid_url_https(self):
        """测试有效的 HTTPS URL"""
        assert validate_url("https://example.com") is True
    
    def test_valid_url_with_query(self):
        """测试带查询参数的 URL"""
        assert validate_url("https://example.com?key=value") is True
    
    def test_invalid_url_no_protocol(self):
        """测试没有协议的 URL"""
        with pytest.raises(ValidationError):
            validate_url("example.com")
    
    def test_invalid_url_wrong_protocol(self):
        """测试错误协议的 URL"""
        with pytest.raises(ValidationError):
            validate_url("ftp://example.com")

