from typing import Optional, Tuple
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time


class Geocoder:
    """Geocoding service using Nominatim (OpenStreetMap)."""

    def __init__(self, user_agent: str = "scrapey/1.0"):
        self.geolocator = Nominatim(user_agent=user_agent)
        self._last_request = 0
        self._min_delay = 1.0  # Nominatim rate limit: 1 request/second

    def _rate_limit(self):
        """Ensure we don't exceed rate limits."""
        elapsed = time.time() - self._last_request
        if elapsed < self._min_delay:
            time.sleep(self._min_delay - elapsed)
        self._last_request = time.time()

    def geocode(self, location_name: str, city: str = None, state: str = "Hawaii") -> Optional[Tuple[float, float]]:
        """
        Geocode a location name to coordinates.

        Args:
            location_name: Name of the place
            city: City name (optional)
            state: State name (default: Hawaii)

        Returns:
            Tuple of (latitude, longitude) or None if not found
        """
        self._rate_limit()

        # Build search query
        query_parts = [location_name]
        if city:
            query_parts.append(city)
        query_parts.append(state)
        query = ", ".join(query_parts)

        try:
            location = self.geolocator.geocode(query, timeout=10)
            if location:
                return (location.latitude, location.longitude)
            return None
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Geocoding error for '{query}': {e}")
            return None

    def reverse_geocode(self, lat: float, lng: float) -> Optional[dict]:
        """
        Reverse geocode coordinates to address info.

        Args:
            lat: Latitude
            lng: Longitude

        Returns:
            Dictionary with address components or None
        """
        self._rate_limit()

        try:
            location = self.geolocator.reverse((lat, lng), timeout=10)
            if location and location.raw.get("address"):
                return location.raw["address"]
            return None
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Reverse geocoding error for ({lat}, {lng}): {e}")
            return None


# Singleton instance
_geocoder = None


def get_geocoder() -> Geocoder:
    """Get or create geocoder instance."""
    global _geocoder
    if _geocoder is None:
        _geocoder = Geocoder()
    return _geocoder
