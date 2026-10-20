// Amounts arrive as decimal strings. Format them with string/BigInt math so
// large values never pass through a JS float. Deal money is VND; a company profile
// states its own reporting currency (VND or JPY).

export type Currency = 'VND' | 'JPY'

function split(raw: string) {
  const value = raw.trim()
  const negative = value.startsWith('-')
  const [whole = '0', fraction = ''] = value.replace(/^[-+]/, '').split('.')
  if (!/^\d+$/.test(whole) || !/^\d*$/.test(fraction)) return null
  return { negative, whole: whole.replace(/^0+(?=\d)/, ''), fraction }
}

/** 42000000000 → "42.000.000.000 VND" (exact, Vietnamese grouping). */
export function formatVnd(raw: string | null | undefined): string {
  return formatMoney(raw, 'VND')
}

/** Exact amount with the given currency code, e.g. "450.000.000 JPY". */
export function formatMoney(
  raw: string | null | undefined,
  currency: Currency,
): string {
  if (raw == null || raw === '') return 'Chưa có'
  const parts = split(String(raw))
  if (!parts) return String(raw)
  const grouped = parts.whole.replace(/\B(?=(\d{3})+(?!\d))/g, '.')
  const fraction = parts.fraction.replace(/0+$/, '')
  return `${parts.negative ? '-' : ''}${grouped}${fraction ? `,${fraction}` : ''} ${currency}`
}

/** 42000000000 → "42,0 tỷ VND"; below one billion falls back to triệu or the exact amount. */
export function formatVndShort(raw: string | null | undefined): string {
  if (raw == null || raw === '') return 'Chưa có'
  const parts = split(String(raw))
  if (!parts) return String(raw)
  const whole = BigInt(parts.whole)
  const sign = parts.negative ? '-' : ''
  const scaled = (unit: bigint, label: string) => {
    const tenths = (whole * 10n + unit / 2n) / unit
    return `${sign}${(tenths / 10n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.')},${tenths % 10n} ${label} VND`
  }
  if (whole >= 1_000_000_000n) return scaled(1_000_000_000n, 'tỷ')
  if (whole >= 1_000_000n) return scaled(1_000_000n, 'triệu')
  return formatVnd(raw)
}
