import React, { useState } from 'react'
import axios from 'axios'
import './Login.css'

const BACKEND_URL = 'http://127.0.0.1:8000'

function Login({ onLogin }) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSpotifyLogin = async () => {
    try {
      setLoading(true)
      setError(null)

      // Get login URL from backend
      const response = await axios.get(`${BACKEND_URL}/auth/login`)
      const { auth_url, state } = response.data

      // Store state for callback validation
      sessionStorage.setItem('oauth_state', state)

      // Redirect to Spotify
      window.location.href = auth_url
    } catch (err) {
      setError('Failed to start login process')
      console.error(err)
      setLoading(false)
    }
  }

  // Check if we're returning from callback
  React.useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    const code = params.get('code')
    const state = params.get('state')

    if (code && state) {
      handleCallback(code, state)
    }
  }, [])

  const handleCallback = async (code, state) => {
    try {
      setLoading(true)
      setError(null)

      // Exchange code for tokens
      const response = await axios.get(`${BACKEND_URL}/auth/callback`, {
        params: { code, state }
      })

      const { access_token, user_id, expires_in } = response.data

      // Fetch user profile
      const profileResponse = await axios.get(`${BACKEND_URL}/user/profile`, {
        params: { user_id },
        headers: { Authorization: `Bearer ${access_token}` }
      })

      const userData = profileResponse.data

      // Call parent callback
      onLogin(userData, access_token)
    } catch (err) {
      setError('Authentication failed. Please try again.')
      console.error(err)
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-box">
        <div className="login-header">
          <h1>🎧 Spotify AI Assistant</h1>
          <p>Powered by LLaMA 3.2</p>
        </div>

        <div className="login-content">
          <p className="login-description">
            Connect your Spotify account to get started with AI-powered music recommendations,
            playlist analysis, and music taste exploration.
          </p>

          {error && <div className="login-error">{error}</div>}

          <button
            className="spotify-login-btn"
            onClick={handleSpotifyLogin}
            disabled={loading}
          >
            {loading ? 'Connecting...' : '🎵 Login with Spotify'}
          </button>

          <div className="login-features">
            <h3>What you can do:</h3>
            <ul>
              <li>✨ Generate playlists with AI</li>
              <li>📊 Analyze your music taste</li>
              <li>🎯 Get mood-based recommendations</li>
              <li>🔄 Blend playlists with friends</li>
              <li>🛠️ Fix and improve your playlists</li>
              <li>👥 Compare music tastes with others</li>
            </ul>
          </div>
        </div>

        <div className="login-footer">
          <p>OAuth 2.0 + PKCE • Secure • No data stored</p>
        </div>
      </div>
    </div>
  )
}

export default Login
