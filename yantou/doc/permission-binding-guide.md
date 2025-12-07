# 权限绑定机制说明文档

## 概述

本系统采用基于角色的访问控制（RBAC - Role-Based Access Control）机制，通过**用户 -> 角色 -> 权限**的三层关系来实现权限管理。

## 权限体系结构

### 1. 后端权限模型

```
用户 (User)
  └─ 用户角色 (UserRole) - 多对多关系
      └─ 角色 (Role)
          └─ 角色权限 (RolePermission) - 多对多关系
              └─ 权限 (Permission)
```

### 2. 权限代码格式

权限代码采用 `资源类型:操作类型` 的格式：

- **资源类型**：如 `user`、`role`、`permission`、`department`
- **操作类型**：如 `create`、`read`、`update`、`delete`、`import`、`export`

示例：
- `user:create` - 用户创建权限
- `user:read` - 用户查询权限
- `role:update` - 角色更新权限
- `permission:delete` - 权限删除权限

### 3. 默认权限列表

系统初始化时会创建以下权限组：

#### 用户管理权限组 (`user:manage`)
- `user:create` - 用户创建
- `user:read` - 用户查询
- `user:update` - 用户更新
- `user:delete` - 用户删除
- `user:import` - 用户导入
- `user:export` - 用户导出

#### 角色管理权限组 (`role:manage`)
- `role:create` - 角色创建
- `role:read` - 角色查询
- `role:update` - 角色更新
- `role:delete` - 角色删除

#### 权限管理权限组 (`permission:manage`)
- `permission:create` - 权限创建
- `permission:read` - 权限查询
- `permission:update` - 权限更新
- `permission:delete` - 权限删除

#### 部门管理权限组 (`department:manage`)
- `department:create` - 部门创建
- `department:read` - 部门查询
- `department:update` - 部门更新
- `department:delete` - 部门删除

## 前端权限绑定

### 1. 权限数据获取

用户登录后，后端 `/api/v1/users/me/` 接口会返回用户的权限和角色信息：

```json
{
  "id": 1,
  "username": "admin",
  "permissions": ["user:create", "user:read", "role:update", ...],
  "roles": ["admin", "super_admin"],
  "is_superuser": true
}
```

这些数据会被存储在 Redux 的 `authSlice` 中。

### 2. 权限检查 Hook

使用 `useAuth` hook 来检查权限：

```typescript
import { useAuth } from '@/hooks/useAuth'

const MyComponent = () => {
  const { hasPermission, hasRole, hasAnyPermission } = useAuth()
  
  // 检查单个权限
  const canCreate = hasPermission('user:create')
  
  // 检查单个角色
  const isAdmin = hasRole('admin')
  
  // 检查任一权限
  const canManage = hasAnyPermission(['user:create', 'user:update'])
  
  return (
    <Button disabled={!canCreate}>创建用户</Button>
  )
}
```

### 3. 菜单权限绑定

在 `frontend/src/router/menus.tsx` 中配置菜单权限：

```typescript
export const menuConfig: MenuItem[] = [
  {
    key: '/system/users',
    labelKey: 'layout.userManagement',
    path: '/system/users',
    permission: 'user:read',  // 需要 user:read 权限才能看到此菜单
  },
  {
    key: '/system/roles',
    labelKey: 'layout.roleManagement',
    path: '/system/roles',
    permission: 'role:read',  // 需要 role:read 权限才能看到此菜单
  },
  {
    key: '/settings',
    labelKey: 'layout.systemSettings',
    path: '/settings',
    role: 'admin',  // 需要 admin 角色才能看到此菜单
  },
]
```

菜单会根据用户权限自动过滤显示。

### 4. 按钮权限绑定

#### 方式一：使用 useAuth Hook（推荐）

```typescript
import { useAuth } from '@/hooks/useAuth'
import { Button } from 'antd'

const UserManagement = () => {
  const { hasPermission } = useAuth()
  
  const canCreate = hasPermission('user:create')
  const canUpdate = hasPermission('user:update')
  const canDelete = hasPermission('user:delete')
  
  return (
    <>
      <Button 
        type="primary" 
        disabled={!canCreate}
        onClick={handleCreate}
      >
        创建用户
      </Button>
      <Button 
        disabled={!canUpdate}
        onClick={handleUpdate}
      >
        编辑
      </Button>
      <Button 
        danger 
        disabled={!canDelete}
        onClick={handleDelete}
      >
        删除
      </Button>
    </>
  )
}
```

#### 方式二：使用 PermissionButton 组件（简化版）

```typescript
import { PermissionButton } from '@/components/Permission/PermissionButton'

const UserManagement = () => {
  return (
    <>
      <PermissionButton 
        permission="user:create"
        type="primary"
        onClick={handleCreate}
      >
        创建用户
      </PermissionButton>
      
      <PermissionButton 
        permission="user:update"
        onClick={handleUpdate}
      >
        编辑
      </PermissionButton>
      
      <PermissionButton 
        permission="user:delete"
        danger
        onClick={handleDelete}
      >
        删除
      </PermissionButton>
    </>
  )
}
```

### 5. 路由权限绑定

使用 `PrivateRoute` 组件保护路由：

```typescript
import { PrivateRoute } from '@/router/PrivateRoute'

const router = createBrowserRouter([
  {
    path: '/system/users',
    element: (
      <PrivateRoute requirePermission="user:read">
        <UserManagement />
      </PrivateRoute>
    ),
  },
  {
    path: '/system/roles',
    element: (
      <PrivateRoute requirePermission="role:read">
        <RoleManagement />
      </PrivateRoute>
    ),
  },
  {
    path: '/admin',
    element: (
      <PrivateRoute requireRole="admin">
        <AdminPanel />
      </PrivateRoute>
    ),
  },
])
```

## 权限绑定最佳实践

### 1. 菜单权限

- **父菜单**：如果父菜单有子菜单，建议使用 `hasAnyPermission` 逻辑（任一子菜单权限即可显示父菜单）
- **子菜单**：使用具体的权限代码，如 `user:read`、`role:read`

### 2. 按钮权限

- **创建按钮**：使用 `资源:create` 权限，如 `user:create`
- **编辑按钮**：使用 `资源:update` 权限，如 `user:update`
- **删除按钮**：使用 `资源:delete` 权限，如 `user:delete`
- **查询按钮**：使用 `资源:read` 权限，如 `user:read`

### 3. 表格操作列

```typescript
{
  title: '操作',
  key: 'actions',
  render: (_: any, record: any) => {
    const { hasPermission } = useAuth()
    const canEdit = hasPermission('user:update')
    const canDelete = hasPermission('user:delete')
    
    return (
      <Space>
        <Button 
          disabled={!canEdit}
          onClick={() => handleEdit(record)}
        >
          编辑
        </Button>
        <Button 
          danger 
          disabled={!canDelete}
          onClick={() => handleDelete(record)}
        >
          删除
        </Button>
      </Space>
    )
  },
}
```

### 4. 系统角色特殊处理

系统角色（`is_system: true`）通常需要特殊处理：

```typescript
const { hasPermission, user } = useAuth()

// 系统角色只有超级管理员可以编辑
const canEditSystemRole = record.is_system && user?.is_superuser
// 非系统角色，有权限就可以编辑
const canEditNonSystemRole = !record.is_system && hasPermission('role:update')
// 是否可以编辑
const editable = canEditSystemRole || canEditNonSystemRole
```

## 权限检查流程

1. **用户登录** → 后端验证用户名密码
2. **获取用户信息** → 调用 `/api/v1/users/me/` 获取用户权限和角色
3. **存储到 Redux** → 权限和角色存储在 `authSlice` 中
4. **组件使用** → 组件通过 `useAuth` hook 检查权限
5. **UI 更新** → 根据权限显示/隐藏菜单、启用/禁用按钮

## 权限代码规范

### 命名规范

- 使用小写字母
- 使用冒号分隔资源类型和操作类型
- 资源类型使用单数形式（如 `user` 而不是 `users`）
- 操作类型使用动词（如 `create`、`read`、`update`、`delete`）

### 常见操作类型

- `create` - 创建
- `read` - 查询/查看
- `update` - 更新/编辑
- `delete` - 删除
- `import` - 导入
- `export` - 导出
- `manage` - 管理（父权限，包含所有子权限）

## 示例：完整的权限绑定

```typescript
// 1. 菜单配置 (menus.tsx)
{
  key: '/system/users',
  labelKey: 'layout.userManagement',
  path: '/system/users',
  permission: 'user:read',  // 需要查询权限才能看到菜单
}

// 2. 路由保护 (router/index.tsx)
{
  path: '/system/users',
  element: (
    <PrivateRoute requirePermission="user:read">
      <UserManagement />
    </PrivateRoute>
  ),
}

// 3. 页面组件 (pages/Users/index.tsx)
const UserManagement = () => {
  const { hasPermission } = useAuth()
  
  const canCreate = hasPermission('user:create')
  const canUpdate = hasPermission('user:update')
  const canDelete = hasPermission('user:delete')
  
  return (
    <PageContainer>
      <Space>
        <Button 
          type="primary" 
          disabled={!canCreate}
          onClick={handleCreate}
        >
          创建用户
        </Button>
      </Space>
      
      <Table
        columns={[
          // ... 其他列
          {
            title: '操作',
            render: (_, record) => (
              <Space>
                <Button 
                  disabled={!canUpdate}
                  onClick={() => handleEdit(record)}
                >
                  编辑
                </Button>
                <Button 
                  danger 
                  disabled={!canDelete}
                  onClick={() => handleDelete(record)}
                >
                  删除
                </Button>
              </Space>
            ),
          },
        ]}
      />
    </PageContainer>
  )
}
```

## 总结

权限绑定遵循以下原则：

1. **后端定义权限**：在 `init_permissions` 命令中定义所有权限
2. **角色绑定权限**：在角色管理中为角色分配权限
3. **用户分配角色**：为用户分配角色（一个用户可以有多个角色）
4. **前端检查权限**：前端通过 `useAuth` hook 检查权限并控制 UI 显示

通过这种方式，实现了灵活的权限管理，可以精确控制用户对各个功能的访问权限。

