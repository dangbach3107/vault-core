import { useState } from 'react'
import type { Company, Fact, Preview } from '../../api/workspace'
import { request } from '../../api/workspace'
import { LoadState } from '../../components/LoadState'
import { useLoad } from '../../hooks/useLoad'
import { fields, optionLabels } from './fields'
import { FactView, PreviewBody } from './PreviewView'
import FactReviewPanel from './FactReviewPanel'
import ActionDialog from '../../components/ActionDialog'

type Tab = 'overview' | 'finance' | 'source' | 'rooms' | 'preview'

function ProfilePreview({ id, layer }: { id: string; layer: number }) {
  const result = useLoad<Preview>(`/companies/${id}/preview/${layer}`)
  if (!result.data) return <LoadState {...result} />
  return (
    <PreviewBody
      data={result.data}
      layer={layer}
      roomsHref={`#/rooms?company=${id}`}
    />
  )
}

function factsOf(company: Company) {
  return fields.map((field) => ({
    field,
    fact: (company.profile[field.key] || { value: null }) as Fact,
  }))
}

export default function CompanyDetail({
  id,
  saved,
}: {
  id: string
  saved: boolean
}) {
  const result = useLoad<Company>(`/companies/${id}`)
  const [tab, setTab] = useState<Tab>('overview')
  const [layer, setLayer] = useState(2)
  const [deleting, setDeleting] = useState(false)
  const [deleteError, setDeleteError] = useState('')
  const [confirmDelete, setConfirmDelete] = useState(false)
  if (!result.data) return <LoadState {...result} />
  const company = result.data
  const items = factsOf(company)
  const overviewKeys = [
    'company_name',
    'tax_id',
    'founded_year',
    'sector',
    'region',
    'address',
    'description',
    'employees',
    'customer_groups',
    'technology',
    'deal_type',
    'stake_percent',
    'funds_destination',
    'objectives',
    'shareholders',
    'decision_maker',
    'permitted_use',
  ]
  return (
    <section>
      <div className="page-heading">
        <div>
          <p className="eyebrow">
            {company.alias} · BẢN SỬA {company.revision}
          </p>
          <h2>{company.profile.company_name.value}</h2>
          <p className="muted">
            {optionLabels[String(company.profile.sector?.value || '')] ||
              'Ngành chưa cung cấp'}{' '}
            ·{' '}
            {optionLabels[String(company.profile.region?.value || '')] ||
              'Khu vực chưa cung cấp'}{' '}
            · Cập nhật {new Date(company.updated_at).toLocaleString('vi-VN')}
          </p>
          <p className="muted">
            Nhãn xác minh gắn với từng dữ kiện — không phải toàn bộ doanh nghiệp
            đã được kiểm toán.
          </p>
        </div>
        <div className="context-actions">
          <a className="button-link ghost" href={`#/companies/${id}/edit`}>
            Chỉnh sửa
          </a>
          <button type="button" onClick={() => setTab('preview')}>
            Xem trước công bố
          </button>
          <button
            type="button"
            className="danger"
            disabled={deleting}
            onClick={() => setConfirmDelete(true)}
          >
            {deleting ? 'Đang xoá…' : 'Xoá hồ sơ'}
          </button>
        </div>
      </div>
      {confirmDelete && (
        <ActionDialog
          title={`Xóa hồ sơ “${company.profile.company_name.value}”?`}
          description="Hồ sơ nháp sẽ bị xóa vĩnh viễn. Hồ sơ có phòng dữ liệu liên quan sẽ được backend chặn để bảo toàn tài liệu."
          confirmLabel="Xóa hồ sơ"
          danger
          busy={deleting}
          onCancel={() => setConfirmDelete(false)}
          onSubmit={async () => {
            setDeleting(true)
            setDeleteError('')
            try {
              await request(`/companies/${id}`, { method: 'DELETE' })
              location.hash = '/companies'
            } catch (error) {
              setDeleteError(
                error instanceof Error
                  ? error.message
                  : 'Không xoá được hồ sơ.',
              )
              setDeleting(false)
              setConfirmDelete(false)
            }
          }}
        />
      )}
      {deleteError && (
        <p className="error-box" role="alert">
          {deleteError}
        </p>
      )}
      {saved && (
        <p className="success-box" role="status">
          Đã lưu hồ sơ.
        </p>
      )}
      <div className="tabs" aria-label="Phần hồ sơ">
        {(
          [
            ['overview', 'Tổng quan'],
            ['finance', 'Tài chính'],
            ['source', 'Nguồn & xác minh'],
            ['rooms', 'Phòng dữ liệu'],
            ['preview', 'Xem trước công bố'],
          ] as const
        ).map(([key, label]) => (
          <button
            key={key}
            type="button"
            aria-pressed={tab === key}
            className={tab === key ? '' : 'secondary'}
            onClick={() => setTab(key)}
          >
            {label}
          </button>
        ))}
      </div>
      {tab === 'overview' && (
        <div className="panel">
          <dl className="preview-grid">
            {items
              .filter((item) => overviewKeys.includes(item.field.key))
              .map((item) => (
                <FactView
                  key={item.field.key}
                  name={item.field.label}
                  fact={item.fact}
                />
              ))}
          </dl>
        </div>
      )}
      {tab === 'finance' && (
        <div className="panel">
          <h2>Tài chính (VND)</h2>
          {(company.profile.financials || []).length === 0 && (
            <p>Chưa cung cấp năm tài chính.</p>
          )}
          {(company.profile.financials || []).map((row) => (
            <section key={row.year}>
              <h3>{row.year}</h3>
              <dl className="preview-grid">
                <FactView
                  name="Doanh thu"
                  money
                  fact={(row.revenue_vnd || {}) as Fact}
                />
                <FactView
                  name="EBITDA"
                  money
                  fact={(row.ebitda_vnd || {}) as Fact}
                />
              </dl>
            </section>
          ))}
        </div>
      )}
      {tab === 'source' && <FactReviewPanel company={company} />}
      {tab === 'source' && (
        <div className="panel">
          <p className="muted">
            Mở từng dữ kiện để xem nguồn và lịch sử đối chiếu. Việc có nguồn
            không tự nâng nhãn xác minh.
          </p>
          <dl className="preview-grid">
            {items.map((item) => (
              <FactView
                key={item.field.key}
                name={item.field.label}
                fact={item.fact}
              />
            ))}
          </dl>
        </div>
      )}
      {tab === 'rooms' && (
        <div className="panel">
          <p>
            Phòng dữ liệu gắn với thương vụ của doanh nghiệp này. Chọn lớp xem
            trước không cấp quyền mở tài liệu.
          </p>
          <a className="button-link" href={`#/rooms?company=${id}`}>
            Mở phòng dữ liệu theo thương vụ
          </a>
        </div>
      )}
      {tab === 'preview' && (
        <>
          <p className="notice">
            Bản xem trước nội bộ — đổi tab không cấp quyền.
          </p>
          <div className="tabs" aria-label="Chọn lớp xem trước">
            {['Lớp 1 · Ẩn danh', 'Lớp 2 · Định danh', 'Lớp 3 · Hạn chế'].map(
              (label, index) => (
                <button
                  key={label}
                  type="button"
                  aria-pressed={layer === index + 1}
                  className={layer === index + 1 ? '' : 'secondary'}
                  onClick={() => setLayer(index + 1)}
                >
                  {label}
                </button>
              ),
            )}
          </div>
          <ProfilePreview key={layer} id={id} layer={layer} />
        </>
      )}
    </section>
  )
}
