/**
 * 权限树组件
 */
import { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Tree, Card, Spin, message, Tag, Space, Button } from 'antd'
import { ReloadOutlined } from '@ant-design/icons'
import type { DataNode } from 'antd/es/tree'
import { getPermissionTree } from '@/api/permission'
import type { PermissionTreeNode } from '@/types/role'

const PermissionTree = () => {
  const { t } = useTranslation()
  const [loading, setLoading] = useState(false)
  const [treeData, setTreeData] = useState<DataNode[]>([])

  // 将权限树转换为 Ant Design Tree 的数据格式
  const convertToTreeData = (nodes: PermissionTreeNode[]): DataNode[] => {
    return nodes.map((node) => ({
      title: (
        <Space>
          <span>{node.name}</span>
          <Tag color="blue">{node.code}</Tag>
          {node.content_type && <Tag>{node.content_type}</Tag>}
          {node.action && <Tag>{node.action}</Tag>}
          {node.is_system && <Tag color="orange">系统</Tag>}
        </Space>
      ),
      key: node.id.toString(),
      children: node.children ? convertToTreeData(node.children) : undefined,
    }))
  }

  // 加载权限树
  const loadPermissionTree = async () => {
    setLoading(true)
    try {
      const data = await getPermissionTree()
      setTreeData(convertToTreeData(data))
    } catch (error: any) {
      message.error(error.message || '加载权限树失败')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadPermissionTree()
  }, [])

  return (
    <Card
      title="权限树形结构"
      extra={
        <Button icon={<ReloadOutlined />} onClick={loadPermissionTree} loading={loading}>
          刷新
        </Button>
      }
    >
      <Spin spinning={loading}>
        {treeData.length > 0 ? (
          <Tree
            showLine
            defaultExpandAll
            treeData={treeData}
            style={{ background: '#fff' }}
          />
        ) : (
          <div style={{ textAlign: 'center', padding: '40px 0', color: '#999' }}>
            暂无权限数据
          </div>
        )}
      </Spin>
    </Card>
  )
}

export default PermissionTree

