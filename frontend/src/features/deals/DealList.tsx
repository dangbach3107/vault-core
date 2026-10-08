import { FormEvent, useEffect, useMemo, useState } from 'react'
import { request } from '../../api/workspace'

type DealRecord = {
  id: string
  title: string
  revision: number
  updated_at: string
  state: { steps?: Record<string, boolean> }
}

export default function DealList({ role }: { role?: string }) {
  const [deals, setDeals] = useState<DealRecord[]>([])
  const [title, setTitle] = useState('')
  const [status, setStatus] = useState('Đang tải danh sách deal…')
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    request<DealRecord[]>('/deals')
      .then((records) => {
        setDeals(records)
        setStatus(records.length ? '' : 'Chưa có deal nào. Hãy tạo lead/deal đầu tiên.')
      })
      .catch((reason) => setStatus(reason instanceof Error ? reason.message : 'Không tải được danh sách deal.'))
  }, [])

  const completed = useMemo(() => deals.reduce<Record<string, number>>((result, deal) => {
    const values = Object.values(deal.state.steps || {})
    result[deal.id] = values.length ? Math.round((values.filter(Boolean).length / values.length) * 100) : 0
    return result
  }, {}), [deals])

  const create = async (event: FormEvent) => {
    event.preventDefault()
    if (!title.trim()) return
    setBusy(true)
    try {
      const record = await request<DealRecord>('/deals', {
        method: 'POST', body: JSON.stringify({ title: title.trim() }),
      })
      location.hash = `/disclosures?deal=${record.id}`
    } catch (reason) {
      setStatus(reason instanceof Error ? reason.message : 'Không tạo được deal.')
    } finally { setBusy(false) }
  }

  return <section className="deal-hub" aria-labelledby="deal-hub-title">
    <div className="hero-panel deal-hub-hero">
      <div><p className="eyebrow">Deal workspace</p><h1 id="deal-hub-title">Lead & thương vụ</h1>
        <p className="hero-sub">Quản lý buyer request, seller profile, approvals, VDR, DD, offer, closing, phí và bàn giao theo từng deal.</p></div>
      <span className="status-pill ready">{deals.length} deal</span>
    </div>
    {role === 'VAULT_ADMIN' && <form className="panel deal-create-form" onSubmit={create}>
      <div><p className="eyebrow">Lead mới</p><h2>Tạo hồ sơ deal</h2></div>
      <label>Tên cơ hội / thương vụ<input value={title} onChange={(event) => setTitle(event.target.value)} maxLength={200} placeholder="Buyer Nhật × Seller SaaS Việt Nam" required /></label>
      <button disabled={busy}>{busy ? 'Đang tạo…' : 'Tạo deal'}</button>
    </form>}
    {status && <p className="notice" role="status">{status}</p>}
    <div className="deal-card-grid">{deals.map((deal) => <a className="panel deal-card" href={`#/disclosures?deal=${deal.id}`} key={deal.id}>
      <div className="deal-card-top"><span className="eyebrow">Deal · rev {deal.revision}</span><span className="status-pill">{completed[deal.id]}%</span></div>
      <h2>{deal.title}</h2><div className="progress-track"><span style={{ width: `${completed[deal.id]}%` }} /></div>
      <p className="muted">Cập nhật {new Date(deal.updated_at).toLocaleString('vi-VN')}</p><strong>Mở chức năng deal →</strong>
    </a>)}</div>
  </section>
}
