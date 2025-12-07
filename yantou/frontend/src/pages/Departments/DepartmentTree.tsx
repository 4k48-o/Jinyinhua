/**
 * 部门树形视图组件
 */
import { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Card, Tree, Input, Space, Button, message, Spin } from 'antd'
import { SearchOutlined, ReloadOutlined } from '@ant-design/icons'
import type { DataNode } from 'antd/es/tree'
import { getDepartmentTree } from '@/api/department'
import type { DepartmentTreeNode } from '@/types/department'

const DepartmentTree = () => {
  const { t } = useTranslation()
  const [loading, setLoading] = useState(false)
  const [treeData, setTreeData] = useState<DataNode[]>([])
  const [expandedKeys, setExpandedKeys] = useState<React.Key[]>([])
  const [searchValue, setSearchValue] = useState('')
  const [autoExpandParent, setAutoExpandParent] = useState(true)

  // 将部门树转换为 Ant Design Tree 的数据格式
  const convertToTreeData = (departments: DepartmentTreeNode[]): DataNode[] => {
    return departments.map((dept) => ({
      title: (
        <span>
          {dept.name}
          {dept.code && <span style={{ color: '#999', marginLeft: 8 }}>({dept.code})</span>}
          {dept.manager_name && <span style={{ color: '#999', marginLeft: 8 }}>- {dept.manager_name}</span>}
        </span>
      ),
      key: dept.id,
      children: dept.children && dept.children.length > 0 ? convertToTreeData(dept.children) : undefined,
    }))
  }

  // 加载部门树
  const loadTree = async () => {
    setLoading(true)
    try {
      const tree = await getDepartmentTree()
      const data = convertToTreeData(tree)
      setTreeData(data)
      // 默认展开所有节点
      const allKeys = getAllKeys(data)
      setExpandedKeys(allKeys)
    } catch (error: any) {
      message.error(error.message || '加载部门树失败')
    } finally {
      setLoading(false)
    }
  }

  // 获取所有节点的 key
  const getAllKeys = (data: DataNode[]): React.Key[] => {
    let keys: React.Key[] = []
    data.forEach((node) => {
      keys.push(node.key)
      if (node.children) {
        keys = keys.concat(getAllKeys(node.children))
      }
    })
    return keys
  }

  // 搜索过滤
  const getFilteredTreeData = (data: DataNode[], searchValue: string): DataNode[] => {
    if (!searchValue) {
      return data
    }

    const filter = (nodes: DataNode[]): DataNode[] => {
      return nodes
        .map((node) => {
          const title = typeof node.title === 'string' ? node.title : (node.title as any)?.props?.children?.[0] || ''
          const match = title.toLowerCase().includes(searchValue.toLowerCase())
          
          if (match) {
            return node
          }
          
          if (node.children) {
            const filteredChildren = filter(node.children)
            if (filteredChildren.length > 0) {
              return {
                ...node,
                children: filteredChildren,
              }
            }
          }
          
          return null
        })
        .filter((node) => node !== null) as DataNode[]
    }

    return filter(data)
  }

  useEffect(() => {
    loadTree()
  }, [])

  // 处理搜索
  const handleSearch = (value: string) => {
    setSearchValue(value)
    if (value) {
      const filtered = getFilteredTreeData(treeData, value)
      const keys = getAllKeys(filtered)
      setExpandedKeys(keys)
      setAutoExpandParent(true)
    }
  }

  // 处理展开/收起
  const handleExpand = (keys: React.Key[]) => {
    setExpandedKeys(keys)
    setAutoExpandParent(false)
  }

  const filteredTreeData = getFilteredTreeData(treeData, searchValue)

  return (
    <Card>
      <Space style={{ marginBottom: 16, width: '100%', justifyContent: 'space-between' }}>
        <Input.Search
          placeholder={t('department.searchPlaceholder') || '搜索部门名称'}
          allowClear
          style={{ width: 300 }}
          value={searchValue}
          onChange={(e) => handleSearch(e.target.value)}
          enterButton={<SearchOutlined />}
        />
        <Button icon={<ReloadOutlined />} onClick={loadTree} loading={loading}>
          {t('common.refresh') || '刷新'}
        </Button>
      </Space>

      <Spin spinning={loading}>
        {filteredTreeData.length > 0 ? (
          <Tree
            treeData={filteredTreeData}
            expandedKeys={expandedKeys}
            autoExpandParent={autoExpandParent}
            onExpand={handleExpand}
            defaultExpandAll
          />
        ) : (
          <div style={{ textAlign: 'center', padding: '40px 0', color: '#999' }}>
            {t('common.noData') || '暂无数据'}
          </div>
        )}
      </Spin>
    </Card>
  )
}

export default DepartmentTree

