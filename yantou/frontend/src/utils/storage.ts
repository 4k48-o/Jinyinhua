/**
 * 本地存储工具
 * 封装 localStorage 和 sessionStorage
 */

const TOKEN_KEY = 'access_token'
const REFRESH_TOKEN_KEY = 'refresh_token'

/**
 * localStorage 封装
 */
export const localStore = {
  get<T = any>(key: string): T | null {
    try {
      const item = localStorage.getItem(key)
      return item ? JSON.parse(item) : null
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error)
      return null
    }
  },

  set<T = any>(key: string, value: T): void {
    try {
      localStorage.setItem(key, JSON.stringify(value))
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error)
    }
  },

  remove(key: string): void {
    try {
      localStorage.removeItem(key)
    } catch (error) {
      console.error(`Error removing localStorage key "${key}":`, error)
    }
  },

  clear(): void {
    try {
      localStorage.clear()
    } catch (error) {
      console.error('Error clearing localStorage:', error)
    }
  },
}

/**
 * sessionStorage 封装
 */
export const sessionStore = {
  get<T = any>(key: string): T | null {
    try {
      const item = sessionStorage.getItem(key)
      return item ? JSON.parse(item) : null
    } catch (error) {
      console.error(`Error reading sessionStorage key "${key}":`, error)
      return null
    }
  },

  set<T = any>(key: string, value: T): void {
    try {
      sessionStorage.setItem(key, JSON.stringify(value))
    } catch (error) {
      console.error(`Error setting sessionStorage key "${key}":`, error)
    }
  },

  remove(key: string): void {
    try {
      sessionStorage.removeItem(key)
    } catch (error) {
      console.error(`Error removing sessionStorage key "${key}":`, error)
    }
  },

  clear(): void {
    try {
      sessionStorage.clear()
    } catch (error) {
      console.error('Error clearing sessionStorage:', error)
    }
  },
}

/**
 * Token 存储和获取
 */
export const tokenStore = {
  getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY)
  },

  setToken(token: string): void {
    localStorage.setItem(TOKEN_KEY, token)
  },

  removeToken(): void {
    localStorage.removeItem(TOKEN_KEY)
  },

  getRefreshToken(): string | null {
    return localStorage.getItem(REFRESH_TOKEN_KEY)
  },

  setRefreshToken(token: string): void {
    localStorage.setItem(REFRESH_TOKEN_KEY, token)
  },

  removeRefreshToken(): void {
    localStorage.removeItem(REFRESH_TOKEN_KEY)
  },

  clear(): void {
    this.removeToken()
    this.removeRefreshToken()
  },
}

// 导出便捷函数
export const getToken = tokenStore.getToken.bind(tokenStore)
export const setToken = tokenStore.setToken.bind(tokenStore)
export const removeToken = tokenStore.removeToken.bind(tokenStore)
export const getRefreshToken = tokenStore.getRefreshToken.bind(tokenStore)
export const setRefreshToken = tokenStore.setRefreshToken.bind(tokenStore)
export const removeRefreshToken = tokenStore.removeRefreshToken.bind(tokenStore)

// 通用存储函数（用于语言等设置）
export const getItem = (key: string): string | null => {
  try {
    return localStorage.getItem(key)
  } catch (error) {
    console.error(`Error reading localStorage key "${key}":`, error)
    return null
  }
}

export const setItem = (key: string, value: string): void => {
  try {
    localStorage.setItem(key, value)
  } catch (error) {
    console.error(`Error setting localStorage key "${key}":`, error)
  }
}

export const removeItem = (key: string): void => {
  try {
    localStorage.removeItem(key)
  } catch (error) {
    console.error(`Error removing localStorage key "${key}":`, error)
  }
}

