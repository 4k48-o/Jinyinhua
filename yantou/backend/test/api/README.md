# API 测试说明

## 测试文件结构

```
test/api/
├── __init__.py
├── test_health.py          # 健康检查 API 测试
├── test_auth.py            # 认证 API 测试（待实现）
├── test_users.py           # 用户管理 API 测试（待实现）
├── test_permissions.py     # 权限管理 API 测试（待实现）
└── README.md              # 本文件
```

## 运行测试

### 运行所有 API 测试

```bash
pytest test/api/
```

### 运行特定测试文件

```bash
pytest test/api/test_health.py
```

### 运行特定测试用例

```bash
pytest test/api/test_health.py::TestHealthCheckAPI::test_health_check_success
```

### 带标记运行

```bash
# 只运行 API 测试
pytest -m api

# 运行慢速测试
pytest -m slow
```

### 生成覆盖率报告

```bash
pytest test/api/ --cov=config --cov-report=html
```

## 测试用例编写规范

### 1. 测试类命名

使用 `Test` 开头，描述测试的 API 模块：

```python
class TestHealthCheckAPI:
    """健康检查 API 测试类"""
    pass
```

### 2. 测试方法命名

使用 `test_` 开头，描述测试场景：

```python
def test_health_check_success(self, api_client):
    """测试健康检查成功场景"""
    pass
```

### 3. 使用 Fixtures

优先使用 `conftest.py` 中定义的 fixtures：

- `api_client`: 未认证的 API 客户端
- `authenticated_client`: 已认证的 API 客户端
- `user`: 测试用户
- `admin_user`: 管理员用户

### 4. 测试结构

遵循 AAA 模式（Arrange-Act-Assert）：

```python
def test_example(self, api_client):
    # Arrange: 准备测试数据
    data = {'key': 'value'}
    
    # Act: 执行 API 调用
    response = api_client.post('/api/v1/endpoint/', data)
    
    # Assert: 验证结果
    assert response.status_code == 200
    assert response.json()['key'] == 'value'
```

### 5. 使用标记

为测试用例添加适当的标记：

```python
@pytest.mark.api
@pytest.mark.requires_db
@pytest.mark.slow
def test_slow_api(self, api_client):
    pass
```

## 已实现的测试

### ✅ 健康检查 API (`test_health.py`)

- ✅ `test_health_check_success` - 测试 `/health/` 端点
- ✅ `test_api_health_check_success` - 测试 `/api/v1/health/` 端点
- ✅ `test_health_check_post_method` - 测试 POST 方法
- ✅ `test_health_check_response_format` - 测试响应格式
- ✅ `test_health_check_database_connection` - 测试数据库连接检查
- ✅ `test_health_check_without_authentication` - 测试不需要认证
- ✅ `test_health_check_cors_headers` - 测试 CORS 头

## 待实现的测试

### ⏳ 认证 API (`test_auth.py`) - Phase 2

- [ ] 用户注册测试
- [ ] 用户登录测试
- [ ] Token 刷新测试
- [ ] 用户登出测试
- [ ] 密码重置测试

### ⏳ 用户管理 API (`test_users.py`) - Phase 3

- [ ] 用户列表查询测试
- [ ] 用户详情查询测试
- [ ] 用户创建测试
- [ ] 用户更新测试
- [ ] 用户删除测试

### ⏳ 权限管理 API (`test_permissions.py`) - Phase 4

- [ ] 角色管理测试
- [ ] 权限管理测试
- [ ] 用户角色分配测试
- [ ] 角色权限分配测试

## 注意事项

1. **测试隔离**: 每个测试用例应该是独立的，不依赖其他测试的执行顺序
2. **数据清理**: 使用 `db` fixture 确保测试数据自动清理
3. **Mock 使用**: 对于外部依赖，使用 `mock_redis` 等 fixtures
4. **性能考虑**: 标记慢速测试，避免影响开发效率
5. **覆盖率**: 目标是 100% API 端点覆盖

