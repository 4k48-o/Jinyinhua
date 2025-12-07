import { MenuProps } from 'antd'
import {
  DashboardOutlined,
  UserOutlined,
  TeamOutlined,
  SafetyOutlined,
  SettingOutlined,
} from '@ant-design/icons'
import type { MenuItemType } from 'antd/es/menu/hooks/useItems'

export interface MenuItem {
  key: string
  labelKey: string // 使用 i18n key 而不是直接 label
  icon?: React.ReactNode
  path: string
  children?: MenuItem[]
  permission?: string | string[]
  role?: string | string[]
}

/**
 * 菜单配置
 * 定义所有菜单项及其权限要求
 * 使用 labelKey 指向 i18n 翻译键
 */
export const menuConfig: MenuItem[] = [
  {
    key: '/dashboard',
    labelKey: 'layout.dashboard',
    icon: <DashboardOutlined />,
    path: '/dashboard',
  },
  {
    key: '/system',
    labelKey: 'layout.systemManagement',
    icon: <SettingOutlined />,
    path: '/system',
    // 临时移除权限检查，让所有用户都能看到菜单（用于测试）
    // 后续可以根据需要恢复权限检查
    // permission: ['permission:read', 'role:read', 'user:read', 'department:read'],
    children: [
      {
        key: '/system/permissions',
        labelKey: 'layout.permissionList',
        path: '/system/permissions',
        // 临时移除权限检查
        // permission: 'permission:read',
      },
      {
        key: '/system/roles',
        labelKey: 'layout.roleManagement',
        path: '/system/roles',
        // 临时移除权限检查
        // permission: 'role:read',
      },
      {
        key: '/system/users',
        labelKey: 'layout.userManagement',
        path: '/system/users',
        // 临时移除权限检查
        // permission: 'user:read',
      },
      {
        key: '/system/departments',
        labelKey: 'layout.departmentManagement',
        path: '/system/departments',
        // 临时移除权限检查
        // permission: 'department:read',
      },
    ],
  },
  {
    key: '/settings',
    labelKey: 'layout.systemSettings',
    icon: <SettingOutlined />,
    path: '/settings',
    role: 'admin',
  },
]

/**
 * 检查用户是否有权限访问菜单项
 */
const hasMenuPermission = (
  item: MenuItem,
  permissions: string[],
  roles: string[]
): boolean => {
  // 如果没有权限要求，则允许访问
  if (!item.permission && !item.role) {
    return true
  }

  // 检查权限
  if (item.permission) {
    const permissionList = Array.isArray(item.permission) ? item.permission : [item.permission]
    const hasPermission = permissionList.some((p) => permissions.includes(p))
    if (!hasPermission) {
      return false
    }
  }

  // 检查角色
  if (item.role) {
    const roleList = Array.isArray(item.role) ? item.role : [item.role]
    const hasRole = roleList.some((r) => roles.includes(r))
    if (!hasRole) {
      return false
    }
  }

  return true
}

/**
 * 将菜单配置转换为 Ant Design Menu 的 items 格式
 */
const convertToMenuItems = (
  items: MenuItem[],
  permissions: string[],
  roles: string[],
  t: (key: string) => string
): MenuItemType[] => {
  return items
    .filter((item) => hasMenuPermission(item, permissions, roles))
    .map((item) => {
      const menuItem: MenuItemType = {
        key: item.key,
        icon: item.icon,
        label: t(item.labelKey), // 使用 i18n 翻译
      }

      if (item.children && item.children.length > 0) {
        const filteredChildren = item.children.filter((child) =>
          hasMenuPermission(child, permissions, roles)
        )
        if (filteredChildren.length > 0) {
          menuItem.children = convertToMenuItems(filteredChildren, permissions, roles, t)
        }
      }

      return menuItem
    })
}

/**
 * 获取菜单项（根据权限过滤）
 */
export const getMenuItems = (
  permissions: string[] = [],
  roles: string[] = [],
  t: (key: string) => string
): MenuItemType[] => {
  return convertToMenuItems(menuConfig, permissions, roles, t)
}

/**
 * 根据路径获取面包屑项
 */
export const getBreadcrumbItems = (
  pathname: string,
  t: (key: string) => string
): Array<{ title: string; path: string }> => {
  const items: Array<{ title: string; path: string }> = []

  // 查找匹配的菜单项
  const findMenuItem = (items: MenuItem[], path: string): MenuItem | null => {
    for (const item of items) {
      if (item.path === path) {
        return item
      }
      if (item.children) {
        const found = findMenuItem(item.children, path)
        if (found) {
          return found
        }
      }
    }
    return null
  }

  // 从根路径开始查找
  const pathParts = pathname.split('/').filter(Boolean)
  let currentPath = ''

  for (const part of pathParts) {
    currentPath += `/${part}`
    const menuItem = findMenuItem(menuConfig, currentPath)
    if (menuItem) {
      items.push({
        title: t(menuItem.labelKey), // 使用 i18n 翻译
        path: menuItem.path,
      })
    }
  }

  return items
}

