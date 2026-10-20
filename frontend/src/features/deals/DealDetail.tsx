import { useCallback, useEffect, useState, type ReactNode } from 'react'
import { request } from '../../api/workspace'
import type { AuthUser } from '../../api/config'
import type { Role } from '../auth/roles'
import AccessControlPanel from './AccessControlPanel'
import ActionPanel from './ActionPanel'
import BuyerPanel from './BuyerPanel'
import DealRecords from './DealRecords'
import FinancePanel from './FinancePanel'
import TechDdPanel from './TechDdPanel'
import WorkflowPanel from './WorkflowPanel'
import { formatDateTime, type Catalog, type Deal } from './types'
import './deals.css'

type PanelKey =
  'records' | 'buyer' | 'access' | 'tech' | 'finance' | 'actions' | 'workflow'

// Each role opens the deal on its own work first.
const PANELS: Record<Role, PanelKey[]> = {
  BUYER: ['buyer', 'access', 'actions', 'records', 'workflow'],
  SELLER: ['access', 'actions', 'records', 'tech', 'workflow'],
  VAULT_ADMIN: ['actions', 'records', 'access', 'tech', 'finance', 'workflow'],
  LEGAL: ['access', 'actions', 'records', 'tech', 'workflow'],
  TECH_DD: ['tech', 'actions', 'workflow'],
  FINANCE: ['finance', 'actions', 'workflow'],
}

function closingLabel(deal: Deal) {
  if (deal.state.closing?.status === 'CLOSED') return 'Đã đóng giao dịch'
  if (deal.state.signing) return 'Đã ký, chưa đóng'
  return 'Chưa ký'
}

export default function DealDetail({
  id,
  user,
}: {
  id: string
  user: AuthUser
}) {
  const [deal, setDeal] = useState<Deal | null>(null)
  const [catalog, setCatalog] = useState<Catalog | null>(null)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const load = useCallback(() => {
    Promise.all([
      request<Deal>(`/deals/${id}`),
      request<Catalog>('/deals/catalog'),
    ])
      .then(([record, meta]) => {
        setDeal(record)
        setCatalog(meta)
      })
      .catch((reason: Error) => setError(reason.message))
  }, [id])
  useEffect(load, [load])

  const adminCall = async (
    path: 'reset' | 'complete-sample',
    confirmText: string,
  ) => {
    if (!window.confirm(confirmText)) return
    setBusy(true)
    try {
      setDeal(await request<Deal>(`/deals/${id}/${path}`, { method: 'POST' }))
    } catch (reason) {
      setError((reason as Error).message)
    } finally {
      setBusy(false)
    }
  }

  if (error && !deal) return <p className="error-box">{error}</p>
  if (!deal || !catalog) return <p className="muted">Đang tải deal…</p>
  const role = user.role
  const props = { deal, role, onChange: setDeal }
  const panels: Record<PanelKey, ReactNode> = {
    buyer: <BuyerPanel deal={deal} />,
    records: <DealRecords deal={deal} />,
    access: <AccessControlPanel {...props} />,
    tech: <TechDdPanel {...props} />,
    finance: <FinancePanel {...props} />,
    actions: <ActionPanel {...props} catalog={catalog} />,
    workflow: <WorkflowPanel {...props} catalog={catalog} />,
  }
  return (
    <section className="deal-detail">
      <div className="hero-panel deal-detail-hero">
        <div>
          <p className="eyebrow">Thương vụ · phiên bản {deal.revision}</p>
          <h2>{deal.title}</h2>
          <p className="hero-sub">
            Buyer phụ trách:{' '}
            <strong>{deal.state.buyer_username || 'chưa gán'}</strong> · Cập
            nhật {formatDateTime(deal.updated_at)}
          </p>
        </div>
        <div className="deal-detail-badges">
          {deal.state.is_sample && (
            <span className="status-pill sample">Dữ liệu minh họa</span>
          )}
          <span className="status-pill">{closingLabel(deal)}</span>
        </div>
      </div>
      {deal.state.is_sample && (
        <p className="notice">
          Deal này đang chứa dữ liệu minh họa do Admin nạp. Các ghi chú,
          finding, phí trong đó không phải bằng chứng thật.
        </p>
      )}
      {error && <p className="error-box">{error}</p>}
      {role === 'VAULT_ADMIN' && (
        <div className="actions deal-admin-actions">
          <button
            type="button"
            className="secondary"
            disabled={busy}
            onClick={() =>
              adminCall(
                'complete-sample',
                'Thay toàn bộ dữ liệu deal bằng dữ liệu minh họa?',
              )
            }
          >
            Nạp dữ liệu minh họa
          </button>
          <button
            type="button"
            className="danger-button"
            disabled={busy}
            onClick={() =>
              adminCall('reset', 'Xóa tiến độ và đưa deal về bước đầu?')
            }
          >
            Đặt lại deal
          </button>
        </div>
      )}
      {role === 'TECH_DD' && deal.state.seller_profile?.company_id && (
        <p>
          <a
            className="button-link"
            href={`#/rooms?company=${deal.state.seller_profile.company_id}`}
          >
            Mở phòng dữ liệu của seller
          </a>
        </p>
      )}
      {PANELS[role].map((key) => (
        <div key={key}>{panels[key]}</div>
      ))}
    </section>
  )
}
