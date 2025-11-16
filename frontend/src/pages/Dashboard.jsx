import React, { useState, useEffect } from 'react'
import axios from 'axios'
import UserCard from '../components/UserCard'
import './Dashboard.css'

const BACKEND_URL = 'http://127.0.0.1:8000'

function Dashboard({ user }) {
  const [profileData, setProfileData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (user) {
      fetchProfileData()
    }
  }, [user])

  const fetchProfileData = async () => {
    try {
      setLoading(true)
      setError(null)

      const userId = localStorage.getItem('userId')
      const accessToken = localStorage.getItem('accessToken')

      const response = await axios.get(`${BACKEND_URL}/user/profile`, {
        params: { user_id: userId },
        headers: { Authorization: `Bearer ${accessToken}` }
      })

      setProfileData(response.data)
    } catch (err) {
      setError('Failed to load profile')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="dashboard-loading">Loading profile...</div>
  }

  if (error) {
    return <div className="dashboard-error">{error}</div>
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Welcome, {user?.display_name || 'User'}! 🎵</h1>
        <p>Your Spotify AI Assistant Dashboard</p>
      </div>

      {profileData && (
        <div className="dashboard-content">
          <UserCard user={profileData} />

          <div className="dashboard-grid">
            <div className="stat-card">
              <div className="stat-icon">📊</div>
              <h3>Listening Stats</h3>
              <p className="stat-value">{profileData.listening_stats?.total_tracks || 0}</p>
              <p className="stat-label">Top Tracks</p>
              <p className="stat-detail">Avg Popularity: {(profileData.listening_stats?.avg_popularity || 0).toFixed(0)}</p>
            </div>

            <div className="stat-card">
              <div className="stat-icon">🎤</div>
              <h3>Top Artists</h3>
              <p className="stat-value">{profileData.top_artists?.length || 0}</p>
              <p className="stat-label">Tracked</p>
              {profileData.top_artists?.length > 0 && (
                <p className="stat-detail">Top: {profileData.top_artists[0]?.name}</p>
              )}
            </div>

            <div className="stat-card">
              <div className="stat-icon">🎸</div>
              <h3>Top Genres</h3>
              <p className="stat-value">{profileData.top_genres?.length || 0}</p>
              <p className="stat-label">Genres</p>
              {profileData.top_genres?.length > 0 && (
                <p className="stat-detail">{profileData.top_genres.slice(0, 3).join(', ')}</p>
              )}
            </div>

            <div className="stat-card">
              <div className="stat-icon">👥</div>
              <h3>Followers</h3>
              <p className="stat-value">{profileData.followers?.toLocaleString() || 0}</p>
              <p className="stat-label">Total</p>
              <p className="stat-detail">Plan: {profileData.plan_type?.toUpperCase()}</p>
            </div>
          </div>

          <div className="top-tracks-section">
            <h2>Your Top Tracks</h2>
            <div className="tracks-list">
              {profileData.top_tracks?.slice(0, 10).map((track, idx) => (
                <div key={idx} className="track-item">
                  <div className="track-number">{idx + 1}</div>
                  <div className="track-info">
                    <h4>{track.name}</h4>
                    <p>{track.artists.join(', ')}</p>
                  </div>
                  <div className="track-popularity">
                    <div className="popularity-bar" style={{ width: track.popularity + '%' }}></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Dashboard
