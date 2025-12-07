"""
敏感数据加密工具
提供数据加密和解密功能
"""
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class DataEncryption:
    """
    数据加密类
    使用 Fernet 对称加密算法
    """
    
    def __init__(self, key=None):
        """
        初始化加密器
        
        Args:
            key: 加密密钥（如果为 None，则从 settings.SECRET_KEY 生成）
        """
        if key is None:
            key = self._generate_key_from_secret()
        elif isinstance(key, str):
            key = key.encode()
        
        self.cipher = Fernet(key)
    
    def _generate_key_from_secret(self):
        """
        从 Django SECRET_KEY 生成加密密钥
        
        Returns:
            bytes: Fernet 密钥
        """
        secret_key = settings.SECRET_KEY
        if not secret_key:
            raise ImproperlyConfigured('SECRET_KEY must be set for encryption')
        
        # 使用 PBKDF2 从 SECRET_KEY 派生密钥
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'yantou_encryption_salt',  # 生产环境应该使用随机盐
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(secret_key.encode()))
        return key
    
    def encrypt(self, data: str) -> str:
        """
        加密数据
        
        Args:
            data: 要加密的字符串
            
        Returns:
            str: 加密后的 base64 编码字符串
        """
        if not data:
            return ''
        
        encrypted = self.cipher.encrypt(data.encode('utf-8'))
        return base64.urlsafe_b64encode(encrypted).decode('utf-8')
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        解密数据
        
        Args:
            encrypted_data: 加密后的 base64 编码字符串
            
        Returns:
            str: 解密后的原始字符串
            
        Raises:
            ValueError: 如果解密失败
        """
        if not encrypted_data:
            return ''
        
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
            decrypted = self.cipher.decrypt(encrypted_bytes)
            return decrypted.decode('utf-8')
        except Exception as e:
            raise ValueError(f'解密失败: {str(e)}')
    
    @staticmethod
    def generate_key() -> str:
        """
        生成新的加密密钥
        
        Returns:
            str: base64 编码的密钥
        """
        key = Fernet.generate_key()
        return key.decode('utf-8')


def encrypt_sensitive_data(data: str) -> str:
    """
    加密敏感数据（便捷函数）
    
    Args:
        data: 要加密的字符串
        
    Returns:
        str: 加密后的字符串
    """
    encryptor = DataEncryption()
    return encryptor.encrypt(data)


def decrypt_sensitive_data(encrypted_data: str) -> str:
    """
    解密敏感数据（便捷函数）
    
    Args:
        encrypted_data: 加密后的字符串
        
    Returns:
        str: 解密后的原始字符串
    """
    encryptor = DataEncryption()
    return encryptor.decrypt(encrypted_data)

