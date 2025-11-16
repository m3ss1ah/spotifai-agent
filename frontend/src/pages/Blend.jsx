import React, { useState } from 'react'
import axios from 'axios'
import './Blend.css'

const BACKEND_URL = 'http://127.0.0.1:8000'

function Blend({ user }) {
  const [otherUserId, setOtherUserId] = useState('')
  const [blendData, setBlendData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleCreateBlend = async (e) => {
    e.preventDefault()
    try {
      setLoading(true)
      setError(null)

      const userId = localStorage.getItem('userId')

      const response = await axios.post(`${BACKEND_URL}/blend`, {
        user_id1: userId,
        user_id2: otherUserId,
        playlist_name: `${user.display_name} & Other Blend`
      })

      setBlendData(response.data)
    } catch (err) {
      setError('Failed to create blend. Make sure the user ID is correct.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="blend-page">
      <div className="blend-header">
        <h1>Blend Music Taste 🔄</h1>
        <p>Compare and combine your music with another user</p>
      </div>

      <div className="blend-content">
        <form onSubmit={handleCreateBlend} className="blend-form">
          <div className="form-group">
            <label>Your User ID</label>
            <input
              type="text"
              value={localStorage.getItem('userId')}
              disabled
              className="disabled-input"
            />
          </div>

          <div className="form-group">
            <label>Their Spotify User ID</label>
            <input
              type="text"
              placeholder="Enter Spotify username or user ID"
              value={otherUserId}
              onChange={(e) => setOtherUserId(e.target.value)}
              required
            />
          </div>

          <button type="submit" disabled={loading || !otherUserId} className="blend-btn">
            {loading ? 'Creating Blend...' : '🎵 Create Blend'}
          </button>
        </form>

        {error && <div className="blend-error">{error}</div>}

        {blendData && (
          <div className="blend-results">
            <div className="blend-header-result">
              <h2>{blendData.user1} + {blendData.user2}</h2>
              <p className="similarity">Music Similarity: {(blendData.similarity_score * 100).toFixed(0)}%</p>
            </div>

            {/* Venn Diagram representation */}
            <div className="venn-section">
              <h3>Genre Overlap</h3>
              <div className="venn-diagram">
                <div className="venn-left">
                  <p className="venn-title">{blendData.user1}</p>
                  <div className="genres-list">
                    {blendData.user1_unique_genres?.slice(0, 5).map((genre, idx) => (
                      <span key={idx} className="genre-tag">{genre}</span>
                    ))}
                  </div>
                </div>

                <div className="venn-center">
                  <p className="venn-title">Shared</p>
                  <div className="genres-list">
                    {blendData.shared_genres?.slice(0, 5).map((genre, idx) => (
                      <span key={idx} className="genre-tag shared">{genre}</span>
                    ))}
                  </div>
                </div>

                <div className="venn-right">
                  <p className="venn-title">{blendData.user2}</p>
                  <div className="genres-list">
                    {blendData.user2_unique_genres?.slice(0, 5).map((genre, idx) => (
                      <span key={idx} className="genre-tag">{genre}</span>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Recommendations */}
            <section className="recommendations-section">
              <h3>🎵 Blend Recommendations</h3>
              <div className="recommendations-list">
                {blendData.recommendations?.slice(0, 20).map((track, idx) => (
                  <div key={idx} className="rec-track">
                    <span className="rec-num">{idx + 1}</span>
                    <div className="rec-info">
                      <h4>{track.name}</h4>
                      <p>{track.artists.join(', ')}</p>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          </div>
        )}
      </div>
    </div>
  )
}

export default Blend
