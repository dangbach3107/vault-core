import { expect, test } from '@playwright/test'
import { fileURLToPath } from 'node:url'

const fixture = (name: string) =>
  fileURLToPath(new URL(`../../../.tmp/fixtures/${name}`, import.meta.url))

test('room folders, upload, preview and immutable version history', async ({
  page,
}) => {
  const name = `Doanh nghiệp VDR giả lập ${Date.now()}`
  const errors: string[] = []
  page.on('pageerror', (error) => errors.push(error.message))
  const created = await page.request.post('/api/v1/companies', {
    data: { company_name: { value: name } },
  })
  expect(created.status()).toBe(201)
  await page.goto('/#/rooms')
  await page
    .getByRole('button', { name: 'Thêm phòng dữ liệu', exact: true })
    .click()
  await page.getByLabel('Tìm doanh nghiệp để tạo phòng').fill(name)
  await page
    .getByRole('button', { name: 'Tìm doanh nghiệp', exact: true })
    .click()
  await page.getByRole('button', { name: new RegExp(name) }).click()
  await page
    .getByLabel('Tên thương vụ / phòng dữ liệu')
    .fill(`Thương vụ ${name}`)
  await page
    .getByRole('button', { name: 'Tạo phòng dữ liệu', exact: true })
    .click()
  await expect(
    page.getByRole('heading', { name: `Thương vụ ${name}`, exact: true }),
  ).toBeVisible()
  expect(
    await page.getByLabel('Nhóm thư mục').getByRole('button').count(),
  ).toBe(7)
  await page.getByRole('button', { name: 'Thêm tài liệu', exact: true }).click()
  await page
    .getByLabel('Tên tài liệu', { exact: true })
    .fill('Bằng chứng giả lập')
  await page
    .getByRole('combobox', { name: 'Nhóm thư mục', exact: true })
    .selectOption('LEGAL_CORPORATE')
  await page.getByLabel('Chọn file', { exact: true }).setInputFiles({
    name: 'invalid.png',
    mimeType: 'image/png',
    buffer: Buffer.from('not an image'),
  })
  await page.getByRole('button', { name: 'Tải lên', exact: true }).click()
  await expect(page.getByRole('alert')).toContainText(
    'Nội dung file không hợp lệ',
  )
  await expect(page.getByLabel('Tên tài liệu', { exact: true })).toHaveValue(
    'Bằng chứng giả lập',
  )
  await page
    .getByLabel('Chọn file', { exact: true })
    .setInputFiles(fixture('sample-v1.png'))
  await page.getByRole('button', { name: 'Tải lên', exact: true }).click()
  await page.getByRole('link', { name: /Bằng chứng giả lập/ }).click()
  const oldUrl = page.url()
  await expect(
    page.getByRole('img', { name: 'Xem trước sample-v1.png' }),
  ).toBeVisible()
  await expect
    .poll(() =>
      page
        .getByRole('img')
        .evaluate((image) => (image as HTMLImageElement).naturalWidth),
    )
    .toBe(800)
  const download1 = page.waitForEvent('download')
  await page.getByRole('link', { name: 'Tải file phiên bản này' }).click()
  expect((await download1).suggestedFilename()).toBe('sample-v1.png')
  await page
    .getByRole('button', { name: 'Thêm phiên bản', exact: true })
    .click()
  await page
    .getByLabel('File phiên bản mới')
    .setInputFiles(fixture('sample-v2.png'))
  await page.getByLabel('Ghi chú phiên bản').fill('Bản cập nhật giả lập')
  await page
    .getByRole('button', { name: 'Lưu phiên bản mới', exact: true })
    .click()
  await expect(
    page.getByRole('heading', { name: 'Đang xem phiên bản 2' }),
  ).toBeVisible()
  await expect(
    page.getByRole('img', { name: 'Xem trước sample-v2.png' }),
  ).toBeVisible()
  await page.getByRole('button', { name: /^Phiên bản 1/ }).click()
  await expect(
    page.getByRole('img', { name: 'Xem trước sample-v1.png' }),
  ).toBeVisible()
  await page.reload()
  await expect(page.getByRole('button', { name: /^Phiên bản 1/ })).toBeVisible()
  await expect(page.getByRole('button', { name: /^Phiên bản 2/ })).toBeVisible()
  await page.screenshot({
    path: 'test-results/room-version-desktop.png',
    fullPage: true,
  })
  await page.setViewportSize({ width: 390, height: 844 })
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true)
  await page.screenshot({
    path: 'test-results/room-version-mobile.png',
    fullPage: true,
  })
  await page.setViewportSize({ width: 1280, height: 900 })
  await page.getByRole('link', { name: 'Về phòng dữ liệu' }).click()
  await page.getByRole('button', { name: 'Thêm tài liệu', exact: true }).click()
  await page.getByLabel('Tên tài liệu', { exact: true }).fill('PDF giả lập')
  await page
    .getByLabel('Chọn file', { exact: true })
    .setInputFiles(fixture('sample.pdf'))
  await page.getByRole('button', { name: 'Tải lên', exact: true }).click()
  await page.getByRole('link', { name: /PDF giả lập/ }).click()
  await expect(page.getByLabel('Xem trước sample.pdf')).toBeVisible()
  await page.getByText('Văn bản trang 1', { exact: true }).click()
  await expect(page.getByText(/VAULT - SYNTHETIC PDF/)).toBeVisible()
  await page.getByRole('button', { name: 'Trang PDF sau' }).click()
  await page.getByText('Văn bản trang 2', { exact: true }).click()
  await expect(
    page.getByText('SECOND SYNTHETIC PAGE', { exact: true }),
  ).toBeVisible()
  await page.getByRole('button', { name: 'Trang PDF trước' }).click()
  await page.getByText('Văn bản trang 1', { exact: true }).click()
  await expect(page.getByText('Đang tải bản xem trước…')).toHaveCount(0)
  await page.screenshot({
    path: 'test-results/room-pdf-preview.png',
    fullPage: true,
  })
  await page.goto(oldUrl)
  await expect(page.getByRole('button', { name: /^Phiên bản 2/ })).toBeVisible()
  expect(errors).toEqual([])
})
