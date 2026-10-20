import { FormEvent, useState } from 'react'
import { request } from '../../api/workspace'
import ActionDialog from '../../components/ActionDialog'
import type { Role } from '../auth/roles'
import { formatDate, formatDateTime, type Deal } from './types'
import { useSellerFiles } from '../rooms/useSellerFiles'

type DialogAction = { kind: 'approve' | 'reject' | 'revoke'; id: string }

const LEVEL_LABELS: Record<string, string> = {
  L1: 'Lớp 1 · Teaser',
  L2: 'Lớp 2 · Định danh',
  L3: 'Lớp 3 · Tài liệu hạn chế',
  CLOSING: 'Tài liệu closing',
}
const BASIS_LABELS: Record<string, string> = {
  SELLER_L1_APPROVAL: 'Seller đã duyệt Teaser',
  NDA: 'NDA',
  INDICATIVE_LOI: 'LOI sơ bộ',
  LOI: 'Đề nghị chính thức',
}
const STATUS_LABELS: Record<string, string> = {
  PENDING: 'Chờ duyệt',
  APPROVED: 'Đã duyệt',
  REJECTED: 'Từ chối',
  ACTIVE: 'Còn hiệu lực',
  EXPIRED: 'Hết hạn',
  REVOKED: 'Đã thu hồi',
}

/** The record that allows a level (NDA, LOI…); the grant may not outlive it. */
function basisFor(deal: Deal, level?: string) {
  const { nda, indicative_loi, definitive_offer } = deal.state
  if (level === 'L1')
    return { text: 'Căn cứ: Seller đã duyệt Teaser.', until: '' }
  const source =
    level === 'L2'
      ? { name: 'NDA', ref: nda?.reference, until: nda?.expires_on }
      : level === 'L3'
        ? {
            name: 'LOI sơ bộ',
            ref: indicative_loi?.reference,
            until: indicative_loi?.valid_until,
          }
        : {
            name: 'Đề nghị chính thức',
            ref: definitive_offer?.reference,
            until: definitive_offer?.valid_until,
          }
  if (!source.until)
    return {
      text: `Chưa có ${source.name} được ghi nhận theo form; hệ thống sẽ từ chối cấp quyền này.`,
      until: '',
    }
  return {
    text: `Căn cứ: ${source.name} ${source.ref || ''}, hiệu lực đến ${formatDate(source.until)}. Ngày hết hạn quyền không được sau ngày này.`,
    until: source.until,
  }
}

export default function AccessControlPanel({
  deal,
  role,
  onChange,
}: {
  deal: Deal
  role: Role
  onChange: (deal: Deal) => void
}) {
  const [level, setLevel] = useState('L2')
  const [purpose, setPurpose] = useState('')
  const [message, setMessage] = useState('')
  const [dialog, setDialog] = useState<DialogAction | null>(null)
  const [reason, setReason] = useState('')
  const [expires, setExpires] = useState('')
  const [canDownload, setCanDownload] = useState(false)
  const [chosen, setChosen] = useState<string[]>([])
  const [saving, setSaving] = useState(false)
  const canDecide = role === 'SELLER' || role === 'LEGAL'
  const canRevoke = canDecide || role === 'VAULT_ADMIN'
  const files = useSellerFiles(deal.state.seller_profile?.company_id, canDecide)
  const requests = deal.state.access_requests || []
  const grants = deal.state.access_grants || []
  const events = deal.state.access_events || []
  const dialogLevel = requests.find(
    (item) => item.id === dialog?.id,
  )?.requested_level
  const basis = basisFor(deal, dialogLevel)

  const submit = async (event: FormEvent) => {
    event.preventDefault()
    setMessage('Đang gửi yêu cầu…')
    try {
      onChange(
        await request<Deal>(`/deals/${deal.id}/access-requests`, {
          method: 'POST',
          body: JSON.stringify({
            requested_level: level,
            purpose,
            document_ids: [],
          }),
        }),
      )
      setPurpose('')
      setMessage('Đã gửi yêu cầu cho Seller/Legal.')
    } catch (error) {
      setMessage((error as Error).message)
    }
  }
  const openDialog = (action: DialogAction) => {
    setReason('')
    setExpires('')
    setCanDownload(false)
    setChosen(
      requests.find((item) => item.id === action.id)?.document_ids || [],
    )
    setDialog(action)
  }
  const submitDialog = async () => {
    if (!dialog || !reason.trim()) return
    setSaving(true)
    try {
      if (dialog.kind === 'revoke') {
        onChange(
          await request<Deal>(
            `/deals/${deal.id}/access-grants/${dialog.id}/revoke`,
            {
              method: 'POST',
              body: JSON.stringify({ reason: reason.trim() }),
            },
          ),
        )
        setMessage('Đã thu hồi quyền.')
      } else {
        const approved = dialog.kind === 'approve'
        onChange(
          await request<Deal>(
            `/deals/${deal.id}/access-requests/${dialog.id}/decision`,
            {
              method: 'POST',
              body: JSON.stringify({
                approved,
                reason: reason.trim(),
                expires_at: approved && expires ? `${expires}T23:59:59Z` : null,
                ...(approved
                  ? {
                      can_download: canDownload,
                      document_ids: chosen,
                    }
                  : {}),
              }),
            },
          ),
        )
        setMessage(
          approved ? 'Đã cấp quyền có thời hạn.' : 'Đã từ chối yêu cầu.',
        )
      }
      setDialog(null)
    } catch (error) {
      setMessage((error as Error).message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <section
      className="panel access-control-panel"
      aria-labelledby="access-title"
    >
      <div className="section-title">
        <div>
          <p className="eyebrow">Quyền truy cập</p>
          <h2 id="access-title">Yêu cầu và quyền đã cấp</h2>
          <p className="muted">
            Quyền gắn với người, deal, mục đích, lớp, từng file và phiên bản, có
            hạn và thu hồi được. NDA hay LOI chỉ là căn cứ, không tự mở quyền.
          </p>
        </div>
        <span className="status-pill">
          {grants.filter((grant) => grant.status === 'ACTIVE').length} quyền còn
          hiệu lực
        </span>
      </div>
      {role === 'BUYER' && (
        <form className="access-request-form" onSubmit={submit}>
          <label>
            Lớp cần truy cập
            <select
              value={level}
              onChange={(event) => setLevel(event.target.value)}
            >
              {Object.entries(LEVEL_LABELS).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>
          <label>
            Mục đích sử dụng
            <input
              value={purpose}
              onChange={(event) => setPurpose(event.target.value)}
              minLength={3}
              maxLength={500}
              required
              placeholder="Ví dụ: đánh giá mức phù hợp và thẩm định tài chính"
            />
          </label>
          <button>Gửi yêu cầu</button>
        </form>
      )}
      {message && (
        <p className="notice" role="status">
          {message}
        </p>
      )}
      <div className="access-columns">
        <div>
          <h3>Yêu cầu</h3>
          {requests.length === 0 ? (
            <p className="muted">Chưa có yêu cầu.</p>
          ) : (
            requests.map((item) => (
              <article className="access-item" key={item.id}>
                <strong>
                  {item.requester} ·{' '}
                  {LEVEL_LABELS[item.requested_level] || item.requested_level}
                </strong>
                <p>{item.purpose}</p>
                <small>
                  Gửi {formatDateTime(item.requested_at)}
                  {item.reason ? ` · Lý do: ${item.reason}` : ''}
                </small>
                <span className={`status-pill ${item.status.toLowerCase()}`}>
                  {STATUS_LABELS[item.status]}
                </span>
                {canDecide && item.status === 'PENDING' && (
                  <div className="actions">
                    <button
                      onClick={() =>
                        openDialog({ kind: 'approve', id: item.id })
                      }
                    >
                      Duyệt có thời hạn
                    </button>
                    <button
                      className="secondary"
                      onClick={() =>
                        openDialog({ kind: 'reject', id: item.id })
                      }
                    >
                      Từ chối
                    </button>
                  </div>
                )}
              </article>
            ))
          )}
        </div>
        <div>
          <h3>Quyền đã cấp</h3>
          {grants.length === 0 ? (
            <p className="muted">Chưa có quyền.</p>
          ) : (
            grants.map((grant) => (
              <article className="access-item" key={grant.id}>
                <strong>
                  {grant.user} ·{' '}
                  {LEVEL_LABELS[grant.access_level] || grant.access_level}
                </strong>
                <p>{grant.purpose}</p>
                <small>
                  Căn cứ: {BASIS_LABELS[grant.basis || ''] || 'Chưa ghi'}
                  {grant.basis_ref ? ` (${grant.basis_ref})` : ''} · Duyệt bởi{' '}
                  {grant.approved_by} · Hết hạn {formatDate(grant.expires_at)} ·{' '}
                  {grant.can_download ? 'Được tải xuống' : 'Chỉ xem'}
                </small>
                {(grant.documents || []).length > 0 && (
                  <ul className="grant-files">
                    {grant.documents!.map((file) => (
                      <li key={file.document_id}>
                        {file.title} · phiên bản {file.version_number}
                        {file.latest_version > file.version_number &&
                          ` (đã có phiên bản ${file.latest_version}, cần duyệt lại)`}
                      </li>
                    ))}
                  </ul>
                )}
                {grant.revoke_reason && (
                  <small>Lý do thu hồi: {grant.revoke_reason}</small>
                )}
                <span className={`status-pill ${grant.status.toLowerCase()}`}>
                  {STATUS_LABELS[grant.status]}
                </span>
                {grant.status === 'ACTIVE' && canRevoke && (
                  <button
                    className="danger-button"
                    onClick={() => openDialog({ kind: 'revoke', id: grant.id })}
                  >
                    Thu hồi
                  </button>
                )}
              </article>
            ))
          )}
        </div>
      </div>
      {events.length > 0 && (
        <details className="access-log">
          <summary>Nhật ký truy cập ({events.length})</summary>
          <ul>
            {events.map((item, index) => (
              <li key={index}>
                {formatDateTime(item.at)} · {item.actor} · {item.type}
                {item.version_number
                  ? ` · phiên bản ${item.version_number}`
                  : ''}
                {item.reason ? ` · ${item.reason}` : ''}
              </li>
            ))}
          </ul>
        </details>
      )}
      {dialog && (
        <ActionDialog
          title={
            dialog.kind === 'approve'
              ? 'Duyệt quyền truy cập'
              : dialog.kind === 'reject'
                ? 'Từ chối yêu cầu'
                : 'Thu hồi quyền truy cập'
          }
          description={
            dialog.kind === 'approve'
              ? 'Chọn file, thời hạn và quyền tải. Quyền chỉ áp dụng cho phiên bản hiện tại của từng file.'
              : 'Lý do sẽ được lưu trong nhật ký truy cập.'
          }
          confirmLabel={
            dialog.kind === 'approve'
              ? 'Duyệt quyền'
              : dialog.kind === 'reject'
                ? 'Từ chối'
                : 'Thu hồi quyền'
          }
          danger={dialog.kind !== 'approve'}
          busy={saving}
          onCancel={() => setDialog(null)}
          onSubmit={submitDialog}
        >
          <label>
            Lý do / phạm vi
            <textarea
              value={reason}
              onChange={(event) => setReason(event.target.value)}
              required
              minLength={3}
              maxLength={500}
              rows={3}
            />
          </label>
          {dialog.kind === 'approve' && (
            <>
              <p className="basis-box">{basis.text}</p>
              <label>
                Ngày hết hạn
                <input
                  type="date"
                  value={expires}
                  max={basis.until || undefined}
                  onChange={(event) => setExpires(event.target.value)}
                  required
                />
              </label>
              <fieldset className="file-picker">
                <legend>File được mở</legend>
                {files.length === 0 ? (
                  <p className="muted">
                    Phòng dữ liệu của seller chưa có file. Có thể duyệt chỉ lớp
                    hồ sơ.
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
              <label className="check-row">
                <input
                  type="checkbox"
                  checked={canDownload}
                  onChange={(event) => setCanDownload(event.target.checked)}
                />
                Cho phép tải xuống (mặc định chỉ xem)
              </label>
            </>
          )}
        </ActionDialog>
      )}
    </section>
  )
}
