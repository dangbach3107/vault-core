import { fireEvent, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { expect, test, vi } from 'vitest'
import type { RoomDetail } from '../../api/workspace'
import UploadForm from './UploadForm'

const room: RoomDetail = {
  id: 'room',
  title: 'Synthetic',
  company_id: 'company',
  company_name: 'Sample',
  created_at: '2026-01-01T00:00:00Z',
  max_upload_bytes: 1024,
  allowed_extensions: ['.png'],
  documents: [],
  folders: [{ id: 'LEGAL_CORPORATE', label: 'Pháp lý', document_count: 0 }],
}

test('rejects an oversized file before sending it', async () => {
  const user = userEvent.setup()
  const fetchMock = vi.fn()
  vi.stubGlobal('fetch', fetchMock)
  render(<UploadForm room={room} onSaved={vi.fn()} />)
  await user.type(screen.getByLabelText('Tên tài liệu'), 'Sample')
  await user.upload(
    screen.getByLabelText('Chọn file'),
    new File([new Uint8Array(1025)], 'large.png', { type: 'image/png' }),
  )
  // jsdom's native file-required validity differs from Chromium; browser E2E
  // covers native submission, while this test exercises our upload handler.
  fireEvent.submit(
    screen.getByRole('button', { name: 'Tải lên' }).closest('form')!,
  )
  expect(await screen.findByRole('alert')).toHaveTextContent(
    'File vượt giới hạn dung lượng',
  )
  expect(fetchMock).not.toHaveBeenCalled()
})

test('retains file and title after server rejection for a corrected retry', async () => {
  const user = userEvent.setup()
  vi.stubGlobal(
    'fetch',
    vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ detail: 'Invalid file' }), {
        status: 415,
      }),
    ),
  )
  render(<UploadForm room={room} onSaved={vi.fn()} />)
  await user.type(screen.getByLabelText('Tên tài liệu'), 'Evidence')
  await user.upload(
    screen.getByLabelText('Chọn file'),
    new File(['bad'], 'sample.png', { type: 'image/png' }),
  )
  fireEvent.submit(
    screen.getByRole('button', { name: 'Tải lên' }).closest('form')!,
  )
  expect(await screen.findByRole('alert')).toHaveTextContent('Invalid file')
  expect(screen.getByLabelText('Tên tài liệu')).toHaveValue('Evidence')
  expect(screen.getByRole('button', { name: 'Tải lên' })).toBeEnabled()
})
