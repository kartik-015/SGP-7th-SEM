import React, { useEffect, useMemo, useState } from 'react'
import { motion } from 'framer-motion'
import api from '../services/api'
import DataTable from '../components/DataTable'
import SeverityBadge from '../components/SeverityBadge'
import PageHeader from '../components/PageHeader'
import LoadingSkeleton from '../components/LoadingSkeleton'
import ThreatDetailsDrawer from '../components/ThreatDetailsDrawer'
import { useToast } from '../context/ToastContext'

function ThreatExplorerPage() {
  const toast = useToast()
  const [rows, setRows] = useState([])
  const [filters, setFilters] = useState({ severity: '', ioc_type: '', source: '', search: '' })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [selectedThreat, setSelectedThreat] = useState(null)

  const fetchRows = async (nextFilters = filters) => {
    setLoading(true)
    setError('')
    const params = {}
    Object.entries(nextFilters).forEach(([key, value]) => {
      if (value) params[key] = value
    })
    try {
      const { data } = await api.get('/threats', { params })
      setRows(data)
      if (data.length === 0) {
        toast.info('No threats found for the current filters.')
      }
    } catch (requestError) {
      setError(requestError?.response?.data?.detail || 'Threats could not be loaded. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchRows()
  }, [])

  const updateFilter = (field, value) => {
    const nextFilters = { ...filters, [field]: value }
    setFilters(nextFilters)
    fetchRows(nextFilters)
  }

  const resetFilters = () => {
    const cleared = { severity: '', ioc_type: '', source: '', search: '' }
    setFilters(cleared)
    fetchRows(cleared)
  }

  const columns = useMemo(
    () => [
      { key: 'ioc_value', label: 'IOC Value' },
      { key: 'ioc_type', label: 'Type' },
      { key: 'source', label: 'Source' },
      { key: 'confidence', label: 'Confidence', render: (row) => `${Math.round(row.confidence)}%` },
      { key: 'risk_score', label: 'Risk Score', render: (row) => Math.round(row.risk_score) },
      { key: 'severity', label: 'Severity', render: (row) => <SeverityBadge severity={row.severity} /> },
      { key: 'first_seen', label: 'First Seen', render: (row) => new Date(row.first_seen).toLocaleDateString() },
      { key: 'last_seen', label: 'Last Seen', render: (row) => new Date(row.last_seen).toLocaleDateString() },
    ],
    [],
  )

  return (
    <div className="page-stack">
      <PageHeader
        title="Threat Explorer"
        subtitle="Explore, filter, and analyze collected threat intelligence indicators."
        actions={<button type="button" className="secondary-button" onClick={() => window.open('/api/exports/iocs.csv', '_blank')}>Export IOC CSV</button>}
      />

      <section className="panel">
        <div className="panel-head compact">
          <div>
            <h3>Filters</h3>
            <p>Search IOC records by severity, IOC type, source, and keyword</p>
          </div>
        </div>

        <motion.div className="filter-row" layout transition={{ duration: 0.18 }}>
          <input placeholder="Search IOC value" value={filters.search} onChange={(event) => updateFilter('search', event.target.value)} />
          <select value={filters.severity} onChange={(event) => updateFilter('severity', event.target.value)}>
            <option value="">All Severities</option>
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
            <option value="Critical">Critical</option>
          </select>
          <select value={filters.ioc_type} onChange={(event) => updateFilter('ioc_type', event.target.value)}>
            <option value="">All Types</option>
            <option value="IP">IP</option>
            <option value="Domain">Domain</option>
            <option value="URL">URL</option>
            <option value="Hash">Hash</option>
          </select>
          <select value={filters.source} onChange={(event) => updateFilter('source', event.target.value)}>
            <option value="">All Sources</option>
            <option value="VirusTotal">VirusTotal</option>
            <option value="AbuseIPDB">AbuseIPDB</option>
            <option value="AlienVault OTX">AlienVault OTX</option>
            <option value="InternetDB">InternetDB</option>
          </select>
          <button type="button" className="secondary-button" onClick={resetFilters}>Reset Filters</button>
        </motion.div>

        {loading ? <div className="table-skeleton"><LoadingSkeleton lines={5} height={20} /></div> : null}
        {error ? <div className="form-alert">{error}</div> : null}

        <DataTable
          columns={columns}
          rows={rows}
          emptyMessage="No IOC records match the selected filters."
          onRowClick={(row) => setSelectedThreat(row)}
        />
      </section>

      <ThreatDetailsDrawer threat={selectedThreat} open={Boolean(selectedThreat)} onClose={() => setSelectedThreat(null)} />
    </div>
  )
}

export default ThreatExplorerPage
