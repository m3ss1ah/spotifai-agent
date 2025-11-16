import React from 'react'
import './UserCard.css'

function UserCard({ user }) {
  return (
    <div className="user-card">
      <div className="user-card-background">
        <div className="user-card-content">
          {user?.image_url ? (
            <img src={user.image_url} alt={user.display_name} className="user-avatar" />
          ) : (
            <div className="user-avatar-placeholder">👤</div>
          )}

          <div className="user-card-info">
            <h2 className="user-card-name">{user?.display_name || 'User'}</h2>
            <p className="user-card-email">{user?.email}</p>

            <div className="user-stats-row">
              <div className="user-stat">
                <span className="stat-label">Followers</span>
                <span className="stat-value">{(user?.followers || 0).toLocaleString()}</span>
              </div>
              <div className="user-stat">
                <span className="stat-label">Plan</span>
                <span className="stat-value">{(user?.plan_type || 'free').toUpperCase()}</span>
              </div>
            </div>
          </div>

          {user?.profile_url && (
            <a href={user.profile_url} target="_blank" rel="noopener noreferrer" className="profile-link">
              View on Spotify →
            </a>
          )}
        </div>
      </div>
    </div>
  )
}

export default UserCard
