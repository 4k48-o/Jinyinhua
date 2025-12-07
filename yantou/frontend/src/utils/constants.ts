/**
 * 常量定义
 */

// API 相关常量
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

// 应用信息
export const APP_TITLE = import.meta.env.VITE_APP_TITLE || '企业级应用管理系统'
export const APP_VERSION = import.meta.env.VITE_APP_VERSION || '1.0.0'

// 存储键名
export const STORAGE_KEYS = {
  TOKEN: 'access_token',
  REFRESH_TOKEN: 'refresh_token',
  USER_INFO: 'user_info',
  LANGUAGE: 'language',
  THEME: 'theme',
} as const

// 语言选项
export const LANGUAGES = [
  { label: '简体中文', value: 'zh-CN' },
  { label: 'English', value: 'en' },
  { label: '繁體中文', value: 'zh-TW' },
] as const

// 分页默认值
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 20,
  PAGE_SIZE_OPTIONS: ['10', '20', '50', '100'],
} as const

// 日期格式
export const DATE_FORMAT = {
  DATE: 'YYYY-MM-DD',
  DATETIME: 'YYYY-MM-DD HH:mm:ss',
  TIME: 'HH:mm:ss',
} as const

// HTTP 状态码
export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  INTERNAL_SERVER_ERROR: 500,
} as const

// 路由路径
export const ROUTES = {
  LOGIN: '/login',
  REGISTER: '/register',
  HOME: '/',
  DASHBOARD: '/dashboard',
  USERS: '/users',
  ROLES: '/roles',
  PERMISSIONS: '/permissions',
} as const

