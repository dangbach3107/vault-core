import { readFile, mkdir, writeFile } from 'node:fs/promises'
import openapiTS, { astToString } from 'openapi-typescript'

const contract = new URL('../../contracts/openapi.json', import.meta.url)
const output = new URL('../src/api/generated/schema.d.ts', import.meta.url)
const text =
  '// Generated from contracts/openapi.json. Do not edit.\n' +
  astToString(await openapiTS(contract))
if (process.argv.includes('--check')) {
  const current = await readFile(output, 'utf8').catch(() => '')
  if (current.replaceAll('\r\n', '\n') !== text.replaceAll('\r\n', '\n')) {
    console.error('API types are stale. Run npm run api:generate.')
    process.exitCode = 1
  } else {
    console.log('Frontend API types are current.')
  }
} else {
  await mkdir(new URL('.', output), { recursive: true })
  await writeFile(output, text, 'utf8')
  console.log('Generated src/api/generated/schema.d.ts')
}
