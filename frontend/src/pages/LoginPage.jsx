import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Alert } from '../components/Alert'
import { FormField } from '../components/FormField'
import { useAuth } from '../contexts/AuthContext'
import { useAsyncAction } from '../hooks/useAsyncAction'

export const LoginPage = () => {
  const [form, setForm] = useState({ email: '', password: '' })
  const navigate = useNavigate()
  const { login } = useAuth()
  const { loading, error, run } = useAsyncAction()

  const onSubmit = async (e) => {
    e.preventDefault()
    await run(async () => {
      await login(form)
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
        <Alert message={error} />
        <button disabled={loading}>{loading ? 'Signing in...' : 'Sign in'}</button>
      </form>
      <p>
        No account? <Link to="/register">Create one</Link>
      </p>
    </section>
  )
}
