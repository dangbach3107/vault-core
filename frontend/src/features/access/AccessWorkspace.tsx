import { useEffect, useState } from 'react'
import { request } from '../../api/workspace'
import type { Role } from '../auth/roles'
import AccessControlPanel from '../deals/AccessControlPanel'
import type { Deal } from '../deals/types'
import '../deals/deals.css'

export default function AccessWorkspace({
  role,
  initialDealId,
}: {
  role: Role
  initialDealId?: string
}) {
  const [deals, setDeals] = useState<Deal[]>([])
  const [dealId, setDealId] = useState(initialDealId || '')
  const [error, setError] = useState('')
  useEffect(() => {
    request<Deal[]>('/deals')
      .then((rows) => {
        setDeals(rows)
        setDealId((value) => value || rows[0]?.id || '')
      })
      .catch((reason) => setError(reason.message))
  }, [])
  const deal = deals.find((row) => row.id === dealId)
  const replace = (updated: Deal) =>
    setDeals((rows) =>
      rows.map((row) => (row.id === updated.id ? updated : row)),
    )
  return (
    <section className="access-workspace">
      <div className="page-heading">
        <div>
          <p className="eyebrow">Quyền truy cập</p>
          <h2>Yêu cầu và phê duyệt truy cập</h2>
          <p className="muted">
            Mở Lớp 1/2/3 và tài liệu theo người, deal, mục đích, file, phiên bản
            và thời hạn.
          </p>
        </div>
      </div>
      <label className="panel deal-picker">
        Chọn deal
        <select
          value={dealId}
          onChange={(event) => setDealId(event.target.value)}
        >
          {deals.map((row) => (
            <option value={row.id} key={row.id}>
              {row.title}
            </option>
          ))}
        </select>
      </label>
      {error && <p className="error-box">{error}</p>}
      {deal ? (
        <>
          <AccessControlPanel deal={deal} role={role} onChange={replace} />
          <p>
            <a href={`#/deals/${deal.id}`}>Mở toàn bộ deal →</a>
          </p>
        </>
      ) : (
        <p className="empty panel">Chưa có deal để quản lý quyền truy cập.</p>
      )}
    </section>
  )
}
