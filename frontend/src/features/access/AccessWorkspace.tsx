import { useEffect, useState } from 'react'
import { request } from '../../api/workspace'
import AccessControlPanel from '../deals/AccessControlPanel'

type Deal = { id: string; title: string }

export default function AccessWorkspace({ role, initialDealId }: { role?: string; initialDealId?: string }) {
  const [deals, setDeals] = useState<Deal[]>([])
  const [dealId, setDealId] = useState(initialDealId || '')
  const [error, setError] = useState('')
  useEffect(() => { request<Deal[]>('/deals').then((rows) => { setDeals(rows); setDealId((value) => value || rows[0]?.id || '') }).catch((reason) => setError(reason.message)) }, [])
  return <section className="access-workspace">
      <div className="page-heading"><div><p className="eyebrow">DEAL DISCLOSURE</p><h1>Yêu cầu và phê duyệt disclosure</h1><p className="muted">Nghiệp vụ mở L1/L2/L3 theo buyer, deal, mục đích, scope và thời hạn. Quyền tài khoản được xác định từ role đăng nhập.</p></div></div>
    <label className="panel deal-picker">Chọn deal<select value={dealId} onChange={(event) => setDealId(event.target.value)}>{deals.map((deal) => <option value={deal.id} key={deal.id}>{deal.title}</option>)}</select></label>
    {error && <p className="error-box">{error}</p>}
    {dealId ? <AccessControlPanel dealId={dealId} role={role} /> : <p className="empty panel">Chưa có deal để quản lý quyền truy cập.</p>}
  </section>
}
