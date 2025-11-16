import React, { useState } from 'react'
import axios from 'axios'
import './Agent.css'

const BACKEND_URL = 'http://127.0.0.1:8000'

function Agent({ user }) {
  const [activeTab, setActiveTab] = useState('playlist')
  const [loading, setLoading] = useState(false)
  const [playlistName, setPlaylistName] = useState('')
  const [playlist, setPlaylist] = useState(null)
  const [mood, setMood] = useState(null)
  const [summary, setSummary] = useState(null)
  const [playlistFix, setPlaylistFix] = useState(null)
  const [customPrompt, setCustomPrompt] = useState('')
  const [chatMessages, setChatMessages] = useState([])

  const userId = localStorage.getItem('userId')
  const accessToken = localStorage.getItem('accessToken')

  const handleGeneratePlaylist = async (e) => {
    e.preventDefault()
    try {
      setLoading(true)
      const response = await axios.post(`${BACKEND_URL}/ai/playlist`, {
        user_id: userId,
        prompt: customPrompt || 'Generate a new playlist',
        context: { mood: customPrompt }
      }, {
        headers: { Authorization: `Bearer ${accessToken}` }
      })

      setPlaylist(response.data)
      setChatMessages([
        ...chatMessages,
        {
          type: 'user',
          text: customPrompt || 'Generate a new playlist'
        },
        {
          type: 'ai',
          text: `I've generated a playlist called "${response.data.playlist_name}" with recommendations based on your music taste!`
        }
      ])
      setCustomPrompt('')
    } catch (err) {
      console.error('Failed to generate playlist:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleAnalyzeMood = async (e) => {
    e.preventDefault()
    try {
      setLoading(true)
      const response = await axios.post(`${BACKEND_URL}/ai/mood`, {
        user_id: userId,
        prompt: 'Analyze my listening mood'
      }, {
        headers: { Authorization: `Bearer ${accessToken}` }
      })

      setMood(response.data)
      setChatMessages([
        ...chatMessages,
        {
          type: 'user',
          text: 'What is my current listening mood?'
        },
        {
          type: 'ai',
          text: response.data.mood
        }
      ])
    } catch (err) {
      console.error('Failed to analyze mood:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleGetSummary = async (e) => {
    e.preventDefault()
    try {
      setLoading(true)
      const response = await axios.post(`${BACKEND_URL}/ai/summary`, {
        user_id: userId
      }, {
        headers: { Authorization: `Bearer ${accessToken}` }
      })

      setSummary(response.data)
      setChatMessages([
        ...chatMessages,
        {
          type: 'user',
          text: 'What is my music taste profile?'
        },
        {
          type: 'ai',
          text: response.data.summary
        }
      ])
    } catch (err) {
      console.error('Failed to get summary:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleFixPlaylist = async (e) => {
    e.preventDefault()
    if (!playlistName) return

    try {
      setLoading(true)
      const response = await axios.post(`${BACKEND_URL}/ai/fix`, {
        user_id: userId,
        prompt: playlistName
      }, {
        headers: { Authorization: `Bearer ${accessToken}` }
      })

      setPlaylistFix(response.data)
      setChatMessages([
        ...chatMessages,
        {
          type: 'user',
          text: `Fix my playlist: ${playlistName}`
        },
        {
          type: 'ai',
          text: response.data.analysis
        }
      ])
      setPlaylistName('')
    } catch (err) {
      console.error('Failed to fix playlist:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="agent-page">
      <div className="agent-header">
        <h1>🤖 AI Music Assistant</h1>
        <p>Powered by LLaMA 3.2 • Chat with your music data</p>
      </div>

      <div className="agent-layout">
        {/* Chat Interface */}
        <div className="chat-panel">
          <div className="chat-messages">
            {chatMessages.length === 0 ? (
              <div className="chat-welcome">
                <p>👋 Hi! I'm your AI Music Assistant</p>
                <p>Use the tools below to interact with me about your music</p>
              </div>
            ) : (
              chatMessages.map((msg, idx) => (
                <div key={idx} className={`chat-message ${msg.type}`}>
                  <div className="message-content">
                    {msg.type === 'ai' && <span className="msg-icon">🤖</span>}
                    {msg.type === 'user' && <span className="msg-icon">👤</span>}
                    <p>{msg.text}</p>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Tools Panel */}
        <div className="tools-panel">
          <div className="tools-tabs">
            <button
              className={`tab-btn ${activeTab === 'playlist' ? 'active' : ''}`}
              onClick={() => setActiveTab('playlist')}
            >
              🎵 Generate Playlist
            </button>
            <button
              className={`tab-btn ${activeTab === 'mood' ? 'active' : ''}`}
              onClick={() => setActiveTab('mood')}
            >
              🎯 Analyze Mood
            </button>
            <button
              className={`tab-btn ${activeTab === 'fix' ? 'active' : ''}`}
              onClick={() => setActiveTab('fix')}
            >
              🛠️ Fix Playlist
            </button>
            <button
              className={`tab-btn ${activeTab === 'summary' ? 'active' : ''}`}
              onClick={() => setActiveTab('summary')}
            >
              📊 Taste Summary
            </button>
          </div>

          <div className="tools-content">
            {/* Generate Playlist */}
            {activeTab === 'playlist' && (
              <div className="tool-form">
                <h3>Generate AI Playlist</h3>
                <form onSubmit={handleGeneratePlaylist}>
                  <textarea
                    placeholder="Describe what kind of playlist you want (e.g., 'focus music for coding')"
                    value={customPrompt}
                    onChange={(e) => setCustomPrompt(e.target.value)}
                  />
                  <button type="submit" disabled={loading}>
                    {loading ? 'Generating...' : 'Generate'}
                  </button>
                </form>

                {playlist && (
                  <div className="tool-result">
                    <h4>{playlist.playlist_name}</h4>
                    <p>{playlist.description}</p>
                    <div className="rec-tracks">
                      <p className="rec-label">Top Recommendations:</p>
                      {playlist.recommendations?.slice(0, 5).map((track, idx) => (
                        <p key={idx} className="rec-track">
                          {idx + 1}. {track.name} - {track.artists.join(', ')}
                        </p>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Analyze Mood */}
            {activeTab === 'mood' && (
              <div className="tool-form">
                <h3>Analyze Your Listening Mood</h3>
                <button onClick={handleAnalyzeMood} disabled={loading} className="full-btn">
                  {loading ? 'Analyzing...' : 'Analyze My Mood'}
                </button>

                {mood && (
                  <div className="tool-result">
                    <p className="mood-analysis">{mood.mood}</p>
                    <div className="top-artists">
                      <p className="rec-label">Your Top Artists:</p>
                      {mood.top_artists?.map((artist, idx) => (
                        <p key={idx}>🎤 {artist}</p>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Fix Playlist */}
            {activeTab === 'fix' && (
              <div className="tool-form">
                <h3>Fix Your Playlist</h3>
                <form onSubmit={handleFixPlaylist}>
                  <input
                    type="text"
                    placeholder="Enter playlist name"
                    value={playlistName}
                    onChange={(e) => setPlaylistName(e.target.value)}
                  />
                  <button type="submit" disabled={loading || !playlistName}>
                    {loading ? 'Analyzing...' : 'Fix Playlist'}
                  </button>
                </form>

                {playlistFix && (
                  <div className="tool-result">
                    <p className="fix-analysis">{playlistFix.analysis}</p>
                    {playlistFix.suggestions && playlistFix.suggestions.length > 0 && (
                      <div className="suggestions">
                        <p className="rec-label">Suggestions:</p>
                        {playlistFix.suggestions.map((sug, idx) => (
                          <p key={idx}>✨ {sug}</p>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}

            {/* Taste Summary */}
            {activeTab === 'summary' && (
              <div className="tool-form">
                <h3>Your Music Taste Summary</h3>
                <button onClick={handleGetSummary} disabled={loading} className="full-btn">
                  {loading ? 'Generating...' : 'Get My Summary'}
                </button>

                {summary && (
                  <div className="tool-result">
                    <p className="summary-text">{summary.summary}</p>
                    <div className="taste-profile">
                      <h4>Your Profile</h4>
                      <p><strong>Top Artist:</strong> {summary.taste_profile?.top_artist}</p>
                      <p><strong>Favorite Track:</strong> {summary.taste_profile?.top_track}</p>
                      <p><strong>Genre Diversity:</strong> {summary.taste_profile?.diversity}</p>
                    </div>
                    <div className="genres">
                      <p className="rec-label">Top Genres:</p>
                      <div className="genre-list">
                        {summary.top_genres?.slice(0, 10).map((genre, idx) => (
                          <span key={idx} className="genre-tag">{genre}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Agent
