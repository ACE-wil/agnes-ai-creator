import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { settingsApi } from '../api'
import { useDialog } from './useDialog'

export const NO_API_KEY_TITLE = '无法操作'
export const NO_API_KEY_MESSAGE =
  '尚未配置 Agnes AI API Key，无法执行此操作。请前往「设置」页面添加并启用 API Key。'

export function useApiKeyGuard() {
  const router = useRouter()
  const { confirm } = useDialog()

  const hasActiveKey = ref(true)
  const keyStatusLoading = ref(true)

  async function refreshKeyStatus() {
    keyStatusLoading.value = true
    try {
      const status = await settingsApi.getStatus()
      hasActiveKey.value = status.has_active_key
    } catch {
      hasActiveKey.value = false
    } finally {
      keyStatusLoading.value = false
    }
  }

  async function requireApiKey() {
    await refreshKeyStatus()
    if (hasActiveKey.value) return true

    const goSettings = await confirm({
      title: NO_API_KEY_TITLE,
      message: NO_API_KEY_MESSAGE,
      confirmText: '前往设置',
      cancelText: '取消',
      confirmVariant: 'primary',
    })
    if (goSettings) {
      await router.push('/settings')
    }
    return false
  }

  return {
    hasActiveKey,
    keyStatusLoading,
    refreshKeyStatus,
    requireApiKey,
  }
}
