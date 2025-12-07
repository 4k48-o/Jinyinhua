import { useEffect } from 'react'
import { useAppDispatch } from '@/store/hooks'
import { getCurrentUser, setTokens, setInitialized } from '@/store/slices/authSlice'
import { getToken, getRefreshToken } from '@/utils/storage'

/**
 * 初始化认证状态 Hook
 * 在应用启动时检查 Token 并恢复登录状态
 */
export const useInitAuth = () => {
  const dispatch = useAppDispatch()

  useEffect(() => {
    const initAuth = async () => {
      const token = getToken()
      const refreshToken = getRefreshToken()

      // 如果有 Token，尝试恢复登录状态
      if (token && refreshToken) {
        try {
          // 设置 Token 到 Redux（如果还没有设置）
          dispatch(setTokens({ access: token, refresh: refreshToken }))

          // 获取当前用户信息
          await dispatch(getCurrentUser()).unwrap()
        } catch (error) {
          // 如果获取用户信息失败，清除 Token
          // 这个逻辑在 authSlice 的 getCurrentUser.rejected 中已经处理
          console.error('初始化认证失败:', error)
        }
      } else {
        // 如果没有 token，标记为已初始化，避免 PrivateRoute 无限等待
        dispatch(setInitialized(true))
      }
    }

    initAuth()
  }, [dispatch])
}

