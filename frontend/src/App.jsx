import React, { useState, useEffect } from 'react'
import './App.css'
import Sidebar from './components/Sidebar'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Stats from './pages/Stats'
import Playlists from './pages/Playlists'
import Blend from './pages/Blend'
import Agent from './pages/Agent'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [currentPage, setCurrentPage] = useState('dashboard')
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if user is logged in on mount
    const storedUser = localStorage.getItem('user')
    const storedAccessToken = localStorage.getItem('accessToken')
    
    if (storedUser && storedAccessToken) {
      setUser(JSON.parse(storedUser))
      setIsLoggedIn(true)
    }
    setLoading(false)
  }, [])

  const handleLogin = (userData, accessToken) => {
    localStorage.setItem('user', JSON.stringify(userData))
    localStorage.setItem('accessToken', accessToken)
    localStorage.setItem('userId', userData.id)
    setUser(userData)
    setIsLoggedIn(true)
    setCurrentPage('dashboard')
  }

  const handleLogout = () => {
    localStorage.removeItem('user')
    localStorage.removeItem('accessToken')
    localStorage.removeItem('userId')
    setUser(null)
    setIsLoggedIn(false)
    setCurrentPage('dashboard')
  }

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard user={user} />
      case 'stats':
        return <Stats user={user} />
      case 'playlists':
        return <Playlists user={user} />
      case 'blend':
        return <Blend user={user} />
      case 'agent':
        return <Agent user={user} />
      default:
        return <Dashboard user={user} />
    }
  }

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  if (!isLoggedIn) {
    return <Login onLogin={handleLogin} />
  }

  return (
    <div className="app">
      <Sidebar currentPage={currentPage} onNavigate={setCurrentPage} onLogout={handleLogout} user={user} />
      <div className="main-content">
        {renderPage()}
      </div>
    </div>
  )
}

export default App
