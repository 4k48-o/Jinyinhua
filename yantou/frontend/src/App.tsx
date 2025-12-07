import { Suspense, useEffect, useState } from 'react'
import { Provider } from 'react-redux'
import { RouterProvider } from 'react-router-dom'
import { ConfigProvider, Spin } from 'antd'
import zhCN from 'antd/locale/zh_CN'
import enUS from 'antd/locale/en_US'
import zhTW from 'antd/locale/zh_TW'
import { useTranslation } from 'react-i18next'
import { store } from './store'
import router from './router'
import { useInitAuth } from './hooks/useInitAuth'
import './assets/styles/index.css'

// Ant Design 语言映射
const antdLocales: Record<string, any> = {
  'zh-CN': zhCN,
  'zh_CN': zhCN, // 兼容 zh_CN
  'zh-hans': zhCN, // 兼容旧代码
  en: enUS,
  'en-US': enUS, // 兼容 en-US
  'zh-TW': zhTW,
  'zh_TW': zhTW, // 兼容 zh_TW
  'zh-hant': zhTW, // 兼容旧代码
}

// 初始化组件
const AppInit = () => {
  useInitAuth()
  return null
}

// 加载中组件
const Loading = () => (
  <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
    <Spin size="large" />
  </div>
)

// App 内容组件（需要使用 useTranslation Hook）
const AppContent = () => {
  const { i18n } = useTranslation()
  const [antdLocale, setAntdLocale] = useState(antdLocales[i18n.language] || zhCN)
  
  // 监听语言变化，更新 Ant Design locale
  useEffect(() => {
    // 兼容旧的语言代码
    let normalizedLang = i18n.language
    if (normalizedLang === 'zh-hans') {
      normalizedLang = 'zh-CN'
    } else if (normalizedLang === 'zh-hant') {
      normalizedLang = 'zh-TW'
    }
    
    const currentLocale = antdLocales[normalizedLang] || antdLocales[i18n.language] || zhCN
    setAntdLocale(currentLocale)
    
    // 调试信息（开发环境）
    if (import.meta.env.DEV) {
      console.log('🟡 [App] 语言变化:', {
        i18nLanguage: i18n.language,
        normalizedLang,
        antdLocale: currentLocale,
        availableLocales: Object.keys(antdLocales),
        isZhTW: normalizedLang === 'zh-TW',
        localeIsZhTW: currentLocale === zhTW,
        localeIsZhCN: currentLocale === zhCN,
      })
    }
  }, [i18n.language])

  return (
    <ConfigProvider locale={antdLocale}>
      <AppInit />
      <Suspense fallback={<Loading />}>
        <RouterProvider router={router} />
      </Suspense>
    </ConfigProvider>
  )
}

function App() {
  return (
    <Provider store={store}>
      <AppContent />
    </Provider>
  )
}

export default App

