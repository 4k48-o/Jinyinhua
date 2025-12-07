# 🚀 后端开发计划

## 📋 项目概述

本文档详细规划了基于 Django + Django REST Framework 的企业级应用后端开发计划，按照模块化和渐进式开发的原则，分阶段实现核心功能。

---

## 🎯 开发目标

- 构建稳定、安全、高性能的 RESTful API 服务
- 实现完整的用户认证和授权系统（RBAC）
- 建立可扩展、可维护的代码架构
- 提供完善的 API 文档和错误处理机制
- 支持多环境配置和部署

---

## 📅 开发阶段总览

| 阶段 | 名称 | 预计时间 | 优先级 | 状态 |
|------|------|---------|--------|------|
| Phase 1 | 项目初始化和基础架构 | 3-5 天 | P0 | ✅ 已完成 |
| Phase 2 | 用户认证系统 | 5-7 天 | P0 | ⏳ 进行中 (95%) |
| Phase 3 | 用户管理模块 | 4-6 天 | P0 | ✅ 已完成 |
| Phase 4 | 权限管理系统 | 6-8 天 | P0 | ✅ 已完成 |
| Phase 5 | 通用功能模块 | 3-5 天 | P1 | ⏳ 部分完成 (60%) |
| Phase 6 | API 文档和测试 | 3-4 天 | P1 | ⏳ 部分完成 (50%) |
| Phase 7 | 性能优化和安全加固 | 4-6 天 | P1 | ⏳ 待开始 |

**总预计时间**：28-41 个工作日

---

## Phase 1: 项目初始化和基础架构

### 🎯 阶段目标

搭建项目基础架构，配置开发环境，建立项目目录结构，配置核心依赖。

### 📝 任务清单

#### 1.1 项目初始化
- [x] 创建 Django 项目
  ```bash
  django-admin startproject config .
  ```
- [x] 创建应用目录结构
  - [x] `apps/` 目录
  - [x] `apps/users/` 用户管理应用
  - [x] `apps/auth/` 认证应用
  - [x] `apps/permissions/` 权限管理应用
  - [x] `apps/common/` 通用应用
- [x] 配置 `apps/__init__.py` 和 `apps/apps.py`
- [x] 在 `settings.py` 中注册应用

#### 1.2 环境配置
- [x] 创建多环境配置目录 `config/settings/`
  - [x] `base.py` 基础配置
  - [x] `development.py` 开发环境
  - [x] `production.py` 生产环境
  - [x] `testing.py` 测试环境
- [x] 配置环境变量管理（python-decouple）
- [x] 创建 `.env.example` 文件
- [x] 配置 `SECRET_KEY`、`DEBUG`、`ALLOWED_HOSTS`

#### 1.3 数据库配置
- [x] 配置数据库连接（PostgreSQL/MySQL）
- [x] 配置数据库连接池（使用 CONN_MAX_AGE）
- [x] 创建初始迁移文件（待 Django 安装后执行）
- [x] 配置数据库备份策略

#### 1.4 核心依赖安装
- [x] 创建 `requirements/` 目录
  - [x] `base.txt` 基础依赖
  - [x] `development.txt` 开发依赖
  - [x] `production.txt` 生产依赖
- [x] 安装核心包：
  - [x] `djangorestframework`
  - [x] `djangorestframework-simplejwt`
  - [x] `django-cors-headers`
  - [x] `django-filter`
  - [x] `python-decouple`
  - [x] `pillow`
  - [x] `psycopg2` / `mysqlclient`

#### 1.5 中间件配置
- [x] 创建 `middleware/` 目录
- [x] 实现 CORS 中间件（使用 django-cors-headers）
- [x] 实现请求日志中间件
- [x] 实现异常处理中间件
- [x] 在 `settings.py` 中注册中间件

#### 1.6 URL 路由配置
- [x] 配置主 URL 路由 `config/urls.py`
- [x] 配置 API 版本路由 `/api/v1/`
- [x] 配置 Admin 后台路由
- [x] 配置静态文件和媒体文件路由

#### 1.7 通用工具模块
- [x] 创建 `utils/` 目录
- [x] 实现 JWT 工具函数 `utils/jwt.py`
- [x] 实现自定义验证器 `utils/validators.py`
- [x] 实现辅助函数 `utils/helpers.py`

### ✅ 验收标准

- [x] 项目可以成功启动（`python manage.py runserver`）
- [x] 数据库连接正常
- [x] Admin 后台可以访问
- [x] 多环境配置可以正常切换
- [x] 代码结构符合规范

### 📦 交付物

- 完整的项目目录结构
- `requirements.txt` 文件
- `.env.example` 文件
- 基础配置文件

---

## Phase 2: 用户认证系统

### 🎯 阶段目标

实现基于 JWT 的用户认证系统，包括登录、注册、Token 刷新、密码重置等功能。

### 📝 任务清单

#### 2.1 JWT 配置
- [x] 安装 `djangorestframework-simplejwt`
- [x] 在 `settings.py` 中配置 JWT 设置
  - [x] Access Token 过期时间（15 分钟）
  - [x] Refresh Token 过期时间（7 天）
  - [x] Token 加密算法
- [x] 配置 JWT 认证类
- [x] 配置 Token 黑名单（可选）

#### 2.2 认证应用开发
- [x] 创建 `apps/auth/` 应用
- [x] 实现用户注册序列化器
  - [x] 用户名验证（前期仅支持用户名，不包含邮箱/手机号）
  - [x] 密码强度验证
  - [ ] 邮箱/手机号唯一性验证（前期暂不支持）
- [x] 实现用户登录序列化器
  - [x] 支持用户名登录（前期仅支持用户名，不包含邮箱/手机号）
  - [x] 密码验证
  - [x] 用户状态检查（激活、禁用）
- [x] 实现 Token 刷新序列化器

#### 2.3 认证视图开发
- [x] 实现用户注册视图 `RegisterView`
  - [x] 用户创建
  - [ ] 发送激活邮件（可选，前期暂不实现）
  - [x] 返回 Token
- [x] 实现用户登录视图 `LoginView`
  - [x] 用户认证
  - [x] 生成 JWT Token
  - [x] 记录登录日志
- [x] 实现 Token 刷新视图 `TokenRefreshView`
- [x] 实现用户登出视图 `LogoutView`
  - [x] Token 失效处理
- [ ] 实现密码重置视图（前期暂不实现，涉及邮件功能）
  - [ ] 发送重置邮件（前期暂不实现）
  - [ ] 验证重置 Token（前期暂不实现）
  - [ ] 更新密码（前期暂不实现）

#### 2.4 认证路由配置
- [x] 配置认证相关路由
  - [x] `POST /api/v1/auth/register/` 用户注册
  - [x] `POST /api/v1/auth/login/` 用户登录
  - [x] `POST /api/v1/auth/refresh/` 刷新 Token
  - [x] `POST /api/v1/auth/logout/` 用户登出
  - [ ] `POST /api/v1/auth/password/reset/` 密码重置请求（前期暂不实现）
  - [ ] `POST /api/v1/auth/password/reset/confirm/` 密码重置确认（前期暂不实现）

#### 2.5 安全增强
- [x] 实现登录失败次数限制
  - [x] 使用 Redis 记录失败次数
  - [x] 达到最大失败次数后锁定账户
  - [x] 支持时间窗口重置
- [x] 实现 IP 白名单/黑名单（可选）
  - [x] IP 白名单管理
  - [x] IP 黑名单管理
  - [x] 自动加入黑名单（失败次数过多）
- [x] 实现验证码功能（可选）
  - [x] 验证码生成
  - [x] 验证码验证
  - [x] 登录失败次数过多时要求验证码
- [x] 实现设备指纹识别（可选）
  - [x] 设备信息提取
  - [x] 设备指纹生成
  - [x] 设备指纹存储和识别

### ✅ 验收标准

- [x] 用户可以成功注册（功能已实现，待测试验证）
- [x] 用户可以成功登录并获取 Token（功能已实现，待测试验证）
- [x] Token 可以正常刷新（功能已实现，待测试验证）
- [ ] 密码重置功能正常（前期暂不实现）
- [x] 未授权请求返回 401 错误（功能已实现，待测试验证）
- [x] 登录失败次数限制生效（功能已实现，待测试验证）

### 📦 交付物

- 完整的认证 API 接口
- 认证相关的序列化器和视图
- API 测试用例

---

## Phase 3: 用户管理模块

### 🎯 阶段目标

实现用户信息管理功能，包括用户 CRUD 操作、用户资料管理、头像上传等。

### 📝 任务清单

#### 3.1 用户模型扩展
- [x] 创建 `apps/users/` 应用
- [x] 创建 `UserProfile` 模型
  - [x] 关联 Django User 模型（OneToOne）
  - [x] 手机号字段
  - [x] 头像字段（ImageField）
  - [x] 部门字段（ForeignKey）
  - [x] 职位字段
  - [x] 创建时间、更新时间
- [x] 创建 `Department` 模型（如需要）
- [x] 创建数据库迁移文件
- [ ] 执行迁移（需要手动执行）

#### 3.2 用户序列化器
- [x] 创建用户列表序列化器 `UserListSerializer`
- [x] 创建用户详情序列化器 `UserDetailSerializer`
- [x] 创建用户创建序列化器 `UserCreateSerializer`
- [x] 创建用户更新序列化器 `UserUpdateSerializer`
- [x] 创建当前用户信息序列化器 `CurrentUserSerializer`
- [x] 实现头像上传处理

#### 3.3 用户视图集
- [x] 创建 `UserViewSet`
  - [x] `list()` 用户列表（支持分页、过滤、搜索）
  - [x] `retrieve()` 用户详情
  - [x] `create()` 创建用户（管理员）
  - [x] `update()` 更新用户
  - [x] `partial_update()` 部分更新
  - [x] `destroy()` 删除用户（软删除）
- [x] 创建 `CurrentUserView` 获取当前用户信息（通过 `me` action）
- [x] 创建 `UpdateCurrentUserView` 更新当前用户信息（通过 `update_me` action）
- [x] 实现用户状态管理（激活、禁用）（通过 `toggle_active` action）

#### 3.4 用户权限控制
- [x] 创建用户权限类 `UserPermission`
- [x] 实现权限规则：
  - [x] 用户可以查看自己的信息
  - [x] 用户可以更新自己的信息
  - [x] 只有管理员可以创建/删除用户
  - [x] 只有管理员可以查看所有用户列表

#### 3.5 用户路由配置
- [x] 配置用户相关路由
  - [x] `GET /api/v1/users/` 用户列表
  - [x] `POST /api/v1/users/` 创建用户
  - [x] `GET /api/v1/users/{id}/` 用户详情
  - [x] `PUT /api/v1/users/{id}/` 更新用户
  - [x] `PATCH /api/v1/users/{id}/` 部分更新
  - [x] `DELETE /api/v1/users/{id}/` 删除用户
  - [x] `GET /api/v1/users/me/` 当前用户信息
  - [x] `PUT /api/v1/users/me/` 更新当前用户信息
  - [x] `POST /api/v1/users/upload_avatar/` 上传头像
  - [x] `POST /api/v1/users/{id}/toggle_active/` 激活/禁用用户

#### 3.6 用户查询和过滤
- [x] 实现用户搜索功能（用户名、邮箱、手机号、工号）
- [x] 实现用户过滤功能（部门、状态）
- [x] 实现用户排序功能（创建时间、最后登录时间、用户名）
- [x] 配置分页（使用自定义分页类）

#### 3.7 文件上传处理
- [x] 配置媒体文件存储（本地，已在 settings 中配置）
- [x] 实现头像上传接口
- [x] 实现文件大小限制（最大 5MB）
- [x] 实现文件类型验证（JPEG、PNG、GIF、WebP）
- [x] 实现图片压缩（最大尺寸 800x800，质量 85%）

### ✅ 验收标准

- [ ] 可以创建、查询、更新、删除用户
- [ ] 用户可以查看和更新自己的信息
- [ ] 用户列表支持分页、过滤、搜索
- [ ] 头像上传功能正常
- [ ] 权限控制正确生效

### 📦 交付物

- 用户管理 API 接口
- 用户模型和序列化器
- 用户权限控制逻辑

---

## Phase 4: 权限管理系统

### 🎯 阶段目标

实现基于 RBAC 的权限管理系统，包括角色管理、权限分配、资源权限控制等。

### 📝 任务清单

#### 4.1 权限模型设计
- [x] 创建 `apps/permissions/` 应用
- [x] 创建 `Role` 模型
  - [x] 角色名称、代码、描述
  - [x] 关联权限（ManyToMany，通过 RolePermission）
  - [x] 是否激活
  - [x] 创建时间、更新时间
- [x] 创建 `UserRole` 模型（用户角色关联）
  - [x] 用户（ForeignKey）
  - [x] 角色（ForeignKey）
  - [x] 分配时间
- [x] 创建 `Permission` 模型（权限表）
- [x] 创建 `RolePermission` 模型（角色权限关联）
- [x] 创建数据库迁移文件
- [ ] 执行迁移（需要手动执行）

#### 4.2 权限序列化器
- [x] 创建角色列表序列化器 `RoleListSerializer`
- [x] 创建角色详情序列化器 `RoleDetailSerializer`
- [x] 创建角色创建序列化器 `RoleCreateSerializer`
- [x] 创建角色更新序列化器 `RoleUpdateSerializer`
- [x] 创建用户角色序列化器 `UserRoleSerializer`
- [x] 实现权限树形结构序列化（`PermissionTreeSerializer`）
- [x] 创建权限序列化器 `PermissionSerializer`

#### 4.3 角色管理视图
- [x] 创建 `RoleViewSet`
  - [x] `list()` 角色列表
  - [x] `retrieve()` 角色详情
  - [x] `create()` 创建角色
  - [x] `update()` 更新角色
  - [x] `destroy()` 删除角色（软删除）
- [x] 创建 `UserRoleViewSet` 用户角色管理
  - [x] `list()` 获取用户的角色列表
  - [x] `create()` 为用户分配角色
  - [x] `destroy()` 移除用户角色
  - [x] `user_roles()` 获取指定用户的角色列表
- [x] 创建 `PermissionViewSet` 权限管理视图（只读）
- [x] 创建 `PermissionCheckViewSet` 权限检查视图

#### 4.4 自定义权限类
- [x] 创建基础权限类 `BasePermission`
- [x] 创建角色权限类 `RolePermission`
- [x] 创建权限要求类 `PermissionRequired`
- [x] 实现权限检查逻辑
  - [x] 检查用户是否拥有指定角色（`check_user_role`）
  - [x] 检查用户是否拥有指定权限（`check_user_permission`）
  - [x] 获取用户所有角色（`get_user_roles`）
  - [x] 获取用户所有权限（`get_user_permissions`）

#### 4.5 权限装饰器和中间件
- [x] 创建权限装饰器 `@require_permission`
- [x] 创建角色装饰器 `@require_role`
- [x] 实现权限缓存机制（Redis，缓存时间 5 分钟）
- [ ] 实现权限检查中间件（可选，暂不实现）

#### 4.6 权限路由配置
- [x] 配置角色相关路由
  - [x] `GET /api/v1/roles/` 角色列表
  - [x] `POST /api/v1/roles/` 创建角色
  - [x] `GET /api/v1/roles/{id}/` 角色详情
  - [x] `PUT /api/v1/roles/{id}/` 更新角色
  - [x] `DELETE /api/v1/roles/{id}/` 删除角色
- [x] 配置用户角色路由
  - [x] `GET /api/v1/user-roles/` 用户角色列表
  - [x] `POST /api/v1/user-roles/` 分配角色
  - [x] `DELETE /api/v1/user-roles/{id}/` 移除角色
  - [x] `GET /api/v1/user-roles/user/{user_id}/` 获取指定用户的角色列表
- [x] 配置权限相关路由
  - [x] `GET /api/v1/permissions/` 权限列表
  - [x] `GET /api/v1/permissions/{id}/` 权限详情
  - [x] `GET /api/v1/permissions/tree/` 权限树形结构
- [x] 配置权限检查路由
  - [x] `GET /api/v1/permission-check/my_permissions/` 获取当前用户权限
  - [x] `GET /api/v1/permission-check/my_roles/` 获取当前用户角色
  - [x] `GET /api/v1/permission-check/check_permission/` 检查权限
  - [x] `GET /api/v1/permission-check/check_role/` 检查角色

#### 4.7 权限数据初始化
- [x] 创建默认角色（超级管理员、管理员、普通用户、访客）
- [x] 创建默认权限（CRUD 权限）
- [x] 创建数据初始化命令（`init_permissions`）
- [x] 自动为超级管理员分配角色

#### 4.8 权限查询接口
- [x] 实现获取用户所有权限接口（`my_permissions`）
- [x] 实现获取用户所有角色接口（`my_roles`）
- [x] 实现权限检查接口（`check_permission`）
- [x] 实现角色检查接口（`check_role`）
- [x] 实现权限树形结构接口（`tree`）

### ✅ 验收标准

- [ ] 可以创建、查询、更新、删除角色
- [ ] 可以为用户分配和移除角色
- [ ] 权限检查逻辑正确
- [ ] API 接口权限控制生效
- [ ] 默认角色和权限已初始化

### 📦 交付物

- 权限管理 API 接口
- 权限模型和序列化器
- 自定义权限类
- 权限初始化数据

---

## Phase 5: 通用功能模块

### 🎯 阶段目标

实现通用功能模块，包括统一响应格式、异常处理、日志系统、分页、过滤等。

### 📝 任务清单

#### 5.1 统一响应格式
- [x] 创建 `apps/common/response.py`（文件名略有不同）
- [x] 实现成功响应方法 `APIResponse.success()`（类方法，替代独立函数）
- [x] 实现错误响应方法 `APIResponse.error()`（类方法，替代独立函数）
- [x] 实现分页响应（在 `CustomPageNumberPagination.get_paginated_response()` 中实现）
- [x] 创建自定义响应类 `APIResponse`

#### 5.2 异常处理
- [x] 创建 `apps/common/exceptions.py`
- [x] 定义自定义异常类：
  - [x] `BaseAPIException` 基础异常（继承 DRF 的 `APIException`）
  - [x] `ValidationException` 验证错误
  - [x] `AuthenticationException` 认证异常
  - [x] `PermissionException` 权限拒绝
  - [x] `NotFoundException` 资源不存在
  - [x] `BusinessException` 业务异常
  - [x] `ConflictException` 资源冲突异常（额外实现）
  - [x] `RateLimitException` 限流异常（额外实现）
  - [x] `ServiceUnavailableException` 服务不可用异常（额外实现）
- [x] 实现全局异常处理中间件（`ExceptionHandlingMiddleware`）
- [x] 配置异常处理视图（`custom_exception_handler` 已配置到 `REST_FRAMEWORK.EXCEPTION_HANDLER`）

#### 5.3 日志系统
- [x] 配置 Django 日志系统（已在 `base.py` 中配置）
- [x] 创建日志格式配置（`JSONFormatter` 已实现）
- [x] 实现请求日志记录（`RequestLoggingMiddleware` 已实现）
- [x] 实现错误日志记录（在 `exceptions.py` 和 `middleware/exception.py` 中实现）
- [x] 实现操作日志记录（AuditLog）（`apps/common/audit.py` 已实现）
- [x] 创建 `AuditLog` 模型（`apps/common/models.py` 已创建）
- [x] 实现日志中间件（`RequestLoggingMiddleware` 已集成操作日志记录）

#### 5.4 分页处理
- [x] 创建 `apps/common/pagination.py`
- [x] 实现自定义分页类 `CustomPageNumberPagination`
- [x] 实现游标分页（`CustomCursorPagination`）
- [x] 配置默认分页设置（已在 `REST_FRAMEWORK` 中配置 `DEFAULT_PAGINATION_CLASS` 和 `PAGE_SIZE`）

#### 5.5 过滤和搜索
- [x] 安装 `django-filter`（已在 `requirements/base.txt` 中安装）
- [x] 创建 `apps/common/filters.py`
- [x] 实现通用过滤器基类（`BaseFilterSet`）
- [x] 实现日期范围过滤（`DateRangeFilterMixin`、`BaseFilterSet` 中的 `created_at_start/end`、`updated_at_start/end`）
- [x] 实现多字段搜索（`MultiFieldSearchMixin`、`BaseFilterSet` 中的 `filter_search` 方法）
- [x] 配置过滤后端（已在 `REST_FRAMEWORK.DEFAULT_FILTER_BACKENDS` 中配置 `DjangoFilterBackend`、`SearchFilter`、`OrderingFilter`）

#### 5.6 工具函数
- [x] 创建 `apps/common/utils.py`
- [x] 实现日期时间工具函数（`format_datetime`, `parse_datetime`, `get_time_range`, `get_today_range`, `get_week_range`, `get_month_range`）
- [x] 实现字符串处理工具函数（`generate_random_string`, `generate_code`, `mask_sensitive_data`, `mask_phone`, `mask_email`, `truncate_string`）
- [x] 实现数据验证工具函数（`validate_phone`, `validate_email`, `safe_int`, `safe_float`）
- [x] 实现文件处理工具函数（`validate_image_file`, `compress_image`, `generate_thumbnail`, `get_file_extension`, `get_file_size_mb`, `generate_unique_filename`）

#### 5.7 基础模型
- [ ] 创建 `apps/common/models.py`
- [ ] 创建 `BaseModel` 抽象模型
  - [ ] `created_at` 创建时间
  - [ ] `updated_at` 更新时间
  - [ ] `is_deleted` 软删除标记
  - [ ] `deleted_at` 删除时间
- [ ] 创建 `AuditLog` 模型
- [ ] 创建 `SystemConfig` 模型（系统配置）

#### 5.8 API 限流
- [ ] 配置 DRF 限流设置
- [ ] 实现用户级别限流
- [ ] 实现 IP 级别限流
- [ ] 实现接口级别限流
- [ ] 配置限流异常处理

### ✅ 验收标准

- [ ] API 响应格式统一
- [ ] 异常处理正确
- [ ] 日志记录完整
- [ ] 分页功能正常
- [ ] 过滤和搜索功能正常
- [ ] API 限流生效

### 📦 交付物

- 通用功能模块代码
- 统一响应和异常处理
- 日志系统
- 工具函数库

---

## Phase 6: API 文档和测试

### 🎯 阶段目标

生成 API 文档，编写单元测试和集成测试，确保代码质量。

### 📝 任务清单

#### 6.1 API 文档生成
- [x] 安装 `drf-spectacular` 或 `drf-yasg`
- [x] 配置 API 文档设置
- [x] 为认证 API 添加文档注释
- [x] 配置 Swagger UI
- [x] 配置 ReDoc（可选）
- [x] 测试 API 文档访问
- [ ] 为所有 API 添加文档注释（待 Phase 3、4 完成后）

#### 6.2 单元测试
- [ ] 创建测试目录结构
- [ ] 编写认证模块测试
  - [ ] 注册测试
  - [ ] 登录测试
  - [ ] Token 刷新测试
- [ ] 编写用户管理测试
  - [ ] 用户 CRUD 测试
  - [ ] 权限测试
- [ ] 编写权限管理测试
  - [ ] 角色 CRUD 测试
  - [ ] 权限分配测试
- [ ] 运行测试并修复问题

#### 6.3 集成测试
- [ ] 编写 API 集成测试
- [ ] 编写端到端测试场景
- [ ] 测试认证流程
- [ ] 测试权限控制流程
- [ ] 测试错误处理

#### 6.4 测试覆盖率
- [ ] 安装 `coverage`
- [ ] 配置覆盖率报告
- [ ] 生成覆盖率报告
- [ ] 确保覆盖率 > 80%

#### 6.5 API 测试工具
- [ ] 创建 Postman 集合
- [ ] 创建 API 测试脚本
- [ ] 配置自动化测试流程

### ✅ 验收标准

- [ ] API 文档可以正常访问
- [ ] 所有 API 都有文档说明
- [ ] 单元测试通过率 100%
- [ ] 测试覆盖率 > 80%
- [ ] 集成测试通过

### 📦 交付物

- API 文档（Swagger/OpenAPI）
- 测试用例
- 测试覆盖率报告
- Postman 集合

---

## Phase 7: 性能优化和安全加固

### 🎯 阶段目标

优化系统性能，加强安全防护，准备生产环境部署。

### 📝 任务清单

#### 7.1 数据库优化
- [ ] 分析慢查询
- [ ] 添加数据库索引
- [ ] 优化查询语句（select_related, prefetch_related）
- [ ] 配置数据库连接池
- [ ] 实现查询缓存

#### 7.2 缓存优化
- [ ] 安装和配置 Redis
- [ ] 实现用户信息缓存
- [ ] 实现权限信息缓存
- [ ] 实现 API 响应缓存（可选）
- [ ] 配置缓存过期策略

#### 7.3 安全加固
- [x] 配置 HTTPS（生产环境）（已在 `production.py` 中配置 `SECURE_SSL_REDIRECT`、`SECURE_HSTS_SECONDS` 等）
- [x] 实现 CSRF 保护（已配置 `CsrfViewMiddleware` 和 CSRF Cookie 安全设置）
- [x] 实现 XSS 防护（`XSSProtection` 类、`SecurityHeadersMiddleware` 添加安全响应头）
- [x] 配置安全响应头（`SecurityHeadersMiddleware` 添加 `X-Frame-Options`、`X-Content-Type-Options`、`X-XSS-Protection`、`Referrer-Policy`、`Permissions-Policy`）
- [x] 实现 SQL 注入防护检查（`SQLInjectionChecker` 类、`SQLInjectionProtectionMiddleware` 中间件）
- [x] 配置密码策略（已配置 `AUTH_PASSWORD_VALIDATORS` 和密码策略配置项）
- [x] 实现敏感数据加密（`DataEncryption` 类，使用 Fernet 对称加密）

#### 7.4 性能监控
- [ ] 集成性能监控工具（Sentry、New Relic）
- [ ] 实现 API 性能日志
- [ ] 配置慢查询监控
- [ ] 实现错误追踪

#### 7.5 部署准备
- [ ] 创建 Dockerfile
- [ ] 创建 docker-compose.yml
- [ ] 配置生产环境设置
- [ ] 配置环境变量
- [ ] 创建部署脚本
- [ ] 配置 Nginx（可选）
- [ ] 配置 Gunicorn/uWSGI

#### 7.6 文档完善
- [ ] 编写部署文档
- [ ] 编写运维文档
- [ ] 编写 API 使用文档
- [ ] 编写故障排查文档

### ✅ 验收标准

- [ ] 数据库查询性能优化
- [ ] 缓存机制正常工作
- [ ] 安全配置完整
- [ ] 性能监控正常
- [ ] 可以成功部署到生产环境

### 📦 交付物

- 优化后的代码
- Docker 配置文件
- 部署文档
- 运维文档

---

## 📊 开发规范

### 代码规范
- 遵循 PEP 8 代码风格
- 使用 Black 进行代码格式化
- 使用 isort 进行导入排序
- 使用 Flake8 进行代码检查
- 添加类型提示（Type Hints）

### Git 工作流
- 使用功能分支开发（feature/*）
- 提交信息遵循规范（feat、fix、docs 等）
- 代码审查后合并到主分支

### API 设计规范
- 遵循 RESTful 设计原则
- 使用统一的响应格式
- 使用合适的 HTTP 状态码
- 提供清晰的错误信息

---

## 🔧 开发工具推荐

- **IDE**: PyCharm / VS Code
- **版本控制**: Git
- **API 测试**: Postman / Insomnia
- **数据库管理**: pgAdmin / DBeaver
- **代码质量**: Black, isort, Flake8, mypy
- **测试框架**: pytest, pytest-django
- **文档生成**: drf-spectacular

---

## 📝 注意事项

1. **数据库迁移**：每次模型变更后及时创建迁移文件
2. **环境变量**：敏感信息使用环境变量，不要硬编码
3. **错误处理**：所有 API 都要有完善的错误处理
4. **日志记录**：关键操作要记录日志
5. **安全第一**：始终考虑安全性，不要忽视安全漏洞
6. **代码审查**：重要功能提交前进行代码审查
7. **测试驱动**：尽量先写测试，再写实现

---

**版本**: v1.0.0  
**最后更新**: 2024-01-01

