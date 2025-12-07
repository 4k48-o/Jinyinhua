/**
 * 用户相关类型定义
 */

import type { UserProfile } from './index'

/**
 * 用户列表项
 */
export interface UserListItem {
  id: number
  username: string
  email: string
  phone?: string
  first_name?: string
  last_name?: string
  full_name?: string
  is_active: boolean
  is_staff: boolean
  is_superuser?: boolean
  last_login?: string
  date_joined: string
  profile?: UserProfile
}

/**
 * 用户详情
 */
export interface UserDetail extends UserListItem {
  permissions?: string[]
  roles?: string[]
}

/**
 * 创建用户请求
 */
export interface CreateUserRequest {
  username: string
  email: string
  password: string
  password_confirm: string
  phone?: string
  first_name?: string
  last_name?: string
  is_active?: boolean
  is_staff?: boolean
  profile?: {
    phone?: string
    gender?: number
    birthday?: string
    address?: string
    bio?: string
    department?: number
    position?: string
    employee_no?: string
    join_date?: string
  }
}

/**
 * 更新用户请求
 */
export interface UpdateUserRequest {
  email?: string
  phone?: string
  first_name?: string
  last_name?: string
  is_active?: boolean
  is_staff?: boolean
  profile?: {
    phone?: string
    gender?: number
    birthday?: string
    address?: string
    bio?: string
    department?: number
    position?: string
    employee_no?: string
    join_date?: string
  }
}

/**
 * 用户列表查询参数
 */
export interface UserListParams {
  page?: number
  page_size?: number
  search?: string
  is_active?: boolean
  is_staff?: boolean
  department?: number
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

