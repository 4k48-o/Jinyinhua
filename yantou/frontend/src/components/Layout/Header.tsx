import { Layout, Breadcrumb, Avatar, Dropdown, Space, Button } from 'antd'
import { MenuFoldOutlined, MenuUnfoldOutlined, UserOutlined, LogoutOutlined, SettingOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import type { MenuProps } from 'antd'
import { useTranslation } from 'react-i18next'
import { useAuth } from '@/hooks/useAuth'
import { useAppDispatch } from '@/store/hooks'
import { logout } from '@/store/slices/authSlice'
import { ROUTES } from '@/utils/constants'
import BreadcrumbNav from './Breadcrumb'
import LanguageSwitcher from './LanguageSwitcher'
import './Header.css'

const { Header: AntHeader } = Layout

interface HeaderProps {
  collapsed: boolean
  onCollapse: () => void
}

/**
 * 顶部导航栏组件
 * 包含面包屑、用户菜单、折叠按钮等
 */
const Header = ({ collapsed, onCollapse }: HeaderProps) => {
  const navigate = useNavigate()
  const dispatch = useAppDispatch()
  const { user } = useAuth()
  const { t } = useTranslation()

  // 处理登出
  const handleLogout = async () => {
    try {
      await dispatch(logout()).unwrap()
      navigate(ROUTES.LOGIN, { replace: true })
    } catch (error) {
      console.error('登出失败:', error)
    }
  }

  // 用户菜单项
  const userMenuItems: MenuProps['items'] = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: t('layout.profile'),
      onClick: () => {
        navigate('/profile')
      },
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: t('layout.settings'),
      onClick: () => {
        navigate('/settings')
      },
    },
    {
      type: 'divider',
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: t('auth.logout'),
      danger: true,
      onClick: handleLogout,
    },
  ]

  return (
    <AntHeader className="main-header">
      <div className="header-left">
        <Button
          type="text"
          icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
          onClick={onCollapse}
          className="collapse-btn"
        />
        <BreadcrumbNav />
      </div>
      <div className="header-right">
        <Space>
          <LanguageSwitcher />
          <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
            <Space className="user-menu" style={{ cursor: 'pointer' }}>
              <Avatar icon={<UserOutlined />} src={user?.avatar} />
              <span className="username">{user?.username || t('auth.username')}</span>
            </Space>
          </Dropdown>
        </Space>
      </div>
    </AntHeader>
  )
}

export default Header

