import { useTranslation } from 'react-i18next'
import { PageContainer } from '@/components/Layout'
import { Card, Row, Col, Statistic } from 'antd'
import { UserOutlined, TeamOutlined, SafetyOutlined, DashboardOutlined } from '@ant-design/icons'

/**
 * 仪表盘页面
 */
const Dashboard = () => {
  const { t } = useTranslation()

  return (
    <PageContainer title={t('layout.dashboard')}>
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title={t('layout.totalUsers')}
              value={0}
              prefix={<UserOutlined />}
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title={t('layout.totalDepartments')}
              value={0}
              prefix={<TeamOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title={t('layout.totalRoles')}
              value={0}
              prefix={<SafetyOutlined />}
              valueStyle={{ color: '#cf1322' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title={t('layout.systemStatus')}
              value={t('layout.normal')}
              prefix={<DashboardOutlined />}
              valueStyle={{ color: '#722ed1' }}
            />
          </Card>
        </Col>
      </Row>
      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col xs={24} lg={12}>
          <Card title={t('layout.welcome')}>
            <p>{t('layout.welcome')}</p>
            <p>{t('layout.welcomeMessage')}</p>
          </Card>
        </Col>
        <Col xs={24} lg={12}>
          <Card title={t('layout.systemInfo')}>
            <p>{t('layout.systemVersion')}: 1.0.0</p>
            <p>{t('layout.buildTime')}: 2025-12-06</p>
          </Card>
        </Col>
      </Row>
    </PageContainer>
  )
}

export default Dashboard

