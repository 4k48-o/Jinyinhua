/**
 * 部门列表页面
 */
import { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useNavigate } from 'react-router-dom'
import { Table, Card, Input, Space, Tag, Button, message, Popconfirm, Tabs, Skeleton } from 'antd'
import { SearchOutlined, ReloadOutlined, PlusOutlined, EditOutlined, DeleteOutlined, UnorderedListOutlined, ApartmentOutlined, TeamOutlined } from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import { PageContainer } from '@/components/Layout'
import { useAuth } from '@/hooks/useAuth'
import { useDebounceFn } from '@/hooks/useDebounce'
import { getDepartmentList, deleteDepartment, getDepartmentTree } from '@/api/department'
import type { DepartmentListItem, DepartmentTreeNode } from '@/types/department'
import DepartmentForm from './DepartmentForm'
import DepartmentTree from './DepartmentTree'

const Departments = () => {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const { hasPermission } = useAuth()
  const [initialLoading, setInitialLoading] = useState(true) // 初始加载状态（显示骨架屏）
  const [loading, setLoading] = useState(false) // 数据加载状态
  const [departments, setDepartments] = useState<DepartmentListItem[]>([])
  const [total, setTotal] = useState(0)
  const [searchText, setSearchText] = useState('')
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
  })
  const [formVisible, setFormVisible] = useState(false)
  const [editingDepartment, setEditingDepartment] = useState<DepartmentListItem | null>(null)
  const [activeTab, setActiveTab] = useState('list')

  // 加载部门列表
  const loadDepartments = async (page?: number, pageSize?: number, search?: string) => {
    setLoading(true)
    try {
      const response = await getDepartmentList({
        page: page ?? pagination.current,
        page_size: pageSize ?? pagination.pageSize,
        search: search !== undefined ? search : searchText || undefined,
      })
      setDepartments(response.results)
      setTotal(response.count)
    } catch (error: any) {
      message.error(error.message || '加载部门列表失败')
    } finally {
      setLoading(false)
      setInitialLoading(false) // 首次加载完成后隐藏骨架屏
    }
  }

  useEffect(() => {
    if (activeTab === 'list') {
      loadDepartments()
    }
  }, [pagination.current, pagination.pageSize, activeTab])

  // 处理搜索
  const handleSearch = () => {
    setPagination({ ...pagination, current: 1 })
    loadDepartments(1, pagination.pageSize, searchText)
  }

  // 处理刷新
  const handleRefresh = () => {
    loadDepartments()
  }

  // 处理创建（防抖，防止重复点击）
  const handleCreateDebounced = useDebounceFn(() => {
    setEditingDepartment(null)
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
  const handleEdit = (record: DepartmentListItem) => {
    setEditingDepartment(record)
    setFormVisible(true)
  }

  // 处理查看员工
  const handleViewEmployees = (departmentId: number) => {
    navigate(`/system/users?department=${departmentId}`)
  }

  // 处理删除
  const handleDelete = async (id: number) => {
    try {
      await deleteDepartment(id)
      message.success(t('department.deleteSuccess') || '部门删除成功')
      loadDepartments()
    } catch (error: any) {
      message.error(error.message || '删除部门失败')
    }
  }

  // 处理表单关闭
  const handleFormClose = () => {
    setFormVisible(false)
    setEditingDepartment(null)
  }

  // 处理表单成功
  const handleFormSuccess = () => {
    handleFormClose()
    loadDepartments()
  }

  // 处理表格变化
  const handleTableChange = (newPagination: any) => {
    setPagination({
      current: newPagination.current,
      pageSize: newPagination.pageSize,
    })
  }

  // 表格列定义
  const columns: ColumnsType<DepartmentListItem> = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: t('department.name') || '部门名称',
      dataIndex: 'name',
      key: 'name',
      width: 200,
    },
    {
      title: t('department.code') || '部门代码',
      dataIndex: 'code',
      key: 'code',
      width: 150,
      render: (code?: string) => code ? <Tag color="blue">{code}</Tag> : '-',
    },
    {
      title: t('department.parent') || '父部门',
      dataIndex: 'parent_name',
      key: 'parent_name',
      width: 150,
      render: (parentName?: string) => parentName || '-',
    },
    {
      title: t('department.level') || '层级',
      dataIndex: 'level',
      key: 'level',
      width: 80,
      align: 'center',
    },
    {
      title: t('department.manager') || '负责人',
      dataIndex: 'manager_name',
      key: 'manager_name',
      width: 120,
      render: (managerName?: string) => managerName || '-',
    },
    {
      title: t('department.childrenCount') || '子部门数',
      dataIndex: 'children_count',
      key: 'children_count',
      width: 100,
      align: 'center',
      render: (count?: number) => count || 0,
    },
    {
      title: t('department.description') || '描述',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true,
    },
    {
      title: t('department.status') || '状态',
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
      render: (_: any, record: DepartmentListItem) => {
        const canEdit = hasPermission('department:update')
        const canDelete = hasPermission('department:delete')
        const canViewUsers = hasPermission('user:view') || hasPermission('user:read')
        
        return (
          <Space size="small">
            <Button
              type="link"
              size="small"
              icon={<TeamOutlined />}
              onClick={() => handleViewEmployees(record.id)}
              disabled={!canViewUsers}
            >
              {t('department.viewEmployees') || '查看员工'}
            </Button>
            <Button
              type="link"
              size="small"
              icon={<EditOutlined />}
              onClick={() => handleEdit(record)}
              disabled={!canEdit}
            >
              {t('common.edit') || '编辑'}
            </Button>
            <Popconfirm
              title={t('department.deleteConfirm') || '确定要删除这个部门吗？'}
              description={t('department.deleteWarning') || '如果部门下有子部门或用户，将无法删除'}
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

  const tabItems = [
    {
      key: 'list',
      label: (
        <span>
          <UnorderedListOutlined />
          {t('department.listView') || '列表视图'}
        </span>
      ),
      children: (
        <Card>
          <Space style={{ marginBottom: 16, width: '100%', justifyContent: 'space-between' }}>
            <Input.Search
              placeholder={t('department.searchPlaceholder') || '搜索部门名称、代码或描述'}
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
              {hasPermission('department:create') && (
                <Button type="primary" icon={<PlusOutlined />} onClick={handleCreate}>
                  {t('department.create') || '创建部门'}
                </Button>
              )}
            </Space>
          </Space>

          {initialLoading ? (
            <Skeleton {...skeletonConfig} />
          ) : (
            <Table
              columns={columns}
              dataSource={departments}
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
      ),
    },
    {
      key: 'tree',
      label: (
        <span>
          <ApartmentOutlined />
          {t('department.treeView') || '树形视图'}
        </span>
      ),
      children: <DepartmentTree />,
    },
  ]

  return (
    <PageContainer title={t('layout.departmentManagement') || '部门管理'}>
      <Tabs activeKey={activeTab} items={tabItems} onChange={setActiveTab} />
      
      <DepartmentForm
        visible={formVisible}
        department={editingDepartment}
        onClose={handleFormClose}
        onSuccess={handleFormSuccess}
      />
    </PageContainer>
  )
}

export default Departments

