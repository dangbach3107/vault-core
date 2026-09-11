import { useId } from 'react'
import type { Fact } from '../../api/workspace'
import { issueLabels, optionLabels, statusLabels } from './fields'

type Props = {
  label: string
  fact: Fact
  onChange: (fact: Fact) => void
  kind?: 'number' | 'money' | 'long'
  options?: string[]
  required?: boolean
  min?: number
  max?: number
  maxLength?: number
}

export default function FactEditor({
  label,
  fact,
  onChange,
  kind,
  options,
  required,
  min,
  max,
  maxLength = 2000,
}: Props) {
  const id = useId()
  function changeValue(raw: string) {
    onChange({
      ...fact,
      value: raw === '' ? null : kind === 'number' ? Number(raw) : raw,
      verification: 'SELF_DECLARED',
      reviewed_by: '',
      reviewed_on: null,
    })
  }
  const common = {
    id,
    value: fact.value ?? '',
    required,
    onChange: (
      event: React.ChangeEvent<
        HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
      >,
    ) => changeValue(event.target.value),
  }
  const reviewed =
    fact.verification !== undefined && fact.verification !== 'SELF_DECLARED'
  return (
    <div className="fact-editor">
      <label htmlFor={id}>
        {label}
        {required ? ' *' : ''}
      </label>
      {options ? (
        <select {...common}>
          <option value="">Chưa cung cấp</option>
          {options.map((option) => (
            <option key={option} value={option}>
              {optionLabels[option]}
            </option>
          ))}
        </select>
      ) : kind === 'long' ? (
        <textarea {...common} rows={2} maxLength={maxLength} />
      ) : (
        <input
          {...common}
          type={kind === 'number' || kind === 'money' ? 'number' : 'text'}
          min={min}
          max={max}
          step={kind === 'money' ? '0.01' : '1'}
          maxLength={maxLength}
        />
      )}
      <details>
        <summary>
          {fact.value == null
            ? 'Chưa cung cấp'
            : statusLabels[fact.verification || 'SELF_DECLARED']}{' '}
          · Nguồn & xác minh
        </summary>
        <div className="evidence-grid">
          <label>
            Nhãn xác minh
            <select
              value={fact.verification || 'SELF_DECLARED'}
              onChange={(e) =>
                onChange({
                  ...fact,
                  verification: e.target.value as Fact['verification'],
                })
              }
            >
              {Object.entries(statusLabels).map(([value, text]) => (
                <option key={value} value={value}>
                  {text}
                </option>
              ))}
            </select>
          </label>
          <label>
            Tình trạng dữ kiện
            <select
              value={fact.issue || 'NONE'}
              onChange={(e) =>
                onChange({
                  ...fact,
                  issue: e.target.value as Fact['issue'],
                  verification: 'SELF_DECLARED',
                  reviewed_by: '',
                  reviewed_on: null,
                })
              }
            >
              {Object.entries(issueLabels).map(([value, text]) => (
                <option key={value} value={value}>
                  {text}
                </option>
              ))}
            </select>
          </label>
          <label>
            Nguồn / đơn vị xác nhận
            <input
              value={fact.source || ''}
              maxLength={500}
              required={reviewed}
              onChange={(e) => onChange({ ...fact, source: e.target.value })}
            />
          </label>
          <label>
            Ngày nguồn
            <input
              type="date"
              value={fact.source_date || ''}
              max={new Date().toISOString().slice(0, 10)}
              required={reviewed}
              onChange={(e) =>
                onChange({ ...fact, source_date: e.target.value || null })
              }
            />
          </label>
          <label>
            Người nhập
            <input
              value={fact.entered_by || ''}
              maxLength={120}
              onChange={(e) =>
                onChange({ ...fact, entered_by: e.target.value })
              }
            />
          </label>
          <label>
            Người đối chiếu
            <input
              value={fact.reviewed_by || ''}
              maxLength={120}
              required={reviewed}
              onChange={(e) =>
                onChange({ ...fact, reviewed_by: e.target.value })
              }
            />
          </label>
          <label>
            Ngày đối chiếu
            <input
              type="date"
              value={fact.reviewed_on || ''}
              max={new Date().toISOString().slice(0, 10)}
              required={reviewed}
              onChange={(e) =>
                onChange({ ...fact, reviewed_on: e.target.value || null })
              }
            />
          </label>
          <label>
            Ghi chú
            <input
              value={fact.notes || ''}
              maxLength={1000}
              onChange={(e) => onChange({ ...fact, notes: e.target.value })}
            />
          </label>
        </div>
        <p className="muted">
          Thông tin người nhập/đối chiếu do người dùng ghi lại, chưa xác thực
          danh tính. Sửa giá trị sẽ trả nhãn về tự khai.
        </p>
      </details>
    </div>
  )
}
