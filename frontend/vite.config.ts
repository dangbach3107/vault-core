import { fileURLToPath } from 'node:url'
import react from '@vitejs/plugin-react'
import { loadEnv } from 'vite'
import { defineConfig } from 'vitest/config'

const repositoryRoot = fileURLToPath(new URL('..', import.meta.url))

export default defineConfig(({ mode }) => {
  // Load only public values + the dev-server target, never all backend secrets.
  const env = loadEnv(mode, repositoryRoot, ['VITE_', 'BACKEND_PROXY_TARGET'])
  const proxy = {
    '/api': {
      target: env.BACKEND_PROXY_TARGET || 'http://127.0.0.1:8000',
      changeOrigin: true,
    },
  }
  return {
    envDir: repositoryRoot,
    plugins: [react()],
    server: { host: '127.0.0.1', port: 5173, strictPort: true, proxy },
    preview: { host: '127.0.0.1', port: 4173, strictPort: true, proxy },
    test: {
      environment: 'jsdom',
      setupFiles: ['./src/test/setup.ts'],
      include: ['src/**/*.test.{ts,tsx}'],
      restoreMocks: true,
    },
  }
})
