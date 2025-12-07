# API 测试计划

## 📋 文档信息

- **文档版本**: v1.0
- **创建日期**: 2025-12-06
- **最后更新**: 2025-12-06
- **测试负责人**: 待定
- **审核人**: 待定

---

## 1. 测试概述

### 1.1 测试目标

本测试计划旨在确保企业级应用后端 API 的：

- **功能性**: 所有 API 端点按预期工作
- **可靠性**: API 在各种场景下稳定运行
- **安全性**: 认证、授权和数据安全
- **性能**: 响应时间和吞吐量符合要求
- **兼容性**: 与前端和其他系统兼容
- **可维护性**: 代码质量和测试覆盖率

### 1.2 测试范围

#### 包含的测试范围

- ✅ **健康检查 API** (`/api/v1/health/`, `/health/`)
- ⏳ **认证 API** (`/api/v1/auth/`) - Phase 2
  - 用户注册
  - 用户登录
  - Token 刷新
  - 用户登出
  - 密码重置
- ⏳ **用户管理 API** (`/api/v1/users/`) - Phase 3
  - 用户列表查询
  - 用户详情查询
  - 用户创建
  - 用户更新
  - 用户删除（软删除）
  - 用户状态管理
- ⏳ **权限管理 API** (`/api/v1/roles/`, `/api/v1/permissions/`) - Phase 4
  - 角色管理
  - 权限管理
  - 用户角色分配
  - 角色权限分配
- ⏳ **通用功能 API** - Phase 5
  - 文件上传
  - 数据导出
  - 系统配置

#### 不包含的测试范围

- 前端界面测试
- 数据库性能测试（单独进行）
- 基础设施测试（服务器、网络等）
- 第三方服务集成测试（如邮件服务）

### 1.3 测试环境

#### 开发环境 (Development)

- **基础 URL**: `http://localhost:8000`
- **数据库**: PostgreSQL (本地 Docker)
- **Redis**: Redis (本地 Docker)
- **用途**: 开发阶段测试

#### 测试环境 (Testing)

- **基础 URL**: `http://test.example.com` (待配置)
- **数据库**: PostgreSQL (测试数据库)
- **Redis**: Redis (测试实例)
- **用途**: 集成测试和回归测试

#### 预生产环境 (Staging)

- **基础 URL**: `http://staging.example.com` (待配置)
- **数据库**: PostgreSQL (预生产数据库)
- **Redis**: Redis (预生产实例)
- **用途**: 上线前验证

---

## 2. 测试策略

### 2.1 测试类型

#### 2.1.1 单元测试 (Unit Tests)

- **目标**: 测试单个函数、方法或类的功能
- **工具**: `pytest` + `pytest-django`
- **覆盖率目标**: ≥ 80%
- **位置**: `test/unit/`

#### 2.1.2 集成测试 (Integration Tests)

- **目标**: 测试多个组件之间的交互
- **工具**: `pytest` + `pytest-django` + `factory-boy`
- **覆盖率目标**: ≥ 70%
- **位置**: `test/integration/`

#### 2.1.3 API 测试 (API Tests)

- **目标**: 测试 API 端点的完整功能
- **工具**: `pytest` + `pytest-django` + `requests` / `APIClient`
- **覆盖率目标**: 100% API 端点覆盖
- **位置**: `test/api/`

#### 2.1.4 性能测试 (Performance Tests)

- **目标**: 测试 API 响应时间和吞吐量
- **工具**: `pytest` + `locust` / `pytest-benchmark`
- **指标**:
  - 响应时间: P95 < 500ms, P99 < 1000ms
  - 吞吐量: ≥ 100 req/s
- **位置**: `test/performance/`

#### 2.1.5 安全测试 (Security Tests)

- **目标**: 测试 API 安全性和漏洞
- **工具**: `pytest` + 安全测试库
- **测试项**:
  - 认证绕过
  - 授权检查
  - SQL 注入
  - XSS 防护
  - CSRF 防护
- **位置**: `test/security/`

### 2.2 测试方法

#### 2.2.1 黑盒测试

- 基于 API 文档和需求进行测试
- 不关注内部实现细节
- 重点测试输入输出

#### 2.2.2 白盒测试

- 基于代码实现进行测试
- 关注代码逻辑和边界条件
- 提高代码覆盖率

#### 2.2.3 灰盒测试

- 结合黑盒和白盒测试
- 基于 API 文档和代码实现
- 平衡测试效率和覆盖率

### 2.3 测试数据管理

#### 2.3.1 测试数据策略

- **Fixtures**: 使用 `pytest fixtures` 管理测试数据
- **Factory**: 使用 `factory-boy` 生成测试数据
- **隔离**: 每个测试用例使用独立的数据
- **清理**: 测试后自动清理测试数据

#### 2.3.2 测试数据分类

- **基础数据**: 用户、角色、权限等基础数据
- **业务数据**: 业务相关的测试数据
- **边界数据**: 边界值和异常数据
- **性能数据**: 大量数据用于性能测试

---

## 3. 测试工具和框架

### 3.1 测试框架

#### 3.1.1 pytest

- **版本**: ≥ 7.4.4
- **用途**: 主要测试框架
- **优势**: 
  - 丰富的插件生态
  - 简洁的语法
  - 强大的断言
  - 详细的测试报告

#### 3.1.2 pytest-django

- **版本**: ≥ 4.8.0
- **用途**: Django 项目测试支持
- **功能**:
  - Django 测试数据库管理
  - 测试客户端支持
  - 数据库事务管理

#### 3.1.3 factory-boy

- **版本**: ≥ 3.3.0
- **用途**: 测试数据生成
- **功能**:
  - 模型工厂
  - 关联数据生成
  - 序列化数据生成

### 3.2 测试工具

#### 3.2.1 pytest-cov

- **版本**: ≥ 4.1.0
- **用途**: 代码覆盖率统计
- **报告格式**: HTML, XML, Terminal

#### 3.2.2 pytest-mock

- **版本**: ≥ 3.12.0
- **用途**: Mock 和 Stub
- **功能**: 模拟外部依赖

#### 3.2.3 requests

- **版本**: ≥ 2.31.0
- **用途**: HTTP 请求测试
- **功能**: API 端点测试

#### 3.2.4 locust

- **版本**: ≥ 2.17.0
- **用途**: 性能测试
- **功能**: 负载测试和压力测试

### 3.3 辅助工具

#### 3.3.1 HTTPie / curl

- **用途**: 手动 API 测试
- **场景**: 快速验证和调试

#### 3.3.2 Postman / Insomnia

- **用途**: API 测试集合管理
- **场景**: 团队协作和文档

#### 3.3.3 Coverage.py

- **用途**: 代码覆盖率分析
- **报告**: HTML 报告

---

## 4. 测试用例设计

### 4.1 测试用例模板

```python
"""
测试用例模板
"""
import pytest
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class TestExampleAPI(TestCase):
    """示例 API 测试类"""
    
    def setUp(self):
        """测试前置条件"""
        self.client = APIClient()
        # 初始化测试数据
    
    def test_api_endpoint_success(self):
        """测试 API 成功场景"""
        # Arrange: 准备测试数据
        # Act: 执行 API 调用
        # Assert: 验证结果
    
    def test_api_endpoint_validation_error(self):
        """测试 API 验证错误"""
        pass
    
    def test_api_endpoint_authentication_required(self):
        """测试 API 需要认证"""
        pass
    
    def test_api_endpoint_permission_denied(self):
        """测试 API 权限检查"""
        pass
    
    def tearDown(self):
        """测试后清理"""
        pass
```

### 4.2 测试用例分类

#### 4.2.1 功能测试用例

- **正常流程**: 测试 API 的正常使用场景
- **异常流程**: 测试错误处理和异常情况
- **边界测试**: 测试边界值和极限情况
- **组合测试**: 测试多个功能的组合使用

#### 4.2.2 非功能测试用例

- **性能测试**: 响应时间、吞吐量
- **安全测试**: 认证、授权、数据安全
- **兼容性测试**: 不同客户端和版本
- **可用性测试**: 错误处理和用户提示

### 4.3 API 测试用例清单

#### 4.3.1 健康检查 API

- [x] `GET /health/` - 健康检查成功
- [x] `GET /api/v1/health/` - API 健康检查成功
- [ ] 数据库连接失败时的处理
- [ ] Redis 连接失败时的处理

#### 4.3.2 认证 API (Phase 2)

- [ ] `POST /api/v1/auth/register/` - 用户注册
  - [ ] 正常注册
  - [ ] 用户名重复
  - [ ] 邮箱格式错误
  - [ ] 密码强度不足
  - [ ] 必填字段缺失
  
- [ ] `POST /api/v1/auth/login/` - 用户登录
  - [ ] 正常登录
  - [ ] 用户名不存在
  - [ ] 密码错误
  - [ ] 账户被禁用
  
- [ ] `POST /api/v1/auth/refresh/` - Token 刷新
  - [ ] 正常刷新
  - [ ] Token 过期
  - [ ] Token 无效
  - [ ] Token 在黑名单中
  
- [ ] `POST /api/v1/auth/logout/` - 用户登出
  - [ ] 正常登出
  - [ ] Token 无效
  - [ ] 未认证用户

#### 4.3.3 用户管理 API (Phase 3)

- [ ] `GET /api/v1/users/` - 用户列表
  - [ ] 正常查询
  - [ ] 分页功能
  - [ ] 搜索功能
  - [ ] 过滤功能
  - [ ] 排序功能
  - [ ] 权限检查
  
- [ ] `GET /api/v1/users/{id}/` - 用户详情
  - [ ] 正常查询
  - [ ] 用户不存在
  - [ ] 权限检查
  
- [ ] `POST /api/v1/users/` - 创建用户
  - [ ] 正常创建
  - [ ] 数据验证
  - [ ] 权限检查
  
- [ ] `PUT /api/v1/users/{id}/` - 更新用户
  - [ ] 正常更新
  - [ ] 部分更新
  - [ ] 数据验证
  - [ ] 权限检查
  
- [ ] `DELETE /api/v1/users/{id}/` - 删除用户
  - [ ] 软删除
  - [ ] 权限检查
  - [ ] 关联数据检查

#### 4.3.4 权限管理 API (Phase 4)

- [ ] 角色管理 API 测试用例
- [ ] 权限管理 API 测试用例
- [ ] 用户角色分配 API 测试用例
- [ ] 角色权限分配 API 测试用例

---

## 5. 测试环境配置

### 5.1 测试数据库配置

在 `config/settings/testing.py` 中配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'yantou_test_db',
        'USER': 'postgres',
        'PASSWORD': '0qww294e',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5.2 测试 Redis 配置

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://:sj1qaz@localhost:6379/1',  # 使用数据库 1
    }
}
```

### 5.3 pytest 配置

创建 `pytest.ini` 文件：

```ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings.testing
python_files = tests.py test_*.py *_tests.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --strict-markers
    --tb=short
    --cov=apps
    --cov=utils
    --cov=middleware
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=70
markers =
    unit: Unit tests
    integration: Integration tests
    api: API tests
    performance: Performance tests
    security: Security tests
    slow: Slow running tests
```

### 5.4 测试数据 Fixtures

创建 `test/conftest.py`：

```python
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    """API 客户端 Fixture"""
    return APIClient()


@pytest.fixture
def user():
    """测试用户 Fixture"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """已认证的 API 客户端"""
    api_client.force_authenticate(user=user)
    return api_client
```

---

## 6. 测试执行计划

### 6.1 测试阶段

#### 阶段 1: 单元测试 (持续进行)

- **时机**: 代码开发过程中
- **频率**: 每次提交前
- **目标**: 确保单个功能正确

#### 阶段 2: 集成测试 (功能完成后)

- **时机**: 功能模块开发完成后
- **频率**: 每个功能模块
- **目标**: 确保模块间协作正确

#### 阶段 3: API 测试 (API 完成后)

- **时机**: API 端点开发完成后
- **频率**: 每个 API 版本
- **目标**: 确保 API 功能完整

#### 阶段 4: 回归测试 (发布前)

- **时机**: 版本发布前
- **频率**: 每个发布版本
- **目标**: 确保新功能不影响旧功能

#### 阶段 5: 性能测试 (定期)

- **时机**: 性能关键功能完成后
- **频率**: 每月或重大更新后
- **目标**: 确保性能符合要求

#### 阶段 6: 安全测试 (定期)

- **时机**: 安全相关功能完成后
- **频率**: 每个发布版本
- **目标**: 确保安全性

### 6.2 测试执行流程

```
1. 开发人员编写代码
   ↓
2. 编写单元测试
   ↓
3. 运行单元测试 (pytest test/unit/)
   ↓
4. 代码审查
   ↓
5. 合并到主分支
   ↓
6. 运行集成测试 (pytest test/integration/)
   ↓
7. 运行 API 测试 (pytest test/api/)
   ↓
8. 生成测试报告
   ↓
9. 修复问题
   ↓
10. 回归测试
    ↓
11. 发布
```

### 6.3 测试命令

```bash
# 运行所有测试
pytest

# 运行特定类型的测试
pytest -m unit              # 单元测试
pytest -m integration      # 集成测试
pytest -m api              # API 测试
pytest -m performance      # 性能测试
pytest -m security         # 安全测试

# 运行特定目录的测试
pytest test/api/
pytest test/unit/

# 运行特定文件的测试
pytest test/api/test_auth.py

# 运行特定测试用例
pytest test/api/test_auth.py::TestAuthAPI::test_login_success

# 生成覆盖率报告
pytest --cov --cov-report=html

# 并行运行测试
pytest -n auto

# 详细输出
pytest -v

# 显示打印输出
pytest -s
```

---

## 7. 测试报告

### 7.1 测试报告内容

#### 7.1.1 测试执行摘要

- 测试用例总数
- 通过数量
- 失败数量
- 跳过数量
- 执行时间
- 通过率

#### 7.1.2 测试结果详情

- 每个测试用例的执行结果
- 失败原因分析
- 错误日志

#### 7.1.3 代码覆盖率报告

- 总体覆盖率
- 各模块覆盖率
- 未覆盖代码行

#### 7.1.4 性能测试报告

- 响应时间统计
- 吞吐量统计
- 资源使用情况

#### 7.1.5 问题汇总

- Bug 列表
- 优先级分类
- 修复建议

### 7.2 报告格式

- **HTML 报告**: 详细的测试报告和覆盖率报告
- **XML 报告**: CI/CD 集成使用
- **JSON 报告**: 自动化处理
- **Terminal 报告**: 快速查看

### 7.3 报告生成

```bash
# 生成 HTML 测试报告
pytest --html=reports/test_report.html --self-contained-html

# 生成覆盖率报告
pytest --cov --cov-report=html:reports/coverage

# 生成 JUnit XML 报告（CI/CD）
pytest --junitxml=reports/junit.xml
```

---

## 8. 测试质量标准

### 8.1 代码覆盖率标准

- **总体覆盖率**: ≥ 70%
- **单元测试覆盖率**: ≥ 80%
- **API 测试覆盖率**: 100% (所有端点)
- **关键业务逻辑**: ≥ 90%

### 8.2 性能标准

- **API 响应时间**:
  - P50 (中位数): < 200ms
  - P95: < 500ms
  - P99: < 1000ms
- **吞吐量**: ≥ 100 req/s
- **并发用户**: ≥ 50 用户

### 8.3 质量标准

- **Bug 密度**: < 1 bug/1000 行代码
- **严重 Bug**: 0 个
- **测试通过率**: ≥ 95%

---

## 9. 测试风险管理

### 9.1 风险识别

| 风险 | 影响 | 概率 | 应对措施 |
|------|------|------|----------|
| 测试环境不稳定 | 高 | 中 | 使用 Docker 容器化环境 |
| 测试数据不足 | 中 | 中 | 使用 Factory 生成测试数据 |
| 测试时间不足 | 高 | 高 | 优先测试关键功能 |
| 测试工具问题 | 中 | 低 | 准备备用测试方案 |

### 9.2 风险应对

- **环境问题**: 使用 Docker 确保环境一致性
- **数据问题**: 使用 Factory 和 Fixtures 管理测试数据
- **时间问题**: 自动化测试，提高效率
- **工具问题**: 选择成熟稳定的测试工具

---

## 10. 测试维护

### 10.1 测试用例维护

- **更新频率**: 每次功能变更后
- **维护内容**:
  - 更新过时的测试用例
  - 删除冗余的测试用例
  - 添加新的测试用例
  - 优化测试用例结构

### 10.2 测试数据维护

- **清理策略**: 每次测试后自动清理
- **数据备份**: 重要测试数据定期备份
- **数据版本**: 使用版本控制管理测试数据

### 10.3 测试文档维护

- **更新频率**: 每次测试计划变更后
- **维护内容**:
  - 更新测试计划
  - 更新测试用例
  - 更新测试报告模板

---

## 11. 附录

### 11.1 测试用例示例

详见 `test/api/examples/` 目录

### 11.2 测试工具文档

- [pytest 文档](https://docs.pytest.org/)
- [pytest-django 文档](https://pytest-django.readthedocs.io/)
- [factory-boy 文档](https://factoryboy.readthedocs.io/)
- [Django REST Framework 测试文档](https://www.django-rest-framework.org/api-guide/testing/)

### 11.3 相关文档

- [后端开发计划](../doc/backend-development-plan.md)
- [数据库设计文档](../doc/database-design.md)
- [API 文档](API_DOCUMENTATION.md) (待创建)

---

## 12. 更新日志

| 版本 | 日期 | 更新内容 | 更新人 |
|------|------|----------|--------|
| v1.0 | 2025-12-06 | 初始版本，创建测试计划 | - |

---

**文档状态**: ✅ 已完成  
**下一步**: 开始实施测试用例编写

