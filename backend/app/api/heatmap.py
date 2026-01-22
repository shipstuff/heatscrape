from datetime import datetime, timedelta
from typing import Optional, Literal
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Location, Mention, Post
from ..schemas import HeatmapResponse, HeatmapFeature, GeoJSONPoint, HeatmapProperties

router = APIRouter()


def get_time_filter(time_range: str) -> Optional[datetime]:
    """Convert time_range string to datetime filter."""
    if time_range == "day":
        return datetime.utcnow() - timedelta(days=1)
    elif time_range == "week":
        return datetime.utcnow() - timedelta(weeks=1)
    return None  # "all" - no filter


@router.get("", response_model=HeatmapResponse)
def get_heatmap_data(
    time_range: Literal["all", "week", "day"] = Query("all", description="Time range filter"),
    min_lat: Optional[float] = Query(None, description="Minimum latitude for bounds"),
    max_lat: Optional[float] = Query(None, description="Maximum latitude for bounds"),
    min_lng: Optional[float] = Query(None, description="Minimum longitude for bounds"),
    max_lng: Optional[float] = Query(None, description="Maximum longitude for bounds"),
    db: Session = Depends(get_db)
):
    """
    Get heatmap-ready GeoJSON data with aggregated location info.

    Returns locations with mention counts and average sentiment scores.
    Optionally filter by time range and geographic bounds.
    """
    # Base query: aggregate mentions per location
    query = db.query(
        Location,
        func.count(Mention.id).label("mention_count"),
        func.coalesce(func.avg(Mention.sentiment_score), 0.0).label("avg_sentiment")
    ).outerjoin(Mention)

    # Apply time filter
    time_cutoff = get_time_filter(time_range)
    if time_cutoff:
        query = query.filter(
            (Mention.created_at >= time_cutoff) | (Mention.id.is_(None))
        )

    # Apply geographic bounds filter
    if all([min_lat, max_lat, min_lng, max_lng]):
        query = query.filter(
            Location.lat >= min_lat,
            Location.lat <= max_lat,
            Location.lng >= min_lng,
            Location.lng <= max_lng
        )

    # Group by location
    results = query.group_by(Location.id).all()

    # Build GeoJSON features
    features = []
    for location, mention_count, avg_sentiment in results:
        # Only include locations with mentions (or all if no time filter)
        if mention_count > 0 or time_range == "all":
            feature = HeatmapFeature(
                geometry=GeoJSONPoint(coordinates=[location.lng, location.lat]),
                properties=HeatmapProperties(
                    id=location.id,
                    name=location.name,
                    mention_count=mention_count,
                    avg_sentiment=round(float(avg_sentiment), 2),
                    place_type=location.place_type,
                    city=location.city
                )
            )
            features.append(feature)

    return HeatmapResponse(features=features)
