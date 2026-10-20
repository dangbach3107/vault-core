import type { Fact, Preview } from '../../api/workspace'
import { formatMoney, type Currency } from '../../lib/money'
import { fields, issueLabels, optionLabels, statusLabels } from './fields'

export function FactView({
  name,
  fact,
  currency,
}: {
  name: string
  fact: Fact
  /** Set for amounts: formats the value with this currency code. */
  currency?: Currency
}) {
  return (
    <div className="fact-view">
      <dt>{name}</dt>
      <dd>
        {fact.value == null
          ? 'Chưa cung cấp'
          : currency
            ? formatMoney(String(fact.value), currency)
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
              'Quốc gia': optionLabels[data.country || ''],
              Vùng: optionLabels[data.region || ''],
              'Doanh thu': data.revenue_band,
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
            {Object.entries(data.facts).map(([key, fact]) => {
              const field = fields.find((item) => item.key === key)
              return (
                <FactView
                  key={key}
                  name={field?.label || key}
                  fact={fact as Fact}
                  currency={
                    field?.amount && 'currency' in data
                      ? data.currency
                      : undefined
                  }
                />
              )
            })}
          </dl>
          {'financials' in data && (
            <>
              <h2>Tài chính ({data.currency})</h2>
              {data.financials.length === 0 && (
                <p>Chưa cung cấp năm tài chính.</p>
              )}
              {data.financials.map((row) => (
                <section key={row.year}>
                  <h3>
                    {row.year}
                    {row.period_end ? ` · kỳ kết thúc ${row.period_end}` : ''}
                  </h3>
                  <dl className="preview-grid">
                    <FactView
                      name="Doanh thu"
                      currency={data.currency}
                      fact={(row.revenue || {}) as Fact}
                    />
                    <FactView
                      name="EBITDA"
                      currency={data.currency}
                      fact={(row.ebitda || {}) as Fact}
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
