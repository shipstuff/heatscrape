import { useState, useCallback } from 'react'
import Map from './components/Map'
import SearchBar from './components/SearchBar'
import TimeFilter from './components/TimeFilter'
import LocationPopup from './components/LocationPopup'
import { useLocations } from './hooks/useLocations'
import './App.css'

function App() {
  const [timeRange, setTimeRange] = useState('all')
  const [selectedLocation, setSelectedLocation] = useState(null)
  const [searchResults, setSearchResults] = useState([])

  const { locations, loading, error, refetch } = useLocations(timeRange)

  const handleTimeRangeChange = useCallback((newRange) => {
    setTimeRange(newRange)
  }, [])

  const handleLocationSelect = useCallback((location) => {
    setSelectedLocation(location)
    setSearchResults([])
  }, [])

  const handleSearchResults = useCallback((results) => {
    setSearchResults(results)
  }, [])

  const handleClosePopup = useCallback(() => {
    setSelectedLocation(null)
  }, [])

  return (
    <div className="app">
      <header className="app-header">
        <h1>Scrapey</h1>
        <p className="subtitle">Reddit Heatmap for Hawaii Places</p>
      </header>

      <div className="controls">
        <SearchBar
          onSearch={handleSearchResults}
          onSelect={handleLocationSelect}
          searchResults={searchResults}
        />
        <TimeFilter
          value={timeRange}
          onChange={handleTimeRangeChange}
        />
      </div>

      {error && (
        <div className="error-banner">
          Error loading data: {error}
        </div>
      )}

      <Map
        locations={locations}
        loading={loading}
        onLocationClick={handleLocationSelect}
        selectedLocation={selectedLocation}
      />

      {selectedLocation && (
        <LocationPopup
          location={selectedLocation}
          onClose={handleClosePopup}
        />
      )}
    </div>
  )
}

export default App
