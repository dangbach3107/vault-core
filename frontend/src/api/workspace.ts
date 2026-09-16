import { apiBase, demoHeaders } from './config'
export { apiBase } from './config'
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

export async function getFile(
  path: string,
  signal: AbortSignal,
): Promise<Blob> {
  let response: Response
  try {
    response = await fetch(`${apiBase}${path}`, {
      signal: AbortSignal.any([signal, AbortSignal.timeout(30000)]),
      headers: demoHeaders(),
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
        ...demoHeaders(),
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
  const contentType = response.headers.get('content-type') || ''
  if (!contentType.includes('application/json')) {
    throw new Error(
      'Màn này cần backend API đang chạy. Bản Vercel hiện chỉ dùng để demo Investor MVP bằng dữ liệu giả lập.',
    )
  }
  return response.json() as Promise<T>
}
