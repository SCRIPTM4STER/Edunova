import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import { authApi } from '../api/auth'
import { tokenStorage } from '../utils/storage'

const AuthContext = createContext(null)

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  const logout = useCallback(() => {
    tokenStorage.clear()
    setUser(null)
  }, [])

  const fetchProfile = useCallback(async () => {
    try {
      const { data } = await authApi.getProfile()
      setUser(data)
      return data
    } catch (error) {
      logout()
      throw error
    }
  }, [logout])

  useEffect(() => {
    const access = tokenStorage.getAccessToken()
    if (!access) {
      setLoading(false)
      return
    }

    fetchProfile().finally(() => setLoading(false))
  }, [fetchProfile])

  const login = async ({ email, password }) => {
    const { data } = await authApi.login({ email, password })
    tokenStorage.setTokens({ access: data.access, refresh: data.refresh })
    await fetchProfile()
  }

  const register = async (payload) => {
    await authApi.register(payload)
    await login({ email: payload.email, password: payload.password })
  }

  const value = useMemo(
    () => ({ user, loading, login, register, logout, fetchProfile }),
    [user, loading, fetchProfile, logout],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
