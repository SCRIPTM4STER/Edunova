import { Navigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { Loader } from './Loader'

export const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth()

  if (loading) return <Loader text="Checking session..." />
  if (!user) return <Navigate to="/login" replace />

  return children
}
