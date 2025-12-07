/**
 * 权限树选择器组件
 */
import { useEffect, useState, useMemo } from 'react'
import { Tree, Spin, Empty, Checkbox, Space } from 'antd'
import type { DataNode } from 'antd/es/tree'
import type { PermissionTreeNode } from '@/types/role'

interface PermissionTreeSelectorProps {
  treeData: PermissionTreeNode[]
  loading?: boolean
  value?: number[]
  onChange?: (selectedIds: number[]) => void
}

const PermissionTreeSelector = ({
  treeData,
  loading = false,
  value = [],
  onChange,
}: PermissionTreeSelectorProps) => {
  const [checkedKeys, setCheckedKeys] = useState<React.Key[]>([])
  const [expandedKeys, setExpandedKeys] = useState<React.Key[]>([])

  // 将权限树转换为 Tree 组件需要的格式
  const treeNodes = useMemo(() => {
    const convertNode = (node: PermissionTreeNode): DataNode => {
      const children = node.children?.map(convertNode) || []
      return {
        title: (
          <Space>
            <span>{node.name}</span>
            <span style={{ color: '#999', fontSize: '12px' }}>({node.code})</span>
          </Space>
        ),
        key: String(node.id),
        children: children.length > 0 ? children : undefined,
      }
    }

    return treeData.map(convertNode)
  }, [treeData])

  // 获取所有权限ID（包括父权限和子权限）
  const getAllPermissionIds = useMemo(() => {
    const getAllIds = (nodes: PermissionTreeNode[]): number[] => {
      const ids: number[] = []
      nodes.forEach((node) => {
        ids.push(node.id)
        if (node.children && node.children.length > 0) {
          ids.push(...getAllIds(node.children))
        }
      })
      return ids
    }
    return getAllIds(treeData)
  }, [treeData])

  // 初始化选中状态
  useEffect(() => {
    if (value && value.length > 0) {
      setCheckedKeys(value.map(String))
    } else {
      setCheckedKeys([])
    }
  }, [value])

  // 初始化展开所有节点
  useEffect(() => {
    if (treeData.length > 0) {
      setExpandedKeys(getAllPermissionIds.map(String))
    }
  }, [treeData, getAllPermissionIds])

  // 处理选中变化
  const handleCheck = (checked: React.Key[] | { checked: React.Key[]; halfChecked: React.Key[] }) => {
    // Ant Design Tree 的 onCheck 返回格式：{ checked: [], halfChecked: [] }
    const checkedArray = Array.isArray(checked) ? checked : checked.checked
    setCheckedKeys(checkedArray)
    if (onChange) {
      // 转换为数字数组
      const numericIds = checkedArray.map((key) => Number(key)).filter((id) => !isNaN(id))
      onChange(numericIds)
    }
  }

  // 处理全选/取消全选
  const handleSelectAll = (checked: boolean) => {
    if (checked) {
      const allKeys = getAllPermissionIds.map(String)
      setCheckedKeys(allKeys)
      if (onChange) {
        onChange(getAllPermissionIds)
      }
    } else {
      setCheckedKeys([])
      if (onChange) {
        onChange([])
      }
    }
  }

  // 检查是否全选
  const isAllSelected = useMemo(() => {
    if (getAllPermissionIds.length === 0) return false
    return getAllPermissionIds.every((id) => checkedKeys.includes(String(id)))
  }, [getAllPermissionIds, checkedKeys])

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '40px 0' }}>
        <Spin size="large" />
      </div>
    )
  }

  if (treeData.length === 0) {
    return <Empty description="暂无权限数据" />
  }

  return (
    <div>
      <div style={{ marginBottom: 8 }}>
        <Checkbox
          checked={isAllSelected}
          indeterminate={checkedKeys.length > 0 && !isAllSelected}
          onChange={(e) => handleSelectAll(e.target.checked)}
        >
          全选
        </Checkbox>
        <span style={{ marginLeft: 8, color: '#999', fontSize: '12px' }}>
          已选择 {checkedKeys.length} 个权限
        </span>
      </div>
      <Tree
        checkable
        checkedKeys={checkedKeys}
        expandedKeys={expandedKeys}
        onCheck={handleCheck}
        onExpand={setExpandedKeys}
        treeData={treeNodes}
        checkStrictly={false}
        style={{
          maxHeight: '500px',
          overflow: 'auto',
          border: '1px solid #d9d9d9',
          borderRadius: '4px',
          padding: '12px',
        }}
      />
    </div>
  )
}

export default PermissionTreeSelector

