import { Breadcrumb as AntBreadcrumb } from 'antd'
import { useLocation, Link } from 'react-router-dom'
import { HomeOutlined } from '@ant-design/icons'
import type { BreadcrumbProps } from 'antd'
import { useTranslation } from 'react-i18next'
import { getBreadcrumbItems } from '@/router/menus'
import './Breadcrumb.css'

/**
 * 面包屑导航组件
 * 根据当前路由自动生成面包屑路径
 */
const BreadcrumbNav = () => {
  const location = useLocation()
  const { t } = useTranslation()
  const breadcrumbItems = getBreadcrumbItems(location.pathname, t)

  // 构建 Ant Design Breadcrumb 的 items 格式
  const items: BreadcrumbProps['items'] = [
    {
      title: (
        <Link to="/dashboard">
          <HomeOutlined />
        </Link>
      ),
    },
    ...breadcrumbItems.map((item, index) => {
      const isLast = index === breadcrumbItems.length - 1
      return {
        title: isLast ? (
          <span>{item.title}</span>
        ) : (
          <Link to={item.path}>{item.title}</Link>
        ),
      }
    }),
  ]

  return <AntBreadcrumb className="breadcrumb-nav" items={items} />
}

export default BreadcrumbNav

