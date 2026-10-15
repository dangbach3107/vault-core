import type { Fact, Preview } from '../../api/workspace'
import { formatVnd } from '../../lib/money'
import { fields, issueLabels, optionLabels, statusLabels } from './fields'

export function FactView({
  name,
  fact,
  money = false,
}: {
  name: string
  fact: Fact
  money?: boolean
}) {
  return (
    <div className="fact-view">
      <dt>{name}</dt>
      <dd>
        {fact.value == null
          ? 'Chưa cung cấp'
          : money
            ? formatVnd(String(fact.value))
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

export function PreviewBody({
  data,
  layer,
  roomsHref,
}: {
  data: Preview
  layer: number
  roomsHref?: string
}) {
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
            </>
          )}
          {layer === 3 && roomsHref && (
            <p>
              <a href={roomsHref}>Mở phòng dữ liệu theo thương vụ</a>
            </p>
          )}
        </>
      )}
    </div>
  )
}
