# 测试说明文档

## 📋 概述

本文档说明项目的测试结构、运行方法和测试策略。

## 📁 测试目录结构

```
test/
├── __init__.py
├── conftest.py              # pytest 全局配置和 fixtures
├── unit/                    # 单元测试
│   ├── __init__.py
│   ├── test_helpers.py     # 工具函数测试 ✅
│   └── test_validators.py  # 验证器测试 ✅
├── integration/             # 集成测试
│   └── __init__.py
├── api/                     # API 测试
│   ├── __init__.py
│   ├── test_health.py      # 健康检查 API 测试 ✅
│   └── README.md           # API 测试说明
├── performance/             # 性能测试
│   └── __init__.py
└── security/                # 安全测试
    └── __init__.py
```

## 🚀 运行测试

### 运行所有测试

```bash
pytest
# 或
pytest test/
```

### 运行特定类型的测试

```bash
# 单元测试
pytest test/unit/
pytest -m unit

# API 测试
pytest test/api/
pytest -m api

# 集成测试
pytest test/integration/
pytest -m integration
```

### 运行特定测试文件

```bash
pytest test/unit/test_helpers.py
pytest test/api/test_health.py
```

### 运行特定测试用例

```bash
pytest test/unit/test_helpers.py::TestStringGeneration::test_generate_random_string_default
```

### 生成覆盖率报告

```bash
# 终端报告
pytest --cov --cov-report=term-missing

# HTML 报告
pytest --cov --cov-report=html
# 然后打开 htmlcov/index.html

# XML 报告（用于 CI/CD）
pytest --cov --cov-report=xml
```

### 其他有用的选项

```bash
# 详细输出
pytest -v

# 显示打印输出
pytest -s

# 只运行失败的测试
pytest --lf

# 并行运行（需要 pytest-xdist）
pytest -n auto

# 显示最慢的 10 个测试
pytest --durations=10
```

## 📊 测试统计

### 当前测试状态

- ✅ **单元测试**: 65 个测试用例
  - `test_helpers.py`: 33 个测试
  - `test_validators.py`: 32 个测试
- ✅ **API 测试**: 7 个测试用例
  - `test_health.py`: 7 个测试
- **总计**: 72 个测试用例，全部通过 ✅

### 代码覆盖率

- **总体覆盖率**: 67%
- **utils/helpers.py**: 84%
- **utils/validators.py**: 100%
- **config/urls_health.py**: 85%

## 🧪 测试 Fixtures

在 `conftest.py` 中定义了以下 fixtures：

- `api_client`: 未认证的 API 客户端
- `user`: 测试用户
- `admin_user`: 管理员用户
- `authenticated_client`: 已认证的 API 客户端（JWT）
- `admin_client`: 管理员 API 客户端
- `token_pair`: JWT Token 对
- `admin_token_pair`: 管理员 JWT Token 对
- `mock_redis`: Mock Redis 用于测试

## 📝 编写测试

### 测试命名规范

- 测试文件: `test_*.py`
- 测试类: `Test*`
- 测试方法: `test_*`

### 测试结构

遵循 AAA 模式（Arrange-Act-Assert）：

```python
def test_example(self, api_client):
    # Arrange: 准备测试数据
    data = {'key': 'value'}
    
    # Act: 执行操作
    response = api_client.post('/api/v1/endpoint/', data)
    
    # Assert: 验证结果
    assert response.status_code == 200
    assert response.json()['key'] == 'value'
```

### 使用标记

```python
@pytest.mark.unit
@pytest.mark.requires_db
@pytest.mark.slow
def test_slow_function(self):
    pass
```

## ✅ 测试清单

### 已完成的测试

- [x] 健康检查 API 测试
- [x] 工具函数单元测试
  - [x] 字符串生成函数
  - [x] 哈希函数
  - [x] 日期时间函数
  - [x] 掩码函数
  - [x] 安全转换函数
  - [x] 列表函数
  - [x] 缓存键函数
- [x] 验证器单元测试
  - [x] 手机号验证
  - [x] 邮箱验证
  - [x] 密码强度验证
  - [x] 用户名验证
  - [x] 中文姓名验证
  - [x] 身份证号验证
  - [x] URL 验证

### 待实现的测试

- [ ] 认证 API 测试（Phase 2）
- [ ] 用户管理 API 测试（Phase 3）
- [ ] 权限管理 API 测试（Phase 4）
- [ ] JWT 工具函数测试
- [ ] 中间件测试
- [ ] 集成测试
- [ ] 性能测试
- [ ] 安全测试

## 🔧 测试配置

### pytest.ini

主要配置：
- Django 设置: `config.settings.testing`
- 覆盖率目标: 70%（当前临时设为 0）
- 测试标记: unit, integration, api, performance, security

### 测试环境

使用 `config/settings/testing.py`：
- 内存数据库（SQLite）
- 禁用密码验证
- 日志级别: WARNING

## 📚 相关文档

- [API 测试计划](../docs/API_TEST_PLAN.md)
- [API 测试说明](api/README.md)
- [pytest 文档](https://docs.pytest.org/)
- [pytest-django 文档](https://pytest-django.readthedocs.io/)

## 🎯 测试目标

- **覆盖率目标**: ≥ 70%（总体），≥ 80%（单元测试），100%（API 端点）
- **测试通过率**: 100%
- **测试执行时间**: < 5 分钟（所有测试）

## 📝 更新日志

- **2025-12-06**: 初始测试框架搭建
  - 创建测试目录结构
  - 配置 pytest
  - 编写健康检查 API 测试
  - 编写工具函数单元测试
  - 编写验证器单元测试

