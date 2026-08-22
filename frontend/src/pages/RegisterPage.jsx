import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Shield } from 'lucide-react'
import { useAuth } from '../context/AuthContext'

function RegisterPage() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ full_name: '', email: '', password: '', role: 'Analyst' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const updateField = (field, value) => setForm((current) => ({ ...current, [field]: value }))

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    setError('')
    try {
      await register(form)
      navigate('/dashboard')
    } catch (err) {
      setError(err?.response?.data?.detail || 'Registration failed.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page register-page">
      <div className="auth-hero">
        <div className="auth-brand">
          <Shield size={28} />
          <span>Cyber Threat Intelligence Dashboard</span>
        </div>
        <h1>Create a demo account</h1>
        <p>Registration is enabled for Phase 1 so the review can show a complete authentication flow.</p>
      </div>

      <form className="auth-panel" onSubmit={handleSubmit}>
        <h2>Register</h2>
        {error && <div className="form-alert error">{error}</div>}
        <label>
          Full Name
          <input value={form.full_name} onChange={(event) => updateField('full_name', event.target.value)} required />
        </label>
        <label>
          Email
          <input type="email" value={form.email} onChange={(event) => updateField('email', event.target.value)} required />
        </label>
        <label>
          Password
          <input type="password" value={form.password} onChange={(event) => updateField('password', event.target.value)} required />
        </label>
        <label>
          Role
          <select value={form.role} onChange={(event) => updateField('role', event.target.value)}>
            <option value="Analyst">Analyst</option>
            <option value="Administrator">Administrator</option>
          </select>
        </label>
        <button type="submit" className="primary-button" disabled={loading}>
          {loading ? 'Creating account...' : 'Create account'}
        </button>
        <div className="auth-switch">
          Already have an account? <Link to="/login">Back to login</Link>
        </div>
      </form>
    </div>
  )
}

export default RegisterPage
