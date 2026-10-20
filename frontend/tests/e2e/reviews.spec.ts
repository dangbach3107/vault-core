import { expect, test } from '@playwright/test'
import { authHeaders, loginAs } from './auth'

test('seller sends a fact for review, legal approves it from the queue', async ({
  page,
  request,
}) => {
  const name = `E2E Review ${Date.now()}`
  const company = await (
    await request.post('/api/v1/companies', {
      headers: await authHeaders(request, 'seller'),
      data: { company_name: { value: name }, employees: { value: 120 } },
    })
  ).json()

  await loginAs(page, 'seller')
  await page.goto(`/#/companies/${company.id}`)
  await page.getByRole('button', { name: 'Nguồn & xác minh' }).click()
  const row = page.getByRole('row', { name: /Số nhân sự/ })
  await row.getByRole('button', { name: 'Gửi duyệt' }).click()
  await page.getByLabel('Nguồn *', { exact: true }).fill('Bảng lương tháng 9 (minh họa)')
  await page.getByRole('button', { name: 'Gửi duyệt' }).last().click()
  await expect(page.getByText(/Đã gửi duyệt/)).toBeVisible()
  await expect(row.getByText('Chờ duyệt')).toBeVisible()

  await loginAs(page, 'legal')
  await page.goto('/#/reviews')
  const item = page.locator('article').filter({ hasText: name })
  await expect(item.getByText('Giá trị gửi duyệt: 120')).toBeVisible()
  await item.getByRole('button', { name: 'Chấp thuận' }).click()
  await page.getByLabel('Lý do / ghi chú đối chiếu').fill('Khớp bảng lương')
  await page.keyboard.press('Escape')
  await expect(page.getByRole('dialog')).toHaveCount(0)
  await item.getByRole('button', { name: 'Chấp thuận' }).click()
  await page.getByLabel('Lý do / ghi chú đối chiếu').fill('Khớp bảng lương')
  await page
    .getByRole('dialog')
    .getByRole('button', { name: 'Chấp thuận' })
    .click()
  await expect(
    page.getByText('Đã chấp thuận và gắn nhãn xác minh.'),
  ).toBeVisible()

  await loginAs(page, 'seller')
  await page.goto(`/#/companies/${company.id}`)
  await page.getByRole('button', { name: 'Nguồn & xác minh' }).click()
  await expect(
    page.getByRole('row', { name: /Số nhân sự/ }).getByText('Đã đối chiếu'),
  ).toBeVisible()
})
