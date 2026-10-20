import { expect, test } from 'vitest'
import { formPayload } from './formPayload'

test('NDA parties and handoff items come one per line, blanks dropped', () => {
  expect(
    formPayload('ndaRecorded', {
      reference: ' NDA-01 ',
      parties: 'Buyer A\n\n  Seller B  \n',
      signed_on: '2026-10-01',
      expires_on: '2027-10-01',
      document_id: '',
    }),
  ).toEqual({
    nda: {
      reference: 'NDA-01',
      parties: ['Buyer A', 'Seller B'],
      signed_on: '2026-10-01',
      expires_on: '2027-10-01',
      document_id: null,
    },
  })
  expect(
    formPayload('postDealHandoff', {
      recipient: 'Đội tích hợp',
      handed_on: '2026-10-20',
      items: 'Mã nguồn\nTài khoản',
    }).handoff?.items,
  ).toEqual(['Mã nguồn', 'Tài khoản'])
})

test('money stays a string and empty optional money becomes null', () => {
  const body = formPayload('loiSubmitted', {
    reference: 'OFFER-01',
    price_low_vnd: '105000000000',
    price_high_vnd: ' ',
    valuation_basis: 'EQUITY',
    exclusivity_days: '45',
    valid_until: '2027-01-01',
  })
  expect(body.offer).toMatchObject({
    price_low_vnd: '105000000000',
    price_high_vnd: null,
    valuation_basis: 'EQUITY',
    exclusivity_days: 45,
  })
  expect(formPayload('spaSigned', {})).toEqual({})
})
