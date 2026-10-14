import { apiBase, demoHeaders } from './config'
import type { operations } from './generated/schema'

export type HealthResponse =
  operations['get_health']['responses'][200]['content']['application/json']

export async function getHealth(signal?: AbortSignal): Promise<HealthResponse> {
  const timeout = AbortSignal.timeout(5000)
  const response = await fetch(`${apiBase}/health`, {
    signal: signal ? AbortSignal.any([signal, timeout]) : timeout,
    headers: { Accept: 'application/json', ...demoHeaders() },
    cache: 'no-store',
  })
  if (!response.ok) throw new Error(`API trả về lỗi HTTP ${response.status}.`)
  const data: unknown = await response.json()
  if (
    typeof data !== 'object' ||
    data === null ||
    !('status' in data) ||
    data.status !== 'ok' ||
    !('scope' in data) ||
    data.scope !== 'liveness' ||
    !('service' in data) ||
    typeof data.service !== 'string' ||
    !('version' in data) ||
    typeof data.version !== 'string'
  ) {
    throw new Error('Phản hồi API không đúng định dạng.')
  }
  return data as HealthResponse
}
