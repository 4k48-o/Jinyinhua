import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios'
import { message } from 'antd'
import { getToken, removeToken } from '@/utils/storage'

// API 基础 URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

// 创建 Axios 实例
const request: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
request.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    // 自动添加 Token
    const token = getToken()
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }

    // 添加请求头（语言设置）
    if (config.headers) {
      const language = localStorage.getItem('language') || 'zh-CN'
      config.headers['X-Language'] = language
    }

    return config
  },
  (error: AxiosError) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response: AxiosResponse) => {
    const { data } = response

    // 统一响应格式处理
    // 后端返回格式: { success, code, message, data, request_id, timestamp }
    if (data && typeof data === 'object' && 'success' in data) {
      if (data.success) {
        // 成功响应，返回 data 字段
        return data.data !== undefined ? data.data : data
      } else {
        // 业务错误
        const errorMessage = data.message || '操作失败'
        // 不在这里显示错误消息，让调用方处理
        const error = new Error(errorMessage) as any
        error.code = data.code
        error.errors = data.errors
        error.request_id = data.request_id
        error.error_id = data.error_id
        return Promise.reject(error)
      }
    }

    // 如果不是统一格式，直接返回
    return data
  },
  (error: AxiosError) => {
    // 统一错误处理
    if (error.response) {
      const { status, data, config } = error.response
      const url = config?.url || ''
      
      // 检查是否是登录/注册接口（这些接口的 401 不应该自动跳转）
      const isAuthEndpoint = url.includes('/auth/login') || url.includes('/auth/register')

      switch (status) {
        case 401:
          // Token 过期或未认证
          if (isAuthEndpoint) {
            // 登录/注册接口的 401 错误，不在这里处理，让调用方处理
            // 从响应中提取错误消息
            const errorData = data as any
            const errorMessage = errorData?.message || '登录失败，请检查用户名和密码'
            const error = new Error(errorMessage) as any
            error.code = errorData?.code
            error.errors = errorData?.errors
            error.request_id = errorData?.request_id
            error.error_id = errorData?.error_id
            return Promise.reject(error)
          } else {
            // 其他接口的 401，表示 Token 过期
            removeToken()
            message.error('登录已过期，请重新登录')
            window.location.href = '/login'
          }
          break
        case 403:
          message.error('没有权限访问该资源')
          break
        case 404:
          message.error('请求的资源不存在')
          break
        case 500:
          message.error('服务器内部错误')
          break
        default:
          // 尝试从响应中获取错误消息
          const errorData = data as any
          const errorMessage = errorData?.message || errorData?.error || '请求失败'
          message.error(errorMessage)
      }
    } else if (error.request) {
      message.error('网络错误，请检查网络连接')
    } else {
      message.error('请求配置错误')
    }

    return Promise.reject(error)
  }
)

export default request

