import { FormEvent, useState } from 'react'
import { request } from '../../api/workspace'
import { formatVnd, formatVndShort } from '../../lib/money'
import type { Role } from '../auth/roles'
import ClosingEvidence from './ClosingEvidence'
import { formatDate, type Deal, type Fee } from './types'

const FEE_LABELS: Record<Fee['type'], string> = {
  PREP_PACKAGE: 'Phí chuẩn bị hồ sơ',
  TECH_DD: 'Phí Tech DD',
  SUCCESS_FEE: 'Phí thành công',
}
const STATUS_LABELS: Record<Fee['status'], string> = {
  DRAFT: 'Chưa xuất hóa đơn',
  INVOICED: 'Đã xuất hóa đơn',
  PARTIALLY_PAID: 'Thanh toán một phần',
  PAID: 'Đã thanh toán đủ',
  OVERDUE: 'Quá hạn',
}
const today = () => new Date().toISOString().slice(0, 10)
const MONEY_PATTERN = '\\d+(\\.\\d{1,2})?'

function FeeRow({
  fee,
  editable,
  onSubmit,
}: {
  fee: Fee
  editable: boolean
  onSubmit: (path: string, body: object, done: string) => Promise<boolean>
}) {
  const [invoice, setInvoice] = useState({
    invoice_number: '',
    issued_on: today(),
  })
  const [payment, setPayment] = useState({
    amount_vnd: '',
    paid_on: today(),
    reference: '',
  })
  return (
    <article className={`access-item fee ${fee.status.toLowerCase()}`}>
      <strong>
        {FEE_LABELS[fee.type]} · {formatVnd(fee.amount_vnd)}
      </strong>
      <small title={formatVnd(fee.amount_vnd)}>
        {formatVndShort(fee.amount_vnd)} · Hạn {formatDate(fee.due_on)} · Đã thu{' '}
        {formatVnd(fee.paid_vnd)} · Còn {formatVnd(fee.balance_vnd)}
      </small>
      {fee.invoice && (
        <small>
          Hóa đơn {fee.invoice.number} ngày {formatDate(fee.invoice.issued_on)}
        </small>
      )}
      {fee.payments.length > 0 && (
        <ul className="grant-files">
          {fee.payments.map((item, index) => (
            <li key={index}>
              {formatDate(item.paid_on)} · {formatVnd(item.amount_vnd)} ·{' '}
              {item.reference}
            </li>
          ))}
        </ul>
      )}
      {fee.note && <p className="muted">{fee.note}</p>}
      <span className={`status-pill ${fee.status.toLowerCase()}`}>
        {STATUS_LABELS[fee.status]}
      </span>
      {editable && !fee.invoice && (
        <form
          className="inline-form"
          onSubmit={async (event) => {
            event.preventDefault()
            await onSubmit(
              `fees/${fee.id}/invoice`,
              invoice,
              'Đã ghi nhận hóa đơn.',
            )
          }}
        >
          <input
            aria-label="Số hóa đơn"
            placeholder="Số hóa đơn"
            value={invoice.invoice_number}
            onChange={(event) =>
              setInvoice({ ...invoice, invoice_number: event.target.value })
            }
            required
            maxLength={60}
          />
          <input
            aria-label="Ngày xuất hóa đơn"
            type="date"
            max={today()}
            value={invoice.issued_on}
            onChange={(event) =>
              setInvoice({ ...invoice, issued_on: event.target.value })
            }
            required
          />
          <button>Xuất hóa đơn</button>
        </form>
      )}
      {editable && fee.invoice && fee.status !== 'PAID' && (
        <form
          className="inline-form"
          onSubmit={async (event) => {
            event.preventDefault()
            if (
              await onSubmit(
                `fees/${fee.id}/payments`,
                payment,
                'Đã ghi nhận thanh toán.',
              )
            )
              setPayment({ amount_vnd: '', paid_on: today(), reference: '' })
          }}
        >
          <input
            aria-label="Số tiền thanh toán (VND)"
            placeholder="Số tiền (VND)"
            inputMode="numeric"
            pattern={MONEY_PATTERN}
            value={payment.amount_vnd}
            onChange={(event) =>
              setPayment({ ...payment, amount_vnd: event.target.value })
            }
            required
          />
          <input
            aria-label="Ngày thanh toán"
            type="date"
            max={today()}
            value={payment.paid_on}
            onChange={(event) =>
              setPayment({ ...payment, paid_on: event.target.value })
            }
            required
          />
          <input
            aria-label="Số chứng từ"
            placeholder="Số chứng từ / UNC"
            value={payment.reference}
            onChange={(event) =>
              setPayment({ ...payment, reference: event.target.value })
            }
            required
            maxLength={120}
          />
          <button>Ghi nhận thanh toán</button>
        </form>
      )}
    </article>
  )
}

/** Fee line → invoice → payments. Status is computed by the backend. */
export default function FinancePanel({
  deal,
  role,
  onChange,
}: {
  deal: Deal
  role: Role
  onChange: (deal: Deal) => void
}) {
  const [form, setForm] = useState({
    type: 'PREP_PACKAGE',
    amount_vnd: '',
    due_on: today(),
    note: '',
  })
  const [message, setMessage] = useState('')
  const fees = deal.state.fees
  if (!fees) return null
  const editable = role === 'FINANCE'
  const submit = async (path: string, body: object, done: string) => {
    setMessage('')
    try {
      onChange(
        await request<Deal>(`/deals/${deal.id}/${path}`, {
          method: 'POST',
          body: JSON.stringify(body),
        }),
      )
      setMessage(done)
      return true
    } catch (error) {
      setMessage((error as Error).message)
      return false
    }
  }
  const add = async (event: FormEvent) => {
    event.preventDefault()
    if (await submit('fees', form, 'Đã lập khoản phí.'))
      setForm({ ...form, amount_vnd: '', note: '' })
  }
  const opportunities = deal.state.opportunities || []
  return (
    <section className="panel finance-panel" aria-labelledby="finance-title">
      <div className="section-title">
        <div>
          <p className="eyebrow">Tài chính</p>
          <h2 id="finance-title">Phí, hóa đơn và thanh toán</h2>
          <p className="muted">
            Lập khoản phí, xuất hóa đơn rồi ghi nhận từng lần thanh toán. Phí
            thành công chỉ lập sau khi deal đã đóng.
          </p>
        </div>
        <span className="status-pill">
          Ký: {deal.state.signing ? 'đã ký' : 'chưa'} · Đóng:{' '}
          {deal.state.closing?.status === 'CLOSED' ? 'đã đóng' : 'chưa'}
        </span>
      </div>
      {editable && (
        <form className="finding-form" onSubmit={add}>
          <label>
            Loại phí
            <select
              value={form.type}
              onChange={(event) =>
                setForm({ ...form, type: event.target.value })
              }
            >
              {Object.entries(FEE_LABELS).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>
          <label>
            Số tiền (VND)
            <input
              inputMode="numeric"
              pattern={MONEY_PATTERN}
              value={form.amount_vnd}
              onChange={(event) =>
                setForm({ ...form, amount_vnd: event.target.value })
              }
              required
              placeholder="150000000"
            />
            {form.amount_vnd && <small>{formatVnd(form.amount_vnd)}</small>}
          </label>
          <label>
            Hạn thanh toán
            <input
              type="date"
              value={form.due_on}
              onChange={(event) =>
                setForm({ ...form, due_on: event.target.value })
              }
              required
            />
          </label>
          <label className="wide">
            Ghi chú
            <input
              value={form.note}
              onChange={(event) =>
                setForm({ ...form, note: event.target.value })
              }
              maxLength={500}
            />
          </label>
          <button>Lập khoản phí</button>
        </form>
      )}
      {message && (
        <p className="notice" role="status">
          {message}
        </p>
      )}
      {fees.length === 0 ? (
        <p className="muted">Chưa có khoản phí.</p>
      ) : (
        <div className="finding-list">
          {fees.map((fee) => (
            <FeeRow
              key={fee.id}
              fee={fee}
              editable={editable}
              onSubmit={submit}
            />
          ))}
        </div>
      )}
      {opportunities.length > 0 && (
        <>
          <h3>Cơ hội sau giao dịch</h3>
          <p className="muted">
            Build to Buy là cơ hội kinh doanh, chưa phải doanh thu.
          </p>
          <ul className="grant-files">
            {opportunities.map((item, index) => (
              <li key={index}>{item.note}</li>
            ))}
          </ul>
        </>
      )}
      <ClosingEvidence deal={deal} />
    </section>
  )
}
