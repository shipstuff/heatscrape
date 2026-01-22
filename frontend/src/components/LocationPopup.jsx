import { useState, useEffect } from 'react'
import { getLocationDetails } from '../api/client'
import './LocationPopup.css'

function LocationPopup({ location, onClose }) {
  const [details, setDetails] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!location?.id) return

    const fetchDetails = async () => {
      setLoading(true)
      try {
        const data = await getLocationDetails(location.id)
        setDetails(data)
      } catch (error) {
        console.error('Error fetching location details:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchDetails()
  }, [location?.id])

  const getSentimentLabel = (score) => {
    if (score > 0.3) return { label: 'Positive', color: '#38a169' }
    if (score < -0.3) return { label: 'Negative', color: '#e53e3e' }
    return { label: 'Neutral', color: '#ecc94b' }
  }

  const sentiment = getSentimentLabel(location.avg_sentiment)

  return (
    <div className="popup-overlay" onClick={onClose}>
      <div className="popup-content" onClick={(e) => e.stopPropagation()}>
        <button className="popup-close" onClick={onClose}>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M18 6 6 18M6 6l12 12" />
          </svg>
        </button>

        <div className="popup-header">
          <h2>{location.name}</h2>
          <span className="popup-type">{location.place_type}</span>
        </div>

        <div className="popup-stats">
          <div className="stat">
            <span className="stat-value">{location.mention_count}</span>
            <span className="stat-label">Mentions</span>
          </div>
          <div className="stat">
            <span className="stat-value" style={{ color: sentiment.color }}>
              {sentiment.label}
            </span>
            <span className="stat-label">Sentiment</span>
          </div>
          <div className="stat">
            <span className="stat-value">{location.city || 'Hawaii'}</span>
            <span className="stat-label">Location</span>
          </div>
        </div>

        <div className="popup-section">
          <h3>Recent Mentions</h3>
          {loading ? (
            <div className="popup-loading">
              <div className="loading-spinner" />
              Loading mentions...
            </div>
          ) : details?.recent_mentions?.length > 0 ? (
            <ul className="mentions-list">
              {details.recent_mentions.map((mention) => (
                <li key={mention.id} className="mention-item">
                  <p className="mention-context">"{mention.context}"</p>
                  <div className="mention-meta">
                    <span className="mention-subreddit">
                      r/{mention.post.subreddit}
                    </span>
                    <span
                      className="mention-sentiment"
                      style={{
                        color: getSentimentLabel(mention.sentiment_score).color,
                      }}
                    >
                      {mention.sentiment_score > 0 ? '+' : ''}
                      {mention.sentiment_score.toFixed(2)}
                    </span>
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <p className="no-mentions">No recent mentions found.</p>
          )}
        </div>
      </div>
    </div>
  )
}

export default LocationPopup
