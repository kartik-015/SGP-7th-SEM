import React from 'react'

function RiskMeter({ score }) {
  const value = Math.max(0, Math.min(Number(score ?? 0), 100))
  return (
    <div className="risk-meter">
      <div className="risk-meter-track">
        <div className="risk-meter-fill" style={{ width: `${value}%` }} />
      </div>
      <div className="risk-meter-meta">
        <strong>{Math.round(value)} / 100</strong>
        <span>{value >= 75 ? 'CRITICAL' : value >= 50 ? 'HIGH RISK' : value >= 25 ? 'MODERATE' : 'LOW RISK'}</span>
      </div>
    </div>
  )
}

export default RiskMeter