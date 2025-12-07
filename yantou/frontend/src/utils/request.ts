/**
 * 请求工具函数
 * 提供便捷的 API 请求方法
 */
import request from '@/api/index'

/**
 * GET 请求
 */
export const get = <T = any>(url: string, params?: any): Promise<T> => {
  return request.get(url, { params })
}

/**
 * POST 请求
 */
export const post = <T = any>(url: string, data?: any): Promise<T> => {
  return request.post(url, data)
}

/**
 * PUT 请求
 */
export const put = <T = any>(url: string, data?: any): Promise<T> => {
  return request.put(url, data)
}

/**
 * PATCH 请求
 */
export const patch = <T = any>(url: string, data?: any): Promise<T> => {
  return request.patch(url, data)
}

/**
 * DELETE 请求
 */
export const del = <T = any>(url: string, params?: any): Promise<T> => {
  return request.delete(url, { params })
}

/**
 * 文件上传
 */
export const upload = <T = any>(
  url: string,
  file: File | Blob,
  onProgress?: (progress: number) => void
): Promise<T> => {
  const formData = new FormData()
  formData.append('file', file)

  return request.post(url, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    onUploadProgress: (progressEvent) => {
      if (onProgress && progressEvent.total) {
        const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        onProgress(progress)
      }
    },
  })
}

export default {
  get,
  post,
  put,
  patch,
  delete: del,
  upload,
}

