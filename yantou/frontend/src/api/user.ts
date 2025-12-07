/**
 * 用户管理 API
 */
import { get, post, put, patch, del } from '@/utils/request'
import request from '@/api/index'
import type {
  UserListItem,
  UserDetail,
  CreateUserRequest,
  UpdateUserRequest,
  UserListParams,
  PaginatedResponse,
} from '@/types/user'

/**
 * 获取用户列表
 */
export const getUserList = (
  params?: UserListParams
): Promise<PaginatedResponse<UserListItem>> => {
  return get<PaginatedResponse<UserListItem>>('/users/', params)
}

/**
 * 获取用户详情
 */
export const getUserDetail = (id: number): Promise<UserDetail> => {
  return get<UserDetail>(`/users/${id}/`)
}

/**
 * 创建用户
 */
export const createUser = (data: CreateUserRequest): Promise<UserDetail> => {
  return post<UserDetail>('/users/', data)
}

/**
 * 更新用户（完整更新）
 */
export const updateUser = (id: number, data: UpdateUserRequest): Promise<UserDetail> => {
  return put<UserDetail>(`/users/${id}/`, data)
}

/**
 * 更新用户（部分更新）
 */
export const patchUser = (id: number, data: UpdateUserRequest): Promise<UserDetail> => {
  return patch<UserDetail>(`/users/${id}/`, data)
}

/**
 * 删除用户
 */
export const deleteUser = (id: number): Promise<void> => {
  return del<void>(`/users/${id}/`)
}

/**
 * 激活/禁用用户
 */
export const toggleUserActive = (id: number): Promise<{ is_active: boolean }> => {
  return post<{ is_active: boolean }>(`/users/${id}/toggle_active/`)
}

/**
 * 上传用户头像
 */
export const uploadUserAvatar = (file: File): Promise<{ avatar: string }> => {
  const formData = new FormData()
  formData.append('avatar', file)
  // 使用 request 直接调用，因为需要设置 Content-Type
  return request.post('/users/upload_avatar/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}

