import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Link, useNavigate } from 'react-router-dom'
import { Shield, TriangleAlert } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { useToast } from '../context/ToastContext'

function LoginPage() {
  const { login } = useAuth()
  const toast = useToast()
  const navigate = useNavigate()
  const [email, setEmail] = useState('admin@cti.local')
  const [password, setPassword] = useState('Admin@123')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    setError('')
    try {
      await login(email, password)
      toast.success('Login successful')
      navigate('/dashboard')
    } catch (err) {
      const message = err?.response?.data?.detail || 'Invalid email or password.'
      setError(message)
      toast.error(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page premium-auth">
      <motion.div className="auth-hero" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.22 }}>
        <div className="auth-brand">
          <Shield size={28} />
          <span>Cyber Threat Intelligence Dashboard</span>
        </div>
        <h1>Welcome back.</h1>
        <p>Review IOC risk, filter by severity, inspect InternetDB enrichment, and monitor alerts from one secure workspace.</p>

        <div className="demo-card">
          <div className="demo-card-title">Demo Credentials</div>
          <div>Administrator: admin@cti.local / Admin@123</div>
          <div>Analyst: analyst@cti.local / Analyst@123</div>
        </div>
      </motion.div>

      <motion.form className="auth-panel auth-card" onSubmit={handleSubmit} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.22, delay: 0.05 }}>
        <h2>Sign in</h2>
        <p>Use a seeded account to access the Phase 1 dashboard.</p>

        {error && (
          <div className="form-alert error">
            <TriangleAlert size={16} />
            <span>{error}</span>
          </div>
        )}

        <label>
          Email
          <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
        </label>
        <label>
          Password
          <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} required />
        </label>

        <button type="submit" className="primary-button" disabled={loading}>{loading ? 'Signing in...' : 'Login to platform'}</button>

        <div className="auth-switch">
          New user? <Link to="/register">Create an account</Link>
        </div>
      </motion.form>
    </div>
  )
}

export default LoginPage
