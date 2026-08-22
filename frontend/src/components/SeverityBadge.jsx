import React from 'react'
import { getSeverityTone } from '../utils/severity'

function SeverityBadge({ severity }) {
  return (
    <span className="severity-badge" style={{ backgroundColor: `${getSeverityTone(severity)}22`, color: getSeverityTone(severity) }}>
      {severity}
    </span>
  )
}

export default SeverityBadge
