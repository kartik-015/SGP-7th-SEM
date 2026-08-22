import React, { useEffect, useState } from 'react'
import { Bell, Menu, Search, Shield } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { useUI } from '../context/UIContext'

function formatDateTime(date) {
  return new Intl.DateTimeFormat('en-US', {
    weekday: 'short',
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date)
}

function Topbar() {
  const { user } = useAuth()
  const { setMobileSidebarOpen } = useUI()
  const [now, setNow] = useState(new Date())

  useEffect(() => {
    const timer = setInterval(() => setNow(new Date()), 60000)
    return () => clearInterval(timer)
  }, [])

  return (
    <header className="topbar">
      <button type="button" className="header-menu-button" onClick={() => setMobileSidebarOpen(true)} aria-label="Open navigation">
        <Menu size={18} />
      </button>
      <div>
        <div className="eyebrow">Cyber Threat Intelligence</div>
        <h1>Operational threat monitoring</h1>
        <p>Consolidated intelligence, enrichment, and review workflows in one secure workspace</p>
      </div>

      <div className="topbar-meta">
        <div className="search-shortcut">
          <Search size={14} />
          <span>Search</span>
          <kbd>Ctrl K</kbd>
        </div>
        <div className="user-chip">
          <Shield size={16} />
          <span>{user?.full_name}</span>
          <span className="role-pill">{user?.role}</span>
        </div>
        <div className="user-chip ghost">
          <Bell size={16} />
          <span>{formatDateTime(now)}</span>
        </div>
      </div>
    </header>
  )
}

export default Topbar
