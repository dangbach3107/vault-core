import { FormEvent, useEffect, useMemo, useState } from 'react'
import { request, type Summary } from '../../api/workspace'
import type { Catalog, Deal } from './types'
import './deals.css'

const ROLE_HINT: Record<string, string> = {
  BUYER: 'Chỉ hiện các deal được giao cho bạn.',
  SELLER: 'Chỉ hiện các deal gắn với hồ sơ doanh nghiệp của bạn.',
  TECH_DD: 'Mở deal để ghi nhận finding và ký xác nhận thẩm định.',
  FINANCE: 'Mở deal để lập phí, xuất hóa đơn và ghi nhận thanh toán.',
}

export default function DealList({ role }: { role?: string }) {
  const [deals, setDeals] = useState<Deal[]>([])
  const [companies, setCompanies] = useState<Summary[]>([])
  const [buyers, setBuyers] = useState<string[]>([])
  const [form, setForm] = useState({
    title: '',
    seller_company_id: '',
    buyer_username: '',
  })
  const [status, setStatus] = useState('Đang tải danh sách deal…')
  const [busy, setBusy] = useState(false)
  const admin = role === 'VAULT_ADMIN'

  useEffect(() => {
    request<Deal[]>('/deals')
      .then((records) => {
        setDeals(records)
        setStatus(records.length ? '' : 'Chưa có deal nào.')
      })
      .catch((reason) =>
        setStatus(
          reason instanceof Error
            ? reason.message
            : 'Không tải được danh sách deal.',
        ),
      )
    if (admin) {
      request<Summary[]>('/companies?limit=200')
        .then(setCompanies)
        .catch(() => setCompanies([]))
      request<Catalog>('/deals/catalog')
        .then((meta) => setBuyers(meta.buyers))
        .catch(() => setBuyers([]))
    }
  }, [admin])

  const completed = useMemo(
    () =>
      deals.reduce<Record<string, number>>((result, deal) => {
        const values = Object.values(deal.state.steps || {})
        result[deal.id] = values.length
          ? Math.round((values.filter(Boolean).length / values.length) * 100)
          : 0
        return result
      }, {}),
    [deals],
  )

  const create = async (event: FormEvent) => {
    event.preventDefault()
    setBusy(true)
    try {
      const record = await request<Deal>('/deals', {
        method: 'POST',
        body: JSON.stringify({
          title: form.title.trim(),
          seller_company_id: form.seller_company_id || null,
          buyer_username: form.buyer_username || null,
        }),
      })
      location.hash = `/deals/${record.id}`
    } catch (reason) {
      setStatus(
        reason instanceof Error ? reason.message : 'Không tạo được deal.',
      )
    } finally {
      setBusy(false)
    }
  }

  return (
    <section className="deal-hub" aria-labelledby="deal-hub-title">
      <div className="hero-panel deal-hub-hero">
        <div>
          <p className="eyebrow">Thương vụ</p>
          <h2 id="deal-hub-title">Danh sách deal</h2>
          <p className="hero-sub">
            {ROLE_HINT[role || ''] ||
              'Mỗi deal gồm nhu cầu buyer, hồ sơ seller, phê duyệt, phòng dữ liệu, thẩm định, đề nghị, ký, đóng, phí và bàn giao.'}
          </p>
        </div>
        <span className="status-pill ready">{deals.length} deal</span>
      </div>
      {admin && (
        <form className="panel deal-create-form" onSubmit={create}>
          <div>
            <p className="eyebrow">Lead mới</p>
            <h2>Tạo deal</h2>
          </div>
          <label>
            Tên thương vụ
            <input
              value={form.title}
              onChange={(event) =>
                setForm({ ...form, title: event.target.value })
              }
              maxLength={200}
              placeholder="Buyer Nhật × Seller phần mềm Việt Nam"
              required
            />
          </label>
          <label>
            Hồ sơ seller
            <select
              value={form.seller_company_id}
              onChange={(event) =>
                setForm({ ...form, seller_company_id: event.target.value })
              }
              required
            >
              <option value="">Chọn hồ sơ</option>
              {companies.map((company) => (
                <option key={company.id} value={company.id}>
                  {company.alias} · {company.name}
                </option>
              ))}
            </select>
          </label>
          <label>
            Buyer phụ trách
            <select
              value={form.buyer_username}
              onChange={(event) =>
                setForm({ ...form, buyer_username: event.target.value })
              }
              required
            >
              <option value="">Chọn buyer</option>
              {buyers.map((name) => (
                <option key={name} value={name}>
                  {name}
                </option>
              ))}
            </select>
          </label>
          <button disabled={busy}>{busy ? 'Đang tạo…' : 'Tạo deal'}</button>
        </form>
      )}
      {status && (
        <p className="notice" role="status">
          {status}
        </p>
      )}
      <div className="deal-card-grid">
        {deals.map((deal) => (
          <a
            className="panel deal-card"
            href={`#/deals/${deal.id}`}
            key={deal.id}
          >
            <div className="deal-card-top">
              <span className="eyebrow">
                Buyer: {deal.state.buyer_username || 'chưa gán'}
              </span>
              <span className="status-pill">{completed[deal.id]}%</span>
            </div>
            <h2>{deal.title}</h2>
            {deal.state.is_sample && (
              <span className="status-pill sample">Dữ liệu minh họa</span>
            )}
            <div className="progress-track">
              <span style={{ width: `${completed[deal.id]}%` }} />
            </div>
            <p className="muted">
              Cập nhật {new Date(deal.updated_at).toLocaleString('vi-VN')}
            </p>
            <strong>Mở deal →</strong>
          </a>
        ))}
      </div>
    </section>
  )
}
