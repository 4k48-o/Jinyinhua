# 🎨 前端开发计划

## 📋 项目概述

本文档详细规划了基于 React + Ant Design 的企业级应用前端开发计划，按照模块化和组件化的开发原则，分阶段实现用户界面和交互功能。

---

## 🎯 开发目标

- 构建现代化、响应式的用户界面
- 实现完整的用户认证和权限控制
- 建立可复用、可维护的组件库
- 提供流畅的用户体验
- 支持多设备适配（PC、平板、移动端）

---

## 📅 开发阶段总览

| 阶段 | 名称 | 预计时间 | 优先级 | 状态 |
|------|------|---------|--------|------|
| Phase 1 | 项目初始化和基础架构 | 3-4 天 | P0 | ✅ 已完成 |
| Phase 2 | 认证系统开发 | 4-5 天 | P0 | ✅ 已完成 |
| Phase 3 | 布局和导航系统 | 3-4 天 | P0 | ⏳ 待开始 |
| Phase 4 | 用户管理模块 | 5-6 天 | P0 | ⏳ 待开始 |
| Phase 5 | 权限管理模块 | 4-5 天 | P1 | ⏳ 待开始 |
| Phase 6 | 通用组件开发 | 3-4 天 | P1 | ⏳ 待开始 |
| Phase 7 | 性能优化和测试 | 3-4 天 | P1 | ⏳ 待开始 |

**总预计时间**：25-32 个工作日

---

## Phase 1: 项目初始化和基础架构

### 🎯 阶段目标

搭建前端项目基础架构，配置开发环境，建立项目目录结构，配置核心依赖和工具链。

### 📝 任务清单

#### 1.1 项目初始化
- [x] 使用 Vite 创建 React + TypeScript 项目（手动创建项目结构）
- [x] 配置项目基本信息（package.json）
- [x] 配置 TypeScript（tsconfig.json, tsconfig.node.json）
- [x] 配置 ESLint 和 Prettier（.eslintrc.cjs, .prettierrc）

#### 1.2 目录结构创建
- [x] 创建 `src/api/` API 接口目录
- [x] 创建 `src/components/` 组件目录
  - [x] `Layout/` 布局组件
  - [x] `Form/` 表单组件
  - [x] `Table/` 表格组件
  - [x] `common/` 通用组件
- [x] 创建 `src/pages/` 页面目录
- [x] 创建 `src/store/` 状态管理目录
- [x] 创建 `src/hooks/` 自定义 Hooks 目录
- [x] 创建 `src/utils/` 工具函数目录
- [x] 创建 `src/router/` 路由配置目录
- [x] 创建 `src/types/` TypeScript 类型目录
- [x] 创建 `src/assets/` 静态资源目录
  - [x] `images/` 图片
  - [x] `styles/` 样式
  - [x] `fonts/` 字体

#### 1.3 核心依赖安装
- [x] 配置 package.json（包含所有依赖）
  - [x] React Router (react-router-dom)
  - [x] Ant Design (antd)
  - [x] Axios
  - [x] Redux Toolkit (@reduxjs/toolkit, react-redux)
  - [x] 图标库 (@ant-design/icons)
  - [x] 工具库 (dayjs, lodash-es)
- [ ] 运行 `npm install` 安装依赖（需要手动执行）

#### 1.4 开发工具配置
- [x] 配置 Vite（vite.config.ts）
  - [x] 路径别名配置（@/）
  - [x] 代理配置（开发环境）
  - [x] 环境变量配置
- [x] 配置 ESLint（.eslintrc.cjs）
- [x] 配置 Prettier（.prettierrc）
- [x] 配置环境变量文件
  - [x] `.env.development` 开发环境
  - [x] `.env.production` 生产环境
- [x] 配置 Git 忽略文件（.gitignore）

#### 1.5 API 请求封装
- [x] 创建 Axios 实例 `src/api/index.ts`
- [x] 配置请求拦截器
  - [x] 自动添加 Token
  - [x] 添加请求头（X-Language）
  - [x] 请求参数处理
- [x] 配置响应拦截器
  - [x] Token 过期处理（401 自动跳转登录）
  - [x] 统一错误处理
  - [x] 响应数据转换
- [ ] 实现请求取消功能（可选，后续添加）
- [ ] 实现请求重试机制（可选，后续添加）

#### 1.6 国际化（i18n）配置
- [x] 安装国际化依赖
  - [x] react-i18next（React i18n 集成）
  - [x] i18next（核心 i18n 框架）
  - [x] i18next-browser-languagedetector（浏览器语言检测）
- [x] 创建 `src/i18n/` 国际化目录
- [x] 创建 `src/i18n/index.ts` i18n 配置文件
  - [x] 配置 i18next 初始化
  - [x] 配置语言资源加载
  - [x] 配置语言检测（localStorage + 浏览器）
  - [x] 配置 fallback 策略
  - [x] 配置 Ant Design 语言包集成
- [x] 创建翻译文件目录 `src/i18n/locales/`
  - [x] `zh-CN.json` 简体中文翻译
  - [x] `zh-TW.json` 繁体中文翻译
  - [x] `en.json` 英文翻译
- [x] 实现翻译文件结构
  - [x] common（通用翻译）
  - [x] auth（认证相关翻译）
  - [x] layout（布局相关翻译）
  - [x] error（错误信息翻译）
  - [x] validation（验证信息翻译）
- [x] 配置 Ant Design 国际化
  - [x] 在 `App.tsx` 中集成 Ant Design Locale
  - [x] 实现语言切换时自动更新 Ant Design 语言
- [x] 实现语言切换组件
  - [x] 创建 `src/components/Layout/LanguageSwitcher.tsx`
  - [x] 实现语言下拉菜单
  - [x] 实现语言切换功能
  - [x] 实现语言持久化（localStorage）
  - [x] 固定到屏幕右上角显示
- [x] 集成 API 请求语言头
  - [x] 在 `src/api/index.ts` 中添加 `X-Language` 请求头
  - [x] 自动从 localStorage 读取当前语言

#### 1.7 工具函数开发
- [x] 创建 `src/utils/request.ts` 请求工具（get, post, put, patch, delete, upload）
- [x] 创建 `src/utils/storage.ts` 本地存储工具
  - [x] localStorage 封装
  - [x] sessionStorage 封装
  - [x] Token 存储和获取
- [x] 创建 `src/utils/format.ts` 格式化函数
  - [x] 日期格式化（formatDate, formatDateOnly, formatTimeOnly, formatRelativeTime）
  - [x] 数字格式化（formatNumber, formatNumberWithCommas）
  - [x] 文件大小格式化（formatFileSize）
  - [x] 百分比格式化（formatPercent）
- [x] 创建 `src/utils/constants.ts` 常量定义
  - [x] 语言选项常量（LANGUAGES）
- [x] 创建 `src/types/index.ts` TypeScript 类型定义
- [ ] 创建 `src/utils/helpers.ts` 辅助函数

#### 1.8 TypeScript 类型定义
- [ ] 创建 `src/types/api.ts` API 响应类型
- [ ] 创建 `src/types/user.ts` 用户类型
- [ ] 创建 `src/types/role.ts` 角色类型
- [ ] 创建 `src/types/common.ts` 通用类型
- [ ] 创建 `src/types/index.ts` 类型导出

#### 1.9 样式配置
- [ ] 配置 Ant Design 主题定制
- [ ] 创建全局样式文件 `src/styles/global.less`
- [ ] 创建变量文件 `src/styles/variables.less`
- [ ] 配置 CSS Modules（如需要）
- [ ] 配置 Less/Sass（如需要）

### ✅ 验收标准

- [ ] 项目可以成功启动（`npm run dev`）
- [ ] TypeScript 编译无错误
- [ ] ESLint 和 Prettier 配置生效
- [ ] API 请求封装完成
- [ ] 工具函数可以正常使用
- [ ] 代码结构符合规范

### 📦 交付物

- 完整的项目目录结构
- `package.json` 和依赖文件
- 配置文件（tsconfig.json, vite.config.ts 等）
- API 请求封装代码
- 工具函数库

---

## Phase 2: 认证系统开发

### 🎯 阶段目标

实现用户认证功能，包括登录、注册、Token 管理、权限检查等核心功能。

### 📝 任务清单

#### 2.1 状态管理设置
- [x] 配置 Redux Store (`src/store/index.ts`)
- [x] 创建认证状态 Slice `src/store/slices/authSlice.ts`
  - [x] 用户信息状态
  - [x] Token 状态
  - [x] 登录状态
  - [x] 权限列表状态
  - [x] 角色列表状态
- [x] 实现认证 Actions
  - [x] `login` 登录（异步）
  - [x] `register` 注册（异步）
  - [x] `logout` 登出（异步）
  - [x] `setUser` 设置用户信息
  - [x] `setTokens` 设置 Token
  - [x] `refreshToken` 刷新 Token（异步）
  - [x] `getCurrentUser` 获取当前用户（异步）
  - [x] `clearAuth` 清除认证信息

#### 2.2 API 接口开发
- [x] 创建 `src/api/auth.ts` 认证 API
- [x] 实现登录接口 `login()`
- [x] 实现注册接口 `register()`
- [x] 实现刷新 Token 接口 `refreshToken()`
- [x] 实现登出接口 `logout()`
- [x] 实现获取当前用户接口 `getCurrentUser()`
- [ ] 实现密码重置接口 `resetPassword()`（前期暂不实现）

#### 2.3 登录页面开发
- [x] 创建 `src/pages/Login/` 登录页面
- [x] 实现登录表单
  - [x] 用户名输入框
  - [x] 密码输入框
  - [x] 记住我选项
  - [x] 验证码（动态显示，登录失败时触发）
- [x] 实现表单验证
- [x] 实现登录逻辑
  - [x] 调用登录 API
  - [x] 存储 Token（通过 Redux）
  - [x] 更新状态
  - [x] 跳转到 Dashboard
- [x] 实现错误提示
- [x] 实现加载状态

#### 2.4 注册页面开发
- [x] 创建 `src/pages/Register/` 注册页面
- [x] 实现注册表单
  - [x] 用户名输入框
  - [x] 密码输入框
  - [x] 确认密码输入框
  - [ ] 邮箱输入框（前期暂不支持）
  - [ ] 手机号输入框（前期暂不支持）
- [x] 实现表单验证（用户名、密码强度、密码确认）
- [x] 实现注册逻辑
- [x] 实现成功提示和跳转

#### 2.5 Token 管理
- [x] 实现 Token 存储（localStorage，已在 `utils/storage.ts` 中实现）
- [x] 实现 Token 自动刷新机制（Redux 中已实现 `refreshToken` action）
- [x] 实现 Token 过期处理（响应拦截器中已处理 401）
- [x] 在请求拦截器中自动添加 Token（已在 `api/index.ts` 中实现）
- [x] 在响应拦截器中处理 Token 过期（已在 `api/index.ts` 中实现）

#### 2.6 权限检查 Hook
- [x] 创建 `src/hooks/useAuth.ts` 认证 Hook
  - [x] `isAuthenticated` 是否已登录
  - [x] `user` 当前用户信息
  - [x] `hasPermission` 权限检查
  - [x] `hasRole` 角色检查
  - [x] `hasAnyPermission` 检查任一权限
  - [x] `hasAnyRole` 检查任一角色
  - [x] `hasAllPermissions` 检查所有权限
  - [x] `hasAllRoles` 检查所有角色
- [ ] 创建 `src/hooks/usePermission.ts` 权限 Hook（可选，useAuth 已包含）
- [x] 实现权限缓存机制（Redux Store 中存储）

#### 2.7 路由保护
- [x] 创建 `src/router/PrivateRoute.tsx` 私有路由组件
- [x] 实现登录状态检查
- [x] 实现权限检查（requirePermission）
- [x] 实现角色检查（requireRole）
- [x] 实现未授权跳转（未登录跳转登录页，无权限跳转 403）
- [x] 创建 403 无权限页面 (`src/pages/403.tsx`)
- [x] 创建 404 未找到页面 (`src/pages/404.tsx`)
- [x] 配置路由 (`src/router/index.tsx`)

#### 2.8 认证流程优化
- [x] 实现自动登录（记住我功能，Token 存储在 localStorage）
- [x] 实现登录状态持久化（Redux + localStorage）
- [x] 实现登出清理逻辑（clearAuth action）
- [ ] 实现多标签页同步（可选，后续添加）

### ✅ 验收标准

- [x] 用户可以成功登录和注册
- [x] Token 可以正常存储和刷新
- [x] 未登录用户无法访问受保护页面
- [x] 权限检查功能正常
- [x] 登录状态可以持久化
- [x] 错误提示清晰明确

### 📦 交付物

- 登录和注册页面
- 认证相关的 API 接口
- 认证状态管理代码
- 权限检查 Hook
- 路由保护组件

---

## Phase 3: 布局和导航系统

### 🎯 阶段目标

实现应用主布局结构，包括侧边栏、顶部导航、面包屑、用户菜单等。

### 📝 任务清单

#### 3.1 主布局组件
- [x] 创建 `src/components/Layout/MainLayout.tsx` 主布局
- [x] 实现布局结构
  - [x] 侧边栏（Sider）
  - [x] 顶部导航（Header）
  - [x] 内容区域（Content）
  - [ ] 页脚（Footer，可选）
- [x] 实现响应式布局
- [x] 实现侧边栏折叠/展开

#### 3.2 侧边栏菜单
- [x] 创建 `src/components/Layout/Sidebar.tsx` 侧边栏组件
- [x] 实现菜单配置 `src/router/menus.tsx`
- [x] 实现菜单渲染
  - [x] 多级菜单支持
  - [x] 图标显示
  - [x] 菜单高亮
  - [x] 菜单折叠
- [x] 实现菜单权限控制
- [x] 实现菜单路由跳转

#### 3.3 顶部导航栏
- [x] 创建 `src/components/Layout/Header.tsx` 顶部导航
- [x] 实现面包屑导航
- [x] 实现用户菜单
  - [x] 用户头像和名称
  - [x] 下拉菜单（个人中心、设置、退出）
- [ ] 实现通知中心（可选）
- [ ] 实现全屏切换（可选）
- [ ] 实现主题切换（可选）

#### 3.4 路由配置
- [x] 创建 `src/router/index.tsx` 路由配置
- [x] 配置路由列表（集成到 menus.tsx）
- [x] 实现路由懒加载
- [x] 实现路由权限控制
- [x] 配置路由守卫（PrivateRoute）
- [x] 实现 404 页面路由

#### 3.5 页面容器组件
- [x] 创建 `src/components/Layout/PageContainer.tsx` 页面容器
- [x] 实现页面标题
- [x] 实现页面操作按钮区域
- [x] 实现页面内容区域
- [x] 实现页面加载状态

#### 3.6 响应式设计
- [x] 实现移动端适配
- [x] 实现平板适配
- [x] 实现侧边栏移动端抽屉模式（基础实现）
- [x] 实现响应式断点配置

#### 3.7 主题定制
- [x] 配置 Ant Design 主题（基础配置）
- [ ] 实现主题变量定制
- [ ] 实现深色模式（可选）
- [ ] 实现主题切换功能

### ✅ 验收标准

- [ ] 布局结构完整
- [ ] 侧边栏菜单正常显示和跳转
- [ ] 顶部导航功能正常
- [ ] 路由配置正确
- [ ] 响应式布局正常
- [ ] 权限控制生效

### 📦 交付物

- 主布局组件
- 侧边栏和顶部导航组件
- 路由配置
- 页面容器组件

---

## Phase 4: 用户管理模块

### 🎯 阶段目标

实现用户管理功能，包括用户列表、用户详情、用户创建、用户编辑、用户删除等。

### 📝 任务清单

#### 4.1 API 接口开发
- [ ] 创建 `src/api/user.ts` 用户 API
- [ ] 实现获取用户列表接口 `getUserList()`
- [ ] 实现获取用户详情接口 `getUserDetail()`
- [ ] 实现创建用户接口 `createUser()`
- [ ] 实现更新用户接口 `updateUser()`
- [ ] 实现删除用户接口 `deleteUser()`
- [ ] 实现获取当前用户接口 `getCurrentUser()`
- [ ] 实现更新当前用户接口 `updateCurrentUser()`
- [ ] 实现用户头像上传接口 `uploadAvatar()`

#### 4.2 状态管理
- [ ] 创建 `src/store/slices/userSlice.ts` 用户状态
- [ ] 实现用户列表状态管理
- [ ] 实现用户详情状态管理
- [ ] 实现用户操作 Actions
  - [ ] `fetchUsers` 获取用户列表
  - [ ] `fetchUserDetail` 获取用户详情
  - [ ] `createUser` 创建用户
  - [ ] `updateUser` 更新用户
  - [ ] `deleteUser` 删除用户

#### 4.3 用户列表页面
- [ ] 创建 `src/pages/Users/List.tsx` 用户列表页面
- [ ] 实现用户列表表格
  - [ ] 表格列定义（ID、用户名、邮箱、手机号、部门、状态等）
  - [ ] 表格操作列（查看、编辑、删除）
- [ ] 实现搜索功能
  - [ ] 用户名搜索
  - [ ] 邮箱搜索
  - [ ] 手机号搜索
- [ ] 实现过滤功能
  - [ ] 部门过滤
  - [ ] 状态过滤
  - [ ] 角色过滤
- [ ] 实现排序功能
- [ ] 实现分页功能
- [ ] 实现批量操作（可选）

#### 4.4 用户创建/编辑页面
- [ ] 创建 `src/pages/Users/Form.tsx` 用户表单页面
- [ ] 实现用户表单
  - [ ] 基本信息字段（用户名、邮箱、手机号）
  - [ ] 密码字段（创建时必填，编辑时可选）
  - [ ] 扩展信息字段（部门、职位、头像等）
- [ ] 实现表单验证
- [ ] 实现表单提交逻辑
- [ ] 实现表单重置
- [ ] 实现加载状态

#### 4.5 用户详情页面
- [ ] 创建 `src/pages/Users/Detail.tsx` 用户详情页面
- [ ] 实现用户信息展示
- [ ] 实现用户角色展示
- [ ] 实现用户操作日志（可选）
- [ ] 实现编辑按钮和跳转

#### 4.6 个人中心页面
- [ ] 创建 `src/pages/Profile/` 个人中心页面
- [ ] 实现个人信息展示
- [ ] 实现个人信息编辑
- [ ] 实现头像上传
- [ ] 实现密码修改
- [ ] 实现安全设置（可选）

#### 4.7 通用组件开发
- [ ] 创建 `src/components/User/UserAvatar.tsx` 用户头像组件
- [ ] 创建 `src/components/User/UserSelect.tsx` 用户选择器组件
- [ ] 创建 `src/components/Form/UserForm.tsx` 用户表单组件（可复用）

#### 4.8 权限控制
- [ ] 实现用户列表查看权限
- [ ] 实现用户创建权限
- [ ] 实现用户编辑权限
- [ ] 实现用户删除权限
- [ ] 实现按钮级权限控制

### ✅ 验收标准

- [ ] 用户列表可以正常显示
- [ ] 搜索、过滤、排序功能正常
- [ ] 可以成功创建、编辑、删除用户
- [ ] 用户详情页面正常显示
- [ ] 个人中心功能正常
- [ ] 权限控制正确生效

### 📦 交付物

- 用户管理相关页面
- 用户 API 接口
- 用户状态管理代码
- 用户相关组件

---

## Phase 5: 权限管理模块

### 🎯 阶段目标

实现权限管理功能，包括角色列表、角色创建/编辑、权限分配、用户角色管理等。

### 📝 任务清单

#### 5.1 API 接口开发
- [ ] 创建 `src/api/role.ts` 角色 API
- [ ] 实现获取角色列表接口 `getRoleList()`
- [ ] 实现获取角色详情接口 `getRoleDetail()`
- [ ] 实现创建角色接口 `createRole()`
- [ ] 实现更新角色接口 `updateRole()`
- [ ] 实现删除角色接口 `deleteRole()`
- [ ] 实现获取权限列表接口 `getPermissionList()`
- [ ] 实现用户角色管理接口
  - [ ] `getUserRoles()` 获取用户角色
  - [ ] `assignUserRole()` 分配角色
  - [ ] `removeUserRole()` 移除角色

#### 5.2 状态管理
- [ ] 创建 `src/store/slices/roleSlice.ts` 角色状态
- [ ] 实现角色列表状态管理
- [ ] 实现权限列表状态管理
- [ ] 实现角色操作 Actions

#### 5.3 角色列表页面
- [ ] 创建 `src/pages/Roles/List.tsx` 角色列表页面
- [ ] 实现角色列表表格
  - [ ] 表格列定义（ID、角色名称、角色代码、描述、权限数量等）
  - [ ] 表格操作列（查看、编辑、删除）
- [ ] 实现搜索功能
- [ ] 实现分页功能

#### 5.4 角色创建/编辑页面
- [ ] 创建 `src/pages/Roles/Form.tsx` 角色表单页面
- [ ] 实现角色表单
  - [ ] 角色名称
  - [ ] 角色代码
  - [ ] 角色描述
  - [ ] 权限选择（树形选择器）
- [ ] 实现表单验证
- [ ] 实现表单提交逻辑

#### 5.5 角色详情页面
- [ ] 创建 `src/pages/Roles/Detail.tsx` 角色详情页面
- [ ] 实现角色信息展示
- [ ] 实现权限列表展示
- [ ] 实现拥有该角色的用户列表

#### 5.6 权限树组件
- [ ] 创建 `src/components/Permission/PermissionTree.tsx` 权限树组件
- [ ] 实现权限树形结构展示
- [ ] 实现权限选择功能
- [ ] 实现权限搜索功能
- [ ] 实现权限展开/折叠

#### 5.7 用户角色管理
- [ ] 创建 `src/pages/Users/Roles.tsx` 用户角色管理页面
- [ ] 实现用户当前角色展示
- [ ] 实现角色分配功能
- [ ] 实现角色移除功能
- [ ] 实现角色选择器

#### 5.8 权限检查组件
- [ ] 创建 `src/components/Permission/PermissionButton.tsx` 权限按钮组件
- [ ] 创建 `src/components/Permission/PermissionWrapper.tsx` 权限包装组件
- [ ] 实现基于权限的组件显示/隐藏

### ✅ 验收标准

- [ ] 角色列表可以正常显示
- [ ] 可以成功创建、编辑、删除角色
- [ ] 权限分配功能正常
- [ ] 用户角色管理功能正常
- [ ] 权限树组件正常显示
- [ ] 权限检查组件正常工作

### 📦 交付物

- 权限管理相关页面
- 角色 API 接口
- 角色状态管理代码
- 权限相关组件

---

## Phase 6: 通用组件开发

### 🎯 阶段目标

开发可复用的通用组件，提高开发效率和代码复用性。

### 📝 任务清单

#### 6.1 表格组件
- [ ] 创建 `src/components/Table/DataTable.tsx` 数据表格组件
- [ ] 实现表格功能
  - [ ] 列配置
  - [ ] 分页
  - [ ] 排序
  - [ ] 过滤
  - [ ] 选择（单选/多选）
  - [ ] 操作列
- [ ] 实现表格加载状态
- [ ] 实现表格空状态
- [ ] 实现表格导出功能（可选）

#### 6.2 表单组件
- [ ] 创建 `src/components/Form/SearchForm.tsx` 搜索表单组件
- [ ] 创建 `src/components/Form/FormModal.tsx` 表单弹窗组件
- [ ] 创建 `src/components/Form/FormDrawer.tsx` 表单抽屉组件
- [ ] 实现表单验证规则
- [ ] 实现表单重置功能

#### 6.3 文件上传组件
- [ ] 创建 `src/components/Upload/ImageUpload.tsx` 图片上传组件
- [ ] 创建 `src/components/Upload/FileUpload.tsx` 文件上传组件
- [ ] 实现上传进度显示
- [ ] 实现图片预览
- [ ] 实现文件类型验证
- [ ] 实现文件大小限制

#### 6.4 数据展示组件
- [ ] 创建 `src/components/Display/StatusTag.tsx` 状态标签组件
- [ ] 创建 `src/components/Display/UserInfo.tsx` 用户信息组件
- [ ] 创建 `src/components/Display/DateTime.tsx` 日期时间组件
- [ ] 创建 `src/components/Display/Empty.tsx` 空状态组件

#### 6.5 反馈组件
- [ ] 创建 `src/components/Feedback/Loading.tsx` 加载组件
- [ ] 创建 `src/components/Feedback/ErrorBoundary.tsx` 错误边界组件
- [ ] 实现全局消息提示
- [ ] 实现确认对话框封装

#### 6.6 工具组件
- [ ] 创建 `src/components/Common/PageHeader.tsx` 页面头部组件
- [ ] 创建 `src/components/Common/ActionBar.tsx` 操作栏组件
- [ ] 创建 `src/components/Common/FilterBar.tsx` 过滤栏组件
- [ ] 创建 `src/components/Common/Breadcrumb.tsx` 面包屑组件（增强）

#### 6.7 业务组件
- [ ] 创建 `src/components/Business/UserSelector.tsx` 用户选择器
- [ ] 创建 `src/components/Business/RoleSelector.tsx` 角色选择器
- [ ] 创建 `src/components/Business/DepartmentTree.tsx` 部门树组件

### ✅ 验收标准

- [ ] 所有通用组件可以正常使用
- [ ] 组件 API 设计合理
- [ ] 组件文档完整
- [ ] 组件可以复用

### 📦 交付物

- 通用组件库
- 组件使用文档
- 组件示例代码

---

## Phase 7: 性能优化和测试

### 🎯 阶段目标

优化应用性能，编写测试用例，确保代码质量和用户体验。

### 📝 任务清单

#### 7.1 性能优化
- [ ] 实现代码分割（Code Splitting）
- [ ] 实现路由懒加载
- [ ] 实现组件懒加载（React.lazy）
- [ ] 优化图片加载（懒加载、压缩）
- [ ] 实现虚拟滚动（长列表）
- [ ] 优化状态管理（避免不必要的重渲染）
- [ ] 实现请求防抖和节流
- [ ] 优化打包体积（Tree Shaking）

#### 7.2 缓存优化
- [ ] 实现 API 响应缓存（React Query）
- [ ] 实现路由缓存
- [ ] 实现本地存储缓存策略
- [ ] 实现 Service Worker（可选，PWA）

#### 7.3 用户体验优化
- [ ] 实现加载骨架屏
- [ ] 实现平滑过渡动画
- [ ] 优化错误提示
- [ ] 实现操作反馈（成功、失败提示）
- [ ] 优化表单交互体验

#### 7.4 单元测试
- [ ] 配置测试环境（Jest + React Testing Library）
- [ ] 编写工具函数测试
- [ ] 编写 Hook 测试
- [ ] 编写组件测试
- [ ] 实现测试覆盖率 > 80%

#### 7.5 集成测试
- [ ] 编写页面集成测试
- [ ] 编写用户流程测试
- [ ] 编写 API 集成测试

#### 7.6 E2E 测试（可选）
- [ ] 配置 E2E 测试工具（Cypress / Playwright）
- [ ] 编写关键流程 E2E 测试
- [ ] 实现自动化测试流程

#### 7.7 代码质量
- [ ] 配置代码检查工具
- [ ] 修复 ESLint 警告
- [ ] 修复 TypeScript 错误
- [ ] 代码审查

#### 7.8 构建和部署
- [ ] 配置生产环境构建
- [ ] 优化构建配置
- [ ] 配置环境变量
- [ ] 创建部署脚本
- [ ] 配置 CI/CD（可选）

### ✅ 验收标准

- [ ] 页面加载速度优化
- [ ] 代码分割和懒加载生效
- [ ] 测试覆盖率 > 80%
- [ ] 无 ESLint 和 TypeScript 错误
- [ ] 可以成功构建生产版本

### 📦 交付物

- 优化后的代码
- 测试用例
- 测试覆盖率报告
- 构建配置文件

---

## 📊 开发规范

### 代码规范
- 遵循 React 最佳实践
- 使用函数式组件和 Hooks
- 使用 TypeScript 严格模式
- 组件命名使用 PascalCase
- 函数命名使用 camelCase
- 使用 ESLint 和 Prettier

### 组件规范
- 组件单一职责原则
- Props 使用 TypeScript 接口定义
- 组件要有清晰的文档注释
- 可复用组件放在 `components/` 目录
- 页面特定组件放在对应 `pages/` 目录

### Git 工作流
- 使用功能分支开发（feature/*）
- 提交信息遵循规范（feat、fix、docs 等）
- 代码审查后合并到主分支

### API 调用规范
- 所有 API 调用使用封装的请求函数
- 统一错误处理
- 统一加载状态管理
- 使用 TypeScript 类型定义 API 响应

---

## 🔧 开发工具推荐

- **IDE**: VS Code / WebStorm
- **版本控制**: Git
- **包管理**: npm / yarn / pnpm
- **构建工具**: Vite / Webpack
- **UI 组件库**: Ant Design
- **状态管理**: Redux Toolkit / Zustand
- **路由**: React Router
- **HTTP 客户端**: Axios
- **测试框架**: Jest + React Testing Library
- **代码质量**: ESLint, Prettier, TypeScript
- **API 测试**: Postman / Insomnia

---

## 📝 注意事项

1. **性能优化**：注意避免不必要的重渲染，合理使用 useMemo 和 useCallback
2. **状态管理**：避免过度使用全局状态，优先使用本地状态
3. **类型安全**：充分利用 TypeScript，避免使用 any
4. **错误处理**：所有异步操作都要有错误处理
5. **用户体验**：注意加载状态和错误提示
6. **响应式设计**：确保在不同设备上正常显示
7. **代码复用**：提取可复用的组件和逻辑
8. **测试覆盖**：关键功能要有测试覆盖

---

## 🎨 UI/UX 设计建议

1. **一致性**：保持设计风格一致
2. **反馈**：所有用户操作都要有反馈
3. **加载状态**：长时间操作要显示加载状态
4. **错误提示**：错误信息要清晰明确
5. **空状态**：空数据要有友好的提示
6. **响应式**：适配不同屏幕尺寸
7. **可访问性**：考虑无障碍访问

---

## 🌍 国际化（i18n）实现

### 📋 概述

项目已完整实现国际化功能，支持简体中文、繁体中文和英文三种语言，用户可以在运行时动态切换语言，所有界面文本、错误提示、验证信息等都会自动更新。

### 🛠️ 技术栈

- **react-i18next**: React 国际化集成库
- **i18next**: 核心国际化框架
- **i18next-browser-languagedetector**: 浏览器语言自动检测插件
- **Ant Design Locale**: Ant Design 组件库国际化支持

### 📁 目录结构

```
frontend/src/
├── i18n/
│   ├── index.ts              # i18n 配置文件
│   └── locales/              # 翻译文件目录
│       ├── zh-CN.json        # 简体中文翻译
│       ├── zh-TW.json        # 繁体中文翻译
│       └── en.json           # 英文翻译
└── components/
    └── Layout/
        └── LanguageSwitcher.tsx  # 语言切换组件
```

### 🎯 支持的语言

| 语言代码 | 语言名称 | 状态 |
|---------|---------|------|
| `zh-CN` | 简体中文 | ✅ 已实现 |
| `zh-TW` | 繁体中文 | ✅ 已实现 |
| `en` | English | ✅ 已实现 |

### 📝 翻译文件结构

翻译文件采用 JSON 格式，按功能模块组织：

```json
{
  "common": {
    "confirm": "确认",
    "cancel": "取消",
    ...
  },
  "auth": {
    "login": "登录",
    "logout": "退出登录",
    ...
  },
  "layout": {
    "dashboard": "仪表盘",
    "welcome": "欢迎使用企业级应用管理系统",
    ...
  },
  "error": {
    "403": "无权限访问",
    "404": "页面不存在",
    ...
  },
  "validation": {
    "required": "此字段为必填项",
    ...
  }
}
```

### ⚙️ 核心配置

#### i18n 初始化配置

- **语言检测**: 优先从 `localStorage` 读取，其次检测浏览器语言
- **Fallback 策略**: 每个语言只回退到自己，避免语言混淆
- **资源加载**: 使用静态导入，确保翻译资源在构建时包含
- **命名空间**: 使用 `translation` 作为默认命名空间

#### Ant Design 国际化

- 在 `App.tsx` 中使用 `ConfigProvider` 设置 Ant Design 语言包
- 语言切换时自动更新 Ant Design 组件语言
- 支持的语言包：
  - `zh_CN` - 简体中文
  - `zh_TW` - 繁体中文
  - `en_US` - 英文

### 🔧 实现功能

#### 1. 语言切换组件

- **位置**: 固定在屏幕右上角（`position: fixed`）
- **功能**: 
  - 显示当前语言
  - 下拉菜单选择语言
  - 切换后自动更新所有界面文本
  - 语言选择持久化到 `localStorage`

#### 2. API 请求语言头

- 所有 API 请求自动添加 `X-Language` 请求头
- 后端可以根据请求头返回对应语言的响应

#### 3. 组件中使用翻译

```typescript
import { useTranslation } from 'react-i18next'

const MyComponent = () => {
  const { t } = useTranslation()
  
  return (
    <div>
      <h1>{t('layout.welcome')}</h1>
      <button>{t('common.confirm')}</button>
    </div>
  )
}
```

#### 4. 语言代码规范

- 使用标准语言代码：`zh-CN`、`zh-TW`、`en`
- 兼容旧代码自动转换（`zh-hans` → `zh-CN`，`zh-hant` → `zh-TW`）

### 📦 已实现的翻译模块

- ✅ **通用模块** (common): 确认、取消、提交、搜索等
- ✅ **认证模块** (auth): 登录、注册、用户名、密码等
- ✅ **布局模块** (layout): 仪表盘、菜单项、欢迎信息等
- ✅ **错误模块** (error): 403、404、500 等错误提示
- ✅ **验证模块** (validation): 表单验证提示信息

### 🎨 UI 特性

- 语言切换组件固定在屏幕右上角，始终可见
- 登录页面和主页面统一使用相同的语言切换位置
- 语言切换后立即生效，无需刷新页面
- Ant Design 组件自动适配当前语言

### 🔄 语言切换流程

1. 用户点击语言切换组件
2. 选择目标语言
3. 更新 `i18n.language`
4. 更新 `localStorage` 中的语言设置
5. 重新加载翻译资源
6. 更新 Ant Design Locale
7. 触发组件重新渲染，显示新语言文本

### 📝 使用规范

1. **添加新翻译**: 在对应的语言 JSON 文件中添加键值对
2. **使用翻译**: 使用 `useTranslation` Hook 获取 `t` 函数
3. **命名规范**: 使用点分隔的命名空间，如 `auth.login`
4. **保持同步**: 确保所有语言文件包含相同的键

### 🚀 后续优化方向

- [ ] 实现翻译文件的懒加载（按需加载）
- [ ] 添加翻译缺失检测和警告
- [ ] 实现翻译文件的版本管理
- [ ] 支持更多语言（如日语、韩语等）
- [ ] 实现翻译文件的在线编辑功能

---

**版本**: v1.0.0  
**最后更新**: 2024-01-01

