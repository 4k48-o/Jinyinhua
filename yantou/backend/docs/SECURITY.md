# 安全加固文档

## 概述

本文档描述了项目中实现的安全加固措施，包括 HTTPS 配置、CSRF 保护、XSS 防护、安全响应头、SQL 注入防护、密码策略和敏感数据加密。

## 1. HTTPS 配置（生产环境）

### 配置位置
- `config/settings/production.py`

### 配置项
- `SECURE_SSL_REDIRECT`: 强制 HTTPS 重定向（生产环境必须启用）
- `SECURE_HSTS_SECONDS`: HSTS 有效期（默认 1 年）
- `SECURE_HSTS_INCLUDE_SUBDOMAINS`: 包含子域名
- `SECURE_HSTS_PRELOAD`: 启用 HSTS 预加载

### 使用方法
在 `.env` 文件中配置：
```bash
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

## 2. CSRF 保护

### 配置位置
- `config/settings/base.py` - `MIDDLEWARE` 中包含 `CsrfViewMiddleware`
- `config/settings/production.py` - CSRF Cookie 安全配置

### 配置项
- `CSRF_COOKIE_SECURE`: CSRF Cookie 仅通过 HTTPS 传输
- `CSRF_COOKIE_HTTPONLY`: CSRF Cookie 仅 HTTP 访问
- `CSRF_COOKIE_SAMESITE`: SameSite 策略（Lax）
- `CSRF_TRUSTED_ORIGINS`: 信任的来源列表

### 使用方法
在 `.env` 文件中配置：
```bash
CSRF_COOKIE_SECURE=True
CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
```

## 3. XSS 防护

### 实现位置
- `utils/security.py` - `XSSProtection` 类
- `middleware/security.py` - `SecurityHeadersMiddleware` 添加安全响应头
- `config/settings/production.py` - XSS 相关配置

### 功能
- 检测潜在的 XSS 代码
- 清理用户输入
- 添加安全响应头（`X-XSS-Protection`, `X-Content-Type-Options`）

### 使用方法
```python
from utils.security import check_xss, XSSProtection

# 检查 XSS
check_xss(user_input)

# 清理用户输入
cleaned = XSSProtection.sanitize_string(user_input)
```

## 4. 安全响应头

### 实现位置
- `middleware/security.py` - `SecurityHeadersMiddleware`

### 添加的响应头
- `X-Frame-Options`: 防止点击劫持
- `X-Content-Type-Options`: 防止 MIME 类型嗅探
- `X-XSS-Protection`: XSS 保护
- `Referrer-Policy`: 控制 referrer 信息
- `Permissions-Policy`: 控制浏览器功能

### 配置
在 `config/settings/production.py` 中配置：
```python
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
SECURE_PERMISSIONS_POLICY = {
    'geolocation': [],
    'camera': [],
    'microphone': [],
}
```

## 5. SQL 注入防护

### 实现位置
- `utils/security.py` - `SQLInjectionChecker` 类
- `middleware/security.py` - `SQLInjectionProtectionMiddleware`

### 功能
- 检测潜在的 SQL 注入代码
- 自动检查请求参数
- 清理用户输入

### 使用方法
```python
from utils.security import check_sql_injection, SQLInjectionChecker

# 检查 SQL 注入
check_sql_injection(user_input)

# 清理用户输入
cleaned = SQLInjectionChecker.sanitize_string(user_input)
```

### 中间件
`SQLInjectionProtectionMiddleware` 会自动检查所有 GET 和 POST 请求参数。

## 6. 密码策略

### 配置位置
- `config/settings/base.py` - `AUTH_PASSWORD_VALIDATORS`
- `config/settings/base.py` - 密码策略配置项

### 验证器
1. **UserAttributeSimilarityValidator**: 检查密码与用户属性的相似度
2. **MinimumLengthValidator**: 最小长度验证（8 位）
3. **CommonPasswordValidator**: 检查常见密码
4. **NumericPasswordValidator**: 检查纯数字密码

### 策略配置
```python
PASSWORD_MIN_LENGTH = 8
PASSWORD_REQUIRE_UPPERCASE = True
PASSWORD_REQUIRE_LOWERCASE = True
PASSWORD_REQUIRE_DIGITS = True
PASSWORD_REQUIRE_SPECIAL = True
PASSWORD_MAX_AGE_DAYS = 90
PASSWORD_HISTORY_COUNT = 5
```

### 自定义验证
`utils/validators.py` 中的 `validate_password_strength()` 函数提供了额外的密码强度验证。

## 7. 敏感数据加密

### 实现位置
- `utils/encryption.py` - `DataEncryption` 类

### 功能
- 使用 Fernet 对称加密算法
- 从 Django SECRET_KEY 派生加密密钥
- 提供加密和解密函数

### 使用方法
```python
from utils.encryption import encrypt_sensitive_data, decrypt_sensitive_data, DataEncryption

# 便捷函数
encrypted = encrypt_sensitive_data("敏感数据")
decrypted = decrypt_sensitive_data(encrypted)

# 使用类
encryptor = DataEncryption()
encrypted = encryptor.encrypt("敏感数据")
decrypted = encryptor.decrypt(encrypted)
```

### 注意事项
- 加密密钥从 `SECRET_KEY` 派生，确保 `SECRET_KEY` 的安全性
- 生产环境建议使用独立的加密密钥
- 加密后的数据是 base64 编码的字符串

## 8. 安全中间件

### SecurityHeadersMiddleware
自动为所有响应添加安全相关的 HTTP 头。

### SQLInjectionProtectionMiddleware
自动检查请求参数中的潜在 SQL 注入代码。

### 配置
在 `config/settings/base.py` 的 `MIDDLEWARE` 中已配置：
```python
'middleware.security.SQLInjectionProtectionMiddleware',
'middleware.security.SecurityHeadersMiddleware',
```

## 9. 安全最佳实践

### 开发环境
- 使用 `DEBUG=False` 进行安全测试
- 定期检查安全配置
- 使用安全工具扫描漏洞

### 生产环境
1. **必须启用 HTTPS**
   ```bash
   SECURE_SSL_REDIRECT=True
   ```

2. **配置安全 Cookie**
   ```bash
   SESSION_COOKIE_SECURE=True
   CSRF_COOKIE_SECURE=True
   ```

3. **配置 CSRF 信任来源**
   ```bash
   CSRF_TRUSTED_ORIGINS=https://yourdomain.com
   ```

4. **使用强 SECRET_KEY**
   - 至少 50 个字符
   - 包含大小写字母、数字和特殊字符
   - 不要使用默认值

5. **定期更新依赖**
   ```bash
   pip list --outdated
   pip install --upgrade <package>
   ```

6. **监控安全日志**
   - 检查 SQL 注入尝试
   - 检查 XSS 攻击尝试
   - 检查登录失败记录

## 10. 安全检查清单

- [ ] HTTPS 已启用（生产环境）
- [ ] CSRF 保护已配置
- [ ] XSS 防护已启用
- [ ] 安全响应头已配置
- [ ] SQL 注入防护已启用
- [ ] 密码策略已配置
- [ ] 敏感数据加密已实现
- [ ] SECRET_KEY 已更新（生产环境）
- [ ] 安全中间件已启用
- [ ] 日志记录已配置

## 11. 相关文件

- `config/settings/production.py` - 生产环境安全配置
- `config/settings/base.py` - 基础安全配置
- `utils/encryption.py` - 数据加密工具
- `utils/security.py` - 安全工具函数
- `middleware/security.py` - 安全中间件
- `env.example` - 环境变量配置示例

