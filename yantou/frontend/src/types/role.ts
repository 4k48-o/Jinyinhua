/**
 * 角色相关类型定义
 */

/**
 * 权限信息
 */
export interface Permission {
  id: number
  name: string
  code: string
  content_type?: string
  action?: string
  description?: string
  parent?: number | null
  parent_name?: string
  sort_order: number
  is_active: boolean
  is_system: boolean
  children_count?: number
  created_at: string
  updated_at: string
}

/**
 * 权限树节点
 */
export interface PermissionTreeNode extends Permission {
  children?: PermissionTreeNode[]
}

/**
 * 角色基本信息
 */
export interface Role {
  id: number
  name: string
  code: string
  description?: string
  sort_order: number
  is_active: boolean
  is_system: boolean
  created_at: string
  updated_at: string
  created_by?: number
  permissions?: Permission[]
  permission_count?: number
}

/**
 * 角色列表项
 */
export interface RoleListItem {
  id: number
  name: string
  code: string
  description?: string
  sort_order: number
  is_active: boolean
  is_system: boolean
  created_at: string
  updated_at: string
  permission_count?: number
}

/**
 * 创建角色请求
 */
export interface CreateRoleRequest {
  name: string
  code: string
  description?: string
  sort_order?: number
  is_active?: boolean
  permission_ids?: number[] // 权限 ID 列表（后端字段名）
}

/**
 * 更新角色请求
 */
export interface UpdateRoleRequest {
  name?: string
  code?: string
  description?: string
  sort_order?: number
  is_active?: boolean
  permission_ids?: number[] // 权限 ID 列表（后端字段名）
}

/**
 * 角色列表查询参数
 */
export interface RoleListParams {
  page?: number
  page_size?: number
  search?: string
  is_active?: boolean
  is_system?: boolean
  ordering?: string
}

/**
 * 分页响应
 */
export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

