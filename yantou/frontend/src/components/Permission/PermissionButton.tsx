/**
 * 权限控制按钮组件
 * 根据用户权限自动显示/隐藏或启用/禁用按钮
 */
import { Button, ButtonProps } from 'antd'
import { useAuth } from '@/hooks/useAuth'

interface PermissionButtonProps extends ButtonProps {
  /**
   * 需要的权限代码（单个）
   * 如果用户没有此权限，按钮将被禁用或隐藏
   */
  permission?: string
  /**
   * 需要的权限代码列表（任一）
   * 如果用户没有任一权限，按钮将被禁用或隐藏
   */
  permissions?: string[]
  /**
   * 需要的角色代码（单个）
   * 如果用户没有此角色，按钮将被禁用或隐藏
   */
  role?: string
  /**
   * 需要的角色代码列表（任一）
   * 如果用户没有任一角色，按钮将被禁用或隐藏
   */
  roles?: string[]
  /**
   * 当没有权限时的行为
   * - 'hide': 隐藏按钮（默认）
   * - 'disable': 禁用按钮
   */
  noPermissionMode?: 'hide' | 'disable'
  /**
   * 是否需要所有权限（仅当 permissions 为数组时有效）
   * - false: 任一权限即可（默认）
   * - true: 需要所有权限
   */
  requireAll?: boolean
}

/**
 * 权限控制按钮
 * 
 * @example
 * // 单个权限
 * <PermissionButton permission="user:create" onClick={handleCreate}>
 *   创建用户
 * </PermissionButton>
 * 
 * // 多个权限（任一）
 * <PermissionButton permissions={['user:create', 'user:update']} onClick={handleAction}>
 *   操作
 * </PermissionButton>
 * 
 * // 多个权限（全部）
 * <PermissionButton permissions={['user:create', 'user:update']} requireAll onClick={handleAction}>
 *   操作
 * </PermissionButton>
 * 
 * // 角色检查
 * <PermissionButton role="admin" onClick={handleAdminAction}>
 *   管理员操作
 * </PermissionButton>
 * 
 * // 没有权限时禁用而不是隐藏
 * <PermissionButton 
 *   permission="user:delete" 
 *   noPermissionMode="disable"
 *   onClick={handleDelete}
 * >
 *   删除
 * </PermissionButton>
 */
export const PermissionButton = ({
  permission,
  permissions,
  role,
  roles,
  noPermissionMode = 'hide',
  requireAll = false,
  ...buttonProps
}: PermissionButtonProps) => {
  const { hasPermission, hasRole, hasAnyPermission, hasAnyRole, hasAllPermissions, hasAllRoles } = useAuth()

  // 检查权限
  let hasAccess = true

  // 检查单个权限
  if (permission) {
    hasAccess = hasPermission(permission)
  }

  // 检查多个权限
  if (permissions && permissions.length > 0) {
    hasAccess = requireAll
      ? hasAllPermissions(permissions)
      : hasAnyPermission(permissions)
  }

  // 检查单个角色
  if (role) {
    hasAccess = hasAccess && hasRole(role)
  }

  // 检查多个角色
  if (roles && roles.length > 0) {
    hasAccess = hasAccess && hasAnyRole(roles)
  }

  // 如果没有权限且模式为隐藏，返回 null
  if (!hasAccess && noPermissionMode === 'hide') {
    return null
  }

  // 如果没有权限且模式为禁用，返回禁用的按钮
  return (
    <Button
      {...buttonProps}
      disabled={!hasAccess || buttonProps.disabled}
    />
  )
}

export default PermissionButton

