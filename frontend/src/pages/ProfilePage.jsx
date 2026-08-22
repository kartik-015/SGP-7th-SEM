import React from 'react'
import { useAuth } from '../context/AuthContext'

function ProfilePage() {
  const { user } = useAuth()

  return (
    <div className="page-stack">
      <section className="panel profile-panel">
        <div className="panel-head compact">
          <div>
            <h3>Profile</h3>
            <p>Authenticated account details</p>
          </div>
        </div>

        <div className="profile-grid">
          <div>
            <span>Full Name</span>
            <strong>{user?.full_name}</strong>
          </div>
          <div>
            <span>Email</span>
            <strong>{user?.email}</strong>
          </div>
          <div>
            <span>Role</span>
            <strong>{user?.role}</strong>
          </div>
          <div>
            <span>Status</span>
            <strong>{user?.is_active ? 'Active' : 'Inactive'}</strong>
          </div>
        </div>
      </section>
    </div>
  )
}

export default ProfilePage
