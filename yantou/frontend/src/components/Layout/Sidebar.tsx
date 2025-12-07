import { useState, useEffect } from 'react'
import { Layout, Menu } from 'antd'
import { useNavigate, useLocation } from 'react-router-dom'
import type { MenuProps } from 'antd'
import { useTranslation } from 'react-i18next'
import { useAuth } from '@/hooks/useAuth'
import { getMenuItems } from '@/router/menus'
import './Sidebar.css'

const { Sider } = Layout

interface SidebarProps {
  collapsed: boolean
}

/**
 * 侧边栏组件
 * 包含菜单导航和折叠功能
 */
const Sidebar = ({ collapsed }: SidebarProps) => {
  const navigate = useNavigate()
  const location = useLocation()
  const { permissions, roles } = useAuth()
  const { t } = useTranslation()
  const [selectedKeys, setSelectedKeys] = useState<string[]>([])
  const [openKeys, setOpenKeys] = useState<string[]>([])

  // 根据当前路径设置选中的菜单项
  useEffect(() => {
    const path = location.pathname
    setSelectedKeys([path])
    
    // 设置展开的父菜单
    const pathParts = path.split('/').filter(Boolean)
    if (pathParts.length > 1) {
      setOpenKeys([`/${pathParts[0]}`])
    }
  }, [location.pathname])

  // 获取菜单项（根据权限过滤）
  const menuItems = getMenuItems(permissions, roles, t)
  
  // 调试：输出菜单项和权限信息
  useEffect(() => {
    console.log('🔵 [Sidebar] 菜单调试信息:', {
      permissions,
      roles,
      menuItemsCount: menuItems.length,
      menuItems: menuItems.map(item => ({
        key: item.key,
        label: item.label,
        hasChildren: !!item.children,
        childrenCount: item.children?.length || 0,
        children: item.children?.map(child => ({
          key: child.key,
          label: child.label,
        })),
      })),
    })
  }, [permissions, roles, menuItems, t])

  // 菜单点击处理
  const handleMenuClick: MenuProps['onClick'] = ({ key }) => {
    navigate(key)
  }

  // 菜单展开/收起处理
  const handleOpenChange = (keys: string[]) => {
    setOpenKeys(keys)
  }

  return (
    <Sider
      trigger={null}
      collapsible
      collapsed={collapsed}
      width={200}
      className="main-sidebar"
      theme="light"
    >
      <div className="sidebar-logo">
        {collapsed ? (
          <div className="logo-icon">企</div>
        ) : (
          <div className="logo-text">{t('layout.appTitle')}</div>
        )}
      </div>
      <Menu
        mode="inline"
        selectedKeys={selectedKeys}
        openKeys={openKeys}
        items={menuItems}
        onClick={handleMenuClick}
        onOpenChange={handleOpenChange}
        className="sidebar-menu"
      />
    </Sider>
  )
}

export default Sidebar

