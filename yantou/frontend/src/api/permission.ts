/**
 * 权限管理 API
 */
import { get } from '@/utils/request'
import type { Permission, PermissionTreeNode, PaginatedResponse } from '@/types/role'

/**
 * 权限列表查询参数
 */
export interface PermissionListParams {
  page?: number
  page_size?: number
  search?: string
  content_type?: string
  action?: string
  parent?: number
  ordering?: string
}

/**
 * 获取权限列表
 */
export const getPermissionList = (
  params?: PermissionListParams
): Promise<PaginatedResponse<Permission>> => {
  return get<PaginatedResponse<Permission>>('/permissions/', params)
}

/**
 * 获取权限详情
 */
export const getPermissionDetail = (id: number): Promise<Permission> => {
  return get<Permission>(`/permissions/${id}/`)
}

/**
 * 获取权限树
 */
export const getPermissionTree = (): Promise<PermissionTreeNode[]> => {
  return get<PermissionTreeNode[]>('/permissions/tree/')
}

