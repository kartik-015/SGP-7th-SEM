export const severityColors = {
  Low: '#2dd4bf',
  Medium: '#fbbf24',
  High: '#fb923c',
  Critical: '#ef4444',
}

export function getSeverityTone(severity) {
  return severityColors[severity] || '#94a3b8'
}
