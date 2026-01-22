import { useEffect, useRef, useState } from 'react'
import mapboxgl from 'mapbox-gl'
import { useGeolocation } from '../hooks/useGeolocation'
import './Map.css'

// Hawaii center coordinates
const HAWAII_CENTER = [-157.8583, 21.3069]
const DEFAULT_ZOOM = 7

function Map({ locations, loading, onLocationClick, selectedLocation }) {
  const mapContainer = useRef(null)
  const map = useRef(null)
  const popupRef = useRef(null)
  const [mapLoaded, setMapLoaded] = useState(false)
  const { position, error: geoError } = useGeolocation()

  // Initialize map
  useEffect(() => {
    if (map.current) return

    const token = import.meta.env.VITE_MAPBOX_TOKEN
    if (!token) {
      console.error('Mapbox token not found. Set VITE_MAPBOX_TOKEN in .env')
      return
    }

    mapboxgl.accessToken = token

    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/dark-v11',
      center: HAWAII_CENTER,
      zoom: DEFAULT_ZOOM,
    })

    // Add navigation controls
    map.current.addControl(new mapboxgl.NavigationControl(), 'top-right')

    // Add geolocation control
    map.current.addControl(
      new mapboxgl.GeolocateControl({
        positionOptions: { enableHighAccuracy: true },
        trackUserLocation: true,
        showUserHeading: true,
      }),
      'top-right'
    )

    map.current.on('load', () => {
      setMapLoaded(true)

      // Add empty source for locations
      map.current.addSource('locations', {
        type: 'geojson',
        data: { type: 'FeatureCollection', features: [] },
      })

      // Heatmap layer for overview
      map.current.addLayer({
        id: 'locations-heat',
        type: 'heatmap',
        source: 'locations',
        maxzoom: 12,
        paint: {
          'heatmap-weight': [
            'interpolate',
            ['linear'],
            ['get', 'mention_count'],
            0, 0,
            100, 1,
          ],
          'heatmap-intensity': [
            'interpolate',
            ['linear'],
            ['zoom'],
            0, 1,
            12, 3,
          ],
          'heatmap-color': [
            'interpolate',
            ['linear'],
            ['heatmap-density'],
            0, 'rgba(33,102,172,0)',
            0.2, 'rgb(103,169,207)',
            0.4, 'rgb(209,229,240)',
            0.6, 'rgb(253,219,199)',
            0.8, 'rgb(239,138,98)',
            1, 'rgb(178,24,43)',
          ],
          'heatmap-radius': [
            'interpolate',
            ['linear'],
            ['zoom'],
            0, 2,
            12, 20,
          ],
          'heatmap-opacity': [
            'interpolate',
            ['linear'],
            ['zoom'],
            7, 1,
            12, 0,
          ],
        },
      })

      // Circle layer for zoomed in view
      map.current.addLayer({
        id: 'locations-point',
        type: 'circle',
        source: 'locations',
        minzoom: 10,
        paint: {
          'circle-radius': [
            'interpolate',
            ['linear'],
            ['get', 'mention_count'],
            5, 6,
            50, 15,
            100, 25,
          ],
          'circle-color': [
            'interpolate',
            ['linear'],
            ['get', 'avg_sentiment'],
            -1, '#e53e3e',
            0, '#ecc94b',
            1, '#38a169',
          ],
          'circle-stroke-color': '#fff',
          'circle-stroke-width': 2,
          'circle-opacity': [
            'interpolate',
            ['linear'],
            ['zoom'],
            10, 0,
            11, 0.9,
          ],
        },
      })

      // Labels for zoomed in view
      map.current.addLayer({
        id: 'locations-label',
        type: 'symbol',
        source: 'locations',
        minzoom: 12,
        layout: {
          'text-field': ['get', 'name'],
          'text-font': ['DIN Pro Medium', 'Arial Unicode MS Bold'],
          'text-size': 12,
          'text-offset': [0, 1.5],
          'text-anchor': 'top',
        },
        paint: {
          'text-color': '#fff',
          'text-halo-color': '#000',
          'text-halo-width': 1,
        },
      })

      // Click handler for points
      map.current.on('click', 'locations-point', (e) => {
        if (e.features.length > 0) {
          const feature = e.features[0]
          onLocationClick({
            id: feature.properties.id,
            name: feature.properties.name,
            mention_count: feature.properties.mention_count,
            avg_sentiment: feature.properties.avg_sentiment,
            place_type: feature.properties.place_type,
            city: feature.properties.city,
            coordinates: feature.geometry.coordinates,
          })
        }
      })

      // Hover effect
      map.current.on('mouseenter', 'locations-point', (e) => {
        map.current.getCanvas().style.cursor = 'pointer'

        if (e.features.length > 0) {
          const feature = e.features[0]
          const coords = feature.geometry.coordinates.slice()
          const { name, mention_count, avg_sentiment } = feature.properties

          const sentimentLabel =
            avg_sentiment > 0.3 ? 'Positive' :
            avg_sentiment < -0.3 ? 'Negative' : 'Neutral'

          popupRef.current = new mapboxgl.Popup({
            closeButton: false,
            closeOnClick: false,
            className: 'location-popup-hover',
          })
            .setLngLat(coords)
            .setHTML(`
              <strong>${name}</strong><br/>
              ${mention_count} mentions<br/>
              Sentiment: ${sentimentLabel}
            `)
            .addTo(map.current)
        }
      })

      map.current.on('mouseleave', 'locations-point', () => {
        map.current.getCanvas().style.cursor = ''
        if (popupRef.current) {
          popupRef.current.remove()
          popupRef.current = null
        }
      })
    })

    return () => {
      if (map.current) {
        map.current.remove()
        map.current = null
      }
    }
  }, [onLocationClick])

  // Update locations data
  useEffect(() => {
    if (!map.current || !mapLoaded || !locations) return

    const source = map.current.getSource('locations')
    if (source) {
      source.setData(locations)
    }
  }, [locations, mapLoaded])

  // Fly to selected location
  useEffect(() => {
    if (!map.current || !selectedLocation?.coordinates) return

    map.current.flyTo({
      center: selectedLocation.coordinates,
      zoom: 14,
      duration: 1500,
    })
  }, [selectedLocation])

  return (
    <div className="map-wrapper">
      <div ref={mapContainer} className="map-container" />
      {loading && (
        <div className="loading-overlay">
          <div className="loading-spinner" />
          <span>Loading locations...</span>
        </div>
      )}
      {!import.meta.env.VITE_MAPBOX_TOKEN && (
        <div className="map-error">
          <p>Mapbox token not configured.</p>
          <p>Add VITE_MAPBOX_TOKEN to your .env file.</p>
        </div>
      )}
    </div>
  )
}

export default Map
