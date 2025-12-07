import dayjs from 'dayjs'
import 'dayjs/locale/zh-cn'

/**
 * 格式化工具函数
 */

// 配置 dayjs 中文
dayjs.locale('zh-cn')

/**
 * 日期格式化
 * @param date 日期（Date、字符串、时间戳）
 * @param format 格式（默认：YYYY-MM-DD HH:mm:ss）
 * @returns 格式化后的日期字符串
 */
export const formatDate = (
  date: Date | string | number | null | undefined,
  format: string = 'YYYY-MM-DD HH:mm:ss'
): string => {
  if (!date) return '-'
  return dayjs(date).format(format)
}

/**
 * 日期格式化（仅日期）
 */
export const formatDateOnly = (date: Date | string | number | null | undefined): string => {
  return formatDate(date, 'YYYY-MM-DD')
}

/**
 * 日期格式化（仅时间）
 */
export const formatTimeOnly = (date: Date | string | number | null | undefined): string => {
  return formatDate(date, 'HH:mm:ss')
}

/**
 * 相对时间格式化（如：2小时前）
 */
export const formatRelativeTime = (date: Date | string | number | null | undefined): string => {
  if (!date) return '-'
  return dayjs(date).fromNow()
}

/**
 * 数字格式化
 * @param num 数字
 * @param decimals 小数位数（默认：2）
 * @returns 格式化后的数字字符串
 */
export const formatNumber = (num: number | null | undefined, decimals: number = 2): string => {
  if (num === null || num === undefined) return '-'
  return num.toFixed(decimals)
}

/**
 * 千分位格式化
 */
export const formatNumberWithCommas = (num: number | null | undefined): string => {
  if (num === null || num === undefined) return '-'
  return num.toLocaleString('zh-CN')
}

/**
 * 文件大小格式化
 * @param bytes 字节数
 * @returns 格式化后的文件大小字符串
 */
export const formatFileSize = (bytes: number | null | undefined): string => {
  if (bytes === null || bytes === undefined || bytes === 0) return '0 B'

  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))

  return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`
}

/**
 * 百分比格式化
 */
export const formatPercent = (num: number | null | undefined, decimals: number = 2): string => {
  if (num === null || num === undefined) return '-'
  return `${(num * 100).toFixed(decimals)}%`
}

