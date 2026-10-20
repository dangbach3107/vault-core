import { useCallback, useEffect, useState } from 'react'
import { request } from '../../api/workspace'
import ActionDialog from '../../components/ActionDialog'
import '../deals/deals.css'
import {
  REVIEW_STATUS,
  fieldLabel,
  valueText,
  type Review,
} from '../profiles/reviewFields'

type Filter = Review['status']
type Decision = { review: Review; approved: boolean }

/** Legal/Admin queue: decide fact reviews other people sent, after checking the evidence. */
export default function ReviewQueue({ username }: { username: string }) {
  const [filter, setFilter] = useState<Filter>('PENDING')
  const [rows, setRows] = useState<Review[] | null>(null)
  const [message, setMessage] = useState('')
  const [decision, setDecision] = useState<Decision | null>(null)
  const [verification, setVerification] = useState('DOCUMENT_VERIFIED')
  const [reason, setReason] = useState('')
  const [saving, setSaving] = useState(false)
  const load = useCallback(
    () =>
      request<Review[]>(`/reviews?status=${filter}`)
        .then(setRows)
        .catch((reason: Error) => setMessage(reason.message)),
    [filter],
  )
  useEffect(() => {
    void load()
  }, [load])

  const submit = async () => {
    if (!decision || reason.trim().length < 3) return
    setSaving(true)
    try {
      await request(`/reviews/${decision.review.id}/decision`, {
        method: 'POST',
        body: JSON.stringify({
          approved: decision.approved,
          verification: decision.approved ? verification : null,
          reason: reason.trim(),
        }),
      })
      setMessage(
        decision.approved
          ? 'Đã chấp thuận và gắn nhãn xác minh.'
          : 'Đã từ chối yêu cầu.',
      )
      setDecision(null)
      await load()
    } catch (error) {
      setMessage((error as Error).message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <section className="review-queue">
      <div className="page-heading">
        <div>
          <p className="eyebrow">Xác minh dữ kiện</p>
          <h2>Duyệt dữ kiện</h2>
          <p className="muted">
            Mở file bằng chứng, đối chiếu với giá trị được gửi, rồi chấp thuận
            hoặc từ chối kèm lý do. Bạn không duyệt được yêu cầu do chính mình
            gửi.
          </p>
        </div>
      </div>
      <div className="tabs" aria-label="Lọc theo trạng thái">
        {(Object.keys(REVIEW_STATUS) as Filter[]).map((status) => (
          <button
            key={status}
            type="button"
            aria-pressed={filter === status}
            className={filter === status ? '' : 'secondary'}
            onClick={() => setFilter(status)}
          >
            {REVIEW_STATUS[status]}
          </button>
        ))}
      </div>
      {message && (
        <p className="notice" role="status">
          {message}
        </p>
      )}
      {rows === null ? (
        <p className="muted">Đang tải…</p>
      ) : rows.length === 0 ? (
        <p className="empty panel">Không có yêu cầu nào ở trạng thái này.</p>
      ) : (
        <div className="finding-list">
          {rows.map((row) => (
            <article className="access-item" key={row.id}>
              <strong>
                {row.company_alias} · {row.company_name} ·{' '}
                {fieldLabel(row.field)}
              </strong>
              <p>
                Giá trị gửi duyệt: <b>{valueText(row.field, row.value)}</b>
              </p>
              <small>
                Nguồn: {row.source} ({row.source_date}) · gửi bởi{' '}
                {row.requested_by}
                {row.note ? ` · ${row.note}` : ''}
              </small>
              {row.document ? (
                <a
                  href={`#/rooms/${row.document.room_id}/documents/${row.document.document_id}`}
                >
                  Mở bằng chứng: {row.document.title} · phiên bản{' '}
                  {row.document.version_number}
                </a>
              ) : (
                <small>Không đính kèm file bằng chứng.</small>
              )}
              <span className={`status-pill ${row.status.toLowerCase()}`}>
                {REVIEW_STATUS[row.status]}
                {row.decided_by ? ` · ${row.decided_by}` : ''}
              </span>
              {row.reason && <small>Lý do: {row.reason}</small>}
              {row.status === 'PENDING' &&
                (row.requested_by === username ? (
                  <small>Bạn đã gửi yêu cầu này; cần người khác duyệt.</small>
                ) : (
                  <div className="actions">
                    <button
                      onClick={() => {
                        setReason('')
                        setVerification('DOCUMENT_VERIFIED')
                        setDecision({ review: row, approved: true })
                      }}
                    >
                      Chấp thuận
                    </button>
                    <button
                      className="secondary"
                      onClick={() => {
                        setReason('')
                        setDecision({ review: row, approved: false })
                      }}
                    >
                      Từ chối
                    </button>
                  </div>
                ))}
            </article>
          ))}
        </div>
      )}
      {decision && (
        <ActionDialog
          title={
            decision.approved ? 'Chấp thuận dữ kiện' : 'Từ chối yêu cầu duyệt'
          }
          description={`${fieldLabel(decision.review.field)}: ${valueText(decision.review.field, decision.review.value)}`}
          confirmLabel={decision.approved ? 'Chấp thuận' : 'Từ chối'}
          danger={!decision.approved}
          busy={saving}
          onCancel={() => setDecision(null)}
          onSubmit={submit}
        >
          {decision.approved && (
            <label>
              Loại xác minh
              <select
                value={verification}
                onChange={(event) => setVerification(event.target.value)}
              >
                <option value="DOCUMENT_VERIFIED">Đã đối chiếu chứng từ</option>
                <option value="THIRD_PARTY_CONFIRMED">
                  Bên thứ ba xác nhận
                </option>
              </select>
            </label>
          )}
          <label>
            Lý do / ghi chú đối chiếu
            <textarea
              value={reason}
              onChange={(event) => setReason(event.target.value)}
              required
              minLength={3}
              maxLength={500}
              rows={3}
            />
          </label>
        </ActionDialog>
      )}
    </section>
  )
}
