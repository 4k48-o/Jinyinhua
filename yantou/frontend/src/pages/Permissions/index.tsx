/**
 * 权限列表页面
 */
import { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Table, Card, Input, Space, Tag, Button, Tabs, message } from 'antd'
import { SearchOutlined, ReloadOutlined, UnorderedListOutlined, ApartmentOutlined } from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import { PageContainer } from '@/components/Layout'
import { getPermissionList, getPermissionTree } from '@/api/permission'
import type { Permission, PermissionTreeNode } from '@/types/role'
import PermissionTree from '@/components/Permission/PermissionTree'

const Permissions = () => {
  const { t } = useTranslation()
  const [loading, setLoading] = useState(false)
  const [permissions, setPermissions] = useState<Permission[]>([])
  const [total, setTotal] = useState(0)
  const [searchText, setSearchText] = useState('')
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
  })
  const [activeTab, setActiveTab] = useState('list')

  // 加载权限列表
  const loadPermissions = async () => {
    setLoading(true)
    try {
      const response = await getPermissionList({
        page: pagination.current,
        page_size: pagination.pageSize,
        search: searchText || undefined,
      })
      setPermissions(response.results)
      setTotal(response.count)
    } catch (error: any) {
      message.error(error.message || '加载权限列表失败')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (activeTab === 'list') {
      loadPermissions()
    }
  }, [pagination.current, pagination.pageSize, searchText, activeTab])

  // 表格列定义
  const columns: ColumnsType<Permission> = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: '权限名称',
      dataIndex: 'name',
      key: 'name',
      width: 200,
    },
    {
      title: '权限代码',
      dataIndex: 'code',
      key: 'code',
      width: 200,
      render: (code: string) => <Tag color="blue">{code}</Tag>,
    },
    {
      title: '资源类型',
      dataIndex: 'content_type',
      key: 'content_type',
      width: 120,
      render: (contentType?: string) => contentType || '-',
    },
    {
      title: '操作类型',
      dataIndex: 'action',
      key: 'action',
      width: 120,
      render: (action?: string) => action || '-',
    },
    {
      title: '父权限',
      dataIndex: 'parent_name',
      key: 'parent_name',
      width: 150,
      render: (parentName?: string) => parentName || '-',
    },
    {
      title: '子权限数',
      dataIndex: 'children_count',
      key: 'children_count',
      width: 100,
      render: (count?: number) => count || 0,
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true,
    },
    {
      title: '状态',
      dataIndex: 'is_active',
      key: 'is_active',
      width: 100,
      render: (isActive: boolean) => (
        <Tag color={isActive ? 'success' : 'default'}>
          {isActive ? '启用' : '禁用'}
        </Tag>
      ),
    },
    {
      title: '系统权限',
      dataIndex: 'is_system',
      key: 'is_system',
      width: 100,
      render: (isSystem: boolean) => (
        <Tag color={isSystem ? 'orange' : 'default'}>
          {isSystem ? '是' : '否'}
        </Tag>
      ),
    },
    {
      title: '排序',
      dataIndex: 'sort_order',
      key: 'sort_order',
      width: 80,
    },
  ]

  // 处理搜索
  const handleSearch = (value: string) => {
    setSearchText(value)
    setPagination({ ...pagination, current: 1 })
  }

  // 处理表格变化
  const handleTableChange = (newPagination: any) => {
    setPagination({
      current: newPagination.current,
      pageSize: newPagination.pageSize,
    })
  }

  const tabItems = [
    {
      key: 'list',
      label: (
        <span>
          <UnorderedListOutlined />
          列表视图
        </span>
      ),
      children: (
        <Card>
          <Space style={{ marginBottom: 16, width: '100%', justifyContent: 'space-between' }}>
            <Input.Search
              placeholder="搜索权限名称、代码或描述"
              allowClear
              style={{ width: 300 }}
              onSearch={handleSearch}
              enterButton={<SearchOutlined />}
            />
            <Button icon={<ReloadOutlined />} onClick={loadPermissions}>
              刷新
            </Button>
          </Space>

          <Table
            columns={columns}
            dataSource={permissions}
            rowKey="id"
            loading={loading}
            scroll={{ x: 'max-content' }}
            pagination={{
              current: pagination.current,
              pageSize: pagination.pageSize,
              total,
              showSizeChanger: true,
              showTotal: (total) => `共 ${total} 条`,
            }}
            onChange={handleTableChange}
          />
        </Card>
      ),
    },
    {
      key: 'tree',
      label: (
        <span>
          <ApartmentOutlined />
          树形视图
        </span>
      ),
      children: <PermissionTree />,
    },
  ]

  return (
    <PageContainer title={t('layout.permissionList')}>
      <Tabs activeKey={activeTab} items={tabItems} onChange={setActiveTab} />
    </PageContainer>
  )
}

export default Permissions

