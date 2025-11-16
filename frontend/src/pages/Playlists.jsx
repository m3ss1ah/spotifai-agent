import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './Playlists.css'

const BACKEND_URL = 'http://127.0.0.1:8000'

function Playlists({ user }) {
  const [playlists, setPlaylists] = useState([])
  const [loading, setLoading] = useState(true)
  const [creating, setCreating] = useState(false)
  const [newPlaylist, setNewPlaylist] = useState({
    name: '',
    description: '',
    public: false
  })
  const [selectedPlaylist, setSelectedPlaylist] = useState(null)
  const [playlistTracks, setPlaylistTracks] = useState([])

  useEffect(() => {
    if (user) {
      fetchPlaylists()
    }
  }, [user])

  const fetchPlaylists = async () => {
    try {
      setLoading(true)
      const userId = localStorage.getItem('userId')
      const accessToken = localStorage.getItem('accessToken')

      const response = await axios.get(`${BACKEND_URL}/playlists`, {
        params: { user_id: userId },
        headers: { Authorization: `Bearer ${accessToken}` }
      })

      setPlaylists(response.data.playlists)
    } catch (err) {
      console.error('Failed to load playlists:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleCreatePlaylist = async (e) => {
    e.preventDefault()
    try {
      setCreating(true)
      const userId = localStorage.getItem('userId')
      const accessToken = localStorage.getItem('accessToken')

      const response = await axios.post(
        `${BACKEND_URL}/playlists/create`,
        newPlaylist,
        {
          params: { user_id: userId },
          headers: { Authorization: `Bearer ${accessToken}` }
        }
      )

      setPlaylists([...playlists, response.data])
      setNewPlaylist({ name: '', description: '', public: false })
      alert('Playlist created successfully!')
    } catch (err) {
      console.error('Failed to create playlist:', err)
      alert('Failed to create playlist')
    } finally {
      setCreating(false)
    }
  }

  const handleSelectPlaylist = async (playlist) => {
    try {
      setSelectedPlaylist(playlist)
      const userId = localStorage.getItem('userId')
      const accessToken = localStorage.getItem('accessToken')

      const response = await axios.get(
        `${BACKEND_URL}/playlists/${playlist.id}/tracks`,
        {
          params: { user_id: userId },
          headers: { Authorization: `Bearer ${accessToken}` }
        }
      )

      setPlaylistTracks(response.data.tracks)
    } catch (err) {
      console.error('Failed to load playlist tracks:', err)
    }
  }

  if (loading) return <div className="playlists-loading">Loading playlists...</div>

  return (
    <div className="playlists-page">
      <div className="playlists-header">
        <h1>Your Playlists 🎵</h1>
        <p>Manage and explore your Spotify playlists</p>
      </div>

      <div className="playlists-content">
        {/* Create Playlist Form */}
        <section className="create-playlist-section">
          <h2>Create New Playlist</h2>
          <form onSubmit={handleCreatePlaylist} className="playlist-form">
            <input
              type="text"
              placeholder="Playlist name"
              value={newPlaylist.name}
              onChange={(e) => setNewPlaylist({ ...newPlaylist, name: e.target.value })}
              required
            />
            <textarea
              placeholder="Description (optional)"
              value={newPlaylist.description}
              onChange={(e) => setNewPlaylist({ ...newPlaylist, description: e.target.value })}
            />
            <label>
              <input
                type="checkbox"
                checked={newPlaylist.public}
                onChange={(e) => setNewPlaylist({ ...newPlaylist, public: e.target.checked })}
              />
              Make public
            </label>
            <button type="submit" disabled={creating} className="create-btn">
              {creating ? 'Creating...' : 'Create Playlist'}
            </button>
          </form>
        </section>

        {/* Playlists Grid */}
        <section className="playlists-grid-section">
          <h2>Your Playlists ({playlists.length})</h2>
          <div className="playlists-grid">
            {playlists.map((playlist) => (
              <div
                key={playlist.id}
                className={`playlist-card ${selectedPlaylist?.id === playlist.id ? 'selected' : ''}`}
                onClick={() => handleSelectPlaylist(playlist)}
              >
                <div className="playlist-cover">🎵</div>
                <h3>{playlist.name}</h3>
                <p className="playlist-tracks">{playlist.track_count} tracks</p>
                <p className="playlist-visibility">
                  {playlist.public ? '🌐 Public' : '🔒 Private'}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* Playlist Details */}
        {selectedPlaylist && (
          <section className="playlist-details-section">
            <h2>Tracks in "{selectedPlaylist.name}"</h2>
            <div className="playlist-tracks-list">
              {playlistTracks.length > 0 ? (
                playlistTracks.map((track, idx) => (
                  <div key={idx} className="playlist-track-item">
                    <span className="track-num">{idx + 1}</span>
                    <div className="track-info">
                      <h4>{track.name}</h4>
                      <p>{track.artists.join(', ')}</p>
                    </div>
                  </div>
                ))
              ) : (
                <p className="no-tracks">No tracks in this playlist</p>
              )}
            </div>
          </section>
        )}
      </div>
    </div>
  )
}

export default Playlists
