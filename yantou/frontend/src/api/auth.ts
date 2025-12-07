/**
 * 认证相关 API
 */
import { post, get } from '@/utils/request'
import { LoginRequest, LoginResponse, RegisterRequest, User } from '@/types'

/**
 * 用户登录
 */
export const login = (data: LoginRequest): Promise<LoginResponse> => {
  return post<LoginResponse>('/auth/login/', data)
}

/**
 * 用户注册
 */
export const register = (data: RegisterRequest): Promise<LoginResponse> => {
  return post<LoginResponse>('/auth/register/', data)
}

/**
 * 刷新 Token
 */
export const refreshToken = (refresh: string): Promise<{ access: string; refresh?: string }> => {
  return post<{ access: string; refresh?: string }>('/auth/refresh/', { refresh })
}

/**
 * 用户登出
 */
export const logout = (refreshToken: string): Promise<void> => {
  return post<void>('/auth/logout/', { refresh: refreshToken })
}

/**
 * 获取当前用户信息
 */
export const getCurrentUser = (): Promise<User> => {
  return get<User>('/users/me/')
}

/**
 * 获取验证码
 */
export const getCaptcha = (): Promise<{ image: string; key: string }> => {
  return get<{ image: string; key: string }>('/auth/captcha/')
}

