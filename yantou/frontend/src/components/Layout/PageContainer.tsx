import { ReactNode } from 'react'
import { Card, Spin } from 'antd'
import './PageContainer.css'

interface PageContainerProps {
  title?: string
  extra?: ReactNode
  loading?: boolean
  children: ReactNode
}

/**
 * 页面容器组件
 * 提供统一的页面布局和样式
 */
const PageContainer = ({ title, extra, loading = false, children }: PageContainerProps) => {
  return (
    <div className="page-container">
      {(title || extra) && (
        <div className="page-header">
          {title && <h2 className="page-title">{title}</h2>}
          {extra && <div className="page-extra">{extra}</div>}
        </div>
      )}
      <Card className="page-content" loading={loading}>
        {children}
      </Card>
    </div>
  )
}

export default PageContainer

