import { useState, ReactNode } from 'react'
import { Layout } from 'antd'
import Sidebar from './Sidebar'
import Header from './Header'
import './MainLayout.css'

const { Content } = Layout

interface MainLayoutProps {
  children: ReactNode
}

/**
 * 主布局组件
 * 包含侧边栏、顶部导航和内容区域
 */
const MainLayout = ({ children }: MainLayoutProps) => {
  const [collapsed, setCollapsed] = useState(false)

  return (
    <Layout className="main-layout" style={{ minHeight: '100vh' }}>
      <Sidebar collapsed={collapsed} />
      <Layout>
        <Header collapsed={collapsed} onCollapse={() => setCollapsed(!collapsed)} />
        <Content className="main-content">
          {children}
        </Content>
      </Layout>
    </Layout>
  )
}

export default MainLayout

