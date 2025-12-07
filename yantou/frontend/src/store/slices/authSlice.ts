import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit'
import { User, LoginRequest, LoginResponse, RegisterRequest } from '@/types'
import * as authAPI from '@/api/auth'
import { setToken, setRefreshToken, removeToken, removeRefreshToken, getToken, getRefreshToken } from '@/utils/storage'

// 认证状态接口
interface AuthState {
  user: User | null
  token: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  isLoading: boolean
  isInitialized: boolean // 是否已初始化（用于防止刷新时立即重定向）
  error: string | null
  permissions: string[]
  roles: string[]
}

// 从 localStorage 读取 token（用于初始化状态）
const initialToken = getToken()
const initialRefreshToken = getRefreshToken()

// 初始状态
const initialState: AuthState = {
  user: null,
  token: initialToken,
  refreshToken: initialRefreshToken,
  isAuthenticated: !!initialToken, // 如果有 token，先设置为已认证（等待验证）
  isLoading: false,
  isInitialized: false, // 初始化为 false，等待 useInitAuth 完成
  error: null,
  permissions: [],
  roles: [],
}

// 异步 Actions

/**
 * 登录
 */
export const login = createAsyncThunk(
  'auth/login',
  async (credentials: LoginRequest, { rejectWithValue }) => {
    try {
      const response = await authAPI.login(credentials)
      return response
    } catch (error: any) {
      return rejectWithValue(error.message || '登录失败')
    }
  }
)

/**
 * 注册
 */
export const register = createAsyncThunk(
  'auth/register',
  async (data: RegisterRequest, { rejectWithValue }) => {
    try {
      const response = await authAPI.register(data)
      return response
    } catch (error: any) {
      return rejectWithValue(error.message || '注册失败')
    }
  }
)

/**
 * 刷新 Token
 */
export const refreshToken = createAsyncThunk(
  'auth/refreshToken',
  async (_, { getState, rejectWithValue }) => {
    try {
      const state = getState() as { auth: AuthState }
      const refresh = state.auth.refreshToken
      if (!refresh) {
        throw new Error('没有刷新令牌')
      }
      const response = await authAPI.refreshToken(refresh)
      return response
    } catch (error: any) {
      return rejectWithValue(error.message || '刷新令牌失败')
    }
  }
)

/**
 * 获取当前用户信息
 */
export const getCurrentUser = createAsyncThunk(
  'auth/getCurrentUser',
  async (_, { rejectWithValue }) => {
    try {
      const response = await authAPI.getCurrentUser()
      return response
    } catch (error: any) {
      return rejectWithValue(error.message || '获取用户信息失败')
    }
  }
)

/**
 * 登出
 */
export const logout = createAsyncThunk('auth/logout', async (_, { rejectWithValue, getState }) => {
  try {
    const state = getState() as { auth: { refreshToken: string | null } }
    const refreshToken = state.auth.refreshToken
    
    // 如果有 refresh token，调用后端 API 将 token 加入黑名单
    if (refreshToken) {
      try {
        await authAPI.logout(refreshToken)
      } catch (error: any) {
        // 即使后端登出失败，也继续清除本地状态
        console.error('后端登出失败:', error)
      }
    }
  } catch (error: any) {
    // 即使登出失败，也要清除本地状态
    console.error('登出失败:', error)
  }
  return null
})

// Slice
const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    // 设置用户信息
    setUser: (state, action: PayloadAction<User | null>) => {
      state.user = action.payload
      state.isAuthenticated = !!action.payload
    },
    // 设置 Token
    setTokens: (state, action: PayloadAction<{ access: string; refresh: string }>) => {
      state.token = action.payload.access
      state.refreshToken = action.payload.refresh
      setToken(action.payload.access)
      setRefreshToken(action.payload.refresh)
    },
    // 清除认证信息
    clearAuth: (state) => {
      state.user = null
      state.token = null
      state.refreshToken = null
      state.isAuthenticated = false
      state.isInitialized = true // 清除时标记为已初始化
      state.permissions = []
      state.roles = []
      removeToken()
      removeRefreshToken()
    },
    // 设置权限
    setPermissions: (state, action: PayloadAction<string[]>) => {
      state.permissions = action.payload
    },
    // 设置角色
    setRoles: (state, action: PayloadAction<string[]>) => {
      state.roles = action.payload
    },
    // 清除错误
    clearError: (state) => {
      state.error = null
    },
    // 设置初始化状态
    setInitialized: (state, action: PayloadAction<boolean>) => {
      state.isInitialized = action.payload
    },
  },
  extraReducers: (builder) => {
    // 登录
    builder
      .addCase(login.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(login.fulfilled, (state, action) => {
        state.isLoading = false
        state.isInitialized = true
        const { access, refresh, user } = action.payload
        state.token = access
        state.refreshToken = refresh
        state.user = user
        state.isAuthenticated = true
        // 设置权限和角色（如果登录响应中包含）
        if (user?.permissions) {
          state.permissions = user.permissions
        }
        if (user?.roles) {
          state.roles = user.roles
        }
        setToken(access)
        setRefreshToken(refresh)
      })
      .addCase(login.rejected, (state, action) => {
        state.isLoading = false
        // 确保错误消息是字符串
        const errorMsg = action.payload
        state.error = typeof errorMsg === 'string' ? errorMsg : errorMsg?.message || '登录失败'
        state.isAuthenticated = false
      })

    // 注册
    builder
      .addCase(register.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(register.fulfilled, (state, action) => {
        state.isLoading = false
        state.isInitialized = true
        const { access, refresh, user } = action.payload
        state.token = access
        state.refreshToken = refresh
        state.user = user
        state.isAuthenticated = true
        setToken(access)
        setRefreshToken(refresh)
      })
      .addCase(register.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload as string
      })

    // 刷新 Token
    builder
      .addCase(refreshToken.fulfilled, (state, action) => {
        const { access, refresh } = action.payload
        state.token = access
        if (refresh) {
          state.refreshToken = refresh
          setRefreshToken(refresh)
        }
        setToken(access)
      })
      .addCase(refreshToken.rejected, (state) => {
        // Token 刷新失败，清除认证信息
        state.token = null
        state.refreshToken = null
        state.user = null
        state.isAuthenticated = false
        removeToken()
        removeRefreshToken()
      })

    // 获取当前用户
    builder
      .addCase(getCurrentUser.pending, (state) => {
        state.isLoading = true
      })
      .addCase(getCurrentUser.fulfilled, (state, action) => {
        state.isLoading = false
        state.isInitialized = true // 标记为已初始化
        state.user = action.payload
        state.isAuthenticated = true
        // 设置权限和角色
        if (action.payload.permissions) {
          state.permissions = action.payload.permissions
        }
        if (action.payload.roles) {
          state.roles = action.payload.roles
        }
      })
      .addCase(getCurrentUser.rejected, (state) => {
        state.isLoading = false
        state.isInitialized = true // 即使失败也标记为已初始化
        state.user = null
        state.isAuthenticated = false
        // 清除无效的 token
        state.token = null
        state.refreshToken = null
        removeToken()
        removeRefreshToken()
      })

    // 登出
    builder
      .addCase(logout.fulfilled, (state) => {
        state.user = null
        state.token = null
        state.refreshToken = null
        state.isAuthenticated = false
        state.permissions = []
        state.roles = []
        removeToken()
        removeRefreshToken()
      })
  },
})

export const { setUser, setTokens, clearAuth, setPermissions, setRoles, clearError, setInitialized } =
  authSlice.actions

export default authSlice.reducer

