# 🗄️ 数据库设计文档

## 📋 文档概述

本文档详细描述了企业级应用系统的数据库设计，所有基础表均以 `sys_` 前缀开头，采用关系型数据库设计，支持 PostgreSQL 和 MySQL。

### 设计原则

- **命名规范**：所有基础表以 `sys_` 前缀开头
- **字段规范**：使用下划线命名（snake_case）
- **主键策略**：统一使用自增 ID 作为主键
- **时间字段**：统一使用 `created_at` 和 `updated_at`
- **软删除**：重要表支持软删除（`is_deleted`、`deleted_at`）
- **索引优化**：为常用查询字段添加索引
- **无外键设计**：不使用数据库外键约束，数据一致性由应用层维护，提高灵活性和性能

---

## 📊 数据库表总览

| 表名 | 说明 | 类型 |
|------|------|------|
| sys_user | 用户基础表 | 核心表 |
| sys_user_profile | 用户扩展信息表 | 核心表 |
| sys_department | 部门表 | 核心表 |
| sys_role | 角色表 | 权限表 |
| sys_permission | 权限表 | 权限表 |
| sys_user_role | 用户角色关联表 | 关联表 |
| sys_role_permission | 角色权限关联表 | 关联表 |
| sys_menu | 菜单表 | 功能表 |
| sys_menu_permission | 菜单权限关联表 | 关联表 |
| sys_audit_log | 操作日志表 | 日志表 |
| sys_system_config | 系统配置表 | 配置表 |
| sys_file | 文件表 | 文件表 |
| sys_login_log | 登录日志表 | 日志表 |

---

## 👤 用户相关表

### 1. sys_user - 用户基础表

**表说明**：存储用户基础信息，扩展 Django 的 auth_user 表或独立实现。

| 字段名 | 类型 | 长度 | 允许空 | 默认值 | 说明 | 索引 |
|--------|------|------|--------|--------|------|------|
| id | BIGINT | - | NO | AUTO_INCREMENT | 主键 ID | PRIMARY |
| username | VARCHAR | 150 | NO | - | 用户名（唯一） | UNIQUE |
| email | VARCHAR | 254 | YES | NULL | 邮箱地址 | INDEX |
| phone | VARCHAR | 20 | YES | NULL | 手机号 | UNIQUE |
| password | VARCHAR | 128 | NO | - | 密码（加密） | - |
| first_name | VARCHAR | 150 | YES | '' | 名 | - |
| last_name | VARCHAR | 150 | YES | '' | 姓 | - |
| is_active | BOOLEAN | - | NO | TRUE | 是否激活 | INDEX |
| is_staff | BOOLEAN | - | NO | FALSE | 是否员工 | - |
| is_superuser | BOOLEAN | - | NO | FALSE | 是否超级管理员 | - |
| is_deleted | BOOLEAN | - | NO | FALSE | 是否删除（软删除） | INDEX |
| last_login | DATETIME | - | YES | NULL | 最后登录时间 | - |
| date_joined | DATETIME | - | NO | CURRENT_TIMESTAMP | 注册时间 | INDEX |
| created_at | DATETIME | - | NO | CURRENT_TIMESTAMP | 创建时间 | INDEX |
| updated_at | DATETIME | - | NO | CURRENT_TIMESTAMP ON UPDATE | 更新时间 | - |
| deleted_at | DATETIME | - | YES | NULL | 删除时间 | - |

**索引设计**：
- PRIMARY KEY: `id`
- UNIQUE: `username`, `phone`
- INDEX: `email`, `is_active`, `is_deleted`, `date_joined`, `created_at`

**备注**：
- 用户名、邮箱、手机号至少提供一个
- 密码使用 Django 的 PBKDF2 加密存储
- 支持软删除，删除后 `is_deleted = TRUE`

---

### 2. sys_user_profile - 用户扩展信息表

**表说明**：存储用户的扩展信息，与 sys_user 一对一关系。

| 字段名 | 类型 | 长度 | 允许空 | 默认值 | 说明 | 索引 |
|--------|------|------|--------|--------|------|------|
| id | BIGINT | - | NO | AUTO_INCREMENT | 主键 ID | PRIMARY |
| user_id | BIGINT | - | NO | - | 用户 ID（关联 sys_user.id） | UNIQUE, INDEX |
| avatar | VARCHAR | 500 | YES | NULL | 头像 URL | - |
| gender | TINYINT | - | YES | NULL | 性别（0:未知, 1:男, 2:女） | - |
| birthday | DATE | - | YES | NULL | 生日 | - |
| address | VARCHAR | 500 | YES | NULL | 地址 | - |
| bio | TEXT | - | YES | NULL | 个人简介 | - |
| department_id | BIGINT | - | YES | NULL | 部门 ID（关联 sys_department.id） | INDEX |
| position | VARCHAR | 100 | YES | NULL | 职位 | - |
| employee_no | VARCHAR | 50 | YES | NULL | 工号 | UNIQUE |
| join_date | DATE | - | YES | NULL | 入职日期 | - |
| created_at | DATETIME | - | NO | CURRENT_TIMESTAMP | 创建时间 | - |
| updated_at | DATETIME | - | NO | CURRENT_TIMESTAMP ON UPDATE | 更新时间 | - |

**索引设计**：
- PRIMARY KEY: `id`
- UNIQUE: `user_id`, `employee_no`
- INDEX: `department_id`

**备注**：
- 与 sys_user 一对一关系，通过 user_id 关联（应用层维护数据一致性）
- 头像存储 URL 路径，实际文件存储在 sys_file 表或 OSS

---

### 3. sys_department - 部门表

**表说明**：存储部门/组织架构信息，支持树形结构。

| 字段名 | 类型 | 长度 | 允许空 | 默认值 | 说明 | 索引 |
|--------|------|------|--------|--------|------|------|
| id | BIGINT | - | NO | AUTO_INCREMENT | 主键 ID | PRIMARY |
| name | VARCHAR | 100 | NO | - | 部门名称 | INDEX |
| code | VARCHAR | 50 | YES | NULL | 部门代码（唯一） | UNIQUE |
| parent_id | BIGINT | - | YES | NULL | 父部门 ID（关联 sys_department.id） | INDEX |
| level | INT | - | NO | 1 | 部门层级 | INDEX |
| path | VARCHAR | 500 | YES | NULL | 部门路径（如：1/2/3） | - |
| manager_id | BIGINT | - | YES | NULL | 部门负责人 ID（关联 sys_user.id） | INDEX |
| description | TEXT | - | YES | NULL | 部门描述 | - |
| sort_order | INT | - | NO | 0 | 排序顺序 | - |
| is_active | BOOLEAN | - | NO | TRUE | 是否激活 | INDEX |
| is_deleted | BOOLEAN | - | NO | FALSE | 是否删除 | INDEX |
| created_at | DATETIME | - | NO | CURRENT_TIMESTAMP | 创建时间 | - |
| updated_at | DATETIME | - | NO | CURRENT_TIMESTAMP ON UPDATE | 更新时间 | - |
| deleted_at | DATETIME | - | YES | NULL | 删除时间 | - |

**索引设计**：
- PRIMARY KEY: `id`
- UNIQUE: `code`
- INDEX: `name`, `parent_id`, `level`, `manager_id`, `is_active`, `is_deleted`

**备注**：
- 支持树形结构，通过 parent_id 建立层级关系（应用层维护数据一致性）
- path 字段存储从根到当前节点的路径，便于查询
- level 字段表示层级深度，根部门为 1

---

## 🔐 权限相关表

### 4. sys_role - 角色表

**表说明**：存储角色信息，用于 RBAC 权限控制。

| 字段名 | 类型 | 长度 | 允许空 | 默认值 | 说明 | 索引 |
|--------|------|------|--------|--------|------|------|
| id | BIGINT | - | NO | AUTO_INCREMENT | 主键 ID | PRIMARY |
| name | VARCHAR | 50 | NO | - | 角色名称 | UNIQUE |
| code | VARCHAR | 50 | NO | - | 角色代码（唯一，如：admin） | UNIQUE |
| description | TEXT | - | YES | NULL | 角色描述 | - |
| sort_order | INT | - | NO | 0 | 排序顺序 | - |
| is_active | BOOLEAN | - | NO | TRUE | 是否激活 | INDEX |
| is_system | BOOLEAN | - | NO | FALSE | 是否系统角色（不可删除） | - |
| is_deleted | BOOLEAN | - | NO | FALSE | 是否删除 | INDEX |
| created_at | DATETIME | - | NO | CURRENT_TIMESTAMP | 创建时间 | - |
| updated_at | DATETIME | - | NO | CURRENT_TIMESTAMP ON UPDATE | 更新时间 | - |
| deleted_at | DATETIME | - | YES | NULL | 删除时间 | - |
| created_by | BIGINT | - | YES | NULL | 创建人 ID（关联 sys_user.id） | INDEX |

**索引设计**：
- PRIMARY KEY: `id`
- UNIQUE: `name`, `code`
- INDEX: `is_active`, `is_deleted`, `created_by`

**备注**：
- code 字段用于程序内识别角色，如：admin, user, guest
- is_system 为 TRUE 的角色不可删除，如超级管理员角色
- 默认角色：超级管理员（super_admin）、管理员（admin）、普通用户（user）、访客（guest）

---

### 5. sys_permission - 权限表

**表说明**：存储权限信息，可以扩展 Django 的 auth_permission 或独立实现。

| 字段名 | 类型 | 长度 | 允许空 | 默认值 | 说明 | 索引 |
|--------|------|------|--------|--------|------|------|
| id | BIGINT | - | NO | AUTO_INCREMENT | 主键 ID | PRIMARY |
| name | VARCHAR | 100 | NO | - | 权限名称 | - |
| code | VARCHAR | 100 | NO | - | 权限代码（唯一，如：user:create） | UNIQUE |
| content_type | VARCHAR | 100 | YES | NULL | 资源类型（如：user, role） | INDEX |
| action | VARCHAR | 50 | YES | NULL | 操作类型（如：create, read, update, delete） | - |
| description | TEXT | - | YES | NULL | 权限描述 | - |
| parent_id | BIGINT | - | YES | NULL | 父权限 ID（关联 sys_permission.id） | INDEX |
| sort_order | INT | - | NO | 0 | 排序顺序 | - |
| is_active | BOOLEAN | - | NO | TRUE | 是否激活 | INDEX |
| is_system | BOOLEAN | - | NO | FALSE | 是否系统权限 | - |
| created_at | DATETIME | - | NO | CURRENT_TIMESTAMP | 创建时间 | - |
| updated_at | DATETIME | - | NO | CURRENT_TIMESTAMP ON UPDATE | 更新时间 | - |

**索引设计**：
- PRIMARY KEY: `id`
- UNIQUE: `code`
- INDEX: `content_type`, `parent_id`, `is_active`

**备注**：
- code 格式：`资源类型:操作类型`，如：`user:create`, `user:read`, `role:update`
- 支持权限树形结构，通过 parent_id 建立层级关系（应用层维护数据一致性）
- 常用操作：create（创建）、read（查看）、update（更新）、delete（删除）、export（导出）、import（导入）

---

### 6. sys_user_role - 用户角色关联表

**表说明**：存储用户和角色的多对多关系。

| 字段名 | 类型 | 长度 | 允许空 | 默认值 | 说明 | 索引 |
|--------|------|------|--------|--------|------|------|
| id | BIGINT | - | NO | AUTO_INCREMENT | 主键 ID | PRIMARY |
| user_id | BIGINT | - | NO | - | 用户 ID（关联 sys_user.id） | INDEX |
| role_id | BIGINT | - | NO | - | 角色 ID（关联 sys_role.id） | INDEX |
| assigned_at | DATETIME | - | NO | CURRENT_TIMESTAMP | 分配时间 | - |
| assigned_by | BIGINT | - | YES | NULL | 分配人 ID（关联 sys_user.id） | INDEX |
| is_active | BOOLEAN | - | NO | TRUE | 是否激活 | - |
| expires_at | DATETIME | - | YES | NULL | 过期时间（NULL 表示永久） | INDEX |

**索引设计**：
- PRIMARY KEY: `id`
- UNIQUE: `(user_id, role_id)` - 防止重复分配
- INDEX: `user_id`, `role_id`, `assigned_by`, `expires_at`

**备注**：
- 一个用户可以有多个角色（应用层维护数据一致性）
- 支持角色过期时间，可用于临时授权
- assigned_by 记录是谁分配的这个角色

---

### 7. sys_role_permission - 角色权限关联表

**表说明**：存储角色和权限的多对多关系。

| 字段名 | 类型 | 长度 | 允许空 | 默认值 | 说明 | 索引 |
|--------|------|------|--------|--------|------|------|
| id | BIGINT | - | NO | AUTO_INCREMENT | 主键 ID | PRIMARY |
| role_id | BIGINT | - | NO | - | 角色 ID（关联 sys_role.id） | INDEX |
| permission_id | BIGINT | - | NO | - | 权限 ID（关联 sys_permission.id） | INDEX |
| granted_at | DATETIME | - | NO | CURRENT_TIMESTAMP | 授权时间 | - |
| granted_by | BIGINT | - | YES | NULL | 授权人 ID（关联 sys_user.id） | INDEX |

**索引设计**：
- PRIMARY KEY: `id`
- UNIQUE: `(role_id, permission_id)` - 防止重复授权
- INDEX: `role_id`, `permission_id`, `granted_by`

**备注**：
- 一个角色可以有多个权限（应用层维护数据一致性）
- 一个权限可以分配给多个角色
- granted_by 记录是谁授权的

---

## 🎨 菜单相关表

### 8. sys_menu - 菜单表

**表说明**：存储前端菜单信息，用于菜单权限控制。

| 字段名 | 类型 | 长度 | 允许空 | 默认值 | 说明 | 索引 |
|--------|------|------|--------|--------|------|------|
| id | BIGINT | - | NO | AUTO_INCREMENT | 主键 ID | PRIMARY |
| name | VARCHAR | 50 | NO | - | 菜单名称 | - |
| title | VARCHAR | 100 | NO | - | 菜单标题（显示名称） | - |
| path | VARCHAR | 200 | YES | NULL | 路由路径 | INDEX |
| component | VARCHAR | 200 | YES | NULL | 组件路径 | - |
| icon | VARCHAR | 100 | YES | NULL | 图标名称 | - |
| parent_id | BIGINT | - | YES | NULL | 父菜单 ID（关联 sys_menu.id） | INDEX |
| level | INT | - | NO | 1 | 菜单层级 | INDEX |
| sort_order | INT | - | NO | 0 | 排序顺序 | - |
| is_visible | BOOLEAN | - | NO | TRUE | 是否显示 | INDEX |
| is_cache | BOOLEAN | - | NO | FALSE | 是否缓存 | - |
| is_external | BOOLEAN | - | NO | FALSE | 是否外部链接 | - |
| external_url | VARCHAR | 500 | YES | NULL | 外部链接地址 | - |
| permission_code | VARCHAR | 100 | YES | NULL | 所需权限代码 | INDEX |
| is_active | BOOLEAN | - | NO | TRUE | 是否激活 | INDEX |
| created_at | DATETIME | - | NO | CURRENT_TIMESTAMP | 创建时间 | - |
| updated_at | DATETIME | - | NO | CURRENT_TIMESTAMP ON UPDATE | 更新时间 | - |

**索引设计**：
- PRIMARY KEY: `id`
- INDEX: `path`, `parent_id`, `level`, `is_visible`, `permission_code`, `is_active`

**备注**：
- 支持树形结构菜单（应用层维护数据一致性）
- permission_code 关联权限，控制菜单显示
- is_external 为 TRUE 时，点击菜单跳转到外部链接

---

### 9. sys_menu_permission - 菜单权限关联表

**表说明**：存储菜单和权限的关联关系（可选，如果菜单直接使用 permission_code 字段则不需要此表）。

| 字段名 | 类型 | 长度 | 允许空 | 默认值 | 说明 | 索引 |
|--------|------|------|--------|--------|------|------|
| id | BIGINT | - | NO | AUTO_INCREMENT | 主键 ID | PRIMARY |
| menu_id | BIGINT | - | NO | - | 菜单 ID（关联 sys_menu.id） | INDEX |
| permission_id | BIGINT | - | NO | - | 权限 ID（关联 sys_permission.id） | INDEX |

**索引设计**：
- PRIMARY KEY: `id`
- UNIQUE: `(menu_id, permission_id)`
- INDEX: `menu_id`, `permission_id`

**备注**：
- 如果菜单只需要一个权限，可以直接使用 sys_menu 的 permission_code 字段
- 如果菜单需要多个权限，使用此关联表（应用层维护数据一致性）

---

## 📝 日志相关表

### 10. sys_audit_log - 操作日志表

**表说明**：记录用户操作日志，用于审计和追踪。

| 字段名 | 类型 | 长度 | 允许空 | 默认值 | 说明 | 索引 |
|--------|------|------|--------|--------|------|------|
| id | BIGINT | - | NO | AUTO_INCREMENT | 主键 ID | PRIMARY |
| user_id | BIGINT | - | YES | NULL | 用户 ID（关联 sys_user.id） | INDEX |
| username | VARCHAR | 150 | YES | NULL | 用户名（冗余字段） | INDEX |
| action | VARCHAR | 50 | NO | - | 操作类型（create, update, delete, view） | INDEX |
| resource_type | VARCHAR | 100 | NO | - | 资源类型（user, role, etc.） | INDEX |
| resource_id | BIGINT | - | YES | NULL | 资源 ID | INDEX |
| resource_name | VARCHAR | 200 | YES | NULL | 资源名称 | - |
| description | TEXT | - | YES | NULL | 操作描述 | - |
| request_method | VARCHAR | 10 | YES | NULL | HTTP 方法（GET, POST, etc.） | - |
| request_path | VARCHAR | 500 | YES | NULL | 请求路径 | - |
| request_params | TEXT | - | YES | NULL | 请求参数（JSON） | - |
| ip_address | VARCHAR | 50 | YES | NULL | IP 地址 | INDEX |
| user_agent | VARCHAR | 500 | YES | NULL | 用户代理 | - |
| status | TINYINT | - | NO | 1 | 操作状态（1:成功, 0:失败） | INDEX |
| error_message | TEXT | - | YES | NULL | 错误信息 | - |
| execution_time | INT | - | YES | NULL | 执行时间（毫秒） | - |
| created_at | DATETIME | - | NO | CURRENT_TIMESTAMP | 创建时间 | INDEX |

**索引设计**：
- PRIMARY KEY: `id`
- INDEX: `user_id`, `username`, `action`, `resource_type`, `resource_id`, `ip_address`, `status`, `created_at`

**备注**：
- 记录所有重要操作，用于审计和问题追踪
- 定期归档旧日志数据
- 可以按时间、用户、操作类型等维度查询

---

### 11. sys_login_log - 登录日志表

**表说明**：记录用户登录日志。

| 字段名 | 类型 | 长度 | 允许空 | 默认值 | 说明 | 索引 |
|--------|------|------|--------|--------|------|------|
| id | BIGINT | - | NO | AUTO_INCREMENT | 主键 ID | PRIMARY |
| user_id | BIGINT | - | YES | NULL | 用户 ID（关联 sys_user.id） | INDEX |
| username | VARCHAR | 150 | YES | NULL | 用户名 | INDEX |
| login_type | VARCHAR | 20 | NO | - | 登录类型（password, token, etc.） | - |
| ip_address | VARCHAR | 50 | YES | NULL | IP 地址 | INDEX |
| user_agent | VARCHAR | 500 | YES | NULL | 用户代理 | - |
| location | VARCHAR | 200 | YES | NULL | 登录地点 | - |
| device | VARCHAR | 100 | YES | NULL | 设备信息 | - |
| browser | VARCHAR | 100 | YES | NULL | 浏览器信息 | - |
| os | VARCHAR | 100 | YES | NULL | 操作系统 | - |
| status | TINYINT | - | NO | 0 | 登录状态（1:成功, 0:失败） | INDEX |
| failure_reason | VARCHAR | 200 | YES | NULL | 失败原因 | - |
| created_at | DATETIME | - | NO | CURRENT_TIMESTAMP | 登录时间 | INDEX |

**索引设计**：
- PRIMARY KEY: `id`
- INDEX: `user_id`, `username`, `ip_address`, `status`, `created_at`

**备注**：
- 记录所有登录尝试，包括成功和失败
- 用于安全审计和异常登录检测
- 可以基于此表实现登录失败次数限制

---

## ⚙️ 系统配置表

### 12. sys_system_config - 系统配置表

**表说明**：存储系统配置信息，支持键值对配置。

| 字段名 | 类型 | 长度 | 允许空 | 默认值 | 说明 | 索引 |
|--------|------|------|--------|--------|------|------|
| id | BIGINT | - | NO | AUTO_INCREMENT | 主键 ID | PRIMARY |
| config_key | VARCHAR | 100 | NO | - | 配置键（唯一） | UNIQUE |
| config_value | TEXT | - | YES | NULL | 配置值 | - |
| config_type | VARCHAR | 50 | NO | 'string' | 配置类型（string, number, boolean, json） | INDEX |
| category | VARCHAR | 50 | YES | NULL | 配置分类 | INDEX |
| description | TEXT | - | YES | NULL | 配置描述 | - |
| is_encrypted | BOOLEAN | - | NO | FALSE | 是否加密存储 | - |
| is_system | BOOLEAN | - | NO | FALSE | 是否系统配置（不可删除） | - |
| created_at | DATETIME | - | NO | CURRENT_TIMESTAMP | 创建时间 | - |
| updated_at | DATETIME | - | NO | CURRENT_TIMESTAMP ON UPDATE | 更新时间 | - |
| updated_by | BIGINT | - | YES | NULL | 更新人 ID（关联 sys_user.id） | INDEX |

**索引设计**：
- PRIMARY KEY: `id`
- UNIQUE: `config_key`
- INDEX: `config_type`, `category`, `updated_by`

**备注**：
- 用于存储系统配置，如：邮件服务器配置、文件上传限制等
- is_encrypted 为 TRUE 时，config_value 需要加密存储
- is_system 为 TRUE 的配置不可删除

---

## 📁 文件相关表

### 13. sys_file - 文件表

**表说明**：存储文件信息，用于文件管理。

| 字段名 | 类型 | 长度 | 允许空 | 默认值 | 说明 | 索引 |
|--------|------|------|--------|--------|------|------|
| id | BIGINT | - | NO | AUTO_INCREMENT | 主键 ID | PRIMARY |
| file_name | VARCHAR | 255 | NO | - | 原始文件名 | - |
| file_path | VARCHAR | 500 | NO | - | 文件存储路径 | INDEX |
| file_url | VARCHAR | 500 | YES | NULL | 文件访问 URL | - |
| file_type | VARCHAR | 50 | YES | NULL | 文件类型（MIME） | INDEX |
| file_size | BIGINT | - | NO | 0 | 文件大小（字节） | - |
| file_ext | VARCHAR | 20 | YES | NULL | 文件扩展名 | INDEX |
| storage_type | VARCHAR | 20 | NO | 'local' | 存储类型（local, oss, s3） | - |
| bucket_name | VARCHAR | 100 | YES | NULL | 存储桶名称（OSS/S3） | - |
| md5_hash | VARCHAR | 32 | YES | NULL | 文件 MD5 值 | INDEX |
| uploader_id | BIGINT | - | YES | NULL | 上传人 ID（关联 sys_user.id） | INDEX |
| related_type | VARCHAR | 100 | YES | NULL | 关联类型（user, article, etc.） | INDEX |
| related_id | BIGINT | - | YES | NULL | 关联 ID | INDEX |
| is_public | BOOLEAN | - | NO | FALSE | 是否公开 | - |
| download_count | INT | - | NO | 0 | 下载次数 | - |
| created_at | DATETIME | - | NO | CURRENT_TIMESTAMP | 创建时间 | INDEX |
| updated_at | DATETIME | - | NO | CURRENT_TIMESTAMP ON UPDATE | 更新时间 | - |

**索引设计**：
- PRIMARY KEY: `id`
- INDEX: `file_path`, `file_type`, `file_ext`, `md5_hash`, `uploader_id`, `related_type`, `related_id`, `created_at`

**备注**：
- 支持本地存储和云存储（OSS、S3）
- md5_hash 用于文件去重
- related_type 和 related_id 用于关联业务数据

---

## 📐 数据库关系图

```
sys_user (1) ────── (1) sys_user_profile
    │                      │
    │                      │
    │ (1)                  │ (N)
    │                      │
    │                      │
    │                      ▼
    │                sys_department
    │                      │
    │                      │ (1)
    │                      │
    │                      ▼
    │                sys_user_profile.department_id
    │
    │ (N)
    │
    ▼
sys_user_role (N) ──── (1) sys_role
    │
    │ (N)
    │
    ▼
sys_role_permission (N) ──── (1) sys_permission
```

---

## 🔍 索引优化建议

### 常用查询场景索引

1. **用户登录查询**：
   - `sys_user`: `username`, `email`, `phone`, `is_active`

2. **用户列表查询**：
   - `sys_user`: `is_deleted`, `created_at`, `is_active`
   - `sys_user_profile`: `department_id`

3. **权限检查查询**：
   - `sys_user_role`: `user_id`, `role_id`
   - `sys_role_permission`: `role_id`, `permission_id`

4. **日志查询**：
   - `sys_audit_log`: `user_id`, `created_at`, `action`, `resource_type`
   - `sys_login_log`: `user_id`, `created_at`, `status`

5. **菜单查询**：
   - `sys_menu`: `parent_id`, `is_active`, `is_visible`

---

## 📝 初始化数据

### 默认角色

```sql
INSERT INTO sys_role (name, code, description, is_system, is_active) VALUES
('超级管理员', 'super_admin', '拥有所有权限', TRUE, TRUE),
('管理员', 'admin', '系统管理员', TRUE, TRUE),
('普通用户', 'user', '普通用户', TRUE, TRUE),
('访客', 'guest', '访客用户', TRUE, TRUE);
```

### 默认权限

```sql
-- 用户管理权限
INSERT INTO sys_permission (name, code, content_type, action, description) VALUES
('用户创建', 'user:create', 'user', 'create', '创建用户'),
('用户查看', 'user:read', 'user', 'read', '查看用户'),
('用户更新', 'user:update', 'user', 'update', '更新用户'),
('用户删除', 'user:delete', 'user', 'delete', '删除用户');

-- 角色管理权限
INSERT INTO sys_permission (name, code, content_type, action, description) VALUES
('角色创建', 'role:create', 'role', 'create', '创建角色'),
('角色查看', 'role:read', 'role', 'read', '查看角色'),
('角色更新', 'role:update', 'role', 'update', '更新角色'),
('角色删除', 'role:delete', 'role', 'delete', '删除角色');
```

### 默认菜单

```sql
INSERT INTO sys_menu (name, title, path, icon, sort_order) VALUES
('dashboard', '仪表盘', '/dashboard', 'DashboardOutlined', 1),
('user', '用户管理', '/users', 'UserOutlined', 2),
('role', '角色管理', '/roles', 'TeamOutlined', 3),
('menu', '菜单管理', '/menus', 'MenuOutlined', 4);
```

---

## 🔒 数据安全建议

1. **敏感数据加密**：
   - 密码使用 PBKDF2 加密
   - 系统配置中的敏感信息加密存储

2. **软删除**：
   - 重要表支持软删除，避免数据丢失

3. **审计日志**：
   - 所有重要操作记录到 sys_audit_log

4. **数据备份**：
   - 定期备份数据库
   - 保留历史版本

5. **权限控制**：
   - 数据库层面使用最小权限原则
   - 应用层面使用 RBAC 权限控制

6. **数据一致性**：
   - 不使用数据库外键约束，数据一致性由应用层维护
   - 在业务逻辑中验证关联数据的有效性
   - 使用事务保证数据操作的原子性

---

## 📊 性能优化建议

1. **索引优化**：
   - 为常用查询字段添加索引
   - 避免过度索引

2. **查询优化**：
   - 使用 select_related 和 prefetch_related 减少查询次数
   - 避免 N+1 查询问题

3. **分表策略**：
   - 日志表可以按时间分表
   - 大表可以考虑分区

4. **缓存策略**：
   - 权限信息缓存到 Redis
   - 菜单信息缓存到 Redis
   - 系统配置缓存到 Redis

---

## 🛠️ 数据库迁移

### Django 迁移命令

```bash
# 创建迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 查看迁移状态
python manage.py showmigrations
```

### 手动 SQL 迁移（如需要）

```sql
-- 创建表
CREATE TABLE sys_user (...);

-- 添加索引
CREATE INDEX idx_user_email ON sys_user(email);
CREATE INDEX idx_user_profile_user_id ON sys_user_profile(user_id);
CREATE INDEX idx_user_profile_department_id ON sys_user_profile(department_id);

-- 注意：不使用外键约束，数据一致性由应用层维护
```

---

## 📚 参考文档

- [Django 模型字段参考](https://docs.djangoproject.com/en/stable/ref/models/fields/)
- [PostgreSQL 文档](https://www.postgresql.org/docs/)
- [MySQL 文档](https://dev.mysql.com/doc/)

---

**版本**: v1.0.0  
**最后更新**: 2024-01-01

