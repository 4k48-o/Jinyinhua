import { useCallback } from 'react'
import { useAppSelector, useAppDispatch } from '@/store/hooks'
import { clearAuth, setPermissions, setRoles } from '@/store/slices/authSlice'

/**
 * 认证 Hook
 * 提供认证相关的状态和方法
 */
export const useAuth = () => {
  const dispatch = useAppDispatch()
  const { user, token, isAuthenticated, isLoading, isInitialized, error, permissions, roles } = useAppSelector(
    (state) => state.auth
  )

  /**
   * 检查是否有指定权限
   */
  const hasPermission = useCallback(
    (permission: string): boolean => {
      if (!isAuthenticated || !permissions.length) return false
      return permissions.includes(permission)
    },
    [isAuthenticated, permissions]
  )

  /**
   * 检查是否有指定角色
   */
  const hasRole = useCallback(
    (role: string): boolean => {
      if (!isAuthenticated || !roles.length) return false
      return roles.includes(role)
    },
    [isAuthenticated, roles]
  )

  /**
   * 检查是否有任一权限
   */
  const hasAnyPermission = useCallback(
    (permissionList: string[]): boolean => {
      if (!isAuthenticated || !permissions.length) return false
      return permissionList.some((permission) => permissions.includes(permission))
    },
    [isAuthenticated, permissions]
  )

  /**
   * 检查是否有任一角色
   */
  const hasAnyRole = useCallback(
    (roleList: string[]): boolean => {
      if (!isAuthenticated || !roles.length) return false
      return roleList.some((role) => roles.includes(role))
    },
    [isAuthenticated, roles]
  )

  /**
   * 检查是否有所有权限
   */
  const hasAllPermissions = useCallback(
    (permissionList: string[]): boolean => {
      if (!isAuthenticated || !permissions.length) return false
      return permissionList.every((permission) => permissions.includes(permission))
    },
    [isAuthenticated, permissions]
  )

  /**
   * 检查是否有所有角色
   */
  const hasAllRoles = useCallback(
    (roleList: string[]): boolean => {
      if (!isAuthenticated || !roles.length) return false
      return roleList.every((role) => roles.includes(role))
    },
    [isAuthenticated, roles]
  )

  /**
   * 设置权限列表
   */
  const updatePermissions = useCallback(
    (permissionList: string[]) => {
      dispatch(setPermissions(permissionList))
    },
    [dispatch]
  )

  /**
   * 设置角色列表
   */
  const updateRoles = useCallback(
    (roleList: string[]) => {
      dispatch(setRoles(roleList))
    },
    [dispatch]
  )

  /**
   * 清除认证信息
   */
  const clearAuthData = useCallback(() => {
    dispatch(clearAuth())
  }, [dispatch])

  return {
    // 状态
    user,
    token,
    isAuthenticated,
    isLoading,
    isInitialized,
    error,
    permissions,
    roles,
    // 方法
    hasPermission,
    hasRole,
    hasAnyPermission,
    hasAnyRole,
    hasAllPermissions,
    hasAllRoles,
    updatePermissions,
    updateRoles,
    clearAuthData,
  }
}

