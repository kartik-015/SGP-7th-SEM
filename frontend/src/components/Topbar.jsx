import React, { useEffect, useState } from 'react'
import { Bell, Menu, Search, Shield } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
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
  const navigate = useNavigate()
  const [now, setNow] = useState(new Date())

  useEffect(() => {
    const timer = setInterval(() => setNow(new Date()), 60000)
    return () => clearInterval(timer)
  }, [])

  useEffect(() => {
    const handleShortcut = (event) => {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
        event.preventDefault()
        navigate('/search')
      }
    }

    window.addEventListener('keydown', handleShortcut)
    return () => window.removeEventListener('keydown', handleShortcut)
  }, [navigate])

  return (
    <header className="topbar">
      <button type="button" className="header-menu-button" onClick={() => setMobileSidebarOpen(true)} aria-label="Open navigation">
        <Menu size={18} />
      </button>
      <div>
        <div className="eyebrow">{user?.role === 'Administrator' ? 'Security operations control' : 'Cyber threat intelligence'}</div>
        <h1>{user?.role === 'Administrator' ? 'Governance and access control' : 'Operational threat monitoring'}</h1>
        <p>{user?.role === 'Administrator' ? 'Manage people, permissions, and accountability across the intelligence workspace' : 'Consolidated intelligence, enrichment, and review workflows in one secure workspace'}</p>
      </div>

      <div className="topbar-meta">
        <button type="button" className="search-shortcut" onClick={() => navigate('/search')} aria-label="Open IOC search">
          <Search size={14} />
          <span>Search</span>
          <kbd>Ctrl K</kbd>
        </button>
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
