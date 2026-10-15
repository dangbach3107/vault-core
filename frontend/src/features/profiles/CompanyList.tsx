import { useMemo, useState } from 'react'
import type { Summary } from '../../api/workspace'
import { LoadState } from '../../components/LoadState'
import { useLoad } from '../../hooks/useLoad'
import { optionLabels } from './fields'

const REVENUE_BANDS = [
  'Dưới 20 tỷ',
  '20–dưới 50 tỷ',
  '50–dưới 100 tỷ',
  '100–dưới 200 tỷ',
  '200–dưới 500 tỷ',
  'Từ 500 tỷ',
]

export default function CompanyList() {
  const [viewMode, setViewMode] = useState<'buyer' | 'admin'>('buyer')
  const [search, setSearch] = useState('')
  const [sector, setSector] = useState('')
  const [region, setRegion] = useState('')
  const [dealType, setDealType] = useState('')
  const [revenueBand, setRevenueBand] = useState('')
  const [page, setPage] = useState(0)
  const pageSize = 12

  // Load companies (up to 200 to allow instant interactive filtering across the portfolio)
  const result = useLoad<Summary[]>('/companies?limit=200')

  const allCompanies = useMemo(() => result.data || [], [result.data])

  // Filter companies according to investment mandate / appetite
  const filtered = useMemo(() => {
    const term = search.trim().toLowerCase()
    return allCompanies.filter((item) => {
      // Sector filter
      if (sector && item.sector !== sector) return false
      // Region filter
      if (region && item.region !== region) return false
      // Deal type filter
      if (dealType && item.deal_type !== dealType) return false
      // Revenue band filter
      if (revenueBand && item.revenue_band !== revenueBand) return false

      // Search keyword
      if (term) {
        const matchesAlias = item.alias?.toLowerCase().includes(term)
        const matchesName =
          viewMode === 'admin' && item.name?.toLowerCase().includes(term)
        const matchesTax =
          viewMode === 'admin' && item.tax_id?.toLowerCase().includes(term)
        const matchesSector = optionLabels[item.sector || '']
          ?.toLowerCase()
          .includes(term)
        const matchesRegion = optionLabels[item.region || '']
          ?.toLowerCase()
          .includes(term)
        if (
          !matchesAlias &&
          !matchesName &&
          !matchesTax &&
          !matchesSector &&
          !matchesRegion
        ) {
          return false
        }
      }

      return true
    })
  }, [allCompanies, sector, region, dealType, revenueBand, search, viewMode])

  const hasActiveFilters = Boolean(
    search || sector || region || dealType || revenueBand,
  )

  const resetFilters = () => {
    setSearch('')
    setSector('')
    setRegion('')
    setDealType('')
    setRevenueBand('')
    setPage(0)
  }

  const paginated = useMemo(() => {
    const start = page * pageSize
    return filtered.slice(start, start + pageSize)
  }, [filtered, page, pageSize])

  const totalPages = Math.ceil(filtered.length / pageSize)

  return (
    <section>
      <div className="page-heading">
        <div>
          <p className="eyebrow">Hồ sơ doanh nghiệp</p>
          <h1>Danh mục hồ sơ seller</h1>
          <p className="muted">
            Quản lý hồ sơ và xem trước cách hồ sơ hiển thị ở từng lớp công bố.
          </p>
        </div>
        <a className="button-link" href="#/companies/new">
          + Tạo hồ sơ mới
        </a>
      </div>

      {/* Mode Switcher */}
      <div className="mode-switch-container">
        <div className="mode-tabs">
          <button
            type="button"
            className={`mode-tab-btn ${viewMode === 'buyer' ? 'active' : ''}`}
            onClick={() => {
              setViewMode('buyer')
              setPage(0)
            }}
          >
            Xem trước dạng Teaser (Lớp 1)
          </button>
          <button
            type="button"
            className={`mode-tab-btn ${viewMode === 'admin' ? 'active' : ''}`}
            onClick={() => {
              setViewMode('admin')
              setPage(0)
            }}
          >
            Danh sách quản trị (có danh tính)
          </button>
        </div>
        <span className="muted" style={{ fontSize: '13px' }}>
          Tổng cộng <strong>{allCompanies.length}</strong> doanh nghiệp trong hệ
          thống
        </span>
      </div>

      <div className="doublecheck-callout">
        <strong>Đây là bản xem trước nội bộ.</strong> Dải doanh thu và nhân sự
        được tính theo quy tắc cố định từ dữ kiện đã nhập; dữ kiện đang mâu
        thuẫn hoặc hết hạn bị ẩn. Buyer chỉ thấy Teaser trong trang deal của họ,
        sau khi Seller duyệt. Teaser vẫn cần người duyệt kiểm tra nguy cơ nhận
        diện trước khi chia sẻ.
      </div>

      {/* Faceted Filter Panel (Investment Mandate) */}
      <div className="discovery-filter-box">
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          <strong style={{ fontSize: '14px', color: 'var(--text)' }}>
            Bộ lọc theo khẩu vị đầu tư
          </strong>
          {hasActiveFilters && (
            <button
              type="button"
              className="secondary"
              style={{ fontSize: '12px', padding: '4px 10px' }}
              onClick={resetFilters}
            >
              Đặt lại bộ lọc
            </button>
          )}
        </div>

        <div className="filter-controls-grid">
          <div>
            <label htmlFor="filter-sector">Ngành</label>
            <select
              id="filter-sector"
              value={sector}
              onChange={(e) => {
                setSector(e.target.value)
                setPage(0)
              }}
            >
              <option value="">Tất cả các ngành</option>
              <option value="SOFTWARE">{optionLabels.SOFTWARE}</option>
              <option value="MANUFACTURING">
                {optionLabels.MANUFACTURING}
              </option>
              <option value="SERVICES">{optionLabels.SERVICES}</option>
              <option value="OTHER">{optionLabels.OTHER}</option>
            </select>
          </div>

          <div>
            <label htmlFor="filter-region">Khu vực</label>
            <select
              id="filter-region"
              value={region}
              onChange={(e) => {
                setRegion(e.target.value)
                setPage(0)
              }}
            >
              <option value="">Toàn quốc (Bắc - Trung - Nam)</option>
              <option value="NORTH">Miền Bắc</option>
              <option value="CENTRAL">Miền Trung</option>
              <option value="SOUTH">Miền Nam</option>
            </select>
          </div>

          <div>
            <label htmlFor="filter-revenue">Dải doanh thu</label>
            <select
              id="filter-revenue"
              value={revenueBand}
              onChange={(e) => {
                setRevenueBand(e.target.value)
                setPage(0)
              }}
            >
              <option value="">Tất cả quy mô doanh thu</option>
              {REVENUE_BANDS.map((b) => (
                <option key={b} value={b}>
                  {b}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label htmlFor="filter-deal">Cấu trúc giao dịch</label>
            <select
              id="filter-deal"
              value={dealType}
              onChange={(e) => {
                setDealType(e.target.value)
                setPage(0)
              }}
            >
              <option value="">Tất cả hình thức</option>
              <option value="PRIMARY">Phát hành mới (Tăng vốn)</option>
              <option value="SECONDARY">Chuyển nhượng (Thoái vốn)</option>
              <option value="MIXED">Kết hợp</option>
            </select>
          </div>

          <div>
            <label htmlFor="filter-keyword">
              {viewMode === 'buyer'
                ? 'Tìm mã deal hoặc từ khóa'
                : 'Tìm tên hoặc MST'}
            </label>
            <input
              id="filter-keyword"
              placeholder={
                viewMode === 'buyer'
                  ? 'Ví dụ: VAULT-01, Phần mềm...'
                  : 'Tên công ty hoặc MST...'
              }
              value={search}
              onChange={(e) => {
                setSearch(e.target.value)
                setPage(0)
              }}
            />
          </div>
        </div>

        <div className="filter-actions-row">
          <span
            style={{
              fontSize: '13px',
              color: 'var(--text-2)',
              fontWeight: 600,
            }}
          >
            Tìm thấy {filtered.length} hồ sơ
          </span>
          <span className="muted" style={{ fontSize: '12px' }}>
            Trang {page + 1} / {totalPages || 1}
          </span>
        </div>
      </div>

      {!result.data && <LoadState {...result} />}

      {/* Results Rendering */}
      {filtered.length === 0 && result.data ? (
        <div className="empty panel">
          <p>
            Không có doanh nghiệp nào khớp với tiêu chí khẩu vị đầu tư hiện tại.
          </p>
          <button type="button" className="secondary" onClick={resetFilters}>
            Bỏ chọn bộ lọc để xem toàn bộ danh mục
          </button>
        </div>
      ) : viewMode === 'buyer' ? (
        /* Buyer Mode: Teaser Deal Cards Grid */
        <div className="deal-cards-grid">
          {paginated.map((item) => (
            <div className="deal-card" key={item.id}>
              <div>
                <div className="deal-card-header">
                  <span className="deal-alias">{item.alias}</span>
                  <span className="deal-sector-badge">
                    {optionLabels[item.sector || ''] || 'Chưa có ngành'}
                  </span>
                </div>
                <div className="deal-region-pill">
                  {optionLabels[item.region || ''] || 'Chưa có khu vực'}
                </div>

                <div className="deal-metrics-table">
                  <div className="metric-box-item">
                    <span className="metric-box-label">
                      Doanh thu năm gần nhất
                    </span>
                    <span className="metric-box-value">
                      {item.revenue_band || 'Chưa có'}
                    </span>
                  </div>
                  <div className="metric-box-item">
                    <span className="metric-box-label">Quy mô nhân sự</span>
                    <span className="metric-box-value">
                      {item.employee_band || 'Chưa có'}
                    </span>
                  </div>
                  <div className="metric-box-item">
                    <span className="metric-box-label">Cấu trúc thương vụ</span>
                    <span className="metric-box-value">
                      {optionLabels[item.deal_type || ''] || 'Chưa có'}
                    </span>
                  </div>
                  <div className="metric-box-item">
                    <span className="metric-box-label">Cổ phần chào bán</span>
                    <span className="metric-box-value">
                      {item.stake_percent != null
                        ? `${item.stake_percent}%`
                        : 'Chưa có'}
                    </span>
                  </div>
                </div>

                <div className="deal-trust-status">
                  <span className="dot" />
                  {/* Real counts only: 0 stays 0, never a placeholder. */}
                  <span>
                    {(item.verified_facts_count ?? 0) > 0
                      ? `${item.verified_facts_count}/${item.total_facts_count ?? 0} dữ kiện đã được người duyệt xác minh`
                      : `Chưa có dữ kiện được xác minh (0/${item.total_facts_count ?? 0})`}
                  </span>
                </div>
              </div>

              <div className="deal-action-buttons">
                <a className="deal-btn-primary" href={`#/companies/${item.id}`}>
                  Mở hồ sơ và xem trước các lớp →
                </a>
              </div>
            </div>
          ))}
        </div>
      ) : (
        /* Admin Mode: Internal Management List with Real Names & Tax IDs */
        <div className="record-list">
          {paginated.map((row) => (
            <a
              className="record panel"
              key={row.id}
              href={`#/companies/${row.id}`}
            >
              <div>
                <span className="eyebrow">{row.alias}</span>
                <h2>{row.name}</h2>
                <p>
                  MST: <strong>{row.tax_id || 'Chưa cung cấp'}</strong> · Ngành:{' '}
                  {optionLabels[row.sector || ''] || 'Chưa đặt'} · Vùng:{' '}
                  {optionLabels[row.region || ''] || 'Chưa đặt'} · Xác minh:{' '}
                  <span className="badge DOCUMENT_VERIFIED">
                    {row.verified_facts_count ?? 0}/{row.total_facts_count ?? 0}{' '}
                    dữ kiện
                  </span>
                </p>
              </div>
              <span>Quản trị hồ sơ →</span>
            </a>
          ))}
        </div>
      )}

      {/* Pagination Controls */}
      {totalPages > 1 && (
        <div
          className="actions"
          style={{ justifyContent: 'center', marginTop: '24px' }}
        >
          <button
            type="button"
            className="secondary"
            disabled={page === 0}
            onClick={() => setPage(page - 1)}
          >
            ← Trang trước
          </button>
          <span style={{ fontSize: '13px', padding: '0 8px' }}>
            Trang {page + 1} / {totalPages}
          </span>
          <button
            type="button"
            className="secondary"
            disabled={page >= totalPages - 1}
            onClick={() => setPage(page + 1)}
          >
            Trang sau →
          </button>
        </div>
      )}
    </section>
  )
}
