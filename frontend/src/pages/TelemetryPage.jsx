import React, { useEffect, useState } from 'react'
import api from '../services/api'
import DataTable from '../components/DataTable'
import PageHeader from '../components/PageHeader'
import LoadingSkeleton from '../components/LoadingSkeleton'
import SeverityBadge from '../components/SeverityBadge'

function TelemetryPage() {
  const [events, setEvents] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const loadEvents = () => {
    setError('')
    return api.get('/telemetry/events')
      .then(({ data }) => setEvents(data))
      .catch((requestError) => setError(requestError?.response?.data?.detail || 'Telemetry could not be loaded.'))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    loadEvents()
    const refreshTimer = setInterval(loadEvents, 5000)
    return () => clearInterval(refreshTimer)
  }, [])

  return (
    <div className="page-stack">
      <PageHeader
        title="Host Telemetry"
        subtitle="Review authorized command activity from Kali Linux, Termux, and other connected devices."
      />
      <section className="panel">
        <div className="panel-head compact">
          <div>
            <h3>Recent command activity</h3>
            <p>Every event includes its device, user, source address, result, and detection outcome.</p>
          </div>
        </div>
        {loading ? <LoadingSkeleton lines={5} height={20} /> : null}
        {error ? <div className="form-alert error">{error}</div> : null}
        <DataTable
          columns={[
            { key: 'executed_at', label: 'Time', render: (row) => new Date(row.executed_at).toLocaleString() },
            { key: 'device_name', label: 'Device' },
            { key: 'username', label: 'User' },
            { key: 'command', label: 'Command' },
            { key: 'source_address', label: 'Source' },
            { key: 'success', label: 'Result', render: (row) => row.success ? 'Success' : `Exit ${row.exit_code}` },
            { key: 'severity', label: 'Severity', render: (row) => <SeverityBadge severity={row.severity} /> },
            { key: 'detection_name', label: 'Detection', render: (row) => row.detection_name || 'Normal activity' },
          ]}
          rows={events}
          emptyMessage="No telemetry events have been received yet."
        />
      </section>
    </div>
  )
}

export default TelemetryPage