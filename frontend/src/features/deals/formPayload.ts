/** Steps that carry a typed form instead of a free note; mirrors FORM_ACTIONS in the backend. */
export const FORM_ACTIONS = [
  'buyerRequest',
  'ndaRecorded',
  'indicativeLoiSubmitted',
  'loiSubmitted',
  'postDealHandoff',
]

export type Fields = Record<string, string>

const today = () => new Date().toISOString().slice(0, 10)
const lines = (value = '') =>
  value
    .split('\n')
    .map((line) => line.trim())
    .filter(Boolean)
const optional = (value = '') => value.trim() || null

export function initialFields(action: string): Fields {
  if (action === 'ndaRecorded') return { signed_on: today() }
  if (action === 'postDealHandoff') return { handed_on: today() }
  if (action === 'indicativeLoiSubmitted' || action === 'loiSubmitted')
    return { valuation_basis: 'EV', exclusivity_days: '0' }
  return {}
}

/** The request body part for a form step; the backend validates every rule again. */
export function formPayload(action: string, fields: Fields) {
  if (action === 'buyerRequest')
    return {
      buyer_request: {
        capability: fields.capability?.trim() || '',
        goal: fields.goal?.trim() || '',
        budget_min_vnd: optional(fields.budget_min_vnd),
        budget_max_vnd: optional(fields.budget_max_vnd),
        timeline: fields.timeline?.trim() || '',
      },
    }
  if (action === 'ndaRecorded')
    return {
      nda: {
        reference: fields.reference?.trim() || '',
        parties: lines(fields.parties),
        signed_on: fields.signed_on,
        expires_on: fields.expires_on,
        document_id: optional(fields.document_id),
      },
    }
  if (action === 'indicativeLoiSubmitted' || action === 'loiSubmitted')
    return {
      offer: {
        reference: fields.reference?.trim() || '',
        price_low_vnd: fields.price_low_vnd?.trim() || '',
        price_high_vnd: optional(fields.price_high_vnd),
        valuation_basis: fields.valuation_basis || 'EV',
        exclusivity_days: Number(fields.exclusivity_days || 0),
        valid_until: fields.valid_until,
        conditions: fields.conditions?.trim() || '',
      },
    }
  if (action === 'postDealHandoff')
    return {
      handoff: {
        recipient: fields.recipient?.trim() || '',
        handed_on: fields.handed_on,
        items: lines(fields.items),
      },
    }
  return {}
}
