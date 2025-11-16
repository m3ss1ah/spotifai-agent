import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './Stats.css'

const BACKEND_URL = 'http://127.0.0.1:8000'

function Stats({ user }) {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [timeRange, setTimeRange] = useState('medium_term')

  useEffect(() => {
    if (user) {
      fetchStats()
    }
  }, [user])

  const fetchStats = async () => {
    try {
      setLoading(true)
      const userId = localStorage.getItem('userId')
      const accessToken = localStorage.getItem('accessToken')

      const response = await axios.get(`${BACKEND_URL}/user/profile`, {
        params: { user_id: userId },
        headers: { Authorization: `Bearer ${accessToken}` }
      })

      setStats(response.data)
    } catch (err) {
      console.error('Failed to load stats:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div className="stats-loading">Loading stats...</div>

  return (
    <div className="stats-page">
      <div className="stats-header">
        <h1>Your Music Statistics 📊</h1>
        <p>Deep dive into your listening habits</p>
      </div>

      <div className="stats-content">
        {/* Top Artists */}
        <section className="stats-section">
          <h2>🎤 Top Artists</h2>
          <div className="artists-grid">
            {stats?.top_artists?.slice(0, 12).map((artist, idx) => (
              <div key={idx} className="artist-card">
                <div className="artist-rank">{idx + 1}</div>
                <h3>{artist.name}</h3>
                <p className="artist-genres">{artist.genres.slice(0, 2).join(', ')}</p>
                <div className="artist-popularity">
                  <span>Popularity: {artist.popularity}%</span>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Top Genres */}
        <section className="stats-section">
          <h2>🎸 Top Genres</h2>
          <div className="genres-grid">
            {stats?.top_genres?.slice(0, 15).map((genre, idx) => (
              <div key={idx} className="genre-tag">
                <span>{genre}</span>
              </div>
            ))}
          </div>
        </section>

        {/* Listening Stats */}
        <section className="stats-section">
          <h2>📈 Listening Insights</h2>
          <div className="insights-grid">
            <div className="insight-card">
              <h3>Total Tracks</h3>
              <p className="insight-value">{stats?.listening_stats?.total_tracks || 0}</p>
            </div>
            <div className="insight-card">
              <h3>Average Popularity</h3>
              <p className="insight-value">{(stats?.listening_stats?.avg_popularity || 0).toFixed(1)}</p>
            </div>
            <div className="insight-card">
              <h3>Highest Popularity</h3>
              <p className="insight-value">{stats?.listening_stats?.max_popularity || 0}</p>
            </div>
            <div className="insight-card">
              <h3>Lowest Popularity</h3>
              <p className="insight-value">{stats?.listening_stats?.min_popularity || 0}</p>
            </div>
          </div>
        </section>

        {/* Top Tracks */}
        <section className="stats-section">
          <h2>🎵 Top Tracks</h2>
          <div className="tracks-detailed">
            {stats?.top_tracks?.slice(0, 20).map((track, idx) => (
              <div key={idx} className="track-row">
                <span className="track-rank">#{idx + 1}</span>
                <div className="track-details">
                  <h4>{track.name}</h4>
                  <p>{track.artists.join(', ')}</p>
                </div>
                <div className="track-album">{track.album}</div>
                <div className="track-pop">{track.popularity}%</div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  )
}

export default Stats
