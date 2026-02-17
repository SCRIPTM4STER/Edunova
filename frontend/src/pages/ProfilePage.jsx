import { useState } from 'react'
import { authApi } from '../api/auth'
import { Alert } from '../components/Alert'
import { useAuth } from '../contexts/AuthContext'

export const ProfilePage = () => {
  const { user } = useAuth()
  const [message, setMessage] = useState('')
  const [form, setForm] = useState({ old_password: '', new_password: '', confirm_password: '' })

  const changePassword = async (e) => {
    e.preventDefault()
    setMessage('')
    try {
      await authApi.changePassword(form)
      setMessage('Password changed successfully.')
    } catch (err) {
      setMessage(err?.response?.data?.detail || JSON.stringify(err?.response?.data))
    }
  }

  return (
    <section>
      <h1>Profile</h1>
      <div className="panel">
        <p>
          <strong>Email:</strong> {user?.user?.email}
        </p>
        <p>
          <strong>Username:</strong> {user?.user?.username}
        </p>
        <p>
          <strong>Full Name:</strong> {user?.full_name || '-'}
        </p>
      </div>
      <form className="panel" onSubmit={changePassword}>
        <h3>Change Password</h3>
        <Alert type="info" message={message} />
        <input
          type="password"
          placeholder="Old password"
          value={form.old_password}
          onChange={(e) => setForm((prev) => ({ ...prev, old_password: e.target.value }))}
          required
        />
        <input
          type="password"
          placeholder="New password"
          value={form.new_password}
          onChange={(e) => setForm((prev) => ({ ...prev, new_password: e.target.value }))}
          required
        />
        <input
          type="password"
          placeholder="Confirm new password"
          value={form.confirm_password}
          onChange={(e) => setForm((prev) => ({ ...prev, confirm_password: e.target.value }))}
          required
        />
        <button>Submit</button>
        <p className="muted">Backend requires a re-auth session flag before this endpoint allows updates.</p>
      </form>
    </section>
  )
}
