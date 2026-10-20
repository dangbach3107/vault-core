import type { ReactNode } from 'react'
import { formatVnd } from '../../lib/money'
import {
  formatDate,
  formatDateTime,
  type Deal,
  type EvidenceRecord,
} from './types'

const BASIS: Record<string, string> = {
  EV: 'EV (giá trị doanh nghiệp)',
  EQUITY: 'Equity (giá trị vốn chủ)',
}

function expired(day?: string | null) {
  return Boolean(day) && day! < new Date().toISOString().slice(0, 10)
}

function Card({
  title,
  record,
  rows,
  badge,
}: {
  title: string
  record: EvidenceRecord
  rows: [string, ReactNode][]
  badge?: string
}) {
  return (
    <article className="access-item deal-record">
      <strong>{title}</strong>
      {badge && <span className="status-pill expired">{badge}</span>}
      <dl className="record-rows">
        {rows
          .filter(
            ([, value]) =>
              value !== null && value !== undefined && value !== '',
          )
          .map(([label, value]) => (
            <div key={label}>
              <dt>{label}</dt>
              <dd>{value}</dd>
            </div>
          ))}
      </dl>
      <small>
        {record.by} · {formatDateTime(record.at)}
        {record.note ? ` · ${record.note}` : ''}
      </small>
    </article>
  )
}

function price(low?: string | number | null, high?: string | number | null) {
  if (low == null) return null
  return high != null && String(high) !== String(low)
    ? `${formatVnd(String(low))} – ${formatVnd(String(high))}`
    : formatVnd(String(low))
}

/** What was entered on the business steps: buyer brief, NDA, LOI, offer, handoff. */
export default function DealRecords({ deal }: { deal: Deal }) {
  const { buyer_request, nda, indicative_loi, definitive_offer, handoff } =
    deal.state
  const offerRows = (offer: NonNullable<typeof indicative_loi>) =>
    [
      ['Số hiệu', offer.reference],
      ['Giá', price(offer.price_low_vnd, offer.price_high_vnd)],
      [
        'Cơ sở định giá',
        offer.valuation_basis ? BASIS[offer.valuation_basis] : null,
      ],
      [
        'Độc quyền',
        offer.exclusivity_days ? `${offer.exclusivity_days} ngày` : null,
      ],
      [
        'Hiệu lực đến',
        offer.valid_until ? formatDate(offer.valid_until) : null,
      ],
      ['Điều kiện', offer.conditions],
    ] as [string, ReactNode][]
  const cards = [
    buyer_request && (
      <Card
        key="request"
        title="Nhu cầu mua"
        record={buyer_request}
        rows={[
          ['Năng lực cần mua', buyer_request.capability],
          [
            'Ngân sách',
            price(buyer_request.budget_min_vnd, buyer_request.budget_max_vnd),
          ],
          ['Thời gian', buyer_request.timeline],
          ['Mục tiêu', buyer_request.goal],
        ]}
      />
    ),
    nda && (
      <Card
        key="nda"
        title="NDA"
        record={nda}
        badge={expired(nda.expires_on) ? 'Đã hết hạn' : undefined}
        rows={[
          ['Số hiệu', nda.reference],
          ['Các bên', nda.parties?.join(', ')],
          ['Ngày ký', formatDate(nda.signed_on)],
          ['Hết hạn', formatDate(nda.expires_on)],
        ]}
      />
    ),
    indicative_loi && (
      <Card
        key="loi"
        title="LOI sơ bộ (không ràng buộc)"
        record={indicative_loi}
        badge={expired(indicative_loi.valid_until) ? 'Hết hiệu lực' : undefined}
        rows={offerRows(indicative_loi)}
      />
    ),
    definitive_offer && (
      <Card
        key="offer"
        title="Đề nghị chính thức"
        record={definitive_offer}
        badge={
          expired(definitive_offer.valid_until) ? 'Hết hiệu lực' : undefined
        }
        rows={offerRows(definitive_offer)}
      />
    ),
    handoff && (
      <Card
        key="handoff"
        title="Bàn giao"
        record={handoff}
        rows={[
          ['Bên nhận', handoff.recipient],
          ['Ngày', handoff.handed_on ? formatDate(handoff.handed_on) : null],
          ['Danh mục', handoff.items?.join(', ')],
        ]}
      />
    ),
  ].filter(Boolean)
  if (cards.length === 0) return null
  return (
    <section className="panel" aria-labelledby="deal-records-title">
      <div className="section-title">
        <div>
          <p className="eyebrow">Hồ sơ giao dịch</p>
          <h2 id="deal-records-title">Nội dung đã ghi nhận</h2>
        </div>
      </div>
      <div className="finding-list">{cards}</div>
    </section>
  )
}
