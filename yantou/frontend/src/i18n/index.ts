import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import LanguageDetector from 'i18next-browser-languagedetector'
// 使用动态导入确保 JSON 文件正确加载
import zhCNData from './locales/zh-CN.json'
import enData from './locales/en.json'
import zhTWData from './locales/zh-TW.json'
import { STORAGE_KEYS } from '@/utils/constants'

// 确保导入的是对象而不是默认导出
const zhCN = zhCNData as any
const en = enData as any
const zhTW = zhTWData as any

// ========== 详细日志：资源导入检查 ==========
console.log('🔵 [i18n] ========== 资源导入检查 ==========')
console.log('🔵 [i18n] 开始导入资源文件...')
console.log('🔵 [i18n] zhCN 类型:', typeof zhCN)
console.log('🔵 [i18n] zhCN 值:', JSON.stringify(zhCN).substring(0, 200) + '...')
console.log('🔵 [i18n] zhCN 是否为对象:', typeof zhCN === 'object' && zhCN !== null)
console.log('🔵 [i18n] zhCN 键名:', zhCN && typeof zhCN === 'object' ? Object.keys(zhCN) : 'N/A')
console.log('🔵 [i18n] zhCN.auth:', (zhCN as any)?.auth)
console.log('🔵 [i18n] zhCN.auth.login:', (zhCN as any)?.auth?.login, `(期望: "登录", 实际: ${(zhCN as any)?.auth?.login})`)
console.log('🔵 [i18n] en 类型:', typeof en)
console.log('🔵 [i18n] zhTW 类型:', typeof zhTW)
console.log('🔵 [i18n] ======================================')

// 语言资源
const resources = {
  'zh-CN': {
    translation: zhCN,
  },
  en: {
    translation: en,
  },
  'zh-TW': {
    translation: zhTW,
  },
}

// ========== 详细日志：资源结构检查 ==========
console.log('🟢 [i18n] 资源结构:', {
  'zh-CN': {
    hasTranslation: !!resources['zh-CN'].translation,
    translationType: typeof resources['zh-CN'].translation,
    translationKeys: resources['zh-CN'].translation ? Object.keys(resources['zh-CN'].translation as any).slice(0, 5) : [],
  },
  en: {
    hasTranslation: !!resources.en.translation,
    translationType: typeof resources.en.translation,
  },
  'zh-TW': {
    hasTranslation: !!resources['zh-TW'].translation,
    translationType: typeof resources['zh-TW'].translation,
  },
})

// 从 localStorage 获取保存的语言设置
const getSavedLanguage = (): string | null => {
  try {
    const saved = localStorage.getItem(STORAGE_KEYS.LANGUAGE)
    console.log('🟡 [i18n] 从 localStorage 读取语言:', saved)
    return saved
  } catch (error) {
    console.error('🔴 [i18n] 读取 localStorage 失败:', error)
    return null
  }
}

// ========== 详细日志：初始化配置 ==========
const savedLang = getSavedLanguage()
// 兼容旧的语言代码，自动转换
let initialLang = savedLang || 'zh-CN'
if (initialLang === 'zh-hans') {
  initialLang = 'zh-CN'
} else if (initialLang === 'zh-hant') {
  initialLang = 'zh-TW'
}
console.log('🟡 [i18n] 初始化配置:', {
  savedLang,
  initialLang,
  fallbackLng: 'zh-CN',
  hasResources: !!resources,
  resourceKeys: Object.keys(resources),
})

// 初始化 i18n
const initPromise = i18n
  .use(LanguageDetector) // 检测浏览器语言
  .use(initReactI18next) // 将 i18n 传递给 react-i18next
  .init({
    resources,
    fallbackLng: {
      'zh-CN': ['zh-CN'], // 简体中文只回退到自己
      'zh-TW': ['zh-TW'], // 繁体中文只回退到自己
      'en': ['en'], // 英文只回退到自己
      default: ['zh-CN'], // 默认回退到简体中文
    },
    lng: initialLang, // 当前语言
    debug: true, // 强制启用调试（开发环境）
    
    // 命名空间配置
    defaultNS: 'translation',
    ns: ['translation'],
    
    interpolation: {
      escapeValue: false, // React 已经转义了
    },
    
    // 兼容性配置
    compatibilityJSON: 'v3',
    
    detection: {
      // 检测顺序
      order: ['localStorage', 'navigator'],
      // localStorage 键名
      lookupLocalStorage: STORAGE_KEYS.LANGUAGE,
      // 缓存用户选择的语言
      caches: ['localStorage'],
    },
    
    // 如果找不到翻译，返回 key 而不是显示错误
    returnNull: false,
    returnEmptyString: false,
    
    // 关键配置：确保资源正确加载
    load: 'languageOnly', // 只加载语言代码，不加载地区代码
    cleanCode: false, // 不清理语言代码，保持 zh-CN 格式
    nonExplicitSupportedLngs: true, // 支持非显式语言
  })
  
// 手动添加资源到 store（确保资源被正确加载）
initPromise.then(() => {
  // 强制添加所有资源到 store
  Object.keys(resources).forEach((lang) => {
    if (i18n.store && resources[lang as keyof typeof resources]) {
      const resource = resources[lang as keyof typeof resources]
      // 确保 store 结构存在
      if (!i18n.store.data[lang]) {
        i18n.store.data[lang] = {}
      }
      // 强制设置 translation（覆盖已存在的）
      i18n.store.data[lang].translation = resource.translation
      // 使用 addResourceBundle 确保资源被正确添加
      i18n.addResourceBundle(lang, 'translation', resource.translation, true, true)
      console.log(`🔄 [i18n] 强制添加资源到 store: ${lang}`, {
        hasTranslation: !!i18n.store.data[lang].translation,
        translationKeys: Object.keys(resource.translation as any).slice(0, 5),
        authLogin: (resource.translation as any)?.auth?.login,
      })
    }
  })
  
  // 验证当前语言的资源
  const currentLang = i18n.language
  if (i18n.store?.data?.[currentLang]?.translation) {
    const translation = i18n.store.data[currentLang].translation as any
    console.log('🔄 [i18n] 验证当前语言资源:', {
      currentLang,
      hasTranslation: true,
      translationKeys: Object.keys(translation).slice(0, 5),
      authLogin: translation?.auth?.login,
      testTranslation: i18n.t('auth.login'),
    })
    
    // 如果仍然返回 key，尝试重新初始化
    if (i18n.t('auth.login') === 'auth.login') {
      console.error('❌ [i18n] 资源已添加但翻译仍失败，尝试重新加载...')
      // 使用 addResourceBundle 强制添加
      i18n.addResourceBundle(currentLang, 'translation', translation, true, true)
      console.log('🔄 [i18n] 使用 addResourceBundle 重新添加资源后测试:', i18n.t('auth.login'))
    }
  }
})
  
// ========== 详细日志：初始化完成检查 ==========
initPromise.then(() => {
  console.log('✅ [i18n] 初始化完成')
  console.log('✅ [i18n] 当前语言:', i18n.language)
  console.log('✅ [i18n] 可用语言:', Object.keys(resources))
  console.log('✅ [i18n] 当前语言资源键:', resources[i18n.language as keyof typeof resources] ? Object.keys((resources[i18n.language as keyof typeof resources].translation as any) || {}).slice(0, 10) : 'N/A')
  
  // 详细测试翻译
  console.log('✅ [i18n] 测试翻译结果:')
  const testKeys = ['auth.login', 'auth.username', 'layout.dashboard', 'common.confirm']
  testKeys.forEach(key => {
    const result = i18n.t(key)
    console.log(`  - ${key}:`, result, `(类型: ${typeof result}, 是否等于key: ${result === key})`)
  })
  
  // 检查是否返回了 key 本身
  const loginResult = i18n.t('auth.login')
  if (loginResult === 'auth.login') {
    console.error('❌ [i18n] 翻译失败！返回了 key 而不是翻译文本')
    console.error('❌ [i18n] 这可能是因为资源没有正确加载')
  } else {
    console.log('✅ [i18n] 翻译成功，返回了翻译文本')
  }
  
  // 检查 store
  console.log('✅ [i18n] store 信息:', {
    hasStore: !!i18n.store,
    hasData: !!i18n.store?.data,
    dataKeys: i18n.store?.data ? Object.keys(i18n.store.data) : [],
    currentLangData: i18n.store?.data?.[i18n.language] ? Object.keys(i18n.store.data[i18n.language]) : [],
    translationData: i18n.store?.data?.[i18n.language]?.translation ? Object.keys(i18n.store.data[i18n.language].translation as any).slice(0, 5) : [],
  })
  
  // 直接访问资源测试
  const currentResource = resources[i18n.language as keyof typeof resources]
  if (currentResource) {
    const translation = currentResource.translation as any
    console.log('✅ [i18n] 直接访问资源测试:')
    console.log('  - translation.auth?.login:', translation?.auth?.login)
    console.log('  - translation.layout?.dashboard:', translation?.layout?.dashboard)
  }
}).catch((error) => {
  console.error('❌ [i18n] 初始化失败:', error)
  console.error('❌ [i18n] 错误堆栈:', error.stack)
})

// ========== 详细日志：语言切换监听 ==========
i18n.on('languageChanged', (lng) => {
  console.log('🟣 [i18n] ========== 语言切换事件 ==========')
  console.log('🟣 [i18n] 原始语言代码:', lng)
  try {
    // 兼容旧的语言代码，自动转换
    let normalizedLang = lng
    if (normalizedLang === 'zh-hans') {
      normalizedLang = 'zh-CN'
      console.log('🟣 [i18n] 转换: zh-hans -> zh-CN')
    } else if (normalizedLang === 'zh-hant') {
      normalizedLang = 'zh-TW'
      console.log('🟣 [i18n] 转换: zh-hant -> zh-TW')
    }
    
    console.log('🟣 [i18n] 标准化后的语言代码:', normalizedLang)
    console.log('🟣 [i18n] 可用资源键:', Object.keys(resources))
    console.log('🟣 [i18n] 目标资源是否存在:', !!resources[normalizedLang as keyof typeof resources])
    
    localStorage.setItem(STORAGE_KEYS.LANGUAGE, normalizedLang)
    console.log('🟣 [i18n] 语言已保存到 localStorage:', normalizedLang)
    
    // 确保切换后的语言资源被正确加载
    const resource = resources[normalizedLang as keyof typeof resources]
    if (resource && i18n.store) {
      console.log('🟣 [i18n] 找到资源，开始加载...')
      if (!i18n.store.data[normalizedLang]) {
        i18n.store.data[normalizedLang] = {}
      }
      // 强制更新 translation 命名空间
      i18n.store.data[normalizedLang].translation = resource.translation
      console.log('🔄 [i18n] 语言切换后手动添加资源到 store:', normalizedLang)
      console.log('🔄 [i18n] 资源键名:', Object.keys(resource.translation as any).slice(0, 5))
      console.log('🔄 [i18n] zh-TW 资源示例 - auth.login:', (resource.translation as any)?.auth?.login)
      
      // 使用 addResourceBundle 强制添加资源
      i18n.addResourceBundle(normalizedLang, 'translation', resource.translation, true, true)
      console.log('🔄 [i18n] 使用 addResourceBundle 添加资源完成')
    } else {
      console.error('🔴 [i18n] 资源不存在或 store 不可用:', {
        hasResource: !!resource,
        hasStore: !!i18n.store,
        normalizedLang,
        availableResources: Object.keys(resources),
      })
    }
    
    // 等待一下让资源加载完成
    setTimeout(() => {
      console.log('🟣 [i18n] ========== 切换后验证 ==========')
      console.log('🟣 [i18n] 当前 i18n.language:', i18n.language)
      console.log('🟣 [i18n] 当前 i18n.languages:', i18n.languages)
      console.log('🟣 [i18n] 当前 i18n.options.fallbackLng:', i18n.options.fallbackLng)
      
      // 强制设置语言并重新加载资源
      if (i18n.language !== normalizedLang) {
        console.log('🟣 [i18n] 语言不匹配，强制设置语言:', normalizedLang)
        i18n.changeLanguage(normalizedLang).then(() => {
          console.log('🟣 [i18n] 语言强制切换完成')
          // 再次添加资源确保正确
          if (resource && i18n.store) {
            i18n.addResourceBundle(normalizedLang, 'translation', resource.translation, true, true)
            console.log('🟣 [i18n] 资源再次添加完成')
          }
        })
      }
      
      console.log('🟣 [i18n] 切换后测试翻译 auth.login:', i18n.t('auth.login'))
      console.log('🟣 [i18n] 切换后 store 数据:', {
        exists: !!i18n.store?.data?.[normalizedLang],
        hasTranslation: !!i18n.store?.data?.[normalizedLang]?.translation,
        translationKeys: i18n.store?.data?.[normalizedLang]?.translation ? Object.keys(i18n.store.data[normalizedLang].translation as any).slice(0, 5) : [],
        authLogin: (i18n.store?.data?.[normalizedLang]?.translation as any)?.auth?.login,
        testTranslation: i18n.t('auth.login'),
        currentLanguage: i18n.language,
        storeLanguage: normalizedLang,
      })
      
      // 验证是否是繁体中文
      if (normalizedLang === 'zh-TW') {
        const twLogin = (i18n.store?.data?.[normalizedLang]?.translation as any)?.auth?.login
        console.log('🟣 [i18n] 繁体中文验证:', {
          expected: '登入',
          actual: twLogin,
          match: twLogin === '登入',
          currentTranslation: i18n.t('auth.login'),
          i18nLanguage: i18n.language,
          usingFallback: i18n.language !== normalizedLang,
        })
        
        // 如果仍然返回简体中文，尝试直接使用 store 中的数据
        if (i18n.t('auth.login') === '登录' && twLogin === '登入') {
          console.error('🔴 [i18n] 检测到资源不匹配，尝试强制修复...')
          // 强制设置语言
          i18n.changeLanguage('zh-TW').then(() => {
            // 再次添加资源
            i18n.addResourceBundle('zh-TW', 'translation', resource.translation, true, true)
            console.log('🟣 [i18n] 强制修复后测试:', i18n.t('auth.login'))
          })
        }
      }
    }, 200)
  } catch (error) {
    console.error('🔴 [i18n] 保存语言设置失败:', error)
  }
})

// 添加其他事件监听
i18n.on('loaded', (loaded) => {
  console.log('🟢 [i18n] 资源加载完成:', loaded)
})

i18n.on('failedLoading', (lng, ns, msg) => {
  console.error('🔴 [i18n] 资源加载失败:', { lng, ns, msg })
})

export default i18n
