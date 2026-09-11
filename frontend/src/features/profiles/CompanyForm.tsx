import { useState } from 'react'
import type { Company, Fact, Profile } from '../../api/workspace'
import { request } from '../../api/workspace'
import { LoadState } from '../../components/LoadState'
import { useLoad } from '../../hooks/useLoad'
import FactEditor from './FactEditor'
import { blankFact, blankProfile, fields } from './fields'

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
      location.hash = `/companies/${saved.id}?saved=1`
    } catch (reason) {
      setError((reason as Error).message)
    } finally {
      setSaving(false)
    }
  }
  function financialFact(
    index: number,
    key: 'revenue_vnd' | 'ebitda_vnd',
    value: Fact,
  ) {
    setProfile({
      ...profile,
      financials: profile.financials?.map((row, i) =>
        i === index ? { ...row, [key]: value } : row,
      ),
    })
  }
  return (
    <section>
      <div className="page-heading">
        <div>
          <p className="eyebrow">HỒ SƠ DOANH NGHIỆP</p>
          <h1>{company ? 'Sửa hồ sơ' : 'Tạo hồ sơ mới'}</h1>
        </div>
        <a href={company ? `#/companies/${company.id}` : '#/companies'}>
          Quay lại
        </a>
      </div>
      <p className="muted">
        Lưu bản nháp chỉ cần tên doanh nghiệp. Ô trống được giữ là chưa cung
        cấp. Tiền tệ: VND; không tự làm tròn số tiền.
      </p>
      <form onSubmit={submit}>
        <fieldset disabled={saving} className="form-grid panel">
          <legend>Thông tin & nguồn dữ kiện</legend>
          {fields.map((field) => (
            <FactEditor
              {...field}
              key={field.key}
              required={field.key === 'company_name'}
              fact={(profile[field.key] || blankFact()) as Fact}
              onChange={(fact) => setProfile({ ...profile, [field.key]: fact })}
            />
          ))}
        </fieldset>
        <fieldset disabled={saving} className="panel">
          <legend>Tài chính — tối đa 3 năm</legend>
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
                    setProfile({
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
              <FactEditor
                label={`Doanh thu VND — dòng ${index + 1}`}
                kind="money"
                min={0}
                fact={(row.revenue_vnd || blankFact()) as Fact}
                onChange={(fact) => financialFact(index, 'revenue_vnd', fact)}
              />
              <FactEditor
                label={`EBITDA VND — dòng ${index + 1}`}
                kind="money"
                fact={(row.ebitda_vnd || blankFact()) as Fact}
                onChange={(fact) => financialFact(index, 'ebitda_vnd', fact)}
              />
              <button
                type="button"
                className="secondary"
                onClick={() =>
                  setProfile({
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
                setProfile({
                  ...profile,
                  financials: [
                    ...(profile.financials || []),
                    {
                      year: new Date().getFullYear() - 1,
                      revenue_vnd: blankFact(),
                      ebitda_vnd: blankFact(),
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
        <div className="actions">
          <button type="submit" disabled={saving}>
            {saving ? 'Đang lưu…' : 'Lưu hồ sơ'}
          </button>
          {saving && <span role="status">Đang lưu hồ sơ…</span>}
        </div>
      </form>
    </section>
  )
}
