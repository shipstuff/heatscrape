"""
Location extraction from text using pattern matching and NLP.

Uses a combination of:
1. Known Hawaii locations list
2. Pattern matching for common phrases
3. spaCy NER for general place names (optional)
"""

import re
from typing import List, Tuple, Optional


# Known Hawaii locations - restaurants, beaches, landmarks, etc.
KNOWN_LOCATIONS = {
    # Restaurants - Oahu
    "rainbow drive-in": ("restaurant", "Honolulu", 21.2761, -157.8141),
    "helena's hawaiian food": ("restaurant", "Honolulu", 21.3180, -157.8653),
    "leonard's bakery": ("restaurant", "Honolulu", 21.2853, -157.8185),
    "marukame udon": ("restaurant", "Honolulu", 21.2812, -157.8286),
    "side street inn": ("restaurant", "Honolulu", 21.2970, -157.8432),
    "ono seafood": ("restaurant", "Honolulu", 21.2770, -157.8152),
    "giovanni's shrimp truck": ("restaurant", "Kahuku", 21.6836, -157.9436),
    "ted's bakery": ("restaurant", "Haleiwa", 21.6478, -158.0631),
    "matsumoto shave ice": ("restaurant", "Haleiwa", 21.5922, -158.1032),
    "duke's waikiki": ("restaurant", "Honolulu", 21.2766, -157.8263),

    # Restaurants - Maui
    "mama's fish house": ("restaurant", "Paia", 20.9369, -156.3456),
    "tin roof maui": ("restaurant", "Kahului", 20.8893, -156.4729),
    "ululani's shave ice": ("restaurant", "Lahaina", 20.8783, -156.6825),

    # Restaurants - Big Island
    "cafe 100": ("restaurant", "Hilo", 19.7114, -155.0850),
    "ken's house of pancakes": ("restaurant", "Hilo", 19.7222, -155.0839),

    # Beaches - Oahu
    "waikiki beach": ("beach", "Honolulu", 21.2766, -157.8278),
    "lanikai beach": ("beach", "Kailua", 21.3920, -157.7150),
    "kailua beach": ("beach", "Kailua", 21.4022, -157.7267),
    "hanauma bay": ("beach", "Honolulu", 21.2690, -157.6940),
    "sunset beach": ("beach", "Haleiwa", 21.6761, -158.0431),
    "waimea bay": ("beach", "Haleiwa", 21.6422, -158.0656),
    "north shore": ("beach", "Haleiwa", 21.6400, -158.0500),
    "ala moana beach": ("beach", "Honolulu", 21.2890, -157.8500),

    # Beaches - Maui
    "kaanapali beach": ("beach", "Lahaina", 20.9261, -156.6944),
    "wailea beach": ("beach", "Wailea", 20.6867, -156.4422),
    "big beach": ("beach", "Makena", 20.6306, -156.4461),
    "makena beach": ("beach", "Makena", 20.6306, -156.4461),
    "ho'okipa beach": ("beach", "Paia", 20.9350, -156.3569),

    # Beaches - Big Island
    "hapuna beach": ("beach", "Waimea", 19.9889, -155.8261),
    "punalu'u black sand beach": ("beach", "Pahala", 19.1361, -155.5047),

    # Beaches - Kauai
    "poipu beach": ("beach", "Poipu", 21.8769, -159.4583),
    "hanalei bay": ("beach", "Hanalei", 22.2067, -159.5008),

    # Parks/Hikes - Oahu
    "diamond head": ("park", "Honolulu", 21.2614, -157.8056),
    "manoa falls": ("park", "Honolulu", 21.3331, -157.8025),
    "koko head": ("park", "Honolulu", 21.2781, -157.6972),
    "pillbox hike": ("park", "Kailua", 21.3867, -157.7419),
    "makapuu lighthouse": ("park", "Waimanalo", 21.3108, -157.6500),

    # Parks/Hikes - Maui
    "haleakala": ("park", "Kula", 20.7097, -156.1731),
    "iao valley": ("park", "Wailuku", 20.8833, -156.5431),
    "road to hana": ("attraction", "Hana", 20.7575, -155.9903),

    # Parks/Hikes - Big Island
    "hawaii volcanoes national park": ("park", "Volcano", 19.4194, -155.2878),
    "akaka falls": ("park", "Honomu", 19.8536, -155.1522),

    # Parks/Hikes - Kauai
    "na pali coast": ("park", "Kauai", 22.1833, -159.6500),
    "waimea canyon": ("park", "Waimea", 22.0728, -159.6603),
    "kalalau trail": ("park", "Kauai", 22.2153, -159.5839),

    # Entertainment/Attractions
    "pearl harbor": ("attraction", "Honolulu", 21.3650, -157.9683),
    "polynesian cultural center": ("attraction", "Laie", 21.6392, -157.9231),
    "dole plantation": ("attraction", "Wahiawa", 21.5250, -158.0389),
    "aulani disney resort": ("resort", "Ko Olina", 21.3400, -158.1300),
}


class LocationExtractor:
    """Extract location mentions from text."""

    def __init__(self):
        # Compile patterns for location mentions
        self.patterns = [
            r"(?:at|to|from|near|visited?|went to|tried|love|recommend)\s+([A-Z][a-zA-Z'\-\s]+(?:Beach|Restaurant|Cafe|Grill|Inn|Bar|Bakery|Falls|Trail|Bay|Point|Park|Resort))",
            r"(?:at|to|from|near|visited?|went to)\s+([A-Z][a-zA-Z'\-\s]{2,30})",
        ]
        self.compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.patterns]

    def extract(self, text: str) -> List[Tuple[str, str, str, float, float]]:
        """
        Extract location mentions from text.

        Args:
            text: Text to search for location mentions

        Returns:
            List of tuples: (name, place_type, city, lat, lng)
        """
        if not text:
            return []

        found_locations = []
        text_lower = text.lower()

        # First, check for known locations
        for name, (place_type, city, lat, lng) in KNOWN_LOCATIONS.items():
            if name in text_lower:
                found_locations.append((name.title(), place_type, city, lat, lng))

        # Then try pattern matching for unknown locations
        for pattern in self.compiled_patterns:
            matches = pattern.findall(text)
            for match in matches:
                normalized = match.strip().lower()
                # Skip if already found in known locations
                if normalized not in KNOWN_LOCATIONS:
                    # Skip common words
                    if normalized not in ["the", "a", "an", "this", "that", "it"]:
                        # These would need geocoding - return without coordinates
                        found_locations.append((match.strip(), "unknown", None, None, None))

        return found_locations

    def extract_context(self, text: str, location_name: str, window: int = 100) -> str:
        """
        Extract text context around a location mention.

        Args:
            text: Full text
            location_name: Location name to find
            window: Number of characters before/after to include

        Returns:
            Context snippet
        """
        text_lower = text.lower()
        loc_lower = location_name.lower()

        idx = text_lower.find(loc_lower)
        if idx == -1:
            return ""

        start = max(0, idx - window)
        end = min(len(text), idx + len(location_name) + window)

        snippet = text[start:end]

        # Add ellipsis if truncated
        if start > 0:
            snippet = "..." + snippet
        if end < len(text):
            snippet = snippet + "..."

        return snippet


# Singleton instance
_extractor = None


def get_extractor() -> LocationExtractor:
    """Get or create extractor instance."""
    global _extractor
    if _extractor is None:
        _extractor = LocationExtractor()
    return _extractor
