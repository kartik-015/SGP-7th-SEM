import React from 'react'
import { Activity, AlertTriangle, ChevronLeft, ChevronRight, FileSearch, LayoutDashboard, LogOut, Shield, UserRound, UsersRound } from 'lucide-react'
import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useUI } from '../context/UIContext'

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/threats', label: 'Threat Explorer', icon: Shield },
  { to: '/search', label: 'IOC Search', icon: FileSearch },
  { to: '/alerts', label: 'Alerts', icon: AlertTriangle },
  { to: '/profile', label: 'Profile', icon: UserRound },
]

function Sidebar() {
  const { logout, user } = useAuth()
  const { sidebarCollapsed, setSidebarCollapsed, mobileSidebarOpen, setMobileSidebarOpen } = useUI()
  const navigate = useNavigate()
  const collapsed = sidebarCollapsed

  return (
    <>
      <button type="button" className="mobile-sidebar-toggle" onClick={() => setMobileSidebarOpen(true)} aria-label="Open navigation">
        <LayoutDashboard size={18} />
      </button>
      <aside className={`sidebar ${user?.role === 'Administrator' ? 'sidebar-admin' : 'sidebar-analyst'} ${collapsed ? 'collapsed' : ''} ${mobileSidebarOpen ? 'mobile-open' : ''}`}>
        <div className="sidebar-top">
          <button type="button" className="brand-block" onClick={() => navigate('/dashboard')} aria-label="Go to Dashboard">
            <div className="brand-mark">CI</div>
            {!collapsed && (
              <div>
                <div className="brand-title">CYBER INTELLIGENCE</div>
                <div className="brand-subtitle">Threat Operations Platform</div>
              </div>
            )}
          </button>
          <button type="button" className="collapse-button" onClick={() => setSidebarCollapsed((value) => !value)} aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}>
            {collapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
          </button>
        </div>

        <nav className="sidebar-nav">
          {navItems.map((item) => {
            const Icon = item.icon
            return (
              <NavLink key={item.to} to={item.to} className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`} onClick={() => setMobileSidebarOpen(false)}>
                <Icon size={18} />
                {!collapsed && <span>{item.label}</span>}
              </NavLink>
            )
          })}
        </nav>

        {user?.role === 'Administrator' && !collapsed && (
          <NavLink to="/admin" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`} onClick={() => setMobileSidebarOpen(false)}>
            <UsersRound size={18} />
            <span>Admin Console</span>
          </NavLink>
        )}

        <div className="sidebar-footer">
          <div className="sidebar-user">
            <div className="avatar">{user?.full_name?.slice(0, 1) || 'U'}</div>
            {!collapsed && (
              <div>
                <strong>{user?.full_name}</strong>
                <span>{user?.role === 'Administrator' ? 'Operations administrator' : 'Threat analyst'}</span>
              </div>
            )}
          </div>
          <button
            type="button"
            className="logout-button"
            onClick={() => {
              logout()
              navigate('/login')
            }}
          >
            <LogOut size={18} />
            {!collapsed && 'Logout'}
          </button>
        </div>
      </aside>
      {mobileSidebarOpen ? <button type="button" className="sidebar-overlay" onClick={() => setMobileSidebarOpen(false)} aria-label="Close navigation" /> : null}
    </>
  )
}

export default Sidebar
