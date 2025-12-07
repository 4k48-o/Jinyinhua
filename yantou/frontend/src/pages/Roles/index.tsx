/**
 * 角色列表页面
 */
import { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useNavigate } from 'react-router-dom'
import { Table, Card, Input, Space, Tag, Button, message, Modal, Popconfirm, Skeleton } from 'antd'
import { SearchOutlined, ReloadOutlined, PlusOutlined, EditOutlined, DeleteOutlined, SafetyOutlined } from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import { PageContainer } from '@/components/Layout'
import { useAppDispatch, useAppSelector } from '@/store/hooks'
import { fetchRoles, deleteRole, setListParams } from '@/store/slices/roleSlice'
import { useAuth } from '@/hooks/useAuth'
import { useDebounceFn } from '@/hooks/useDebounce'
import type { RoleListItem } from '@/types/role'
import RoleForm from './RoleForm'

const Roles = () => {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const dispatch = useAppDispatch()
  const { roles, total, loading, listParams } = useAppSelector((state) => state.role)
  const { hasPermission, user } = useAuth()
  
  const [initialLoading, setInitialLoading] = useState(true) // 初始加载状态（显示骨架屏）
  const [searchText, setSearchText] = useState('')
  const [pagination, setPagination] = useState({
    current: listParams.page || 1,
    pageSize: listParams.page_size || 10,
  })
  const [formVisible, setFormVisible] = useState(false)
  const [editingRole, setEditingRole] = useState<RoleListItem | null>(null)

  // 加载角色列表
  const loadRoles = (page?: number, pageSize?: number, search?: string) => {
    const currentPage = page ?? pagination.current
    const currentPageSize = pageSize ?? pagination.pageSize
    const currentSearch = search !== undefined ? search : searchText
    
    const params = {
      page: currentPage,
      page_size: currentPageSize,
      search: currentSearch || undefined,
    }
    
    console.log('📋 [Roles] 加载角色列表:', params)
    
    dispatch(setListParams(params))
    dispatch(fetchRoles(params)).then(() => {
      // 首次加载完成后隐藏骨架屏
      setInitialLoading(false)
    })
  }

  useEffect(() => {
    loadRoles()
  }, [pagination.current, pagination.pageSize])

  // 处理搜索
  const handleSearch = () => {
    console.log('🔍 [Roles] 搜索触发:', { searchText, pagination })
    setPagination({ ...pagination, current: 1 })
    // 直接使用参数调用，避免状态更新延迟
    loadRoles(1, pagination.pageSize, searchText)
  }

  // 处理刷新
  const handleRefresh = () => {
    loadRoles()
  }

  // 处理创建（防抖，防止重复点击）
  const handleCreateDebounced = useDebounceFn(() => {
    setEditingRole(null)
    setFormVisible(true)
  }, 300)

  const handleCreate = () => {
    // 如果表单已打开，不执行
    if (formVisible) {
      return
    }
    handleCreateDebounced()
  }

  // 处理编辑
  const handleEdit = (record: RoleListItem) => {
    setEditingRole(record)
    setFormVisible(true)
  }

  // 处理删除
  const handleDelete = async (id: number) => {
    try {
      await dispatch(deleteRole(id)).unwrap()
      loadRoles()
    } catch (error) {
      // 错误已在 slice 中处理
    }
  }

  // 处理表单关闭
  const handleFormClose = () => {
    setFormVisible(false)
    setEditingRole(null)
  }

  // 处理表单成功
  const handleFormSuccess = () => {
    handleFormClose()
    loadRoles()
  }

  // 表格列定义
  const columns: ColumnsType<RoleListItem> = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: t('role.name') || '角色名称',
      dataIndex: 'name',
      key: 'name',
      width: 150,
    },
    {
      title: t('role.code') || '角色代码',
      dataIndex: 'code',
      key: 'code',
      width: 150,
    },
    {
      title: t('role.description') || '描述',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true,
    },
    {
      title: t('role.permissionCount') || '权限数量',
      dataIndex: 'permissions_count',
      key: 'permissions_count',
      width: 120,
      align: 'center',
      render: (count: number) => count || 0,
    },
    {
      title: t('role.sortOrder') || '排序',
      dataIndex: 'sort_order',
      key: 'sort_order',
      width: 100,
      align: 'center',
    },
    {
      title: t('role.status') || '状态',
      dataIndex: 'is_active',
      key: 'is_active',
      width: 100,
      align: 'center',
      render: (isActive: boolean) => (
        <Tag color={isActive ? 'success' : 'default'}>
          {isActive ? (t('common.active') || '激活') : (t('common.inactive') || '禁用')}
        </Tag>
      ),
    },
    {
      title: t('role.isSystem') || '系统角色',
      dataIndex: 'is_system',
      key: 'is_system',
      width: 120,
      align: 'center',
      render: (isSystem: boolean) => (
        isSystem ? <Tag color="red">{t('common.yes') || '是'}</Tag> : <Tag>{t('common.no') || '否'}</Tag>
      ),
    },
    {
      title: t('common.createdAt') || '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (text: string) => text ? new Date(text).toLocaleString() : '-',
    },
    {
      title: t('common.actions') || '操作',
      key: 'actions',
      width: 150,
      fixed: 'right',
      render: (_: any, record: RoleListItem) => {
        // 检查是否有编辑权限
        const canEdit = hasPermission('role:update')
        // 系统角色只有超级管理员可以编辑
        const canEditSystemRole = record.is_system && user?.is_superuser
        // 非系统角色，有权限就可以编辑
        const canEditNonSystemRole = !record.is_system && canEdit
        // 是否可以编辑
        const editable = canEditSystemRole || canEditNonSystemRole
        
        // 检查是否有删除权限
        const canDelete = hasPermission('role:delete')
        // 系统角色不可删除
        const deletable = !record.is_system && canDelete
        
        return (
          <Space size="small">
            <Button
              type="link"
              size="small"
              icon={<EditOutlined />}
              onClick={() => handleEdit(record)}
              disabled={!editable}
            >
              {t('common.edit') || '编辑'}
            </Button>
            <Popconfirm
              title={t('role.deleteConfirm') || '确定要删除这个角色吗？'}
              description={t('role.deleteWarning') || '删除后无法恢复'}
              onConfirm={() => handleDelete(record.id)}
              okText={t('common.confirm') || '确定'}
              cancelText={t('common.cancel') || '取消'}
              disabled={!deletable}
            >
              <Button
                type="link"
                size="small"
                danger
                icon={<DeleteOutlined />}
                disabled={!deletable}
              >
                {t('common.delete') || '删除'}
              </Button>
            </Popconfirm>
          </Space>
        )
      },
    },
  ]

  // 骨架屏配置
  const skeletonConfig = {
    active: true,
    paragraph: { rows: 10 },
    title: { width: '100%' },
  }

  return (
    <PageContainer title={t('layout.roleManagement') || '角色管理'}>
      <Card>
        <Space direction="vertical" style={{ width: '100%' }} size="large">
          {/* 搜索栏 */}
          <Space>
            <Input
              placeholder={t('role.searchPlaceholder') || '搜索角色名称或代码'}
              prefix={<SearchOutlined />}
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
              onPressEnter={handleSearch}
              style={{ width: 300 }}
              allowClear
            />
            <Button icon={<SearchOutlined />} onClick={handleSearch}>
              {t('common.search') || '搜索'}
            </Button>
            <Button icon={<ReloadOutlined />} onClick={handleRefresh} loading={loading}>
              {t('common.refresh') || '刷新'}
            </Button>
            <Button type="primary" icon={<PlusOutlined />} onClick={handleCreate}>
              {t('role.create') || '创建角色'}
            </Button>
          </Space>

          {/* 表格 */}
          {initialLoading ? (
            <Skeleton {...skeletonConfig} />
          ) : (
            <Table
              columns={columns}
              dataSource={roles}
              rowKey="id"
              loading={loading}
              pagination={{
                current: pagination.current,
                pageSize: pagination.pageSize,
                total: total,
                showSizeChanger: true,
                showQuickJumper: true,
                showTotal: (total) => t('common.totalItems', { count: total }) || `共 ${total} 条`,
                onChange: (page, pageSize) => {
                  setPagination({ current: page, pageSize })
                },
              }}
              scroll={{ x: 1200 }}
            />
          )}
        </Space>
      </Card>

      {/* 创建/编辑表单 */}
      <RoleForm
        visible={formVisible}
        role={editingRole}
        onClose={handleFormClose}
        onSuccess={handleFormSuccess}
      />
    </PageContainer>
  )
}

export default Roles

