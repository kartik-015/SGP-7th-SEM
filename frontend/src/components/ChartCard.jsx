import React from 'react'

function ChartCard({ title, subtitle, children, className = '' }) {
  return (
    <section className={`panel chart-card ${className}`}>
      <div className="panel-head">
        <div>
          <h3>{title}</h3>
          <p>{subtitle}</p>
        </div>
      </div>
      <div className="chart-body">{children}</div>
    </section>
  )
}

export default ChartCard
