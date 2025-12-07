/**
 * 部门管理 API
 */
import { get, post, put, patch, del } from '@/utils/request'
import type {
  Department,
  DepartmentListItem,
  DepartmentTreeNode,
  CreateDepartmentRequest,
  UpdateDepartmentRequest,
  DepartmentListParams,
  PaginatedResponse,
} from '@/types/department'

/**
 * 获取部门列表
 */
export const getDepartmentList = (
  params?: DepartmentListParams
): Promise<PaginatedResponse<DepartmentListItem>> => {
  return get<PaginatedResponse<DepartmentListItem>>('/departments/', params)
}

/**
 * 获取部门详情
 */
export const getDepartmentDetail = (id: number): Promise<Department> => {
  return get<Department>(`/departments/${id}/`)
}

/**
 * 创建部门
 */
export const createDepartment = (data: CreateDepartmentRequest): Promise<Department> => {
  return post<Department>('/departments/', data)
}

/**
 * 更新部门（完整更新）
 */
export const updateDepartment = (id: number, data: UpdateDepartmentRequest): Promise<Department> => {
  return put<Department>(`/departments/${id}/`, data)
}

/**
 * 更新部门（部分更新）
 */
export const patchDepartment = (id: number, data: UpdateDepartmentRequest): Promise<Department> => {
  return patch<Department>(`/departments/${id}/`, data)
}

/**
 * 删除部门
 */
export const deleteDepartment = (id: number): Promise<void> => {
  return del<void>(`/departments/${id}/`)
}

/**
 * 获取部门树形结构
 */
export const getDepartmentTree = (): Promise<DepartmentTreeNode[]> => {
  return get<DepartmentTreeNode[]>('/departments/tree/')
}

