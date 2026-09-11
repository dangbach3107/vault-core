import { useEffect, useState } from 'react'
import { request } from '../api/workspace'

export function useLoad<T>(path: string) {
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState('')
  const [attempt, setAttempt] = useState(0)
  useEffect(() => {
    const controller = new AbortController()
    request<T>(path, { signal: controller.signal })
      .then((value) => {
        if (!controller.signal.aborted) setData(value)
      })
      .catch((reason: Error) => {
        if (!controller.signal.aborted) setError(reason.message)
      })
    return () => controller.abort()
  }, [path, attempt])
  return {
    data,
    error,
    retry: () => {
      setData(null)
      setError('')
      setAttempt((x) => x + 1)
    },
  }
}
