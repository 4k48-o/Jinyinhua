import { Dropdown } from 'antd'
import { GlobalOutlined } from '@ant-design/icons'
import type { MenuProps } from 'antd'
import { useTranslation } from 'react-i18next'
import { LANGUAGES, STORAGE_KEYS } from '@/utils/constants'
import { setItem } from '@/utils/storage'
import './LanguageSwitcher.css'

/**
 * 语言切换组件
 */
const LanguageSwitcher = () => {
  const { i18n } = useTranslation()

  // 语言切换菜单项
  const languageMenuItems: MenuProps['items'] = LANGUAGES.map((lang) => ({
    key: lang.value,
    label: lang.label,
    onClick: () => {
      console.log('🟣 [LanguageSwitcher] 切换语言到:', lang.value)
      i18n.changeLanguage(lang.value).then(() => {
        console.log('🟣 [LanguageSwitcher] 语言切换完成，当前语言:', i18n.language)
        console.log('🟣 [LanguageSwitcher] 测试翻译 auth.login:', i18n.t('auth.login'))
        setItem(STORAGE_KEYS.LANGUAGE, lang.value)
        // 更新 API 请求头中的语言
        // 这个会在下次请求时自动更新，因为 api/index.ts 中会从 localStorage 读取
      }).catch((error) => {
        console.error('🔴 [LanguageSwitcher] 语言切换失败:', error)
      })
    },
  }))

  // 获取当前语言的显示名称
  const currentLanguage = LANGUAGES.find((lang) => lang.value === i18n.language) || LANGUAGES[0]

  return (
    <div className="language-switcher-wrapper">
      <Dropdown menu={{ items: languageMenuItems }} placement="bottomRight">
        <div className="language-switcher" style={{ cursor: 'pointer' }}>
          <GlobalOutlined />
          <span className="language-text">{currentLanguage.label}</span>
        </div>
      </Dropdown>
    </div>
  )
}

export default LanguageSwitcher

