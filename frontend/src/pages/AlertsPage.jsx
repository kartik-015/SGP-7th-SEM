import React, { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import api from '../services/api'
import DataTable from '../components/DataTable'
import SeverityBadge from '../components/SeverityBadge'
import PageHeader from '../components/PageHeader'
import LoadingSkeleton from '../components/LoadingSkeleton'
import { useToast } from '../context/ToastContext'

function AlertsPage() {
  const toast = useToast()
  const [alerts, setAlerts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const loadAlerts = async () => {
    setLoading(true)
    setError('')
    try {
      const { data } = await api.get('/alerts')
      setAlerts(data)
    } catch (requestError) {
      setError(requestError?.response?.data?.detail || 'Alerts could not be loaded. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadAlerts()
  }, [])

  const reviewAlert = async (id) => {
    await updateStatus(id, 'Reviewed')
  }

  const updateStatus = async (id, status) => {
    try {
      await api.put(`/alerts/${id}/status`, { status })
      toast.success(`Alert marked ${status.toLowerCase()}`)
      await loadAlerts()
    } catch (requestError) {
      toast.error(requestError?.response?.data?.detail || 'Alert status could not be updated.')
    }
  }

  return (
    <div className="page-stack">
      <PageHeader
        title="Alerts"
        subtitle="Review high and critical detections without disrupting your workflow."
      />

      <section className="panel">
        <div className="panel-head compact">
          <div>
            <h3>Alert feed</h3>
            <p>High and critical detections automatically generate reviewable alerts</p>
          </div>
        </div>

        {loading ? <LoadingSkeleton lines={6} height={20} /> : null}
        {error ? <div className="form-alert">{error}</div> : null}

        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.18 }}>
          <DataTable
            columns={[
              { key: 'ioc_value', label: 'IOC' },
              { key: 'ioc_type', label: 'Type' },
              { key: 'severity', label: 'Severity', render: (row) => <SeverityBadge severity={row.severity} /> },
              { key: 'risk_score', label: 'Risk Score', render: (row) => Math.round(row.risk_score) },
              { key: 'triggered_at', label: 'Triggered At', render: (row) => new Date(row.triggered_at).toLocaleString() },
              { key: 'status', label: 'Status' },
              {
                key: 'action',
                label: 'Action',
                render: (row) => (
                  <select value={row.status} onChange={(event) => updateStatus(row.id, event.target.value)} aria-label={`Update status for ${row.ioc_value}`}>
                    <option>New</option>
                    <option>In Progress</option>
                    <option>Reviewed</option>
                    <option>Resolved</option>
                    <option>False Positive</option>
                  </select>
                ),
              },
            ]}
            rows={alerts}
            emptyMessage="No alerts have been generated yet."
          />
        </motion.div>
      </section>
    </div>
  )
}

export default AlertsPage
