import { useState, useEffect, useCallback } from 'react'
import { getHeatmapData } from '../api/client'

export function useLocations(timeRange = 'all') {
  const [locations, setLocations] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchLocations = useCallback(async () => {
    setLoading(true)
    setError(null)

    try {
      const data = await getHeatmapData(timeRange)
      setLocations(data)
    } catch (err) {
      setError(err.message || 'Failed to fetch locations')
      console.error('Error fetching locations:', err)
    } finally {
      setLoading(false)
    }
  }, [timeRange])

  useEffect(() => {
    fetchLocations()
  }, [fetchLocations])

  return {
    locations,
    loading,
    error,
    refetch: fetchLocations,
  }
}
