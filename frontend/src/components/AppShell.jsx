import React from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { useLocation, useOutlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import Topbar from './Topbar'
import { useAuth } from '../context/AuthContext'

function AppShell() {
  const { user } = useAuth()
  const location = useLocation()
  const outlet = useOutlet()
  const isAdmin = user?.role === 'Administrator'

  return (
    <div className={`app-shell ${isAdmin ? 'admin-mode' : 'analyst-mode'}`}>
      <Sidebar />
      <div className="app-main">
        <Topbar />
        <main className="page-content">
          <AnimatePresence mode="wait">
            <motion.div
              key={location.pathname}
              className="route-stage"
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -6 }}
              transition={{ duration: 0.18 }}
            >
              {outlet}
            </motion.div>
          </AnimatePresence>
        </main>
      </div>
    </div>
  )
}

export default AppShell
