import React from 'react'

function LoadingSkeleton({ className = '', lines = 1, height = 18 }) {
  return (
    <div className={`skeleton-wrap ${className}`} aria-hidden="true">
      {Array.from({ length: lines }).map((_, index) => (
        <div key={index} className="skeleton-line" style={{ height }} />
      ))}
    </div>
  )
}

export default LoadingSkeleton