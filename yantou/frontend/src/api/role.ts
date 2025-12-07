/**
 * 角色管理 API
 */
import { get, post, put, patch, del } from '@/utils/request'
import type {
  Role,
  RoleListItem,
  CreateRoleRequest,
  UpdateRoleRequest,
  RoleListParams,
  PaginatedResponse,
  Permission,
  PermissionTreeNode,
} from '@/types/role'
import { getPermissionTree } from '@/api/permission'

/**
 * 获取角色列表
 */
export const getRoleList = (
  params?: RoleListParams
): Promise<PaginatedResponse<RoleListItem>> => {
  return get<PaginatedResponse<RoleListItem>>('/roles/', params)
}

/**
 * 获取角色详情
 */
export const getRoleDetail = (id: number): Promise<Role> => {
  return get<Role>(`/roles/${id}/`)
}

/**
 * 创建角色
 */
export const createRole = (data: CreateRoleRequest): Promise<Role> => {
  return post<Role>('/roles/', data)
}

/**
 * 更新角色（完整更新）
 */
export const updateRole = (id: number, data: UpdateRoleRequest): Promise<Role> => {
  return put<Role>(`/roles/${id}/`, data)
}

/**
 * 更新角色（部分更新）
 */
export const patchRole = (id: number, data: UpdateRoleRequest): Promise<Role> => {
  return patch<Role>(`/roles/${id}/`, data)
}

/**
 * 删除角色
 */
export const deleteRole = (id: number): Promise<void> => {
  return del<void>(`/roles/${id}/`)
}

/**
 * 获取角色权限列表
 */
export const getRolePermissions = (id: number): Promise<Permission[]> => {
  return get<Permission[]>(`/roles/${id}/permissions/`)
}

/**
 * 批量添加权限到角色
 */
export const addRolePermissions = (id: number, permissionIds: number[]): Promise<{ added_count: number }> => {
  return post<{ added_count: number }>(`/roles/${id}/permissions/add/`, { permission_ids: permissionIds })
}

/**
 * 批量移除角色权限
 */
export const removeRolePermissions = (id: number, permissionIds: number[]): Promise<{ removed_count: number }> => {
  return post<{ removed_count: number }>(`/roles/${id}/permissions/remove/`, { permission_ids: permissionIds })
}

/**
 * 替换角色权限
 */
export const replaceRolePermissions = (id: number, permissionIds: number[]): Promise<{ old_count: number; new_count: number }> => {
  return post<{ old_count: number; new_count: number }>(`/roles/${id}/permissions/replace/`, { permission_ids: permissionIds })
}

/**
 * 获取权限树（从权限API导入）
 */
export { getPermissionTree } from '@/api/permission'

