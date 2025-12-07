# JWT 工具函数测试说明

## 当前状态

JWT 工具函数测试（`test/unit/test_jwt.py`）目前有 17 个测试用例，但由于以下原因暂时无法运行：

1. **需要 token_blacklist 迁移**: JWT Token 黑名单功能需要数据库表支持
2. **测试环境配置**: 需要在测试环境中正确配置 JWT 和数据库迁移

## 解决方案

### 方案 1: 在测试环境中运行迁移

在 `conftest.py` 或测试设置中自动运行迁移：

```python
@pytest.fixture(scope='session', autouse=True)
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        from django.core.management import call_command
        call_command('migrate', '--run-syncdb')
```

### 方案 2: 使用 pytest-django 的迁移功能

确保 `pytest.ini` 中配置了正确的数据库设置。

### 方案 3: Mock JWT 功能

对于不需要真实 JWT 的测试，可以使用 Mock。

## 测试用例列表

### TestCreateTokenPair (2 个测试)
- [ ] `test_create_token_pair_success` - 测试成功创建 Token 对
- [ ] `test_create_token_pair_different_tokens` - 测试每次创建的 Token 不同

### TestGetUserFromToken (4 个测试)
- [ ] `test_get_user_from_token_success` - 测试成功从 Token 获取用户
- [ ] `test_get_user_from_token_invalid` - 测试无效 Token
- [ ] `test_get_user_from_token_expired` - 测试过期 Token
- [ ] `test_get_user_from_token_nonexistent_user` - 测试 Token 中的用户不存在

### TestRefreshAccessToken (3 个测试)
- [ ] `test_refresh_access_token_success` - 测试成功刷新 Access Token
- [ ] `test_refresh_access_token_invalid` - 测试无效的 Refresh Token
- [ ] `test_refresh_access_token_different_access` - 测试刷新后 Access Token 不同

### TestBlacklistToken (3 个测试)
- [ ] `test_blacklist_token_success` - 测试成功将 Token 加入黑名单
- [ ] `test_blacklist_token_invalid` - 测试无效 Token 加入黑名单
- [ ] `test_blacklist_token_twice` - 测试重复加入黑名单

### TestGetTokenPayload (3 个测试)
- [ ] `test_get_token_payload_success` - 测试成功获取 Token 载荷
- [ ] `test_get_token_payload_invalid` - 测试无效 Token 的载荷
- [ ] `test_get_token_payload_user_id` - 测试 Token 载荷中的用户 ID

### TestIsTokenExpired (2 个测试)
- [ ] `test_is_token_expired_valid` - 测试有效 Token 未过期
- [ ] `test_is_token_expired_invalid` - 测试无效 Token

## 下一步

1. 修复测试环境配置，确保 token_blacklist 迁移正确运行
2. 或者将这些测试移到集成测试中，使用真实的数据库
3. 在 Phase 2 实现认证 API 时，一起完善 JWT 测试

