/**
 * 角色状态管理
 */
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit'
import type {
  Role,
  RoleListItem,
  CreateRoleRequest,
  UpdateRoleRequest,
  RoleListParams,
  PermissionTreeNode,
} from '@/types/role'
import * as roleAPI from '@/api/role'
import { getPermissionTree as fetchPermissionTreeAPI } from '@/api/permission'
import { message } from 'antd'

// 角色状态接口
interface RoleState {
  // 角色列表
  roles: RoleListItem[]
  total: number
  loading: boolean
  
  // 当前角色详情
  currentRole: Role | null
  roleLoading: boolean
  
  // 权限树
  permissionTree: PermissionTreeNode[]
  permissionTreeLoading: boolean
  
  // 查询参数
  listParams: RoleListParams
  
  // 错误信息
  error: string | null
}

// 初始状态
const initialState: RoleState = {
  roles: [],
  total: 0,
  loading: false,
  currentRole: null,
  roleLoading: false,
  permissionTree: [],
  permissionTreeLoading: false,
  listParams: {
    page: 1,
    page_size: 10,
  },
  error: null,
}

// 异步 Actions

/**
 * 获取角色列表
 */
export const fetchRoles = createAsyncThunk(
  'role/fetchRoles',
  async (params: RoleListParams | undefined, { rejectWithValue }) => {
    try {
      const response = await roleAPI.getRoleList(params)
      return response
    } catch (error: any) {
      return rejectWithValue(error.message || '获取角色列表失败')
    }
  }
)

/**
 * 获取角色详情
 */
export const fetchRoleDetail = createAsyncThunk(
  'role/fetchRoleDetail',
  async (id: number, { rejectWithValue }) => {
    try {
      const response = await roleAPI.getRoleDetail(id)
      return response
    } catch (error: any) {
      return rejectWithValue(error.message || '获取角色详情失败')
    }
  }
)

/**
 * 创建角色
 */
export const createRole = createAsyncThunk(
  'role/createRole',
  async (data: CreateRoleRequest, { rejectWithValue }) => {
    try {
      const response = await roleAPI.createRole(data)
      message.success('角色创建成功')
      return response
    } catch (error: any) {
      message.error(error.message || '创建角色失败')
      return rejectWithValue(error.message || '创建角色失败')
    }
  }
)

/**
 * 更新角色
 */
export const updateRole = createAsyncThunk(
  'role/updateRole',
  async ({ id, data }: { id: number; data: UpdateRoleRequest }, { rejectWithValue }) => {
    try {
      const response = await roleAPI.patchRole(id, data)
      message.success('角色更新成功')
      return response
    } catch (error: any) {
      message.error(error.message || '更新角色失败')
      return rejectWithValue(error.message || '更新角色失败')
    }
  }
)

/**
 * 删除角色
 */
export const deleteRole = createAsyncThunk(
  'role/deleteRole',
  async (id: number, { rejectWithValue }) => {
    try {
      await roleAPI.deleteRole(id)
      message.success('角色删除成功')
      return id
    } catch (error: any) {
      message.error(error.message || '删除角色失败')
      return rejectWithValue(error.message || '删除角色失败')
    }
  }
)

/**
 * 获取权限树
 */
export const fetchPermissionTree = createAsyncThunk(
  'role/fetchPermissionTree',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetchPermissionTreeAPI()
      return response
    } catch (error: any) {
      return rejectWithValue(error.message || '获取权限树失败')
    }
  }
)

// Slice
const roleSlice = createSlice({
  name: 'role',
  initialState,
  reducers: {
    // 设置查询参数
    setListParams: (state, action: PayloadAction<RoleListParams>) => {
      state.listParams = { ...state.listParams, ...action.payload }
    },
    // 重置当前角色
    clearCurrentRole: (state) => {
      state.currentRole = null
    },
    // 清除错误
    clearError: (state) => {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    // 获取角色列表
    builder
      .addCase(fetchRoles.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchRoles.fulfilled, (state, action) => {
        state.loading = false
        state.roles = action.payload.results
        state.total = action.payload.count
      })
      .addCase(fetchRoles.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload as string
      })

    // 获取角色详情
    builder
      .addCase(fetchRoleDetail.pending, (state) => {
        state.roleLoading = true
        state.error = null
      })
      .addCase(fetchRoleDetail.fulfilled, (state, action) => {
        state.roleLoading = false
        state.currentRole = action.payload
      })
      .addCase(fetchRoleDetail.rejected, (state, action) => {
        state.roleLoading = false
        state.error = action.payload as string
      })

    // 创建角色
    builder
      .addCase(createRole.fulfilled, (state, action) => {
        // 创建成功后，可以选择刷新列表或直接添加到列表
        // 这里选择刷新列表
      })
      .addCase(createRole.rejected, (state, action) => {
        state.error = action.payload as string
      })

    // 更新角色
    builder
      .addCase(updateRole.fulfilled, (state, action) => {
        // 更新成功后，更新当前角色和列表中的角色
        if (state.currentRole?.id === action.payload.id) {
          state.currentRole = action.payload
        }
        const index = state.roles.findIndex((r) => r.id === action.payload.id)
        if (index !== -1) {
          state.roles[index] = action.payload
        }
      })
      .addCase(updateRole.rejected, (state, action) => {
        state.error = action.payload as string
      })

    // 删除角色
    builder
      .addCase(deleteRole.fulfilled, (state, action) => {
        // 从列表中移除
        state.roles = state.roles.filter((r) => r.id !== action.payload)
        if (state.currentRole?.id === action.payload) {
          state.currentRole = null
        }
      })
      .addCase(deleteRole.rejected, (state, action) => {
        state.error = action.payload as string
      })

    // 获取权限树
    builder
      .addCase(fetchPermissionTree.pending, (state) => {
        state.permissionTreeLoading = true
      })
      .addCase(fetchPermissionTree.fulfilled, (state, action) => {
        state.permissionTreeLoading = false
        state.permissionTree = action.payload
      })
      .addCase(fetchPermissionTree.rejected, (state, action) => {
        state.permissionTreeLoading = false
        state.error = action.payload as string
      })
  },
})

export const { setListParams, clearCurrentRole, clearError } = roleSlice.actions
export default roleSlice.reducer

