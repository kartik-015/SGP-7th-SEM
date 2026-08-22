import React from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import SeverityBadge from './SeverityBadge'
import RiskMeter from './RiskMeter'

function ChipList({ items }) {
  if (!items?.length) return <span className="detail-empty">None reported</span>
  return (
    <div className="chip-list">
      {items.map((item) => (
        <span key={item} className="chip">{item}</span>
      ))}
    </div>
  )
}

function ThreatDetailsDrawer({ threat, open, onClose }) {
  return (
    <AnimatePresence>
      {open && threat ? (
        <>
          <motion.div
            className="drawer-backdrop"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.18 }}
            onClick={onClose}
          />
          <motion.aside
            className="drawer-panel"
            initial={{ x: 420 }}
            animate={{ x: 0 }}
            exit={{ x: 420 }}
            transition={{ type: 'spring', stiffness: 280, damping: 32 }}
          >
            <div className="drawer-header">
              <div>
                <h3>Threat Overview</h3>
                <p>{threat.ioc_value}</p>
              </div>
              <button type="button" className="secondary-button small" onClick={onClose}>Close</button>
            </div>

            <div className="drawer-summary">
              <div><span>Type</span><strong>{threat.ioc_type}</strong></div>
              <div><span>Risk Score</span><strong>{Math.round(threat.risk_score)}</strong></div>
              <div><span>Severity</span><SeverityBadge severity={threat.severity} /></div>
              <div><span>Confidence</span><strong>{Math.round(threat.confidence)}%</strong></div>
            </div>

            <div className="drawer-section">
              <h4>Details</h4>
              <div className="drawer-grid">
                <div><span>Source</span><strong>{threat.source}</strong></div>
                <div><span>First Seen</span><strong>{new Date(threat.first_seen).toLocaleString()}</strong></div>
                <div><span>Last Seen</span><strong>{new Date(threat.last_seen).toLocaleString()}</strong></div>
                <div className="drawer-description"><span>Description</span><p>{threat.description || 'No description available.'}</p></div>
              </div>
            </div>

            <div className="drawer-section">
              <h4>Risk Assessment</h4>
              <RiskMeter score={threat.risk_score} />
            </div>

            <div className="drawer-section">
              <h4>Network Exposure</h4>
              <div className="drawer-grid compact">
                <div><span>Open Ports</span><ChipList items={threat.raw_metadata?.ports?.map(String)} /></div>
                <div><span>Hostnames</span><ChipList items={threat.raw_metadata?.hostnames} /></div>
                <div><span>Tags</span><ChipList items={threat.raw_metadata?.tags} /></div>
                <div><span>CPEs</span><ChipList items={threat.raw_metadata?.cpes} /></div>
                <div><span>Known Vulnerabilities</span><ChipList items={threat.raw_metadata?.vulnerabilities} /></div>
              </div>
            </div>
          </motion.aside>
        </>
      ) : null}
    </AnimatePresence>
  )
}

export default ThreatDetailsDrawer