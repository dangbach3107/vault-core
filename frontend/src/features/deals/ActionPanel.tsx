import { FormEvent, useState } from 'react'
import { request } from '../../api/workspace'
import { ROLE_META, type Role } from '../auth/roles'
import { ActionFormFields } from './ActionForms'
import {
  FORM_ACTIONS,
  formPayload,
  initialFields,
  type Fields,
} from './formPayload'
import { formatDateTime, type Catalog, type Deal } from './types'
import { useSellerFiles } from '../rooms/useSellerFiles'

// Files cited on these steps become the closing evidence Finance can read.
const EVIDENCE_ACTIONS = ['legalClosingChecklist', 'spaSigned', 'dealClosed']

type Props = {
  deal: Deal
  catalog: Catalog
  role: Role
  onChange: (deal: Deal) => void
}

/** Every gated step, who owns it, and the evidence recorded when it was done. */
export default function ActionPanel({ deal, catalog, role, onChange }: Props) {
  const [open, setOpen] = useState('')
  const [note, setNote] = useState('')
  const [chosen, setChosen] = useState<string[]>([])
  const [fields, setFields] = useState<Fields>({})
  const [busy, setBusy] = useState(false)
  const [message, setMessage] = useState('')
  const steps = deal.state.steps
  const labels = Object.fromEntries(
    catalog.actions.map((item) => [item.key, item.label]),
  )
  const available = (key: string) =>
    !steps[key] &&
    (catalog.actions.find((item) => item.key === key)?.requires || []).every(
      (need) => steps[need],
    )
  const mine = catalog.actions.filter(
    (item) => item.role === role && available(item.key),
  )
  const done = catalog.actions.filter((item) => steps[item.key]).length
  const citesFiles = EVIDENCE_ACTIONS.includes(open)
  const hasForm = FORM_ACTIONS.includes(open)
  const files = useSellerFiles(
    deal.state.seller_profile?.company_id,
    citesFiles || open === 'ndaRecorded',
  )
  const start = (action: string) => {
    setOpen(action)
    setNote('')
    setChosen([])
    setFields(initialFields(action))
    setMessage('')
  }

  const submit = async (event: FormEvent) => {
    event.preventDefault()
    setBusy(true)
    setMessage('')
    try {
      const updated = await request<Deal>(`/deals/${deal.id}/actions/${open}`, {
        method: 'POST',
        body: JSON.stringify({
          note: note.trim(),
          document_ids: citesFiles ? chosen : [],
          ...formPayload(open, fields),
        }),
      })
      onChange(updated)
      setOpen('')
      setNote('')
      setChosen([])
      setMessage('Đã ghi nhận.')
    } catch (error) {
      setMessage((error as Error).message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <section
      className="panel deal-actions"
      aria-labelledby="deal-actions-title"
    >
      <div className="section-title">
        <div>
          <p className="eyebrow">Tiến độ</p>
          <h2 id="deal-actions-title">Các bước của thương vụ</h2>
        </div>
        <span className="status-pill">
          {done}/{catalog.actions.length} bước
        </span>
      </div>
      <div className="deal-mine">
        <h3>Việc của bạn</h3>
        {mine.length === 0 ? (
          <p className="muted">Chưa có bước nào chờ vai trò của bạn.</p>
        ) : (
          mine.map((item) => (
            <div key={item.key} className="deal-mine-item">
              <strong>{item.label}</strong>
              {open === item.key ? (
                <form onSubmit={submit} className="deal-note-form">
                  {hasForm && (
                    <ActionFormFields
                      action={open}
                      fields={fields}
                      onChange={setFields}
                      files={files}
                    />
                  )}
                  <label>
                    {hasForm
                      ? 'Ghi chú thêm (không bắt buộc)'
                      : 'Ghi chú / bằng chứng (số văn bản, ngày, nội dung chính)'}
                    <textarea
                      value={note}
                      onChange={(event) => setNote(event.target.value)}
                      maxLength={1000}
                      rows={3}
                    />
                  </label>
                  {citesFiles && (
                    <fieldset className="file-picker">
                      <legend>
                        File chứng từ (Finance sẽ xem đúng các file và phiên bản
                        này)
                      </legend>
                      {files.length === 0 ? (
                        <p className="muted">
                          Phòng dữ liệu của seller chưa có file.
                        </p>
                      ) : (
                        files.map((file) => (
                          <label key={file.id} className="check-row">
                            <input
                              type="checkbox"
                              checked={chosen.includes(file.id)}
                              onChange={(event) =>
                                setChosen((value) =>
                                  event.target.checked
                                    ? [...value, file.id]
                                    : value.filter((id) => id !== file.id),
                                )
                              }
                            />
                            {file.title} · phiên bản {file.version}
                            <span className="muted"> · {file.room}</span>
                          </label>
                        ))
                      )}
                    </fieldset>
                  )}
                  <div className="actions">
                    <button disabled={busy}>
                      {busy ? 'Đang lưu…' : 'Xác nhận đã hoàn tất'}
                    </button>
                    <button
                      type="button"
                      className="secondary"
                      onClick={() => setOpen('')}
                    >
                      Hủy
                    </button>
                  </div>
                </form>
              ) : (
                <button type="button" onClick={() => start(item.key)}>
                  Thực hiện
                </button>
              )}
            </div>
          ))
        )}
        {message && (
          <p className="notice" role="status">
            {message}
          </p>
        )}
      </div>
      <ol className="deal-step-list">
        {catalog.actions.map((item) => {
          const record = deal.state.records?.[item.key]
          const state = steps[item.key]
            ? 'done'
            : available(item.key)
              ? 'ready'
              : 'blocked'
          return (
            <li key={item.key} className={`deal-step ${state}`}>
              <span className="deal-step-mark" aria-hidden="true" />
              <div>
                <strong>{item.label}</strong>
                <span className="muted">
                  {' '}
                  · {ROLE_META[item.role as Role]?.label || item.role}
                </span>
                {state === 'done' && record && (
                  <p className="muted">
                    {record.by} · {formatDateTime(record.at)}
                    {record.note ? ` · ${record.note}` : ''}
                  </p>
                )}
                {state === 'blocked' && (
                  <p className="muted">
                    Chờ:{' '}
                    {item.requires
                      .filter((need) => !steps[need])
                      .map((need) => labels[need])
                      .join('; ')}
                  </p>
                )}
              </div>
              <span className="sr-only">
                {state === 'done'
                  ? 'Đã xong'
                  : state === 'ready'
                    ? 'Sẵn sàng'
                    : 'Chưa đủ điều kiện'}
              </span>
            </li>
          )
        })}
      </ol>
    </section>
  )
}
