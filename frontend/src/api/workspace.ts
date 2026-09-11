import type { components } from './generated/schema'

export type Company = components['schemas']['CompanyResponse']
export type Profile = components['schemas']['CompanyInput-Input']
export type Summary = components['schemas']['CompanySummary']
export type Room = components['schemas']['RoomResponse']
export type RoomDetail = components['schemas']['RoomDetail']
export type DocumentDetail = components['schemas']['DocumentDetail']
export type Version = components['schemas']['VersionResponse']
export type Preview =
  | components['schemas']['AnonymousPreview']
  | components['schemas']['IdentifiedPreview']
  | components['schemas']['RestrictedPreview']
export type Fact = Omit<Profile['company_name'], 'value'> & {
  value?: string | number | null
}
export type FieldName = Exclude<keyof Profile, 'financials'>

export const apiBase = (import.meta.env.VITE_API_BASE_URL || '/api/v1').replace(
  /\/$/,
  '',
)

export async function getFile(
  path: string,
  signal: AbortSignal,
): Promise<Blob> {
  let response: Response
  try {
    response = await fetch(`${apiBase}${path}`, {
      signal: AbortSignal.any([signal, AbortSignal.timeout(30000)]),
      cache: 'no-store',
    })
  } catch {
    throw new Error(
      'Không tải được bản xem trước. Kiểm tra kết nối rồi thử lại.',
    )
  }
  if (!response.ok) {
    const error = await response.json().catch(() => null)
    throw new Error(
      typeof error?.detail === 'string'
        ? error.detail
        : 'Không đọc được file xem trước.',
    )
  }
  return response.blob()
}

export async function request<T>(
  path: string,
  init: RequestInit = {},
): Promise<T> {
  let response: Response
  try {
    response = await fetch(`${apiBase}${path}`, {
      ...init,
      signal: init.signal
        ? AbortSignal.any([init.signal, AbortSignal.timeout(30000)])
        : AbortSignal.timeout(30000),
      headers: {
        Accept: 'application/json',
        ...(init.body && !(init.body instanceof FormData)
          ? { 'Content-Type': 'application/json' }
          : {}),
        ...init.headers,
      },
      cache: 'no-store',
    })
  } catch {
    throw new Error(
      'Không kết nối được API hoặc yêu cầu quá thời gian. Kiểm tra backend rồi thử lại. Nếu vừa lưu, kiểm tra danh sách trước khi gửi lại.',
    )
  }
  if (!response.ok) {
    let message = `Yêu cầu thất bại (HTTP ${response.status}).`
    const error = await response.json().catch(() => null)
    if (typeof error?.detail === 'string') message = error.detail
    else if (Array.isArray(error?.detail)) {
      message = error.detail
        .map(
          (item: { loc?: (string | number)[]; msg?: string }) =>
            `${item.loc?.slice(1).join('.')}: ${item.msg || 'Giá trị không hợp lệ'}`,
        )
        .join('; ')
    }
    throw new Error(message)
  }
  return response.json() as Promise<T>
}
