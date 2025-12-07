/**
 * 用户列表页面
 */
import { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useSearchParams } from 'react-router-dom'
import { Table, Card, Input, Space, Tag, Button, message, Popconfirm, Avatar, Skeleton } from 'antd'
import { SearchOutlined, ReloadOutlined, PlusOutlined, EditOutlined, DeleteOutlined, UserOutlined, CloseOutlined } from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import { PageContainer } from '@/components/Layout'
import { useAuth } from '@/hooks/useAuth'
import { useDebounceFn } from '@/hooks/useDebounce'
import { getUserList, deleteUser, toggleUserActive } from '@/api/user'
import type { UserListItem } from '@/types/user'
import UserForm from './UserForm'

const Users = () => {
  const { t } = useTranslation()
  const [searchParams, setSearchParams] = useSearchParams()
  const { hasPermission } = useAuth()
  const [initialLoading, setInitialLoading] = useState(true) // 初始加载状态（显示骨架屏）
  const [loading, setLoading] = useState(false) // 数据加载状态
  const [users, setUsers] = useState<UserListItem[]>([])
  const [total, setTotal] = useState(0)
  const [searchText, setSearchText] = useState('')
  const [selectedDepartmentId, setSelectedDepartmentId] = useState<number | undefined>(
    searchParams.get('department') ? parseInt(searchParams.get('department') || '0', 10) : undefined
  )
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
  })
  const [formVisible, setFormVisible] = useState(false)
  const [editingUser, setEditingUser] = useState<UserListItem | null>(null)

  // 加载用户列表
  const loadUsers = async (page?: number, pageSize?: number, search?: string, departmentId?: number) => {
    setLoading(true)
    try {
      const response = await getUserList({
        page: page ?? pagination.current,
        page_size: pageSize ?? pagination.pageSize,
        search: search !== undefined ? search : searchText || undefined,
        department: departmentId !== undefined ? departmentId : selectedDepartmentId,
      })
      setUsers(response.results)
      setTotal(response.count)
    } catch (error: any) {
      message.error(error.message || '加载用户列表失败')
    } finally {
      setLoading(false)
      setInitialLoading(false) // 首次加载完成后隐藏骨架屏
    }
  }

  // 从URL参数中读取部门ID
  useEffect(() => {
    const departmentParam = searchParams.get('department')
    if (departmentParam) {
      const departmentId = parseInt(departmentParam, 10)
      if (!isNaN(departmentId)) {
        setSelectedDepartmentId(departmentId)
      }
    } else {
      setSelectedDepartmentId(undefined)
    }
  }, [searchParams])

  useEffect(() => {
    loadUsers()
  }, [pagination.current, pagination.pageSize, selectedDepartmentId])

  // 处理搜索
  const handleSearch = () => {
    setPagination({ ...pagination, current: 1 })
    loadUsers(1, pagination.pageSize, searchText, selectedDepartmentId)
  }

  // 清除部门过滤
  const handleClearDepartmentFilter = () => {
    setSelectedDepartmentId(undefined)
    setSearchParams({}, { replace: true })
    setPagination({ ...pagination, current: 1 })
    loadUsers(1, pagination.pageSize, searchText, undefined)
  }

  // 处理刷新
  const handleRefresh = () => {
    loadUsers()
  }

  // 处理创建（防抖）
  const handleCreateDebounced = useDebounceFn(() => {
    setEditingUser(null)
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
  const handleEdit = (record: UserListItem) => {
    setEditingUser(record)
    setFormVisible(true)
  }

  // 处理删除
  const handleDelete = async (id: number) => {
    try {
      await deleteUser(id)
      message.success(t('user.deleteSuccess') || '用户删除成功')
      loadUsers()
    } catch (error: any) {
      message.error(error.message || '删除用户失败')
    }
  }

  // 处理激活/禁用
  const handleToggleActive = async (id: number) => {
    try {
      await toggleUserActive(id)
      message.success(t('user.toggleSuccess') || '操作成功')
      loadUsers()
    } catch (error: any) {
      message.error(error.message || '操作失败')
    }
  }

  // 处理表单关闭
  const handleFormClose = () => {
    setFormVisible(false)
    setEditingUser(null)
  }

  // 处理表单成功
  const handleFormSuccess = () => {
    handleFormClose()
    loadUsers()
  }

  // 处理表格变化
  const handleTableChange = (newPagination: any) => {
    setPagination({
      current: newPagination.current,
      pageSize: newPagination.pageSize,
    })
  }

  // 表格列定义
  const columns: ColumnsType<UserListItem> = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: t('user.avatar') || '头像',
      dataIndex: 'profile',
      key: 'avatar',
      width: 80,
      align: 'center',
      render: (profile?: any) => (
        <Avatar
          src={profile?.avatar}
          icon={<UserOutlined />}
          size="small"
        />
      ),
    },
    {
      title: t('user.username') || '用户名',
      dataIndex: 'username',
      key: 'username',
      width: 150,
    },
    {
      title: t('user.fullName') || '姓名',
      dataIndex: 'full_name',
      key: 'full_name',
      width: 150,
      render: (fullName?: string, record: UserListItem) => {
        if (fullName) return fullName
        if (record.first_name || record.last_name) {
          return `${record.first_name || ''} ${record.last_name || ''}`.trim()
        }
        return record.username
      },
    },
    {
      title: t('user.email') || '邮箱',
      dataIndex: 'email',
      key: 'email',
      width: 200,
    },
    {
      title: t('user.phone') || '手机号',
      dataIndex: 'phone',
      key: 'phone',
      width: 120,
      render: (phone?: string) => phone || '-',
    },
    {
      title: t('user.department') || '部门',
      dataIndex: ['profile', 'department_name'],
      key: 'department',
      width: 150,
      render: (departmentName?: string) => departmentName || '-',
    },
    {
      title: t('user.position') || '职位',
      dataIndex: ['profile', 'position'],
      key: 'position',
      width: 120,
      render: (position?: string) => position || '-',
    },
    {
      title: t('user.status') || '状态',
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
      title: t('user.isStaff') || '员工',
      dataIndex: 'is_staff',
      key: 'is_staff',
      width: 80,
      align: 'center',
      render: (isStaff: boolean) => (
        isStaff ? <Tag color="blue">{t('common.yes') || '是'}</Tag> : <Tag>{t('common.no') || '否'}</Tag>
      ),
    },
    {
      title: t('user.isSuperuser') || '超级管理员',
      dataIndex: 'is_superuser',
      key: 'is_superuser',
      width: 120,
      align: 'center',
      render: (isSuperuser?: boolean) => (
        isSuperuser ? <Tag color="red">{t('common.yes') || '是'}</Tag> : <Tag>{t('common.no') || '否'}</Tag>
      ),
    },
    {
      title: t('common.createdAt') || '创建时间',
      dataIndex: 'date_joined',
      key: 'date_joined',
      width: 180,
      render: (text: string) => text ? new Date(text).toLocaleString() : '-',
    },
    {
      title: t('common.actions') || '操作',
      key: 'actions',
      width: 200,
      fixed: 'right',
      render: (_: any, record: UserListItem) => {
        const canEdit = hasPermission('user:update')
        const canDelete = hasPermission('user:delete')
        const canToggle = hasPermission('user:update')
        
        return (
          <Space size="small">
            <Button
              type="link"
              size="small"
              icon={<EditOutlined />}
              onClick={() => handleEdit(record)}
              disabled={!canEdit}
            >
              {t('common.edit') || '编辑'}
            </Button>
            <Button
              type="link"
              size="small"
              onClick={() => handleToggleActive(record.id)}
              disabled={!canToggle}
            >
              {record.is_active ? (t('user.disable') || '禁用') : (t('user.enable') || '激活')}
            </Button>
            <Popconfirm
              title={t('user.deleteConfirm') || '确定要删除这个用户吗？'}
              description={t('user.deleteWarning') || '删除后用户将无法登录'}
              onConfirm={() => handleDelete(record.id)}
              okText={t('common.confirm') || '确定'}
              cancelText={t('common.cancel') || '取消'}
              disabled={!canDelete}
            >
              <Button
                type="link"
                size="small"
                danger
                icon={<DeleteOutlined />}
                disabled={!canDelete}
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
    <PageContainer title={t('layout.userManagement') || '用户管理'}>
      <Card>
        <Space direction="vertical" style={{ width: '100%', marginBottom: 16 }} size="middle">
          {/* 部门过滤提示 */}
          {selectedDepartmentId && (
            <Space>
              <Tag color="blue" closable onClose={handleClearDepartmentFilter}>
                {t('user.filteredByDepartment') || `已按部门过滤 (ID: ${selectedDepartmentId})`}
                <CloseOutlined style={{ marginLeft: 4 }} />
              </Tag>
            </Space>
          )}
          
          {/* 搜索和操作栏 */}
          <Space style={{ width: '100%', justifyContent: 'space-between' }}>
            <Input.Search
              placeholder={t('user.searchPlaceholder') || '搜索用户名、邮箱或姓名'}
              allowClear
              style={{ width: 300 }}
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
              onSearch={handleSearch}
              enterButton={<SearchOutlined />}
            />
            <Space>
              <Button icon={<ReloadOutlined />} onClick={handleRefresh} loading={loading}>
                {t('common.refresh') || '刷新'}
              </Button>
              {hasPermission('user:create') && (
                <Button type="primary" icon={<PlusOutlined />} onClick={handleCreate}>
                  {t('user.create') || '创建用户'}
                </Button>
              )}
            </Space>
          </Space>
        </Space>

        {initialLoading ? (
          <Skeleton {...skeletonConfig} />
        ) : (
          <Table
            columns={columns}
            dataSource={users}
            rowKey="id"
            loading={loading}
            scroll={{ x: 'max-content' }}
            pagination={{
              current: pagination.current,
              pageSize: pagination.pageSize,
              total,
              showSizeChanger: true,
              showTotal: (total) => t('common.totalItems', { count: total }) || `共 ${total} 条`,
            }}
            onChange={handleTableChange}
          />
        )}
      </Card>
      
      <UserForm
        visible={formVisible}
        user={editingUser}
        onClose={handleFormClose}
        onSuccess={handleFormSuccess}
      />
    </PageContainer>
  )
}

export default Users

