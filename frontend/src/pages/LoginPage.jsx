import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Alert } from '../components/Alert'
import { FormField } from '../components/FormField'
import { useAuth } from '../contexts/AuthContext'
import { useAsyncAction } from '../hooks/useAsyncAction'
import { authApi } from '../api/auth'
import { tokenStorage } from '../utils/storage'

export const LoginPage = () => {
  const [form, setForm] = useState({ email: '', password: '' })
  const [googleToken, setGoogleToken] = useState('')
  const navigate = useNavigate()
  const { login, fetchProfile } = useAuth()
  const { loading, error, run } = useAsyncAction()

  const onSubmit = async (e) => {
    e.preventDefault()
    await run(async () => {
      await login(form)
      navigate('/dashboard')
    })
  }

  const onGoogleSubmit = async (e) => {
    e.preventDefault()
    await run(async () => {
      const { data } = await authApi.googleLogin(googleToken)
      tokenStorage.setTokens({ access: data.access, refresh: data.refresh })
      await fetchProfile()
      navigate('/dashboard')
    })
  }

  return (
    <section className="auth-card">
      <h1>Sign in</h1>
      <form onSubmit={onSubmit}>
        <FormField
          label="Email"
          type="email"
          value={form.email}
          onChange={(e) => setForm((prev) => ({ ...prev, email: e.target.value }))}
          required
        />
        <FormField
          label="Password"
          type="password"
          value={form.password}
          onChange={(e) => setForm((prev) => ({ ...prev, password: e.target.value }))}
          required
        />
        <button disabled={loading}>{loading ? 'Signing in...' : 'Sign in'}</button>
      </form>

      <form onSubmit={onGoogleSubmit} className="oauth-form">
        <FormField
          label="Google ID token"
          value={googleToken}
          onChange={(e) => setGoogleToken(e.target.value)}
          placeholder="Paste Google ID token"
          required
        />
        <button disabled={loading}>{loading ? 'Submitting...' : 'Sign in with Google token'}</button>
      </form>

      <Alert message={error} />

      <p>
        No account? <Link to="/register">Create one</Link>
      </p>
    </section>
  )
}
