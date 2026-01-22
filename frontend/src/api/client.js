const API_BASE = '/api'

async function fetchApi(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`

  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || `HTTP error ${response.status}`)
  }

  return response.json()
}

/**
 * Get heatmap data for all locations
 * @param {string} timeRange - 'all' | 'week' | 'day'
 * @param {object} bounds - Optional bounding box { minLat, maxLat, minLng, maxLng }
 */
export async function getHeatmapData(timeRange = 'all', bounds = null) {
  const params = new URLSearchParams({ time_range: timeRange })

  if (bounds) {
    params.append('min_lat', bounds.minLat)
    params.append('max_lat', bounds.maxLat)
    params.append('min_lng', bounds.minLng)
    params.append('max_lng', bounds.maxLng)
  }

  return fetchApi(`/heatmap?${params}`)
}

/**
 * Search locations by query
 * @param {string} query - Search term
 * @param {string} timeRange - 'all' | 'week' | 'day'
 * @param {number} limit - Maximum results
 */
export async function searchLocations(query, timeRange = 'all', limit = 20) {
  const params = new URLSearchParams({
    q: query,
    time_range: timeRange,
    limit: limit.toString(),
  })

  return fetchApi(`/locations/search?${params}`)
}

/**
 * Get detailed information about a location
 * @param {number} locationId - Location ID
 */
export async function getLocationDetails(locationId) {
  return fetchApi(`/locations/${locationId}`)
}
