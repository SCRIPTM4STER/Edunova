import { useState } from 'react'

export const useAsyncAction = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const run = async (action) => {
    setLoading(true)
    setError('')
    try {
      return await action()
    } catch (err) {
      const message =
        err?.response?.data?.detail ||
        err?.response?.data?.error ||
        JSON.stringify(err?.response?.data) ||
        err.message ||
        'An unexpected error occurred.'
      setError(message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  return { loading, error, run, setError }
}
