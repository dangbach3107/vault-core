/* global window, console */
// Renders scene.html frame by frame and encodes public/hero.mp4 + public/hero-poster.jpg.
// Usage (from frontend/):  node scripts/hero-video/record.mjs
// Needs: Google Chrome and ffmpeg on PATH. Edit scene.html to change the content.
import { chromium } from '@playwright/test'
import { execFileSync } from 'node:child_process'
import { mkdtempSync, mkdirSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const publicDir = join(here, '..', '..', 'public')
const frames = mkdtempSync(join(tmpdir(), 'vault-hero-'))
const FPS = 30
const SECONDS = 8 // must equal T in scene.html so the loop is seamless

const browser = await chromium.launch({ channel: 'chrome' })
const page = await browser.newPage({ viewport: { width: 1600, height: 900 } })
await page.goto('file://' + join(here, 'scene.html'))
for (let i = 0; i < FPS * SECONDS; i++) {
  await page.evaluate((t) => window.render(t), i / FPS)
  await page.screenshot({
    path: join(frames, `${String(i).padStart(4, '0')}.png`),
  })
}
await browser.close()

mkdirSync(publicDir, { recursive: true })
execFileSync('ffmpeg', [
  '-y',
  '-loglevel',
  'error',
  '-framerate',
  String(FPS),
  '-i',
  join(frames, '%04d.png'),
  '-c:v',
  'libx264',
  '-preset',
  'slow',
  '-crf',
  '28',
  '-pix_fmt',
  'yuv420p',
  '-movflags',
  '+faststart',
  '-an',
  join(publicDir, 'hero.mp4'),
])
execFileSync('ffmpeg', [
  '-y',
  '-loglevel',
  'error',
  '-i',
  join(frames, '0000.png'),
  '-vf',
  'scale=1280:-1',
  '-q:v',
  '4',
  join(publicDir, 'hero-poster.jpg'),
])
rmSync(frames, { recursive: true, force: true })
console.log('Wrote public/hero.mp4 and public/hero-poster.jpg')
