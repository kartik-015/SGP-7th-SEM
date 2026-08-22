import React from 'react'

function StatCard({ title, value, helper, accent }) {
  return (
    <article className="stat-card" style={{ '--accent': accent }}>
      <div className="stat-label">{title}</div>
      <div className="stat-value">{value}</div>
      <div className="stat-helper">{helper}</div>
    </article>
  )
}

export default StatCard
