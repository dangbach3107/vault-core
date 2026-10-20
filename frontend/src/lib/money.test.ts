import { expect, test } from 'vitest'
import { formatMoney, formatVnd, formatVndShort } from './money'

test('formats exact VND without floats', () => {
  expect(formatVnd('42000000000')).toBe('42.000.000.000 VND')
  expect(formatVnd('150000000.50')).toBe('150.000.000,5 VND')
  expect(formatVnd('0')).toBe('0 VND')
  expect(formatVnd('-1200000')).toBe('-1.200.000 VND')
  expect(formatVnd('123456789012345678')).toBe('123.456.789.012.345.678 VND')
  expect(formatVnd(null)).toBe('Chưa có')
})

test('formats short VND', () => {
  expect(formatVndShort('42000000000')).toBe('42,0 tỷ VND')
  expect(formatVndShort('2150000000')).toBe('2,2 tỷ VND')
  expect(formatVndShort('90000000')).toBe('90,0 triệu VND')
  expect(formatVndShort('1500000000000')).toBe('1.500,0 tỷ VND')
  expect(formatVndShort('500000')).toBe('500.000 VND')
})

test('formats JPY with the same exact grouping', () => {
  expect(formatMoney('450000000', 'JPY')).toBe('450.000.000 JPY')
  expect(formatMoney(null, 'JPY')).toBe('Chưa có')
})
