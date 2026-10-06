import React, { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import api from '../services/api'
import DataTable from '../components/DataTable'
import PageHeader from '../components/PageHeader'
import LoadingSkeleton from '../components/LoadingSkeleton'
import { useAuth } from '../context/AuthContext'
import { useToast } from '../context/ToastContext'

function AdminPage() {
  const { user } = useAuth()
  const toast = useToast()
  const [users, setUsers] = useState([])
  const [auditLogs, setAuditLogs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [form, setForm] = useState({ full_name: '', email: '', password: '', role: 'Analyst' })

  const loadAdminData = async () => {
    setLoading(true)
    try {
      const [{ data: userData }, { data: auditData }] = await Promise.all([api.get('/admin/users'), api.get('/admin/audit')])
      setUsers(userData)
      setAuditLogs(auditData)
      setError('')
    } catch (requestError) {
      setError(requestError?.response?.data?.detail || 'Administrator data could not be loaded.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (user?.role === 'Administrator') loadAdminData()
  }, [user?.role])

  const createUser = async (event) => {
    event.preventDefault()
    try {
      await api.post('/admin/users', form)
      setForm({ full_name: '', email: '', password: '', role: 'Analyst' })
      toast.success('User created')
      await loadAdminData()
    } catch (requestError) {
      toast.error(requestError?.response?.data?.detail || 'User could not be created.')
    }
  }

  const updateUser = async (id, changes) => {
    try {
      await api.patch(`/admin/users/${id}`, changes)
      toast.success('User updated')
      await loadAdminData()
    } catch (requestError) {
      toast.error(requestError?.response?.data?.detail || 'User could not be updated.')
    }
  }

  if (user?.role !== 'Administrator') {
    return <div className="page-stack"><PageHeader title="Administrator Console" subtitle="This area is restricted to administrators." /><div className="form-alert error">Administrator access required.</div></div>
  }

  return (
    <div className="page-stack admin-console">
      <PageHeader title="Administrator Console" subtitle="Manage access, review audit activity, and maintain operational accountability." />
      {error ? <div className="form-alert error">{error}</div> : null}
      <section className="panel">
        <div className="panel-head compact"><div><h3>Create user</h3><p>Add an analyst or administrator without leaving the dashboard.</p></div></div>
        <form className="filter-row" onSubmit={createUser}>
          <input placeholder="Full name" value={form.full_name} onChange={(event) => setForm({ ...form, full_name: event.target.value })} required minLength={2} />
          <input type="email" placeholder="Email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} required />
          <input type="password" placeholder="Temporary password" value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} required minLength={8} />
          <select value={form.role} onChange={(event) => setForm({ ...form, role: event.target.value })}><option>Analyst</option><option>Administrator</option></select>
          <button type="submit" className="primary-button">Create user</button>
        </form>
      </section>
      <section className="panel">
        <div className="panel-head compact"><div><h3>User access</h3><p>Enable, disable, and adjust roles.</p></div></div>
        {loading ? <LoadingSkeleton lines={4} height={20} /> : <DataTable columns={[
          { key: 'full_name', label: 'Name' },
          { key: 'email', label: 'Email' },
          { key: 'role', label: 'Role', render: (row) => <select value={row.role} onChange={(event) => updateUser(row.id, { role: event.target.value })}><option>Analyst</option><option>Administrator</option></select> },
          { key: 'is_active', label: 'Status', render: (row) => <button type="button" className="secondary-button small" onClick={() => updateUser(row.id, { is_active: !row.is_active })}>{row.is_active ? 'Active' : 'Disabled'}</button> },
        ]} rows={users} emptyMessage="No users found." />}
      </section>
      <section className="panel">
        <div className="panel-head compact"><div><h3>Audit activity</h3><p>Recent administrator and alert actions.</p></div></div>
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}><DataTable columns={[
          { key: 'created_at', label: 'Time', render: (row) => new Date(row.created_at).toLocaleString() },
          { key: 'action', label: 'Action' },
          { key: 'entity_type', label: 'Entity' },
          { key: 'entity_id', label: 'ID' },
        ]} rows={auditLogs} emptyMessage="No audit activity yet." /></motion.div>
      </section>
    </div>
  )
}

export default AdminPage