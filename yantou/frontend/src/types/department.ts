/**
 * 部门相关类型定义
 */

/**
 * 部门信息
 */
export interface Department {
  id: number
  name: string
  code?: string
  parent?: number | null
  parent_name?: string
  level: number
  path?: string
  manager?: number | null
  manager_name?: string
  description?: string
  sort_order: number
  is_active: boolean
  children_count?: number
  created_at: string
  updated_at: string
}

/**
 * 部门列表项
 */
export interface DepartmentListItem extends Department {
  parent_name?: string
  manager_name?: string
  children_count?: number
}

/**
 * 部门树节点
 */
export interface DepartmentTreeNode extends Department {
  children?: DepartmentTreeNode[]
}

/**
 * 创建部门请求
 */
export interface CreateDepartmentRequest {
  name: string
  code?: string
  parent?: number | null
  manager?: number | null
  description?: string
  sort_order?: number
  is_active?: boolean
}

/**
 * 更新部门请求
 */
export interface UpdateDepartmentRequest {
  name?: string
  code?: string
  parent?: number | null
  manager?: number | null
  description?: string
  sort_order?: number
  is_active?: boolean
}

/**
 * 部门列表查询参数
 */
export interface DepartmentListParams {
  page?: number
  page_size?: number
  search?: string
  parent?: number
  level?: number
  is_active?: boolean
  ordering?: string
}

/**
 * 分页响应
 */
export interface PaginatedResponse<T> {
  results: T[]
  count: number
  page: number
  page_size: number
  pages: number
}

