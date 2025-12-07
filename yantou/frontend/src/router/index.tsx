import { lazy } from 'react'
import { createBrowserRouter, Navigate, Outlet } from 'react-router-dom'
import PrivateRoute from './PrivateRoute'
import { MainLayout } from '@/components/Layout'
import Login from '@/pages/Login'
import Register from '@/pages/Register'
import Forbidden from '@/pages/403'
import NotFound from '@/pages/404'
import { ROUTES } from '@/utils/constants'

// 懒加载页面组件
const Dashboard = lazy(() => import('@/pages/Dashboard'))
const Permissions = lazy(() => import('@/pages/Permissions'))
const Roles = lazy(() => import('@/pages/Roles'))
const Departments = lazy(() => import('@/pages/Departments'))
const Users = lazy(() => import('@/pages/Users'))

// 布局路由组件
const LayoutRoute = () => {
  return (
    <PrivateRoute>
      <MainLayout>
        <Outlet />
      </MainLayout>
    </PrivateRoute>
  )
}

// 路由配置
const router = createBrowserRouter([
  {
    path: ROUTES.LOGIN,
    element: <Login />,
  },
  {
    path: ROUTES.REGISTER,
    element: <Register />,
  },
  {
    path: '/',
    element: <LayoutRoute />,
    children: [
      {
        index: true,
        element: <Navigate to={ROUTES.DASHBOARD} replace />,
      },
      {
        path: ROUTES.DASHBOARD,
        element: <Dashboard />,
      },
      {
        path: '/system/permissions',
        element: <Permissions />,
      },
      {
        path: '/system/roles',
        element: <Roles />,
      },
      {
        path: '/system/departments',
        element: <Departments />,
      },
      {
        path: '/system/users',
        element: <Users />,
      },
    ],
  },
  {
    path: '/403',
    element: <Forbidden />,
  },
  {
    path: '/404',
    element: <NotFound />,
  },
  {
    path: '*',
    element: <NotFound />,
  },
])

export default router

