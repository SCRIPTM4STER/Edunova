import { useEffect, useState } from 'react'
import { authApi } from '../api/auth'
import { Alert } from '../components/Alert'
import { Loader } from '../components/Loader'

const initialPasswordForm = { old_password: '', new_password: '', confirm_password: '' }

export const ProfilePage = () => {
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [passwordForm, setPasswordForm] = useState(initialPasswordForm)

  const loadProfile = async () => {
    setLoading(true)
    setError('')
    try {
      const { data } = await authApi.getProfile()
      setProfile(data)
    } catch {
      setError('Failed to load profile.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadProfile()
  }, [])

  const changePassword = async (e) => {
    e.preventDefault()
    setMessage('')
    setError('')

    try {
      await authApi.changePassword(passwordForm)
      setMessage('Password changed successfully.')
      setPasswordForm(initialPasswordForm)
    } catch (err) {
      const responseError = err?.response?.data
      setError(responseError?.detail || JSON.stringify(responseError))
    }
  }

  if (loading) return <Loader text="Loading profile..." />

  return (
    <section>
      <h1>Profile</h1>
      <Alert type="info" message={message} />
      <Alert message={error} />

      <div className="panel profile-grid">
        <p>
          <strong>Handle:</strong> {profile?.user?.handle}
        </p>
        <p>
          <strong>Email:</strong> {profile?.user?.email}
        </p>
        <p>
          <strong>Username:</strong> {profile?.user?.username}
        </p>
        <p>
          <strong>Full Name:</strong> {profile?.full_name || '-'}
        </p>
        <p>
          <strong>Phone:</strong> {profile?.phone_number || '-'}
        </p>
        <p>
          <strong>Date of Birth:</strong> {profile?.date_of_birth || '-'}
        </p>
        <p>
          <strong>Occupation:</strong> {profile?.occupation || '-'}
        </p>
        <p>
          <strong>Interests:</strong> {profile?.interests || '-'}
        </p>
        <p className="full-row">
          <strong>Bio:</strong> {profile?.bio || '-'}
        </p>
        {profile?.avatar ? <img src={profile.avatar} alt="Profile avatar" className="avatar" /> : null}
      </div>

      <form className="panel" onSubmit={changePassword}>
        <h3>Change Password</h3>
        <input
          type="password"
          placeholder="Old password"
          value={passwordForm.old_password}
          onChange={(e) => setPasswordForm((prev) => ({ ...prev, old_password: e.target.value }))}
          required
        />
        <input
          type="password"
          placeholder="New password"
          value={passwordForm.new_password}
          onChange={(e) => setPasswordForm((prev) => ({ ...prev, new_password: e.target.value }))}
          required
        />
        <input
          type="password"
          placeholder="Confirm new password"
          value={passwordForm.confirm_password}
          onChange={(e) => setPasswordForm((prev) => ({ ...prev, confirm_password: e.target.value }))}
          required
        />
        <button>Submit</button>
        <p className="muted">Backend enforces a re-auth session flag before this endpoint succeeds.</p>
      </form>
    </section>
  )
}
