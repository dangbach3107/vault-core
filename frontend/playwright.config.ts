import { defineConfig, devices } from '@playwright/test'
import { fileURLToPath } from 'node:url'
import { readFileSync } from 'node:fs'

const testDatabaseUrl =
  process.env.TEST_DATABASE_URL ||
  (
    JSON.parse(
      readFileSync(new URL('../.tmp/database.json', import.meta.url), 'utf8'),
    ) as { test_database_url: string }
  ).test_database_url
if (!testDatabaseUrl.endsWith('/vault_test'))
  throw new Error('Browser tests require isolated vault_test database.')
process.env.TEST_DATABASE_URL = testDatabaseUrl

process.env.PLAYWRIGHT_BROWSERS_PATH = fileURLToPath(
  new URL('../.tmp/playwright', import.meta.url),
)

export default defineConfig({
  globalSetup: './tests/e2e/setup.ts',
  testDir: './tests/e2e',
  fullyParallel: false,
  use: { baseURL: 'http://127.0.0.1:15173', trace: 'retain-on-failure' },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
  webServer: [
    {
      command:
        '..\\.venv\\Scripts\\python.exe -m uvicorn backend.app.main:app --app-dir .. --host 127.0.0.1 --port 18000',
      url: 'http://127.0.0.1:18000/api/v1/health',
      reuseExistingServer: false,
      timeout: 30000,
      env: {
        DATABASE_URL: testDatabaseUrl,
        INTERNAL_PREVIEW_ENABLED: 'true',
        UPLOAD_DIRECTORY: '.tmp/e2e-uploads',
      },
    },
    {
      command: 'npm.cmd run dev -- --port 15173',
      url: 'http://127.0.0.1:15173',
      reuseExistingServer: false,
      timeout: 30000,
      env: { BACKEND_PROXY_TARGET: 'http://127.0.0.1:18000' },
    },
  ],
})
