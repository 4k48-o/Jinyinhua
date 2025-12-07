# 🏛️ Django + React/AntD 企业级应用架构方案

## 📋 项目概述

本项目旨在构建一个基于 Django + Django REST Framework (DRF) + React + Ant Design 的企业级应用基础架构，提供完整的用户管理、权限控制、API 接口等基础设施，为快速开发企业级应用提供坚实的技术底座。

### 核心目标

- ✅ 提供完整的用户认证和授权系统（基于 RBAC）
- ✅ 实现前后端分离的 RESTful API 架构
- ✅ 构建可扩展、可维护的代码结构
- ✅ 提供统一的错误处理和日志系统
- ✅ 实现完善的 API 文档和开发规范
- ✅ 支持多环境配置和部署方案

---

## 🏗️ 整体架构概览

### 架构模式

采用**前后端分离**的架构模式：
- **前端 (Client)**：专注于用户界面 (UI) 和用户体验
- **后端 (API Server)**：专注于业务逻辑、数据存储和安全控制

### 技术栈

| 层级 | 技术选型 | 说明 |
|------|---------|------|
| 后端框架 | Django 4.x | Web 框架，提供 ORM、路由、中间件等 |
| API 框架 | Django REST Framework | RESTful API 开发框架 |
| 认证机制 | JWT (django-rest-framework-simplejwt) | 无状态认证方案 |
| 前端框架 | React 18.x | 用户界面框架 |
| UI 组件库 | Ant Design 5.x | 企业级 UI 组件库 |
| 状态管理 | Redux Toolkit / Zustand | 全局状态管理 |
| HTTP 客户端 | Axios | API 请求库 |
| 路由管理 | React Router v6 | 前端路由管理 |
| 数据库 | PostgreSQL / MySQL | 关系型数据库 |
| 缓存 | Redis | 缓存和会话存储 |
| 任务队列 | Celery | 异步任务处理 |

### 通信协议

- **协议**：RESTful API
- **数据格式**：JSON
- **认证方式**：JWT Token (Bearer Token)
- **API 版本**：URL 版本控制 (`/api/v1/`)

---

## ⚙️ 后端架构设计

### 1. 技术栈详解

#### 核心框架：Django

**职责**：
- 提供 ORM（对象关系映射）
- 数据库连接和迁移管理
- URL 路由配置
- 中间件处理
- 配置管理（多环境支持）
- 内置用户认证系统

**优势**：
- 利用 Django 内置的 User Model，快速实现用户注册、登录、密码重置等功能
- 完善的 Admin 后台管理系统
- 强大的 ORM 支持多种数据库
- 丰富的第三方包生态

#### API 框架：Django REST Framework (DRF)

**职责**：
- 将 Django 模型快速转化为 RESTful API 接口
- 处理序列化（Serialization）
- 请求解析和验证
- 视图集（ViewSets）和路由自动生成
- 分页、过滤、排序
- API 文档自动生成（Swagger/OpenAPI）

**核心组件**：
- **Serializers**：数据序列化和验证
- **ViewSets**：API 视图逻辑
- **Routers**：URL 路由自动生成
- **Permissions**：权限控制
- **Throttling**：API 限流
- **Pagination**：分页处理

#### 认证/鉴权：JWT (JSON Web Tokens)

**技术选型**：`django-rest-framework-simplejwt`

**工作流程**：
1. 用户登录，后端验证用户名密码
2. 验证成功后，生成 Access Token 和 Refresh Token
3. 前端存储 Token（建议存储在 httpOnly Cookie 或 localStorage）
4. 后续请求在 Header 中携带 Token：`Authorization: Bearer <token>`
5. 后端验证 Token 有效性，决定是否允许访问

**Token 类型**：
- **Access Token**：短期有效（如 15 分钟），用于 API 访问
- **Refresh Token**：长期有效（如 7 天），用于刷新 Access Token

**优势**：
- 无状态认证，适合分布式系统
- 支持跨域访问
- 减少数据库查询（无需存储会话）

#### 权限管理：基于 RBAC (Role-Based Access Control)

**权限模型**：
- **用户 (User)**：系统使用者
- **角色 (Role)**：权限集合，如管理员、普通用户、访客
- **权限 (Permission)**：具体操作权限，如创建、读取、更新、删除
- **资源 (Resource)**：被保护的对象，如用户、订单、产品

**实现方式**：
1. 利用 Django 的 `Permissions` 和 `Groups` 模型
2. 扩展自定义 `Role` 模型，关联多个权限
3. 将角色分配给用户（User -> Role -> Permission）
4. 在 DRF 中使用 `Custom Permissions` 检查用户权限
5. 支持细粒度的资源级权限控制

### 2. 项目结构设计

```
backend/
├── config/                 # Django 项目配置
│   ├── __init__.py
│   ├── settings/          # 多环境配置
│   │   ├── __init__.py
│   │   ├── base.py        # 基础配置
│   │   ├── development.py # 开发环境
│   │   ├── production.py  # 生产环境
│   │   └── testing.py    # 测试环境
│   ├── urls.py            # 主 URL 配置
│   └── wsgi.py            # WSGI 配置
│
├── apps/                   # 应用目录
│   ├── __init__.py
│   ├── users/             # 用户管理应用
│   │   ├── __init__.py
│   │   ├── models.py      # 用户模型（扩展 Django User）
│   │   ├── serializers.py # 用户序列化器
│   │   ├── views.py       # 用户视图
│   │   ├── permissions.py # 用户权限
│   │   ├── urls.py        # 用户路由
│   │   └── admin.py       # Admin 配置
│   │
│   ├── auth/              # 认证应用
│   │   ├── __init__.py
│   │   ├── views.py       # 登录、注册、刷新 Token
│   │   ├── serializers.py # 认证序列化器
│   │   └── urls.py        # 认证路由
│   │
│   ├── permissions/       # 权限管理应用
│   │   ├── __init__.py
│   │   ├── models.py      # 角色、权限模型
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── permissions.py # 自定义权限类
│   │
│   └── common/            # 通用应用
│       ├── __init__.py
│       ├── models.py      # 基础模型（时间戳等）
│       ├── exceptions.py  # 自定义异常
│       ├── responses.py   # 统一响应格式
│       ├── pagination.py  # 自定义分页
│       ├── filters.py     # 自定义过滤器
│       └── utils.py       # 工具函数
│
├── middleware/             # 自定义中间件
│   ├── __init__.py
│   ├── cors.py            # CORS 处理
│   ├── logging.py         # 请求日志
│   └── exception.py       # 异常处理
│
├── utils/                  # 全局工具
│   ├── __init__.py
│   ├── jwt.py             # JWT 工具函数
│   ├── validators.py      # 自定义验证器
│   └── helpers.py         # 辅助函数
│
├── requirements/           # 依赖管理
│   ├── base.txt           # 基础依赖
│   ├── development.txt    # 开发依赖
│   └── production.txt     # 生产依赖
│
├── manage.py
├── .env.example           # 环境变量示例
└── README.md
```

### 3. 核心功能模块

#### 3.1 用户管理模块

**功能**：
- 用户注册（邮箱/手机号验证）
- 用户登录（用户名/邮箱/手机号）
- 密码重置（邮件/短信）
- 用户信息管理（个人资料、头像上传）
- 用户状态管理（激活、禁用、删除）

**模型设计**：
```python
# 扩展 Django User 模型
class UserProfile(models.Model):
    user = OneToOneField(User)
    phone = CharField(max_length=20, unique=True)
    avatar = ImageField()
    department = ForeignKey(Department)
    position = CharField(max_length=100)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

#### 3.2 权限管理模块

**功能**：
- 角色管理（创建、编辑、删除角色）
- 权限分配（为角色分配权限）
- 用户角色管理（为用户分配角色）
- 资源权限控制（API 级别的权限检查）

**模型设计**：
```python
class Role(models.Model):
    name = CharField(max_length=50, unique=True)
    code = CharField(max_length=50, unique=True)  # 角色代码
    description = TextField()
    permissions = ManyToManyField(Permission)
    is_active = BooleanField(default=True)

class UserRole(models.Model):
    user = ForeignKey(User)
    role = ForeignKey(Role)
    assigned_at = DateTimeField(auto_now_add=True)
```

#### 3.3 API 接口设计

**统一响应格式**：
```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "timestamp": "2024-01-01T00:00:00Z"
}
```

**错误响应格式**：
```json
{
  "code": 400,
  "message": "错误信息",
  "errors": {
    "field_name": ["具体错误信息"]
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

**API 端点示例**：
```
# 认证相关
POST   /api/v1/auth/register/          # 用户注册
POST   /api/v1/auth/login/             # 用户登录
POST   /api/v1/auth/refresh/           # 刷新 Token
POST   /api/v1/auth/logout/            # 用户登出
POST   /api/v1/auth/password/reset/    # 密码重置

# 用户管理
GET    /api/v1/users/                  # 用户列表
GET    /api/v1/users/{id}/             # 用户详情
PUT    /api/v1/users/{id}/             # 更新用户
DELETE /api/v1/users/{id}/             # 删除用户
GET    /api/v1/users/me/               # 当前用户信息

# 权限管理
GET    /api/v1/roles/                  # 角色列表
POST   /api/v1/roles/                  # 创建角色
GET    /api/v1/roles/{id}/             # 角色详情
PUT    /api/v1/roles/{id}/             # 更新角色
DELETE /api/v1/roles/{id}/             # 删除角色
POST   /api/v1/users/{id}/roles/       # 为用户分配角色
```

### 4. 数据库设计

#### 核心表结构

**用户相关表**：
- `auth_user`：Django 内置用户表
- `users_userprofile`：用户扩展信息表
- `users_department`：部门表

**权限相关表**：
- `permissions_role`：角色表
- `permissions_userrole`：用户角色关联表
- `auth_permission`：Django 内置权限表
- `auth_group`：Django 内置组表

**通用表**：
- `common_auditlog`：操作日志表
- `common_systemconfig`：系统配置表

### 5. 安全设计

**认证安全**：
- 密码加密存储（Django 默认使用 PBKDF2）
- JWT Token 过期时间设置
- Refresh Token 轮换机制
- 登录失败次数限制（防止暴力破解）

**API 安全**：
- HTTPS 强制使用（生产环境）
- CORS 跨域配置
- API 限流（Throttling）
- SQL 注入防护（ORM 自动处理）
- XSS 防护（输入验证和转义）

**数据安全**：
- 敏感数据加密存储
- 数据库连接加密
- 定期数据备份
- 操作日志记录

---

## 🎨 前端架构设计

### 1. 技术栈详解

#### 核心框架：React 18.x

**特性**：
- 函数式组件 + Hooks
- 组件化开发
- 虚拟 DOM 高效渲染
- 丰富的生态系统

#### UI 组件库：Ant Design 5.x

**优势**：
- 企业级 UI 设计语言
- 丰富的组件库（100+ 组件）
- 完善的 TypeScript 支持
- 主题定制能力
- 国际化支持

**核心组件**：
- Layout（布局）
- Form（表单）
- Table（表格）
- Modal（对话框）
- Menu（菜单）
- Button（按钮）
- Input（输入框）

#### 状态管理：Redux Toolkit / Zustand

**Redux Toolkit**：
- 官方推荐的 Redux 使用方式
- 简化 Redux 配置
- 内置异步处理（createAsyncThunk）

**Zustand**（轻量级选择）：
- 更简单的 API
- 更少的样板代码
- 适合中小型项目

#### HTTP 客户端：Axios

**功能**：
- 请求/响应拦截器
- 自动添加 Token
- 统一错误处理
- 请求取消
- 请求/响应转换

### 2. 项目结构设计

```
frontend/
├── public/                 # 静态资源
│   ├── index.html
│   └── favicon.ico
│
├── src/
│   ├── api/               # API 接口
│   │   ├── index.ts       # Axios 实例配置
│   │   ├── auth.ts        # 认证相关 API
│   │   ├── user.ts        # 用户相关 API
│   │   └── role.ts        # 角色相关 API
│   │
│   ├── assets/            # 静态资源
│   │   ├── images/
│   │   ├── styles/
│   │   └── fonts/
│   │
│   ├── components/         # 通用组件
│   │   ├── Layout/        # 布局组件
│   │   ├── Form/          # 表单组件
│   │   ├── Table/         # 表格组件
│   │   └── common/        # 其他通用组件
│   │
│   ├── pages/             # 页面组件
│   │   ├── Login/         # 登录页
│   │   ├── Dashboard/     # 仪表盘
│   │   ├── Users/         # 用户管理
│   │   └── Roles/        # 角色管理
│   │
│   ├── store/             # 状态管理
│   │   ├── index.ts       # Store 配置
│   │   ├── slices/        # Redux Slices
│   │   │   ├── authSlice.ts
│   │   │   └── userSlice.ts
│   │   └── hooks.ts       # Typed Hooks
│   │
│   ├── hooks/             # 自定义 Hooks
│   │   ├── useAuth.ts     # 认证 Hook
│   │   ├── usePermission.ts # 权限 Hook
│   │   └── useRequest.ts  # 请求 Hook
│   │
│   ├── utils/             # 工具函数
│   │   ├── request.ts     # 请求封装
│   │   ├── storage.ts     # 本地存储
│   │   ├── format.ts      # 格式化函数
│   │   └── constants.ts   # 常量定义
│   │
│   ├── router/             # 路由配置
│   │   ├── index.tsx      # 路由定义
│   │   ├── routes.tsx     # 路由列表
│   │   └── PrivateRoute.tsx # 私有路由
│   │
│   ├── types/             # TypeScript 类型
│   │   ├── api.ts         # API 类型
│   │   ├── user.ts        # 用户类型
│   │   └── common.ts      # 通用类型
│   │
│   ├── App.tsx            # 根组件
│   ├── index.tsx          # 入口文件
│   └── main.tsx           # 主文件（Vite）
│
├── .env.development       # 开发环境变量
├── .env.production        # 生产环境变量
├── package.json
├── tsconfig.json          # TypeScript 配置
├── vite.config.ts         # Vite 配置
└── README.md
```

### 3. 核心功能实现

#### 3.1 认证流程

**登录流程**：
1. 用户输入用户名和密码
2. 调用登录 API，获取 Token
3. 存储 Token 到 localStorage 或 Cookie
4. 设置 Axios 默认 Header
5. 跳转到 Dashboard

**Token 管理**：
```typescript
// 存储 Token
localStorage.setItem('access_token', token);

// 请求拦截器自动添加 Token
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 响应拦截器处理 Token 过期
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Token 过期，跳转登录
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

#### 3.2 权限控制

**路由权限**：
```typescript
// 私有路由组件
const PrivateRoute = ({ children, requiredPermission }) => {
  const { user, hasPermission } = useAuth();
  
  if (!user) {
    return <Navigate to="/login" />;
  }
  
  if (requiredPermission && !hasPermission(requiredPermission)) {
    return <Navigate to="/403" />;
  }
  
  return children;
};
```

**按钮权限**：
```typescript
// 权限按钮组件
const PermissionButton = ({ permission, children, ...props }) => {
  const { hasPermission } = useAuth();
  
  if (!hasPermission(permission)) {
    return null;
  }
  
  return <Button {...props}>{children}</Button>;
};
```

#### 3.3 状态管理

**认证状态**：
```typescript
// authSlice.ts
const authSlice = createSlice({
  name: 'auth',
  initialState: {
    user: null,
    token: null,
    isAuthenticated: false,
  },
  reducers: {
    setCredentials: (state, action) => {
      state.user = action.payload.user;
      state.token = action.payload.token;
      state.isAuthenticated = true;
    },
    logout: (state) => {
      state.user = null;
      state.token = null;
      state.isAuthenticated = false;
    },
  },
});
```

---

## 📦 开发规范

### 1. 代码规范

**后端（Python）**：
- 遵循 PEP 8 代码风格
- 使用 Black 进行代码格式化
- 使用 isort 进行导入排序
- 使用 Flake8 进行代码检查
- 类型提示（Type Hints）

**前端（TypeScript）**：
- 使用 ESLint 进行代码检查
- 使用 Prettier 进行代码格式化
- 严格的 TypeScript 配置
- 组件命名使用 PascalCase
- 函数命名使用 camelCase

### 2. Git 工作流

**分支策略**：
- `main`：生产环境分支
- `develop`：开发环境分支
- `feature/*`：功能分支
- `bugfix/*`：修复分支
- `hotfix/*`：热修复分支

**提交规范**：
```
feat: 新功能
fix: 修复 bug
docs: 文档更新
style: 代码格式调整
refactor: 代码重构
test: 测试相关
chore: 构建/工具相关
```

### 3. API 设计规范

**RESTful 规范**：
- 使用 HTTP 动词（GET、POST、PUT、DELETE、PATCH）
- 使用名词表示资源
- 使用复数形式（`/users` 而不是 `/user`）
- 使用嵌套资源表示关系（`/users/1/roles`）
- 使用查询参数进行过滤、排序、分页

**命名规范**：
- URL 使用小写字母和连字符（`/user-profiles`）
- 字段名使用下划线（`created_at`）
- 常量使用大写字母和下划线（`MAX_RETRY_COUNT`）

---

## 🚀 部署方案

### 1. 后端部署

**Docker 部署**：
```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

**环境变量配置**：
```env
# .env
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@db:5432/dbname
REDIS_URL=redis://redis:6379/0
ALLOWED_HOSTS=yourdomain.com
```

### 2. 前端部署

**构建命令**：
```bash
npm run build
```

**Nginx 配置**：
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    root /var/www/frontend/dist;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. 数据库迁移

```bash
# 生成迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

---

## 📚 开发指南

### 1. 环境搭建

**后端**：
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements/development.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 运行迁移
python manage.py migrate

# 启动开发服务器
python manage.py runserver
```

**前端**：
```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

### 2. 测试

**后端测试**：
```bash
# 运行所有测试
python manage.py test

# 运行特定应用测试
python manage.py test apps.users
```

**前端测试**：
```bash
# 运行单元测试
npm run test

# 运行 E2E 测试
npm run test:e2e
```

---

## 📖 API 文档

### 自动生成 API 文档

使用 `drf-yasg` 或 `drf-spectacular` 自动生成 Swagger/OpenAPI 文档：

```python
# settings.py
INSTALLED_APPS = [
    'drf_spectacular',
]

SPECTACULAR_SETTINGS = {
    'TITLE': '企业级应用 API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
```

访问地址：`http://localhost:8000/api/docs/`

---

## 🔧 常用工具和库

### 后端

- **django-cors-headers**：CORS 跨域处理
- **django-filter**：API 过滤
- **django-extensions**：开发工具扩展
- **celery**：异步任务队列
- **redis**：缓存和消息队列
- **pillow**：图片处理
- **python-decouple**：环境变量管理

### 前端

- **react-router-dom**：路由管理
- **@reduxjs/toolkit**：状态管理
- **react-query**：数据获取和缓存
- **dayjs**：日期处理
- **lodash**：工具函数库
- **axios**：HTTP 客户端

---

## 📝 后续扩展

### 功能扩展方向

1. **文件上传**：支持图片、文档上传（OSS/本地存储）
2. **消息通知**：站内消息、邮件通知、短信通知
3. **数据导出**：Excel、PDF 导出功能
4. **日志系统**：操作日志、系统日志、错误日志
5. **监控告警**：系统监控、性能监控、错误告警
6. **多租户支持**：SaaS 多租户架构
7. **国际化**：多语言支持（i18n）
8. **主题切换**：深色/浅色主题

### 性能优化

1. **数据库优化**：索引优化、查询优化、连接池
2. **缓存策略**：Redis 缓存、CDN 加速
3. **前端优化**：代码分割、懒加载、图片优化
4. **API 优化**：接口合并、批量操作、分页优化

---

## 📞 技术支持

如有问题，请参考：
- Django 官方文档：https://docs.djangoproject.com/
- DRF 官方文档：https://www.django-rest-framework.org/
- React 官方文档：https://react.dev/
- Ant Design 官方文档：https://ant.design/

---

**版本**：v1.0.0  
**最后更新**：2024-01-01
