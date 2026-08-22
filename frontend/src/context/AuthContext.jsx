import React, { createContext, useContext, useEffect, useMemo, useState } from 'react'
import api from '../services/api'

const AuthContext = createContext(null)

function readStoredSession() {
  const token = localStorage.getItem('cti_token')
  const user = localStorage.getItem('cti_user')
  return {
    token,
    user: user ? JSON.parse(user) : null,
  }
}

export function AuthProvider({ children }) {
  const stored = readStoredSession()
  const [token, setToken] = useState(stored.token)
  const [user, setUser] = useState(stored.user)
  const [loading, setLoading] = useState(Boolean(stored.token))

  useEffect(() => {
    if (!stored.token) {
      setLoading(false)
      return
    }

    api
      .get('/auth/me')
      .then(({ data }) => {
        setUser(data)
        localStorage.setItem('cti_user', JSON.stringify(data))
      })
      .catch(() => {
        localStorage.removeItem('cti_token')
        localStorage.removeItem('cti_user')
        setToken(null)
        setUser(null)
      })
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    if (token) {
      localStorage.setItem('cti_token', token)
      api.defaults.headers.common.Authorization = `Bearer ${token}`
    } else {
      delete api.defaults.headers.common.Authorization
      localStorage.removeItem('cti_token')
    }
  }, [token])

  const login = async (email, password) => {
    const { data } = await api.post('/auth/login', { email, password })
    setToken(data.access_token)
    setUser(data.user)
    localStorage.setItem('cti_user', JSON.stringify(data.user))
    return data
  }

  const register = async (payload) => {
    const { data } = await api.post('/auth/register', payload)
    setToken(data.access_token)
    setUser(data.user)
    localStorage.setItem('cti_user', JSON.stringify(data.user))
    return data
  }

  const logout = () => {
    setToken(null)
    setUser(null)
    localStorage.removeItem('cti_token')
    localStorage.removeItem('cti_user')
  }

  const value = useMemo(
    () => ({
      token,
      user,
      loading,
      isAuthenticated: Boolean(token && user),
      login,
      register,
      logout,
    }),
    [token, user, loading],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
