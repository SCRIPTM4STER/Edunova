import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Alert } from '../components/Alert'
import { FormField } from '../components/FormField'
import { useAuth } from '../contexts/AuthContext'
import { useAsyncAction } from '../hooks/useAsyncAction'

export const RegisterPage = () => {
  const [form, setForm] = useState({ email: '', username: '', password: '', password2: '' })
  const navigate = useNavigate()
  const { register } = useAuth()
  const { loading, error, run } = useAsyncAction()

  const onSubmit = async (e) => {
    e.preventDefault()
    await run(async () => {
      await register(form)
      navigate('/dashboard')
    })
  }

  return (
    <section className="auth-card">
      <h1>Create account</h1>
      <form onSubmit={onSubmit}>
        <FormField
          label="Email"
          type="email"
          value={form.email}
          onChange={(e) => setForm((prev) => ({ ...prev, email: e.target.value }))}
          required
        />
        <FormField
          label="Username"
          value={form.username}
          onChange={(e) => setForm((prev) => ({ ...prev, username: e.target.value }))}
          required
        />
        <FormField
          label="Password"
          type="password"
          value={form.password}
          onChange={(e) => setForm((prev) => ({ ...prev, password: e.target.value }))}
          required
        />
        <FormField
          label="Confirm Password"
          type="password"
          value={form.password2}
          onChange={(e) => setForm((prev) => ({ ...prev, password2: e.target.value }))}
          required
        />
        <Alert message={error} />
        <button disabled={loading}>{loading ? 'Creating...' : 'Create account'}</button>
      </form>
      <p>
        Have an account? <Link to="/login">Sign in</Link>
      </p>
    </section>
  )
}
