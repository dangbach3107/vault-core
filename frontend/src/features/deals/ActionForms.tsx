import { formatVnd } from '../../lib/money'
import type { RoomFile } from '../rooms/useSellerFiles'
import type { Fields } from './formPayload'

const MONEY_PATTERN = '\\d+(\\.\\d{1,2})?'
const today = () => new Date().toISOString().slice(0, 10)

function Text({
  label,
  name,
  fields,
  onChange,
  required = false,
  type = 'text',
  max,
  min,
}: {
  label: string
  name: string
  fields: Fields
  onChange: (fields: Fields) => void
  required?: boolean
  type?: 'text' | 'date'
  max?: string
  min?: string
}) {
  return (
    <label>
      {label}
      {required ? ' *' : ''}
      <input
        type={type}
        value={fields[name] || ''}
        onChange={(event) =>
          onChange({ ...fields, [name]: event.target.value })
        }
        required={required}
        max={max}
        min={min}
        maxLength={type === 'text' ? 200 : undefined}
      />
    </label>
  )
}

function Money({
  label,
  name,
  fields,
  onChange,
  required = false,
}: {
  label: string
  name: string
  fields: Fields
  onChange: (fields: Fields) => void
  required?: boolean
}) {
  return (
    <label>
      {label}
      {required ? ' *' : ''}
      <input
        inputMode="numeric"
        pattern={MONEY_PATTERN}
        value={fields[name] || ''}
        onChange={(event) =>
          onChange({ ...fields, [name]: event.target.value })
        }
        required={required}
        placeholder="VND, ví dụ 90000000000"
      />
      {fields[name] && <small>{formatVnd(fields[name])}</small>}
    </label>
  )
}

function Lines({
  label,
  name,
  fields,
  onChange,
}: {
  label: string
  name: string
  fields: Fields
  onChange: (fields: Fields) => void
}) {
  return (
    <label className="wide">
      {label} * (mỗi dòng một mục)
      <textarea
        value={fields[name] || ''}
        onChange={(event) =>
          onChange({ ...fields, [name]: event.target.value })
        }
        rows={3}
        required
      />
    </label>
  )
}

export function ActionFormFields({
  action,
  fields,
  onChange,
  files,
}: {
  action: string
  fields: Fields
  onChange: (fields: Fields) => void
  files: RoomFile[]
}) {
  const props = { fields, onChange }
  if (action === 'buyerRequest')
    return (
      <div className="finding-form action-form">
        <label className="wide">
          Năng lực cần mua *
          <input
            value={fields.capability || ''}
            onChange={(event) =>
              onChange({ ...fields, capability: event.target.value })
            }
            required
            minLength={3}
            maxLength={500}
            placeholder="Ví dụ: phần mềm quản lý kho B2B"
          />
        </label>
        <Money label="Ngân sách tối thiểu" name="budget_min_vnd" {...props} />
        <Money label="Ngân sách tối đa" name="budget_max_vnd" {...props} />
        <Text label="Thời gian mong muốn" name="timeline" {...props} />
        <label className="wide">
          Mục tiêu
          <textarea
            value={fields.goal || ''}
            onChange={(event) =>
              onChange({ ...fields, goal: event.target.value })
            }
            rows={2}
            maxLength={1000}
          />
        </label>
      </div>
    )
  if (action === 'ndaRecorded')
    return (
      <div className="finding-form action-form">
        <Text label="Số hiệu NDA" name="reference" required {...props} />
        <Text
          label="Ngày ký"
          name="signed_on"
          type="date"
          max={today()}
          required
          {...props}
        />
        <Text
          label="Ngày hết hạn"
          name="expires_on"
          type="date"
          min={fields.signed_on}
          required
          {...props}
        />
        <Lines label="Các bên ký" name="parties" {...props} />
        <label className="wide">
          File NDA trong phòng dữ liệu (không bắt buộc)
          <select
            value={fields.document_id || ''}
            onChange={(event) =>
              onChange({ ...fields, document_id: event.target.value })
            }
          >
            <option value="">Không đính kèm</option>
            {files.map((file) => (
              <option key={file.id} value={file.id}>
                {file.title} · phiên bản {file.version} · {file.room}
              </option>
            ))}
          </select>
        </label>
        <p className="muted wide">
          NDA là căn cứ để duyệt Lớp 2; quyền Lớp 2 không được kéo dài quá ngày
          hết hạn này.
        </p>
      </div>
    )
  if (action === 'indicativeLoiSubmitted' || action === 'loiSubmitted')
    return (
      <div className="finding-form action-form">
        <Text label="Số hiệu" name="reference" required {...props} />
        <Money label="Giá (thấp)" name="price_low_vnd" required {...props} />
        <Money
          label="Giá (cao, nếu là khoảng)"
          name="price_high_vnd"
          {...props}
        />
        <label>
          Cơ sở định giá *
          <select
            value={fields.valuation_basis || 'EV'}
            onChange={(event) =>
              onChange({ ...fields, valuation_basis: event.target.value })
            }
          >
            <option value="EV">EV (giá trị doanh nghiệp)</option>
            <option value="EQUITY">Equity (giá trị vốn chủ)</option>
          </select>
        </label>
        <label>
          Số ngày độc quyền
          <input
            type="number"
            min={0}
            max={365}
            value={fields.exclusivity_days || '0'}
            onChange={(event) =>
              onChange({ ...fields, exclusivity_days: event.target.value })
            }
          />
        </label>
        <Text
          label="Hiệu lực đến"
          name="valid_until"
          type="date"
          min={today()}
          required
          {...props}
        />
        <label className="wide">
          Điều kiện chính
          <textarea
            value={fields.conditions || ''}
            onChange={(event) =>
              onChange({ ...fields, conditions: event.target.value })
            }
            rows={2}
            maxLength={2000}
          />
        </label>
        <p className="muted wide">
          {action === 'indicativeLoiSubmitted'
            ? 'LOI sơ bộ không ràng buộc; là căn cứ để duyệt Lớp 3.'
            : 'Đề nghị chính thức là căn cứ để mở tài liệu closing.'}{' '}
          Quyền mở theo căn cứ này không kéo dài quá ngày hiệu lực.
        </p>
      </div>
    )
  if (action === 'postDealHandoff')
    return (
      <div className="finding-form action-form">
        <Text label="Bên nhận" name="recipient" required {...props} />
        <Text
          label="Ngày bàn giao"
          name="handed_on"
          type="date"
          max={today()}
          required
          {...props}
        />
        <Lines label="Danh mục bàn giao" name="items" {...props} />
      </div>
    )
  return null
}
