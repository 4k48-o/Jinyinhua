import { useState } from 'react'
import { Form, Input, Button, message } from 'antd'
import { UserOutlined, LockOutlined, MailOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { useAppDispatch } from '@/store/hooks'
import { register } from '@/store/slices/authSlice'
import { ROUTES } from '@/utils/constants'
import type { RegisterRequest } from '@/types'
import './index.css'

const Register = () => {
  const navigate = useNavigate()
  const dispatch = useAppDispatch()
  const [form] = Form.useForm()
  const [loading, setLoading] = useState(false)

  // 处理注册
  const handleRegister = async (values: RegisterRequest & { password_confirm: string }) => {
    // 验证密码确认
    if (values.password !== values.password_confirm) {
      message.error('两次输入的密码不一致')
      return
    }

    setLoading(true)
    try {
      const registerData: RegisterRequest = {
        username: values.username,
        password: values.password,
        password_confirm: values.password_confirm,
      }

      await dispatch(register(registerData)).unwrap()

      message.success('注册成功，已自动登录')
      navigate(ROUTES.DASHBOARD, { replace: true })
    } catch (error: any) {
      const errorMessage = error || '注册失败，请检查输入信息'
      message.error(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="register-container">
      <div className="register-box">
        <div className="register-header">
          <h1>用户注册</h1>
          <p>创建您的账户</p>
        </div>

        <Form
          form={form}
          name="register"
          onFinish={handleRegister}
          autoComplete="off"
          size="large"
          className="register-form"
        >
          <Form.Item
            name="username"
            rules={[
              { required: true, message: '请输入用户名' },
              { min: 3, message: '用户名至少3个字符' },
              { max: 150, message: '用户名不能超过150个字符' },
              {
                pattern: /^[a-zA-Z0-9_]+$/,
                message: '用户名只能包含字母、数字和下划线',
              },
            ]}
          >
            <Input prefix={<UserOutlined />} placeholder="用户名" autoComplete="username" />
          </Form.Item>

          <Form.Item
            name="password"
            rules={[
              { required: true, message: '请输入密码' },
              { min: 8, message: '密码至少8个字符' },
              {
                pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])/,
                message: '密码必须包含大小写字母、数字和特殊字符',
              },
            ]}
            hasFeedback
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="密码"
              autoComplete="new-password"
            />
          </Form.Item>

          <Form.Item
            name="password_confirm"
            dependencies={['password']}
            rules={[
              { required: true, message: '请确认密码' },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value || getFieldValue('password') === value) {
                    return Promise.resolve()
                  }
                  return Promise.reject(new Error('两次输入的密码不一致'))
                },
              }),
            ]}
            hasFeedback
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="确认密码"
              autoComplete="new-password"
            />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" block loading={loading}>
              注册
            </Button>
          </Form.Item>

          <div className="register-footer">
            <span>已有账户？</span>
            <a href={ROUTES.LOGIN}>立即登录</a>
          </div>
        </Form>
      </div>
    </div>
  )
}

export default Register

