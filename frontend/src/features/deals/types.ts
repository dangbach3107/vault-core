import type { components } from '../../api/generated/schema'
import type { Role } from '../auth/roles'

export type Catalog = components['schemas']['DealCatalog']
export type DealDocument = components['schemas']['DealDocument']
export type BuyerRequestForm = components['schemas']['BuyerRequestForm']
export type NdaForm = components['schemas']['NdaForm']
export type OfferForm = components['schemas']['OfferForm']
export type HandoffForm = components['schemas']['HandoffForm']

export type EvidenceRecord = {
  by: string
  at: string
  note: string
  document_ids?: string[]
}

export type AccessRequest = {
  id: string
  requester: string
  requested_level: string
  purpose: string
  document_ids: string[]
  status: 'PENDING' | 'APPROVED' | 'REJECTED'
  requested_at: string
  decided_by: string | null
  reason: string | null
}

export type GrantDocument = {
  document_id: string
  title: string
  version_number: number
  latest_version: number
  filename: string
}

export type AccessGrant = {
  id: string
  user: string
  access_level: string
  purpose: string
  basis?: string
  basis_ref?: string
  can_download?: boolean
  documents?: GrantDocument[]
  approved_by: string
  granted_at: string
  expires_at: string
  revoked_at: string | null
  revoke_reason: string | null
  status: 'ACTIVE' | 'EXPIRED' | 'REVOKED'
}

export type AccessEvent = {
  type: string
  actor: string
  at: string
  reason?: string
  level?: string
  version_number?: number
}

export type Finding = {
  id: string
  title: string
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'
  description: string
  remediation: string
  impact_vnd: string | null
  status: 'OPEN' | 'RESPONDED' | 'RESOLVED' | 'ACCEPTED_RISK'
  history: {
    status: string
    by: string
    role: Role
    at: string
    note: string
  }[]
}

export type Fee = {
  id: string
  type: 'PREP_PACKAGE' | 'TECH_DD' | 'SUCCESS_FEE'
  amount_vnd: string
  paid_vnd: string
  balance_vnd: string
  due_on: string
  note: string
  invoice: { number: string; issued_on: string } | null
  payments: { amount_vnd: string; paid_on: string; reference: string }[]
  status: 'DRAFT' | 'INVOICED' | 'PARTIALLY_PAID' | 'PAID' | 'OVERDUE'
}

export type WorkflowState = {
  status: 'ACTIVE' | 'STOPPED' | 'CLOSED'
  current_step: number
  stop_reason: string | null
  unmet_conditions: string[]
  history?: {
    step: number
    label: string
    owner: Role
    by?: string
    outcome: string
    note: string
    completed_at: string
  }[]
}

/** The backend sends only the keys a role may see, so most fields are optional. */
export type DealState = {
  steps: Record<string, boolean>
  buyer_username: string | null
  is_sample: boolean
  workflow: WorkflowState
  signing: (EvidenceRecord & { status: string }) | null
  closing: { status: string; closed_at?: string } | null
  records?: Record<string, EvidenceRecord>
  seller_profile?: { company_id: string | null }
  buyer_request?: (EvidenceRecord & BuyerRequestForm) | null
  nda?: (EvidenceRecord & NdaForm) | null
  indicative_loi?: (EvidenceRecord & Partial<OfferForm>) | null
  definitive_offer?: (EvidenceRecord & Partial<OfferForm>) | null
  handoff?: (EvidenceRecord & Partial<HandoffForm>) | null
  tech_dd?: {
    findings: Finding[]
    signed_off_at: string | null
    signed_off_by: string | null
  }
  fees?: Fee[]
  opportunities?: { type: string; status: string; note: string }[]
  access_requests?: AccessRequest[]
  access_grants?: AccessGrant[]
  access_events?: AccessEvent[]
}

export type Deal = {
  id: string
  title: string
  revision: number
  created_at: string
  updated_at: string
  state: DealState
}

export const formatDate = (value?: string | null) =>
  value ? new Date(value).toLocaleDateString('vi-VN') : 'Chưa có'

export const formatDateTime = (value?: string | null) =>
  value ? new Date(value).toLocaleString('vi-VN') : 'Chưa có'
