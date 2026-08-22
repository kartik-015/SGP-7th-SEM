import React, { useMemo, useState } from 'react'
import { motion } from 'framer-motion'
import { ArrowRight, ScanSearch } from 'lucide-react'
import api from '../services/api'
import SeverityBadge from '../components/SeverityBadge'
import PageHeader from '../components/PageHeader'
import LoadingSkeleton from '../components/LoadingSkeleton'
import RiskMeter from '../components/RiskMeter'
import { useToast } from '../context/ToastContext'

function SearchPage() {
  const toast = useToast()
  const [ioc, setIoc] = useState('8.8.8.8')
  const [result, setResult] = useState(null)
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSearch = async (event) => {
    event.preventDefault()
    setLoading(true)
    setMessage('')
    setResult(null)
    try {
      const { data } = await api.post('/search/ioc', { ioc })
      setResult(data)
      toast.success('Threat intelligence lookup complete')
      if (!data.local_matches.length && !data.internetdb) {
        setMessage('No threat intelligence data was found for this indicator.')
      }
    } catch (error) {
      const detail = error?.response?.data?.detail || 'No threat intelligence data was found for this indicator.'
      setMessage(detail)
      toast.error(detail)
    } finally {
      setLoading(false)
    }
  }

  const localMatch = result?.local_matches?.[0]
  const internetdb = result?.internetdb
  const riskScore = localMatch?.risk_score ?? (internetdb?.ports?.length ? 72 : 0)
  const tags = useMemo(() => internetdb?.tags || [], [internetdb])

  return (
    <div className="page-stack">
      <PageHeader
        title="IOC Intelligence Search"
        subtitle="Search and enrich IP addresses, domains, URLs, and file hashes."
      />

      <section className="panel search-hero-panel">
        <div className="panel-head compact">
          <div>
            <h3>Intelligence lookup</h3>
            <p>Press Enter or click search to inspect local data and InternetDB enrichment</p>
          </div>
        </div>

        <form className="search-form" onSubmit={handleSearch}>
          <div className="search-input-wrap">
            <ScanSearch size={18} />
            <input value={ioc} onChange={(event) => setIoc(event.target.value)} placeholder="Enter IP address, domain, URL, or file hash..." />
          </div>
          <button type="submit" className="primary-button" disabled={loading}>
            {loading ? <span className="button-spinner" /> : <ArrowRight size={16} />}
            {loading ? 'Looking up intelligence' : 'Search intelligence'}
          </button>
        </form>

        {message && <div className="form-alert">{message}</div>}
      </section>

      {loading ? (
        <section className="grid-two">
          <LoadingSkeleton className="search-skeleton" lines={8} height={18} />
          <LoadingSkeleton className="search-skeleton" lines={8} height={18} />
        </section>
      ) : null}

      {result && (
        <motion.section className="search-results-grid" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.2 }}>
          <article className="panel search-summary-card">
            <div className="panel-head compact">
              <div>
                <h3>IOC Overview</h3>
                <p>Primary intelligence and risk summary</p>
              </div>
            </div>
            <div className="summary-ioc">{localMatch?.ioc_value || result.query}</div>
            <div className="summary-meta">
              <div><span>Type</span><strong>{localMatch?.ioc_type || result.ioc_type}</strong></div>
              <div><span>Source</span><strong>{localMatch?.source || 'InternetDB'}</strong></div>
              <div><span>Severity</span><SeverityBadge severity={localMatch?.severity || 'Medium'} /></div>
            </div>
            <RiskMeter score={riskScore} />
          </article>

          <article className="panel">
            <div className="panel-head compact"><div><h3>Threat Intelligence</h3><p>Hostnames, ports, tags, CPEs, and known vulnerabilities</p></div></div>
            {internetdb ? (
              <div className="intel-sections">
                <div className="intel-section"><span>Hostnames</span><p>{internetdb.hostnames.length ? internetdb.hostnames.join(', ') : 'None reported'}</p></div>
                <div className="intel-section"><span>Open Ports</span><div className="chip-list">{internetdb.ports.length ? internetdb.ports.map((port) => <span className="chip" key={port}>{port}</span>) : <span className="detail-empty">None reported</span>}</div></div>
                <div className="intel-section"><span>Known Vulnerabilities</span><p>{internetdb.vulnerabilities.length ? internetdb.vulnerabilities.join(', ') : 'None reported'}</p></div>
                <div className="intel-section"><span>CPE Information</span><p>{internetdb.cpes.length ? internetdb.cpes.join(', ') : 'None reported'}</p></div>
                <div className="intel-section"><span>Tags</span><div className="chip-list">{tags.length ? tags.map((tag) => <span key={tag} className="pill">{tag}</span>) : <span className="detail-empty">None reported</span>}</div></div>
              </div>
            ) : (
              <p className="empty-state">No InternetDB information was found for this IP address.</p>
            )}
          </article>
        </motion.section>
      )}
    </div>
  )
}

export default SearchPage
