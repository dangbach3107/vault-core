const configuredBase = import.meta.env.VITE_API_BASE_URL as string | undefined

export const apiBase = (configuredBase || '/api/v1').replace(/\/$/, '')

export function hasConfiguredBackend() {
  return Boolean(configuredBase && configuredBase.trim())
}

const demoPasswordKey = 'vault.demoPassword'

export function getDemoPassword() {
  try {
    return localStorage.getItem(demoPasswordKey) || ''
  } catch {
    return ''
  }
}

export function setDemoPassword(value: string) {
  try {
    if (value) localStorage.setItem(demoPasswordKey, value)
    else localStorage.removeItem(demoPasswordKey)
  } catch {
    // Ignore storage failures; requests will simply omit the demo header.
  }
}

export function demoHeaders(): Record<string, string> {
  const password = getDemoPassword()
  return password ? { 'X-Demo-Password': password } : {}
}
