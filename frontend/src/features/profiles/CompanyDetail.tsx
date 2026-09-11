import { useState } from 'react'
import type { Company, Fact, Preview } from '../../api/workspace'
import { LoadState } from '../../components/LoadState'
import { useLoad } from '../../hooks/useLoad'
import { fields, issueLabels, optionLabels, statusLabels } from './fields'

function FactView({ name, fact }: { name: string; fact: Fact }) {
  return (
    <div className="fact-view">
      <dt>{name}</dt>
      <dd>
        {fact.value == null
          ? 'Chưa cung cấp'
          : optionLabels[String(fact.value)] || String(fact.value)}{' '}
        <span className={`badge ${fact.verification || 'SELF_DECLARED'}`}>
          {fact.value == null
            ? 'Thiếu dữ liệu'
            : statusLabels[fact.verification || 'SELF_DECLARED']}
        </span>
      </dd>
      {fact.issue && fact.issue !== 'NONE' && (
        <p className="issue">{issueLabels[fact.issue]}</p>
      )}
      {(fact.source || fact.notes || fact.reviewed_by || fact.entered_by) && (
        <details>
          <summary>Nguồn & lịch sử đối chiếu</summary>
          <p>
            Nguồn: {fact.source || 'Chưa ghi'} · Ngày:{' '}
            {fact.source_date || 'Chưa ghi'}
          </p>
          <p>
            Người nhập: {fact.entered_by || 'Chưa ghi'} · Đối chiếu:{' '}
            {fact.reviewed_by || 'Chưa ghi'} ({fact.reviewed_on || 'Chưa ghi'})
          </p>
          <p>{fact.notes}</p>
        </details>
      )}
    </div>
  )
}

function ProfilePreview({ id, layer }: { id: string; layer: number }) {
  const result = useLoad<Preview>(`/companies/${id}/preview/${layer}`)
  if (!result.data) return <LoadState {...result} />
  const data = result.data
  return (
    <div className="panel" aria-label={`Nội dung lớp ${layer}`}>
      <p className="notice">{data.notice}</p>
      {'alias' in data ? (
        <>
          <h2>Doanh nghiệp {data.alias}</h2>
          <dl className="preview-grid">
            {Object.entries({
              Ngành: optionLabels[data.sector || ''],
              Vùng: optionLabels[data.region || ''],
              'Doanh thu': data.revenue_band_vnd,
              'Nhân sự': data.employee_band,
              'Giao dịch': optionLabels[data.deal_type || ''],
            }).map(([name, value]) => (
              <div key={name}>
                <dt>{name}</dt>
                <dd>{value || 'Chưa cung cấp'}</dd>
              </div>
            ))}
          </dl>
          <p className="muted">
            Các giá trị là thông tin khai báo theo dải, chưa phải kết luận thẩm
            định.
          </p>
        </>
      ) : (
        <>
          <dl className="preview-grid">
            {Object.entries(data.facts).map(([key, fact]) => (
              <FactView
                key={key}
                name={fields.find((field) => field.key === key)?.label || key}
                fact={fact as Fact}
              />
            ))}
          </dl>
          {'financials' in data && (
            <>
              <h2>Tài chính (VND)</h2>
              {data.financials.length === 0 && (
                <p>Chưa cung cấp năm tài chính.</p>
              )}
              {data.financials.map((row) => (
                <section key={row.year}>
                  <h3>{row.year}</h3>
                  <dl className="preview-grid">
                    <FactView
                      name="Doanh thu"
                      fact={(row.revenue_vnd || {}) as Fact}
                    />
                    <FactView
                      name="EBITDA"
                      fact={(row.ebitda_vnd || {}) as Fact}
                    />
                  </dl>
                </section>
              ))}
            </>
          )}
          {layer === 3 && (
            <p>
              <a href={`#/rooms?company=${id}`}>
                Mở phòng dữ liệu theo thương vụ
              </a>
            </p>
          )}
        </>
      )}
    </div>
  )
}

export default function CompanyDetail({
  id,
  saved,
}: {
  id: string
  saved: boolean
}) {
  const result = useLoad<Company>(`/companies/${id}`)
  const [layer, setLayer] = useState(2)
  if (!result.data) return <LoadState {...result} />
  const company = result.data
  return (
    <section>
      <a href="#/companies">← Danh sách doanh nghiệp</a>
      <div className="page-heading">
        <div>
          <p className="eyebrow">
            {company.alias} · BẢN SỬA {company.revision}
          </p>
          <h1>
            {layer === 1
              ? `Doanh nghiệp ${company.alias}`
              : company.profile.company_name.value}
          </h1>
          <p className="muted">
            Cập nhật {new Date(company.updated_at).toLocaleString('vi-VN')}
          </p>
        </div>
        <a className="button-link" href={`#/companies/${id}/edit`}>
          Sửa hồ sơ
        </a>
      </div>
      {saved && (
        <p className="success-box" role="status">
          Đã lưu hồ sơ.
        </p>
      )}
      <div className="tabs" aria-label="Chọn lớp xem trước">
        {['Lớp 1 · Ẩn danh', 'Lớp 2 · Định danh', 'Lớp 3 · Hạn chế'].map(
          (label, index) => (
            <button
              key={label}
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
    </section>
  )
}
