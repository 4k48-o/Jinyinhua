import { useState, useEffect } from 'react'
import { Form, Input, Button, Checkbox, message } from 'antd'
import { UserOutlined, LockOutlined, SafetyOutlined } from '@ant-design/icons'
import { useNavigate, useLocation } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAppDispatch } from '@/store/hooks'
import { login } from '@/store/slices/authSlice'
import { getCaptcha } from '@/api/auth'
import { ROUTES } from '@/utils/constants'
import LanguageSwitcher from '@/components/Layout/LanguageSwitcher'
import type { LoginRequest } from '@/types'
import './index.css'

const Login = () => {
  const navigate = useNavigate()
  const location = useLocation()
  const dispatch = useAppDispatch()
  const { t, i18n, ready } = useTranslation()
  const [form] = Form.useForm()
  const [loading, setLoading] = useState(false)
  const [needCaptcha, setNeedCaptcha] = useState(false)
  const [captchaImage, setCaptchaImage] = useState<string>('')
  const [captchaKey, setCaptchaKey] = useState<string>('')
  const [captchaLoading, setCaptchaLoading] = useState(false)

  // ========== 详细日志：Login 组件 i18n 状态 ==========
  useEffect(() => {
    console.log('🟠 [Login] useTranslation hook 状态:', {
      ready,
      language: i18n.language,
      hasI18n: !!i18n,
      hasStore: !!i18n.store,
      hasData: !!i18n.store?.data,
      currentLangData: i18n.store?.data?.[i18n.language] ? '存在' : '不存在',
    })
    
    console.log('🟠 [Login] 测试翻译调用:')
    console.log('  - t("auth.login"):', t('auth.login'))
    console.log('  - t("auth.username"):', t('auth.username'))
    console.log('  - t("layout.dashboard"):', t('layout.dashboard'))
    
    // 检查 t 函数
    console.log('🟠 [Login] t 函数信息:', {
      isFunction: typeof t === 'function',
      tType: typeof t,
    })
    
    // 直接使用 i18n.t 测试
    console.log('🟠 [Login] 直接使用 i18n.t 测试:')
    console.log('  - i18n.t("auth.login"):', i18n.t('auth.login'))
    console.log('  - i18n.t("auth.username"):', i18n.t('auth.username'))
    
    // 检查资源
    if (i18n.store?.data?.[i18n.language]) {
      const langData = i18n.store.data[i18n.language]
      console.log('🟠 [Login] 当前语言资源结构:', {
        hasTranslation: !!langData.translation,
        translationKeys: langData.translation ? Object.keys(langData.translation as any).slice(0, 5) : [],
        authLogin: (langData.translation as any)?.auth?.login,
      })
    }
  }, [ready, i18n.language, t, i18n])

  // 从路由状态获取重定向路径
  const from = (location.state as any)?.from?.pathname || ROUTES.DASHBOARD

  // 添加日志：组件初始化
  console.log('🔵 [Login] 组件初始化', {
    needCaptcha,
    captchaImage: captchaImage ? `已设置(${captchaImage.length}字符)` : '未设置',
    captchaKey,
    captchaLoading,
  })

  // 加载验证码
  const loadCaptcha = async () => {
    console.log('🟢 [loadCaptcha] 开始加载验证码')
    console.log('🟢 [loadCaptcha] 当前状态:', {
      needCaptcha,
      captchaImage: captchaImage ? '已设置' : '未设置',
      captchaLoading,
    })
    
    try {
      setCaptchaLoading(true)
      setCaptchaImage('') // 先清空，显示加载状态
      console.log('🟢 [loadCaptcha] 已设置 loading 状态，开始请求 API')
      
      const response = await getCaptcha()
      console.log('🟢 [loadCaptcha] API 响应收到:', {
        response,
        type: typeof response,
        isObject: typeof response === 'object',
        keys: response ? Object.keys(response) : [],
        hasImage: response?.image ? '是' : '否',
        imageLength: response?.image?.length || 0,
        hasKey: response?.key ? '是' : '否',
        keyValue: response?.key,
      })
      
      if (response) {
        // 检查响应格式
        if (response.image) {
          console.log('🟢 [loadCaptcha] 找到 image 字段')
          console.log('🟢 [loadCaptcha] image 前50字符:', response.image.substring(0, 50))
          console.log('🟢 [loadCaptcha] image 总长度:', response.image.length)
          
          setCaptchaImage(response.image)
          setCaptchaKey(response.key || '')
          
          console.log('🟢 [loadCaptcha] 状态已更新:', {
            captchaImage: '已设置',
            captchaKey: response.key || '',
          })
        } else if (typeof response === 'string' && response.startsWith('data:image')) {
          console.log('🟢 [loadCaptcha] 响应是 base64 字符串')
          setCaptchaImage(response)
        } else {
          console.error('🔴 [loadCaptcha] 验证码响应格式错误')
          console.error('🔴 [loadCaptcha] 响应内容:', JSON.stringify(response, null, 2))
          message.error('验证码格式错误，请检查后端接口')
        }
      } else {
        console.error('🔴 [loadCaptcha] 验证码响应为空')
        message.error('获取验证码失败，响应为空')
      }
    } catch (error: any) {
      console.error('🔴 [loadCaptcha] 加载验证码失败')
      console.error('🔴 [loadCaptcha] 错误对象:', error)
      console.error('🔴 [loadCaptcha] 错误详情:', {
        message: error?.message,
        response: error?.response,
        status: error?.response?.status,
        data: error?.response?.data,
        stack: error?.stack,
      })
      message.error(error?.message || '加载验证码失败，请检查网络连接')
    } finally {
      setCaptchaLoading(false)
      console.log('🟢 [loadCaptcha] 完成，loading 状态已清除')
    }
  }

  // 监听 needCaptcha 变化，自动加载验证码
  useEffect(() => {
    console.log('🟡 [useEffect] needCaptcha 状态变化:', {
      needCaptcha,
      captchaImage: captchaImage ? `已设置(${captchaImage.length}字符)` : '未设置',
      shouldLoad: needCaptcha && !captchaImage,
    })
    
    if (needCaptcha && !captchaImage) {
      console.log('🟡 [useEffect] 条件满足，开始加载验证码')
      loadCaptcha()
    } else {
      console.log('🟡 [useEffect] 条件不满足，不加载验证码')
    }
  }, [needCaptcha])
  
  // 监听 captchaImage 变化
  useEffect(() => {
    console.log('🟡 [useEffect] captchaImage 状态变化:', {
      captchaImage: captchaImage ? `已设置(${captchaImage.length}字符)` : '未设置',
      needCaptcha,
    })
  }, [captchaImage])
  
  // 初始加载验证码（如果需要）
  useEffect(() => {
    console.log('🟡 [useEffect] Login 组件已挂载')
    console.log('🟡 [useEffect] 初始状态:', {
      needCaptcha,
      captchaImage: captchaImage ? '已设置' : '未设置',
      captchaKey,
    })
  }, [])

  // 处理登录
  const handleLogin = async (values: LoginRequest & { remember?: boolean }) => {
    console.log('🔵 [handleLogin] 开始登录')
    console.log('🔵 [handleLogin] 表单值:', {
      username: values.username,
      hasPassword: !!values.password,
      hasCaptcha: !!values.captcha,
      needCaptcha,
    })
    
    setLoading(true)
    try {
      const loginData: LoginRequest = {
        username: values.username,
        password: values.password,
      }

      // 如果需要验证码
      if (needCaptcha && values.captcha) {
        loginData.captcha = values.captcha
        console.log('🔵 [handleLogin] 已添加验证码到登录数据')
      }

      console.log('🔵 [handleLogin] 发送登录请求')
      await dispatch(login(loginData)).unwrap()

      console.log('🟢 [handleLogin] 登录成功')
      message.success(t('auth.loginSuccess'))
      navigate(from, { replace: true })
    } catch (error: any) {
      console.log('🔴 [handleLogin] 登录失败')
      console.log('🔴 [handleLogin] 错误对象:', error)
      console.log('🔴 [handleLogin] 错误类型:', typeof error)
      console.log('🔴 [handleLogin] 错误属性:', Object.keys(error || {}))
      
      // 从错误对象中提取错误消息
      let errorMessage = t('auth.loginFailed')
      if (error) {
        if (typeof error === 'string') {
          errorMessage = error
          console.log('🔴 [handleLogin] 错误是字符串:', errorMessage)
        } else if (error.message) {
          errorMessage = error.message
          console.log('🔴 [handleLogin] 从 error.message 获取:', errorMessage)
        } else if (error.payload) {
          errorMessage = error.payload
          console.log('🔴 [handleLogin] 从 error.payload 获取:', errorMessage)
        } else {
          console.log('🔴 [handleLogin] 错误对象结构:', JSON.stringify(error, null, 2))
        }
      }
      
      console.log('🔴 [handleLogin] 最终错误消息:', errorMessage)
      message.error(errorMessage)

      // 如果登录失败，可能需要验证码
      // 检查错误消息中是否包含触发验证码的关键词
      const keywords = ['验证码', '次数', '剩余', '需要验证码', '剩余尝试']
      const matches = keywords.filter(keyword => errorMessage.includes(keyword))
      
      const shouldShowCaptcha = matches.length > 0
      
      console.log('🔴 [handleLogin] 验证码触发检查:', {
        errorMessage,
        keywords,
        matches,
        shouldShowCaptcha,
        currentNeedCaptcha: needCaptcha,
      })
      
      if (shouldShowCaptcha) {
        console.log('🟡 [handleLogin] 需要显示验证码')
        if (!needCaptcha) {
          console.log('🟡 [handleLogin] 设置 needCaptcha 为 true')
          setNeedCaptcha(true)
          console.log('🟡 [handleLogin] needCaptcha 已设置为 true，useEffect 应该会触发 loadCaptcha')
        } else {
          console.log('🟡 [handleLogin] 验证码已显示，刷新验证码')
          loadCaptcha()
        }
      } else {
        console.log('🔴 [handleLogin] 未触发验证码显示条件')
        console.log('🔴 [handleLogin] 错误消息不包含关键词:', keywords)
      }
    } finally {
      setLoading(false)
      console.log('🔵 [handleLogin] 登录处理完成')
    }
  }

  return (
    <div className="login-container">
      <div className="login-box">
        <div className="login-header">
          <LanguageSwitcher />
          <h1>{t('auth.loginTitle')}</h1>
          <p>{t('auth.loginSubtitle')}</p>
        </div>

        <Form
          form={form}
          name="login"
          onFinish={handleLogin}
          autoComplete="off"
          size="large"
          className="login-form"
          initialValues={{
            username: 'admin',
            password: '0qww294e@WSX',
          }}
        >
          <Form.Item
            name="username"
            rules={[
              { required: true, message: t('auth.usernameRequired') },
              { min: 3, message: t('auth.usernameMinLength') },
            ]}
          >
            <Input
              prefix={<UserOutlined />}
              placeholder={t('auth.username')}
              autoComplete="username"
            />
          </Form.Item>

          <Form.Item
            name="password"
            rules={[
              { required: true, message: t('auth.passwordRequired') },
              { min: 8, message: t('auth.passwordMinLength') },
            ]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder={t('auth.password')}
              autoComplete="current-password"
            />
          </Form.Item>

          {needCaptcha && (
            <Form.Item
              name="captcha"
              rules={[{ required: true, message: t('auth.captchaRequired') }]}
            >
              {(() => {
                console.log('🟣 [Render] 渲染验证码输入框，状态:', {
                  needCaptcha,
                  captchaImage: captchaImage ? `已设置(${captchaImage.length}字符)` : '未设置',
                  captchaLoading,
                })
                return (
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <Input
                      prefix={<SafetyOutlined />}
                      placeholder={t('auth.captchaRequired')}
                      style={{ flex: 1 }}
                    />
                    {captchaImage ? (
                      <img
                        src={captchaImage}
                        alt="验证码"
                        onClick={() => {
                          console.log('🟣 [Render] 点击验证码图片，刷新验证码')
                          loadCaptcha()
                        }}
                        style={{
                          cursor: 'pointer',
                          height: 40,
                          width: 120,
                          objectFit: 'contain',
                          border: '1px solid #d9d9d9',
                          borderRadius: '4px',
                          backgroundColor: '#f5f5f5',
                        }}
                        onError={(e) => {
                          console.error('🔴 [Render] 验证码图片加载失败:', e)
                          message.error('验证码图片加载失败，请重试')
                          setCaptchaImage('')
                        }}
                        onLoad={() => {
                          console.log('🟢 [Render] 验证码图片加载成功')
                        }}
                      />
                    ) : (
                      <Button
                        type="default"
                        size="small"
                        onClick={() => {
                          console.log('🟣 [Render] 点击获取验证码按钮')
                          loadCaptcha()
                        }}
                        loading={captchaLoading}
                      >
                        获取验证码
                      </Button>
                    )}
                  </div>
                )
              })()}
            </Form.Item>
          )}

          <Form.Item>
            <div className="login-options">
              <Form.Item name="remember" valuePropName="checked" noStyle>
                <Checkbox>{t('auth.rememberMe')}</Checkbox>
              </Form.Item>
              <a href="#forgot" className="forgot-password">
                {t('auth.forgotPassword')}
              </a>
            </div>
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" block loading={loading}>
              {t('auth.login')}
            </Button>
          </Form.Item>

          <div className="login-footer">
            <span>{t('auth.noAccount')}</span>
            <a href={ROUTES.REGISTER} onClick={(e) => { e.preventDefault(); window.location.href = ROUTES.REGISTER }}>{t('auth.registerNow')}</a>
          </div>
        </Form>
      </div>
    </div>
  )
}

export default Login

