/**
 * TypeScript 类型定义
 */

/**
 * API 响应格式
 */
export interface APIResponse<T = any> {
  success: boolean
  code: number | string
  message: string
  data: T
  request_id?: string
  error_id?: string
  timestamp?: string
}

/**
 * 分页响应格式
 */
export interface PaginationResponse<T = any> {
  results: T[]
  count: number
  page: number
  page_size: number
  pages: number
}

/**
 * 用户信息
 */
export interface User {
  id: number
  username: string
  email: string
  first_name?: string
  last_name?: string
  is_active: boolean
  is_staff: boolean
  is_superuser?: boolean
  date_joined: string
  last_login?: string
  profile?: UserProfile
  permissions?: string[]
  roles?: string[]
}

/**
 * 用户资料
 */
export interface UserProfile {
  id: number
  user: number
  avatar?: string
  phone?: string
  gender?: 'M' | 'F' | 'O'
  birthday?: string
  address?: string
  bio?: string
  department?: number
  position?: string
  employee_no?: string
  join_date?: string
}

/**
 * 部门信息
 */
export interface Department {
  id: number
  name: string
  code: string
  description?: string
  parent?: number
  level: number
  sort_order: number
  is_active: boolean
  created_at: string
  updated_at: string
}

/**
 * 角色信息
 */
export interface Role {
  id: number
  name: string
  code: string
  description?: string
  is_system: boolean
  is_active: boolean
  created_at: string
  updated_at: string
}

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
  parent?: number
  sort_order: number
  is_active: boolean
}

/**
 * 登录请求
 */
export interface LoginRequest {
  username: string
  password: string
  captcha?: string
}

/**
 * 登录响应
 */
export interface LoginResponse {
  access: string
  refresh: string
  user: User
}

/**
 * 注册请求
 */
export interface RegisterRequest {
  username: string
  password: string
  password_confirm: string
  email?: string
}

/**
 * 注册路由常量（补充）
 */
export const REGISTER_ROUTE = '/register'

// 导出角色相关类型
export * from './role'
// 导出部门相关类型
export * from './department'
// 导出用户相关类型
export * from './user'

