import React from 'react'
import './Sidebar.css'

function Sidebar({ currentPage, onNavigate, onLogout, user }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="logo">
          <span className="logo-icon">🎧</span>
          <h1>SpotiAI</h1>
        </div>
      </div>

      <nav className="sidebar-nav">
        <button
          className={`nav-item ${currentPage === 'dashboard' ? 'active' : ''}`}
          onClick={() => onNavigate('dashboard')}
        >
          <span className="nav-icon">🏠</span>
          <span className="nav-label">Dashboard</span>
        </button>

        <button
          className={`nav-item ${currentPage === 'stats' ? 'active' : ''}`}
          onClick={() => onNavigate('stats')}
        >
          <span className="nav-icon">📊</span>
          <span className="nav-label">Stats</span>
        </button>

        <button
          className={`nav-item ${currentPage === 'playlists' ? 'active' : ''}`}
          onClick={() => onNavigate('playlists')}
        >
          <span className="nav-icon">🎵</span>
          <span className="nav-label">Playlists</span>
        </button>

        <button
          className={`nav-item ${currentPage === 'blend' ? 'active' : ''}`}
          onClick={() => onNavigate('blend')}
        >
          <span className="nav-icon">🔄</span>
          <span className="nav-label">Blend</span>
        </button>

        <button
          className={`nav-item ${currentPage === 'agent' ? 'active' : ''}`}
          onClick={() => onNavigate('agent')}
        >
          <span className="nav-icon">🤖</span>
          <span className="nav-label">AI Agent</span>
        </button>
      </nav>

      <div className="sidebar-footer">
        {user && (
          <div className="user-info">
            <p className="user-name">{user.display_name}</p>
            <p className="user-plan">{user.plan_type || 'User'}</p>
          </div>
        )}
        <button className="logout-btn" onClick={onLogout}>
          🚪 Logout
        </button>
      </div>
    </aside>
  )
}

export default Sidebar
