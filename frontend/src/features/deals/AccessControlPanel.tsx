import { FormEvent, useCallback, useEffect, useState } from 'react'
import { request } from '../../api/workspace'
import ActionDialog from '../../components/ActionDialog'

type AccessRequest = { id: string; requester: string; requested_level: string; purpose: string; status: string; requested_at: string }
type AccessGrant = { id: string; user: string; access_level: string; purpose: string; approved_by: string; expires_at: string; revoked_at: string | null }
type DealAccess = { state: { access_requests?: AccessRequest[]; access_grants?: AccessGrant[] } }
type DialogAction = { kind: 'approve' | 'reject' | 'revoke'; id: string }

export default function AccessControlPanel({ dealId, role }: { dealId: string; role?: string }) {
  const [data, setData] = useState<DealAccess | null>(null)
  const [level, setLevel] = useState('L1')
  const [purpose, setPurpose] = useState('')
  const [message, setMessage] = useState('')
  const [dialog, setDialog] = useState<DialogAction | null>(null)
  const [reason, setReason] = useState('')
  const [expires, setExpires] = useState('')
  const [saving, setSaving] = useState(false)
  const load = useCallback(() => request<DealAccess>(`/deals/${dealId}`).then(setData).catch((error) => setMessage(error.message)), [dealId])
  useEffect(() => { void load() }, [load])
  const submit = async (event: FormEvent) => {
    event.preventDefault(); setMessage('Đang gửi yêu cầu…')
    try { await request(`/deals/${dealId}/access-requests`, { method: 'POST', body: JSON.stringify({ requested_level: level, purpose, document_ids: [] }) }); setPurpose(''); setMessage('Đã gửi yêu cầu cho Seller/Legal.'); await load() }
    catch (error) { setMessage((error as Error).message) }
  }
  const openDialog = (action: DialogAction) => { setReason(''); setExpires(''); setDialog(action) }
  const submitDialog = async () => {
    if (!dialog || !reason.trim()) return
    setSaving(true)
    try {
      if (dialog.kind === 'revoke') {
        await request(`/deals/${dealId}/access-grants/${dialog.id}/revoke`, { method: 'POST', body: JSON.stringify({ reason: reason.trim() }) })
        setMessage('Đã thu hồi quyền.')
      } else {
        const approved = dialog.kind === 'approve'
        await request(`/deals/${dealId}/access-requests/${dialog.id}/decision`, { method: 'POST', body: JSON.stringify({ approved, reason: reason.trim(), expires_at: approved && expires ? `${expires}T23:59:59Z` : null }) })
        setMessage(approved ? 'Đã cấp quyền có thời hạn.' : 'Đã từ chối yêu cầu.')
      }
      setDialog(null); await load()
    } catch (error) { setMessage((error as Error).message) }
    finally { setSaving(false) }
  }
  const requests = data?.state.access_requests || []
  const grants = data?.state.access_grants || []
  const canDecide = role === 'SELLER' || role === 'LEGAL'
  const canRevoke = canDecide || role === 'VAULT_ADMIN'
  return <section className="panel access-control-panel">
    <div className="section-title"><div><p className="eyebrow">Controlled access</p><h2>Yêu cầu & quyền truy cập dữ liệu</h2><p className="muted">Quyền theo người, deal, mục đích, tầng dữ liệu, scope và thời hạn.</p></div><span className="status-pill">{grants.filter((grant) => !grant.revoked_at).length} quyền active</span></div>
    {role === 'BUYER' && <form className="access-request-form" onSubmit={submit}><label>Tầng cần truy cập<select value={level} onChange={(event) => setLevel(event.target.value)}><option>L1</option><option>L2</option><option>L3</option><option>CLOSING</option></select></label><label>Mục đích sử dụng<input value={purpose} onChange={(event) => setPurpose(event.target.value)} minLength={3} maxLength={500} required placeholder="Ví dụ: đánh giá strategic fit và financial DD" /></label><button>Gửi access request</button></form>}
    {message && <p className="notice" role="status">{message}</p>}
    <div className="access-columns"><div><h3>Yêu cầu</h3>{requests.length === 0 ? <p className="muted">Chưa có yêu cầu.</p> : requests.map((item) => <article className="access-item" key={item.id}><strong>{item.requester} · {item.requested_level}</strong><p>{item.purpose}</p><span className="status-pill">{item.status}</span>{canDecide && item.status === 'PENDING' && <div className="actions"><button onClick={() => openDialog({ kind: 'approve', id: item.id })}>Duyệt có thời hạn</button><button className="secondary" onClick={() => openDialog({ kind: 'reject', id: item.id })}>Từ chối</button></div>}</article>)}</div>
      <div><h3>Quyền đã cấp</h3>{grants.length === 0 ? <p className="muted">Chưa có quyền.</p> : grants.map((grant) => <article className="access-item" key={grant.id}><strong>{grant.user} · {grant.access_level}</strong><p>{grant.purpose}</p><small>Duyệt bởi {grant.approved_by} · hết hạn {new Date(grant.expires_at).toLocaleDateString('vi-VN')}</small>{grant.revoked_at ? <span className="status-pill">REVOKED</span> : canRevoke && <button className="danger-button" onClick={() => openDialog({ kind: 'revoke', id: grant.id })}>Thu hồi</button>}</article>)}</div></div>
    {dialog && <ActionDialog title={dialog.kind === 'approve' ? 'Duyệt quyền truy cập' : dialog.kind === 'reject' ? 'Từ chối yêu cầu' : 'Thu hồi quyền truy cập'} description={dialog.kind === 'approve' ? 'Nhập phạm vi/lý do và thời hạn cụ thể cho quyền này.' : 'Lý do sẽ được lưu trong lịch sử kiểm soát truy cập.'} confirmLabel={dialog.kind === 'approve' ? 'Duyệt quyền' : dialog.kind === 'reject' ? 'Từ chối' : 'Thu hồi quyền'} danger={dialog.kind !== 'approve'} busy={saving} onCancel={() => setDialog(null)} onSubmit={submitDialog}>
      <label>Lý do / phạm vi<textarea value={reason} onChange={(event) => setReason(event.target.value)} required minLength={3} maxLength={500} rows={3} /></label>
      {dialog.kind === 'approve' && <label>Ngày hết hạn<input type="date" value={expires} onChange={(event) => setExpires(event.target.value)} required /></label>}
    </ActionDialog>}
  </section>
}
