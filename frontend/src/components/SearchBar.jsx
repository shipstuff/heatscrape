import { useState, useEffect, useRef } from 'react'
import { searchLocations } from '../api/client'
import './SearchBar.css'

function SearchBar({ onSearch, onSelect, searchResults }) {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [showResults, setShowResults] = useState(false)
  const inputRef = useRef(null)
  const containerRef = useRef(null)

  // Handle search with debounce
  useEffect(() => {
    if (!query.trim()) {
      onSearch([])
      return
    }

    const timeoutId = setTimeout(async () => {
      setLoading(true)
      try {
        const results = await searchLocations(query)
        onSearch(results)
        setShowResults(true)
      } catch (error) {
        console.error('Search error:', error)
      } finally {
        setLoading(false)
      }
    }, 300)

    return () => clearTimeout(timeoutId)
  }, [query, onSearch])

  // Close results when clicking outside
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (containerRef.current && !containerRef.current.contains(e.target)) {
        setShowResults(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleSelect = (result) => {
    onSelect({
      id: result.id,
      name: result.name,
      mention_count: result.mention_count,
      avg_sentiment: result.avg_sentiment,
      place_type: result.place_type,
      city: result.city,
    })
    setQuery('')
    setShowResults(false)
  }

  const getSentimentColor = (sentiment) => {
    if (sentiment > 0.3) return '#38a169'
    if (sentiment < -0.3) return '#e53e3e'
    return '#ecc94b'
  }

  return (
    <div className="search-container" ref={containerRef}>
      <div className="search-input-wrapper">
        <svg
          className="search-icon"
          xmlns="http://www.w3.org/2000/svg"
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <circle cx="11" cy="11" r="8" />
          <path d="m21 21-4.3-4.3" />
        </svg>
        <input
          ref={inputRef}
          type="text"
          placeholder="Search locations..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => query && setShowResults(true)}
          className="search-input"
        />
        {loading && <div className="search-spinner" />}
      </div>

      {showResults && searchResults.length > 0 && (
        <ul className="search-results">
          {searchResults.map((result) => (
            <li
              key={result.id}
              className="search-result-item"
              onClick={() => handleSelect(result)}
            >
              <div className="result-main">
                <span className="result-name">{result.name}</span>
                <span className="result-type">{result.place_type}</span>
              </div>
              <div className="result-meta">
                <span className="result-city">{result.city || 'Hawaii'}</span>
                <span className="result-mentions">
                  {result.mention_count} mentions
                </span>
                <span
                  className="result-sentiment"
                  style={{ color: getSentimentColor(result.avg_sentiment) }}
                >
                  {result.avg_sentiment > 0 ? '+' : ''}
                  {result.avg_sentiment.toFixed(2)}
                </span>
              </div>
            </li>
          ))}
        </ul>
      )}

      {showResults && query && searchResults.length === 0 && !loading && (
        <div className="search-no-results">No locations found</div>
      )}
    </div>
  )
}

export default SearchBar
