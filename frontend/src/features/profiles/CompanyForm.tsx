import { useEffect, useState } from 'react'
import type { Company, Fact, Profile } from '../../api/workspace'
import { request } from '../../api/workspace'
import { LoadState } from '../../components/LoadState'
import { useLoad } from '../../hooks/useLoad'
import FactEditor from './FactEditor'
import { blankFact, blankProfile, currencyLabels, fields } from './fields'

const groups = [
  {
    title: 'Thông tin doanh nghiệp',
    keys: ['company_name', 'tax_id', 'founded_year', 'address', 'description'],
  },
  {
    title: 'Ngành, khu vực, quy mô',
    keys: [
      'sector',
      'country',
      'region',
      'employees',
      'customer_groups',
      'technology',
    ],
  },
  {
    title: 'Nhu cầu giao dịch',
    keys: [
      'deal_type',
      'stake_percent',
      'expected_valuation',
      'valuation_basis',
      'funds_destination',
      'objectives',
    ],
  },
  {
    title: 'Cổ đông, người quyết định, phạm vi sử dụng',
    keys: ['shareholders', 'decision_maker', 'permitted_use'],
  },
] as const

export function EditCompany({ id }: { id: string }) {
  const result = useLoad<Company>(`/companies/${id}`)
  return result.data ? (
    <CompanyForm company={result.data} />
  ) : (
    <LoadState {...result} />
  )
}

export default function CompanyForm({ company }: { company?: Company }) {
  const [profile, setProfile] = useState<Profile>(
    company?.profile || blankProfile(),
  )
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [dirty, setDirty] = useState(false)
  useEffect(() => {
    if (!dirty) return
    const warn = (event: BeforeUnloadEvent) => {
      event.preventDefault()
      event.returnValue = ''
    }
    addEventListener('beforeunload', warn)
    return () => removeEventListener('beforeunload', warn)
  }, [dirty])
  function update(next: Profile) {
    setDirty(true)
    setProfile(next)
  }
  async function submit(event: React.SubmitEvent<HTMLFormElement>) {
    event.preventDefault()
    setSaving(true)
    setError('')
    try {
      const saved = await request<Company>(
        company ? `/companies/${company.id}` : '/companies',
        {
          method: company ? 'PUT' : 'POST',
          body: JSON.stringify(
            company
              ? { expected_revision: company.revision, profile }
              : profile,
          ),
        },
      )
      setDirty(false)
      location.hash = `/companies/${saved.id}?saved=1`
    } catch (reason) {
      setError((reason as Error).message)
    } finally {
      setSaving(false)
    }
  }
  function financialFact(
    index: number,
    key: 'revenue' | 'ebitda',
    value: Fact,
  ) {
    update({
      ...profile,
      financials: profile.financials?.map((row, i) =>
        i === index ? { ...row, [key]: value } : row,
      ),
    })
  }
  const cancelHref = company ? `#/companies/${company.id}` : '#/companies'
  const currency = profile.currency || 'VND'
  return (
    <section>
      <p className="lede">
        Lưu bản nháp chỉ cần tên doanh nghiệp. Ô trống được giữ là chưa cung
        cấp. Mọi số tiền trong hồ sơ dùng một đơn vị tiền (chọn ở phần Tài
        chính); không tự làm tròn số tiền.
      </p>
      <form onSubmit={submit}>
        {groups.map((group) => (
          <fieldset
            key={group.title}
            disabled={saving}
            className="form-grid panel form-section"
          >
            <legend>{group.title}</legend>
            {fields
              .filter((field) =>
                (group.keys as readonly string[]).includes(field.key),
              )
              .map((field) => (
                <FactEditor
                  {...field}
                  key={field.key}
                  required={field.key === 'company_name'}
                  fact={(profile[field.key] || blankFact()) as Fact}
                  onChange={(fact) => update({ ...profile, [field.key]: fact })}
                />
              ))}
          </fieldset>
        ))}
        <fieldset disabled={saving} className="panel form-section">
          <legend>Tài chính — tối đa 3 năm ({currency})</legend>
          <label>
            Đơn vị tiền của hồ sơ
            <select
              value={currency}
              onChange={(e) =>
                update({
                  ...profile,
                  currency: e.target.value as Profile['currency'],
                })
              }
            >
              {Object.entries(currencyLabels).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>
          {(profile.financials || []).map((row, index) => (
            <div className="financial-row" key={index}>
              <label>
                Năm tài chính {index + 1}
                <input
                  type="number"
                  required
                  min={1900}
                  max={new Date().getFullYear()}
                  value={row.year}
                  onChange={(e) =>
                    update({
                      ...profile,
                      financials: profile.financials?.map((item, i) =>
                        i === index
                          ? { ...item, year: Number(e.target.value) }
                          : item,
                      ),
                    })
                  }
                />
              </label>
              <label>
                Ngày kết thúc kỳ — dòng {index + 1}
                <input
                  type="date"
                  value={row.period_end || ''}
                  max={new Date().toISOString().slice(0, 10)}
                  onChange={(e) =>
                    update({
                      ...profile,
                      financials: profile.financials?.map((item, i) =>
                        i === index
                          ? { ...item, period_end: e.target.value || null }
                          : item,
                      ),
                    })
                  }
                />
              </label>
              <FactEditor
                label={`Doanh thu ${currency} — dòng ${index + 1}`}
                kind="money"
                min={0}
                fact={(row.revenue || blankFact()) as Fact}
                onChange={(fact) => financialFact(index, 'revenue', fact)}
              />
              <FactEditor
                label={`EBITDA ${currency} — dòng ${index + 1}`}
                kind="money"
                fact={(row.ebitda || blankFact()) as Fact}
                onChange={(fact) => financialFact(index, 'ebitda', fact)}
              />
              <button
                type="button"
                className="secondary"
                onClick={() =>
                  update({
                    ...profile,
                    financials: profile.financials?.filter(
                      (_, i) => i !== index,
                    ),
                  })
                }
              >
                Bỏ năm {row.year}
              </button>
            </div>
          ))}
          {(profile.financials?.length || 0) < 3 && (
            <button
              type="button"
              className="secondary"
              onClick={() =>
                update({
                  ...profile,
                  financials: [
                    ...(profile.financials || []),
                    {
                      year: new Date().getFullYear() - 1,
                      period_end: null,
                      revenue: blankFact(),
                      ebitda: blankFact(),
                    },
                  ],
                })
              }
            >
              Thêm năm tài chính
            </button>
          )}
        </fieldset>
        {error && (
          <div role="alert" className="error-box">
            {error}
          </div>
        )}
        <div className="actions sticky-actions">
          <a className="button-link ghost" href={cancelHref}>
            Hủy
          </a>
          <button type="submit" disabled={saving}>
            {saving ? 'Đang lưu…' : 'Lưu bản nháp'}
          </button>
          {saving && <span role="status">Đang lưu hồ sơ…</span>}
        </div>
      </form>
    </section>
  )
}
