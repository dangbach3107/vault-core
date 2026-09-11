import { execFileSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'

export default function setup() {
  const root = fileURLToPath(new URL('../../../', import.meta.url))
  const python = fileURLToPath(
    new URL('../../../.venv/Scripts/python.exe', import.meta.url),
  )
  try {
    for (const module of ['backend.testing', 'backend.preview_fixtures']) {
      execFileSync(python, ['-m', module], {
        cwd: root,
        env: process.env,
        stdio: 'pipe',
        windowsHide: true,
      })
    }
  } catch {
    throw new Error(
      'Could not prepare isolated test database/fixtures. Start Docker PostgreSQL, then run python -m backend.testing and python -m backend.preview_fixtures from the repository root with its .venv.',
    )
  }
}
