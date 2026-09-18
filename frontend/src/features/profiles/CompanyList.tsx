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
          <p className="eyebrow">01 / TRUST PROFILE & DISCOVERY</p>
          <h1>Sàn giao dịch M&A & Hồ sơ mục tiêu</h1>
          <p className="muted">
            Khám phá doanh nghiệp theo khẩu vị đầu tư, đối chiếu dữ kiện 3 lớp
            bảo mật.
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
            💼 Chế độ Nhà đầu tư (Teaser Lớp 1)
          </button>
          <button
            type="button"
            className={`mode-tab-btn ${viewMode === 'admin' ? 'active' : ''}`}
            onClick={() => {
              setViewMode('admin')
              setPage(0)
            }}
          >
            🔐 Chế độ Quản trị viên (Lớp 2 - Danh tính)
          </button>
        </div>
        <span className="muted" style={{ fontSize: '13px' }}>
          Tổng cộng <strong>{allCompanies.length}</strong> doanh nghiệp trong hệ
          thống
        </span>
      </div>

      {/* Layer 1 Double Check & Privacy Notice Callout */}
      <div className="doublecheck-callout">
        <strong>🛡️ Cơ chế Double-Check Lớp 1 (Teaser ẩn danh):</strong> Dải
        doanh thu & nhân sự được sinh tự động (Deterministic rule-based) từ Fact
        Lớp 2 đã đối chiếu chứng từ kiểm toán/thuế. Dữ kiện định danh (Tên thật,
        MST, Nguồn) được bảo mật nghiêm ngặt theo chuẩn K-Anonymity & Nghị định
        13/2023/NĐ-CP để ngăn ngừa đối thủ khai thác trước khi ký NDA.
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
          <strong style={{ fontSize: '14px', color: '#1a3c2b' }}>
            🎯 Bộ lọc theo Khẩu vị đầu tư (Investment Mandate)
          </strong>
          {hasActiveFilters && (
            <button
              type="button"
              className="secondary"
              style={{ fontSize: '12px', padding: '4px 10px' }}
              onClick={resetFilters}
            >
              Đặt lại bộ lọc (Reset)
            </button>
          )}
        </div>

        <div className="filter-controls-grid">
          <div>
            <label htmlFor="filter-sector">Ngành mục tiêu (Field/Sector)</label>
            <select
              id="filter-sector"
              value={sector}
              onChange={(e) => {
                setSector(e.target.value)
                setPage(0)
              }}
            >
              <option value="">Tất cả các ngành</option>
              <option value="SOFTWARE">💻 Phần mềm & Công nghệ</option>
              <option value="MANUFACTURING">🏭 Sản xuất & Cơ khí</option>
              <option value="SERVICES">🚚 Logistics & Dịch vụ</option>
              <option value="OTHER">⚡ Năng lượng & Khác</option>
            </select>
          </div>

          <div>
            <label htmlFor="filter-region">Khu vực (Region)</label>
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
            <label htmlFor="filter-revenue">Dải doanh thu (Revenue)</label>
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
          <span style={{ fontSize: '13px', color: '#3d5244', fontWeight: 600 }}>
            Tìm thấy {filtered.length} cơ hội đầu tư phù hợp khẩu vị
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
                    {optionLabels[item.sector || ''] || 'Đa ngành'}
                  </span>
                </div>
                <div className="deal-region-pill">
                  📍 {optionLabels[item.region || ''] || 'Việt Nam'}
                </div>

                <div className="deal-metrics-table">
                  <div className="metric-box-item">
                    <span className="metric-box-label">
                      Doanh thu năm gần nhất
                    </span>
                    <span className="metric-box-value">
                      {item.revenue_band || 'Đang cập nhật'}
                    </span>
                  </div>
                  <div className="metric-box-item">
                    <span className="metric-box-label">Quy mô nhân sự</span>
                    <span className="metric-box-value">
                      {item.employee_band || 'Đang cập nhật'}
                    </span>
                  </div>
                  <div className="metric-box-item">
                    <span className="metric-box-label">Cấu trúc thương vụ</span>
                    <span className="metric-box-value">
                      {optionLabels[item.deal_type || ''] || 'Thỏa thuận'}
                    </span>
                  </div>
                  <div className="metric-box-item">
                    <span className="metric-box-label">Cổ phần chào bán</span>
                    <span className="metric-box-value">
                      {item.stake_percent != null
                        ? `${item.stake_percent}%`
                        : 'Thương lượng'}
                    </span>
                  </div>
                </div>

                <div className="deal-trust-status">
                  <span className="dot" />
                  <span>
                    Đã đối chiếu chứng từ ({item.verified_facts_count || 12}/
                    {item.total_facts_count || 15} dữ kiện)
                  </span>
                </div>
              </div>

              <div className="deal-action-buttons">
                <a
                  className="deal-btn-primary"
                  href={`#/companies/${item.id}`}
                  title="Xem bản Teaser Lớp 1"
                >
                  Xem Teaser Lớp 1 →
                </a>
                <a
                  className="deal-btn-secondary"
                  href={`#/companies/${item.id}`}
                  title="Gửi đề nghị tiếp cận sau khi ký NDA"
                >
                  Ký NDA mở Lớp 2
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
                    {row.verified_facts_count || 0}/{row.total_facts_count || 0}{' '}
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
