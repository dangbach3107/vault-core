import type { Fact, FieldName, Profile } from '../../api/workspace'

export const statusLabels = {
  SELF_DECLARED: 'Tự khai',
  DOCUMENT_VERIFIED: 'Đã đối chiếu',
  THIRD_PARTY_CONFIRMED: 'Bên thứ ba xác nhận',
}
export const issueLabels = {
  NONE: 'Không ghi nhận vấn đề',
  CONFLICTED: 'Mâu thuẫn',
  EXPIRED: 'Hết hạn',
}
export const optionLabels: Record<string, string> = {
  SOFTWARE: 'Phần mềm & công nghệ',
  MANUFACTURING: 'Sản xuất',
  SERVICES: 'Dịch vụ',
  OTHER: 'Khác',
  NORTH: 'Miền Bắc',
  CENTRAL: 'Miền Trung',
  SOUTH: 'Miền Nam',
  PRIMARY: 'Phát hành mới',
  SECONDARY: 'Chuyển nhượng',
  MIXED: 'Kết hợp',
}
export type FieldDefinition = {
  key: FieldName
  label: string
  kind?: 'number' | 'money' | 'long'
  options?: string[]
  min?: number
  max?: number
  maxLength?: number
}
export const fields: FieldDefinition[] = [
  { key: 'company_name', label: 'Tên doanh nghiệp', maxLength: 200 },
  { key: 'tax_id', label: 'Mã số thuế', maxLength: 30 },
  {
    key: 'founded_year',
    label: 'Năm thành lập',
    kind: 'number',
    min: 1800,
    max: new Date().getFullYear(),
  },
  {
    key: 'sector',
    label: 'Ngành hoạt động',
    options: ['SOFTWARE', 'MANUFACTURING', 'SERVICES', 'OTHER'],
  },
  {
    key: 'region',
    label: 'Vùng hoạt động',
    options: ['NORTH', 'CENTRAL', 'SOUTH'],
  },
  { key: 'address', label: 'Địa chỉ', kind: 'long' },
  { key: 'description', label: 'Mô tả doanh nghiệp', kind: 'long' },
  { key: 'customer_groups', label: 'Nhóm khách hàng', kind: 'long' },
  {
    key: 'employees',
    label: 'Số nhân sự',
    kind: 'number',
    min: 0,
    max: 10000000,
  },
  { key: 'technology', label: 'Tài sản & nền tảng công nghệ', kind: 'long' },
  { key: 'shareholders', label: 'Cổ đông & sở hữu (lớp 3)', kind: 'long' },
  { key: 'decision_maker', label: 'Người có quyền quyết định (lớp 3)' },
  {
    key: 'deal_type',
    label: 'Loại giao dịch',
    options: ['PRIMARY', 'SECONDARY', 'MIXED'],
  },
  {
    key: 'stake_percent',
    label: 'Tỷ lệ giao dịch (%)',
    kind: 'money',
    min: 0,
    max: 100,
  },
  { key: 'funds_destination', label: 'Mục đích sử dụng vốn', kind: 'long' },
  { key: 'objectives', label: 'Mục tiêu thương vụ', kind: 'long' },
  {
    key: 'permitted_use',
    label: 'Phạm vi đồng ý sử dụng dữ liệu (lớp 3)',
    kind: 'long',
  },
]

export function blankFact(): Omit<Fact, 'value'> & { value: null } {
  return {
    value: null,
    verification: 'SELF_DECLARED',
    issue: 'NONE',
    source: '',
    source_date: null,
    entered_by: '',
    reviewed_by: '',
    reviewed_on: null,
    notes: '',
  }
}

export function blankProfile(): Profile {
  return {
    company_name: blankFact(),
    financials: Array.from({ length: 3 }, (_, i) => ({
      year: new Date().getFullYear() - 1 - i,
      revenue_vnd: blankFact(),
      ebitda_vnd: blankFact(),
    })),
  }
}
