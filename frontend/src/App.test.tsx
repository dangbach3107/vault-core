import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { expect, test, vi } from 'vitest'
import App from './App'
import type { HealthResponse } from './api/client'

const health: HealthResponse = {
  status: 'ok',
  service: 'VAULT test API',
  version: '0.1.0',
  scope: 'liveness',
}

test('shows values returned by the API', async () => {
  const fetchMock = vi
    .fn()
    .mockResolvedValue(new Response(JSON.stringify(health)))
  vi.stubGlobal('fetch', fetchMock)
  render(<App />)
  expect(await screen.findByText('Frontend đã kết nối backend')).toBeVisible()
  expect(screen.getByText('VAULT test API')).toBeVisible()
  expect(fetchMock).toHaveBeenCalledWith('/api/v1/health', expect.any(Object))
})

test('reports failure and lets the user retry', async () => {
  const user = userEvent.setup()
  const fetchMock = vi
    .fn()
    .mockRejectedValueOnce(new Error('offline'))
    .mockResolvedValue(new Response(JSON.stringify(health)))
  vi.stubGlobal('fetch', fetchMock)
  render(<App />)
  expect(await screen.findByText('Không thể kết nối')).toBeVisible()
  await user.click(screen.getByRole('button', { name: /Kiểm tra lại/ }))
  expect(await screen.findByText('Frontend đã kết nối backend')).toBeVisible()
})

test('does not present a malformed response as connected', async () => {
  vi.stubGlobal(
    'fetch',
    vi.fn().mockResolvedValue(new Response(JSON.stringify({ status: 'ok' }))),
  )
  render(<App />)
  expect(await screen.findByText('Không thể kết nối')).toBeVisible()
})
