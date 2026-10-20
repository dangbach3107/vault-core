import {
  expect,
  test,
  type APIRequestContext,
  type Page,
} from '@playwright/test'
import { authHeaders, loginAs } from './auth'

const ACTION_USERS: Record<string, string> = {
  buyerRequest: 'buyer',
  sellerProfile: 'seller',
  sellerL1Approval: 'seller',
  matchPrepared: 'admin',
}

async function setupDeals(request: APIRequestContext) {
  const seller = await authHeaders(request, 'seller')
  const admin = await authHeaders(request, 'admin')
  const company = await (
    await request.post('/api/v1/companies', {
      headers: seller,
      data: { company_name: { value: `E2E Seller ${Date.now()}` } },
    })
  ).json()
  const create = async (buyer: string, title: string) =>
    (
      await request.post('/api/v1/deals', {
        headers: admin,
        data: { title, seller_company_id: company.id, buyer_username: buyer },
      })
    ).json()
  const mine = await create('buyer', `E2E deal buyer ${Date.now()}`)
  const other = await create('buyer2', `E2E deal buyer2 ${Date.now()}`)
  for (const [action, user] of Object.entries(ACTION_USERS)) {
    const response = await request.post(
      `/api/v1/deals/${mine.id}/actions/${action}`,
      {
        headers: await authHeaders(request, user),
        data: {
          note: 'Ghi chú kiểm thử',
          ...(action === 'buyerRequest'
            ? { buyer_request: { capability: 'Phần mềm quản lý kho' } }
            : {}),
        },
      },
    )
    expect(response.ok(), action).toBe(true)
  }
  return { mine, other, company }
}

test('buyer fills the buyer request form and sees what was recorded', async ({
  page,
  request,
}) => {
  const admin = await authHeaders(request, 'admin')
  const deal = await (
    await request.post('/api/v1/deals', {
      headers: admin,
      data: { title: `E2E form ${Date.now()}`, buyer_username: 'buyer' },
    })
  ).json()
  await loginAs(page, 'buyer')
  await page.goto(`/#/deals/${deal.id}`)
  await page.getByRole('button', { name: 'Thực hiện' }).first().click()
  await page.getByLabel('Năng lực cần mua *').fill('Phần mềm quản lý kho B2B')
  await page.getByLabel('Ngân sách tối thiểu').fill('70000000000')
  await page.getByLabel('Ngân sách tối đa').fill('150000000000')
  await page.getByRole('button', { name: 'Xác nhận đã hoàn tất' }).click()
  const records = page.getByRole('region', { name: 'Nội dung đã ghi nhận' })
  await expect(records.getByText('Phần mềm quản lý kho B2B')).toBeVisible()
  await expect(
    records.getByText('70.000.000.000 VND – 150.000.000.000 VND'),
  ).toBeVisible()
  await noHorizontalScroll(page)
})

async function noHorizontalScroll(page: Page) {
  for (const width of [390, 768]) {
    await page.setViewportSize({ width, height: 900 })
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
      `overflow at ${width}px`,
    ).toBe(true)
  }
  await page.setViewportSize({ width: 1280, height: 900 })
}

test('buyer sees only the assigned deal and the approved teaser', async ({
  page,
  request,
}) => {
  const { mine, other } = await setupDeals(request)
  await loginAs(page, 'buyer')
  await page.goto('/#/deals')
  await expect(page.getByRole('heading', { name: mine.title })).toBeVisible()
  await expect(page.getByRole('heading', { name: other.title })).toHaveCount(0)
  await page.getByRole('heading', { name: mine.title }).click()
  await expect(
    page.getByRole('heading', { name: 'Hồ sơ doanh nghiệp theo quyền' }),
  ).toBeVisible()
  await expect(
    page.getByRole('heading', { name: /Doanh nghiệp VAULT-/ }),
  ).toBeVisible()
  await page.getByRole('button', { name: /Lớp 2/ }).click()
  await expect(page.getByText(/Chưa có quyền L2/)).toBeVisible()
  await expect(page.getByText('Phí, hóa đơn và thanh toán')).toHaveCount(0)
  await noHorizontalScroll(page)
})

test('finance opens fees on the deal; tech dd waits for the data room', async ({
  page,
  request,
}) => {
  const { mine } = await setupDeals(request)
  await loginAs(page, 'finance')
  await page.goto(`/#/deals/${mine.id}`)
  await expect(
    page.getByRole('heading', { name: 'Phí, hóa đơn và thanh toán' }),
  ).toBeVisible()
  await page.getByLabel('Số tiền (VND)').fill('150000000')
  await expect(page.getByText('150.000.000 VND').first()).toBeVisible()
  await page.getByRole('button', { name: 'Lập khoản phí' }).click()
  await expect(page.getByText('Chưa xuất hóa đơn')).toBeVisible()
  await expect(
    page.getByRole('heading', { name: 'Chứng từ ký và đóng' }),
  ).toBeVisible()
  await expect(page.getByText(/Chưa có chứng từ/)).toBeVisible()
  await noHorizontalScroll(page)

  await loginAs(page, 'tech')
  await page.goto(`/#/deals/${mine.id}`)
  await expect(
    page.getByText('Phòng dữ liệu chưa mở nên chưa bắt đầu thẩm định.'),
  ).toBeVisible()
  await expect(page.getByText('Phí, hóa đơn và thanh toán')).toHaveCount(0)
  await page.goto('/#/rooms')
  await expect(
    page.getByText(/Chỉ hiện phòng dữ liệu của seller/),
  ).toBeVisible()
  await expect(
    page.getByRole('button', { name: 'Tạo phòng dữ liệu' }),
  ).toHaveCount(0)
})

test('admin opens the deal detail instead of the disclosure screen', async ({
  page,
  request,
}) => {
  const { mine } = await setupDeals(request)
  await loginAs(page, 'admin')
  await page.goto('/#/deals')
  await page.getByRole('heading', { name: mine.title }).click()
  await expect(page).toHaveURL(new RegExp(`#/deals/${mine.id}`))
  await expect(
    page.getByRole('heading', { name: 'Các bước của thương vụ' }),
  ).toBeVisible()
  await expect(
    page.getByRole('heading', { name: '20 bước điều phối' }),
  ).toBeVisible()
  await noHorizontalScroll(page)
})
