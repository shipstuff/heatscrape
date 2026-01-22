import { useState, useEffect } from 'react'

export function useGeolocation() {
  const [position, setPosition] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by your browser')
      setLoading(false)
      return
    }

    const successHandler = (position) => {
      setPosition({
        lat: position.coords.latitude,
        lng: position.coords.longitude,
        accuracy: position.coords.accuracy,
      })
      setLoading(false)
    }

    const errorHandler = (error) => {
      let message
      switch (error.code) {
        case error.PERMISSION_DENIED:
          message = 'User denied the request for Geolocation'
          break
        case error.POSITION_UNAVAILABLE:
          message = 'Location information is unavailable'
          break
        case error.TIMEOUT:
          message = 'The request to get user location timed out'
          break
        default:
          message = 'An unknown error occurred'
      }
      setError(message)
      setLoading(false)
    }

    navigator.geolocation.getCurrentPosition(successHandler, errorHandler, {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 0,
    })
  }, [])

  return { position, error, loading }
}
