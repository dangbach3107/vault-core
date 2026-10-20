import { FormEvent, useCallback, useEffect, useState } from 'react'
import { request, type Company } from '../../api/workspace'
import type { components } from '../../api/generated/schema'
import { getAuthSession } from '../../api/config'
import { useSellerFiles } from '../rooms/useSellerFiles'
import '../deals/deals.css'
import { statusLabels } from './fields'
import {
  REVIEW_STATUS,
  fieldLabel,
  reviewableFacts,
  valueText,
} from './reviewFields'

type Review = components['schemas']['ReviewResponse']

const today = () => new Date().toISOString().slice(0, 10)

/** Send self-declared facts for review with a source and an evidence file; see the outcome. */
export default function FactReviewPanel({
  company,
  onDecided,
}: {
  company: Company
  onDecided?: () => void
}) {
  const role = getAuthSession()?.user.role
  const canRequest = role === 'SELLER' || role === 'VAULT_ADMIN'
  const [reviews, setReviews] = useState<Review[]>([])
  const [open, setOpen] = useState('')
  const [form, setForm] = useState({
    source: '',
    source_date: today(),
    document_id: '',
    note: '',
  })
  const [message, setMessage] = useState('')
  const files = useSellerFiles(company.id, canRequest && Boolean(open))
  const load = useCallback(
    () =>
      request<Review[]>(`/companies/${company.id}/reviews`)
        .then(setReviews)
        .catch((reason: Error) => setMessage(reason.message)),
    [company.id],
  )
  useEffect(() => {
    void load()
  }, [load, company.revision])

  const pending = new Set(
    reviews.filter((row) => row.status === 'PENDING').map((row) => row.field),
  )
  const facts = reviewableFacts(company).filter(
    (item) => item.fact.value != null,
  )

  const submit = async (event: FormEvent) => {
    event.preventDefault()
    setMessage('')
    try {
      await request(`/companies/${company.id}/reviews`, {
        method: 'POST',
        body: JSON.stringify({
          field: open,
          source: form.source.trim(),
          source_date: form.source_date,
          document_id: form.document_id || null,
          note: form.note.trim(),
        }),
      })
      setOpen('')
      setMessage(
        'Đã gửi duyệt. Legal hoặc Admin (không phải người gửi) sẽ quyết định.',
      )
      await load()
      onDecided?.()
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  return (
    <div className="panel fact-review-panel">
      <div className="section-title">
        <div>
          <p className="eyebrow">Xác minh dữ kiện</p>
          <h2>Gửi duyệt và kết quả</h2>
          <p className="muted">
            Nhãn xác minh chỉ được gắn khi người duyệt chấp thuận yêu cầu có
            nguồn và bằng chứng. Người gửi không tự duyệt.
          </p>
        </div>
      </div>
      {message && (
        <p className="notice" role="status">
          {message}
        </p>
      )}
      <table className="fact-review-table">
        <thead>
          <tr>
            <th>Dữ kiện</th>
            <th>Giá trị</th>
            <th>Trạng thái</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {facts.map(({ path, fact }) => (
            <tr key={path}>
              <td>{fieldLabel(path)}</td>
              <td>{valueText(path, fact.value)}</td>
              <td>
                {pending.has(path)
                  ? 'Chờ duyệt'
                  : fact.issue && fact.issue !== 'NONE'
                    ? 'Đang có vấn đề'
                    : statusLabels[fact.verification || 'SELF_DECLARED']}
              </td>
              <td>
                {canRequest &&
                  !pending.has(path) &&
                  (fact.verification || 'SELF_DECLARED') === 'SELF_DECLARED' &&
                  (fact.issue || 'NONE') === 'NONE' && (
                    <button
                      type="button"
                      className="secondary"
                      onClick={() => {
                        setOpen(path)
                        setForm({
                          source: '',
                          source_date: today(),
                          document_id: '',
                          note: '',
                        })
                      }}
                    >
                      Gửi duyệt
                    </button>
                  )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {open && (
        <form className="finding-form" onSubmit={submit}>
          <strong className="wide">Gửi duyệt: {fieldLabel(open)}</strong>
          <label>
            Nguồn *
            <input
              value={form.source}
              onChange={(event) =>
                setForm({ ...form, source: event.target.value })
              }
              required
              maxLength={500}
              placeholder="Ví dụ: Giấy ĐKDN, BCTC kiểm toán 2025"
            />
          </label>
          <label>
            Ngày nguồn *
            <input
              type="date"
              max={today()}
              value={form.source_date}
              onChange={(event) =>
                setForm({ ...form, source_date: event.target.value })
              }
              required
            />
          </label>
          <label>
            File bằng chứng
            <select
              value={form.document_id}
              onChange={(event) =>
                setForm({ ...form, document_id: event.target.value })
              }
            >
              <option value="">Không đính kèm</option>
              {files.map((file) => (
                <option key={file.id} value={file.id}>
                  {file.title} · phiên bản {file.version} · {file.room}
                </option>
              ))}
            </select>
          </label>
          <label className="wide">
            Ghi chú cho người duyệt
            <input
              value={form.note}
              onChange={(event) =>
                setForm({ ...form, note: event.target.value })
              }
              maxLength={1000}
            />
          </label>
          <div className="actions wide">
            <button>Gửi duyệt</button>
            <button
              type="button"
              className="secondary"
              onClick={() => setOpen('')}
            >
              Hủy
            </button>
          </div>
        </form>
      )}
      <h3>Lịch sử duyệt</h3>
      {reviews.length === 0 ? (
        <p className="muted">Chưa có yêu cầu duyệt.</p>
      ) : (
        <ul className="grant-files">
          {reviews.map((row) => (
            <li key={row.id}>
              {fieldLabel(row.field)} · {valueText(row.field, row.value)} ·{' '}
              {REVIEW_STATUS[row.status]}
              {row.decided_by ? ` bởi ${row.decided_by}` : ''}
              {row.reason ? ` · ${row.reason}` : ''} · gửi bởi{' '}
              {row.requested_by}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
