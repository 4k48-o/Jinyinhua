import { ReactNode } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { Spin } from 'antd'
import { useAppSelector } from '@/store/hooks'
import { useAuth } from '@/hooks/useAuth'
import { ROUTES } from '@/utils/constants'

interface PrivateRouteProps {
  children: ReactNode
  requireAuth?: boolean
  requirePermission?: string | string[]
  requireRole?: string | string[]
  requireAllPermissions?: boolean
  requireAllRoles?: boolean
}

/**
 * 私有路由组件
 * 用于保护需要认证或特定权限的页面
 */
const PrivateRoute = ({
  children,
  requireAuth = true,
  requirePermission,
  requireRole,
  requireAllPermissions = false,
  requireAllRoles = false,
}: PrivateRouteProps) => {
  const { isAuthenticated, hasPermission, hasRole, hasAnyPermission, hasAnyRole, hasAllPermissions, hasAllRoles } =
    useAuth()
  const { isLoading, isInitialized, token } = useAppSelector((state) => state.auth)
  const location = useLocation()

  // 如果正在初始化认证状态，显示加载中
  // 只有在有 token 但还未初始化完成时才显示加载
  if (requireAuth && token && !isInitialized) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <Spin size="large" tip="正在验证登录状态..." />
      </div>
    )
  }

  // 如果没有 token 且未初始化，也显示加载（等待 useInitAuth 完成）
  if (requireAuth && !token && !isInitialized) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <Spin size="large" tip="正在检查登录状态..." />
      </div>
    )
  }

  // 需要认证但未登录（只有在初始化完成后才检查）
  if (requireAuth && isInitialized && !isAuthenticated) {
    return <Navigate to={ROUTES.LOGIN} state={{ from: location }} replace />
  }

  // 权限检查
  if (requirePermission) {
    const permissionList = Array.isArray(requirePermission) ? requirePermission : [requirePermission]
    const hasAccess = requireAllPermissions
      ? hasAllPermissions(permissionList)
      : hasAnyPermission(permissionList)

    if (!hasAccess) {
      return <Navigate to="/403" replace />
    }
  }

  // 角色检查
  if (requireRole) {
    const roleList = Array.isArray(requireRole) ? requireRole : [requireRole]
    const hasAccess = requireAllRoles ? hasAllRoles(roleList) : hasAnyRole(roleList)

    if (!hasAccess) {
      return <Navigate to="/403" replace />
    }
  }

  return <>{children}</>
}

export default PrivateRoute

