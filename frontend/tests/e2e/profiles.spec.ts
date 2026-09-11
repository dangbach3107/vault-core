import { expect, test } from '@playwright/test'

test('create, persist, edit and preview a company through the real API and PostgreSQL', async ({
  page,
}) => {
  const name = `Doanh nghiệp giả lập ${Date.now()}`
  const errors: string[] = []
  page.on('pageerror', (error) => errors.push(error.message))
  await page.goto('/#/companies')
  await page.getByRole('link', { name: 'Tạo hồ sơ', exact: true }).click()
  await page.getByLabel('Tên doanh nghiệp *', { exact: true }).fill(name)
  await page
    .getByLabel('Mã số thuế', { exact: true })
    .fill(`TEST-${Date.now()}`)
  await page
    .getByLabel('Ngành hoạt động', { exact: true })
    .selectOption('SOFTWARE')
  await page.getByLabel('Vùng hoạt động', { exact: true }).selectOption('SOUTH')
  await page.getByLabel('Địa chỉ', { exact: true }).fill('123 Địa chỉ riêng tư')
  await page
    .getByLabel('Doanh thu VND — dòng 1', { exact: true })
    .fill('25000000000.01')
  await page.getByRole('button', { name: 'Lưu hồ sơ', exact: true }).click()
  await expect(
    page.getByRole('status').filter({ hasText: 'Đã lưu hồ sơ.' }),
  ).toBeVisible()
  await expect(page.getByRole('heading', { name, exact: true })).toBeVisible()
  await page.reload()
  await expect(page.getByRole('heading', { name, exact: true })).toBeVisible()
  await page.getByRole('button', { name: 'Lớp 1 · Ẩn danh' }).click()
  await expect(page.getByText('20–dưới 50 tỷ', { exact: true })).toBeVisible()
  await expect(page.getByText(name, { exact: true })).toHaveCount(0)
  await expect(
    page.getByText('123 Địa chỉ riêng tư', { exact: true }),
  ).toHaveCount(0)
  await expect(page.getByText('25000000000.01', { exact: true })).toHaveCount(0)
  await page.getByRole('link', { name: 'Sửa hồ sơ' }).click()
  await page
    .getByLabel('Tên doanh nghiệp *', { exact: true })
    .fill(`${name} đã sửa`)
  await page.getByRole('button', { name: 'Lưu hồ sơ', exact: true }).click()
  await expect(
    page.getByRole('heading', { name: `${name} đã sửa`, exact: true }),
  ).toBeVisible()
  await page.getByRole('button', { name: 'Lớp 3 · Hạn chế' }).click()
  await expect(page.getByLabel('Nội dung lớp 3')).toContainText(
    'Cổ đông & sở hữu',
  )
  await page.screenshot({
    path: 'test-results/profile-desktop.png',
    fullPage: true,
  })
  await page.setViewportSize({ width: 390, height: 844 })
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true)
  await page.screenshot({
    path: 'test-results/profile-mobile.png',
    fullPage: true,
  })
  await page.getByRole('link', { name: 'Danh sách doanh nghiệp' }).click()
  await page.getByLabel('Tìm tên hoặc mã số thuế').fill(name)
  await page.getByRole('button', { name: 'Tìm kiếm' }).click()
  await expect(
    page.getByRole('heading', { name: `${name} đã sửa`, exact: true }),
  ).toBeVisible()
  expect(errors).toEqual([])
})
