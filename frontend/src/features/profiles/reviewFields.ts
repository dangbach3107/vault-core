import type { Company, Fact } from '../../api/workspace'
import type { components } from '../../api/generated/schema'
import { formatVnd } from '../../lib/money'
import { fields, optionLabels } from './fields'

/** Review paths: a top-level fact key, or financials.<year>.revenue_vnd|ebitda_vnd. */
export function fieldLabel(path: string) {
  const [first, year, metric] = path.split('.')
  if (first === 'financials')
    return `${metric === 'ebitda_vnd' ? 'EBITDA' : 'Doanh thu'} ${year}`
  return fields.find((field) => field.key === first)?.label || path
}

export function valueText(path: string, value: unknown) {
  if (value === null || value === undefined || value === '') return 'Chưa có'
  if (path.startsWith('financials.')) return formatVnd(String(value))
  return optionLabels[String(value)] || String(value)
}

export function reviewableFacts(company: Company) {
  const profile = company.profile as unknown as Record<string, unknown>
  const top = fields.map((field) => ({
    path: field.key as string,
    fact: (profile[field.key] || { value: null }) as Fact,
  }))
  const money = (company.profile.financials || []).flatMap((row) =>
    (['revenue_vnd', 'ebitda_vnd'] as const).map((metric) => ({
      path: `financials.${row.year}.${metric}`,
      fact: (row[metric] || { value: null }) as Fact,
    })),
  )
  return [...top, ...money]
}

export type Review = components['schemas']['ReviewResponse']

export const REVIEW_STATUS: Record<Review['status'], string> = {
  PENDING: 'Chờ duyệt',
  APPROVED: 'Đã chấp thuận',
  REJECTED: 'Bị từ chối',
}
