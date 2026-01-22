from datetime import datetime, timedelta
from typing import Optional, Literal
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Location, Mention, Post
from ..schemas import (
    LocationResponse,
    LocationDetail,
    LocationSearchResult,
    MentionWithPost,
    PostResponse
)

router = APIRouter()


def get_time_filter(time_range: str) -> Optional[datetime]:
    """Convert time_range string to datetime filter."""
    if time_range == "day":
        return datetime.utcnow() - timedelta(days=1)
    elif time_range == "week":
        return datetime.utcnow() - timedelta(weeks=1)
    return None


@router.get("/search", response_model=list[LocationSearchResult])
def search_locations(
    q: str = Query(..., min_length=1, description="Search query"),
    time_range: Literal["all", "week", "day"] = Query("all", description="Time range filter"),
    limit: int = Query(20, ge=1, le=100, description="Maximum results to return"),
    db: Session = Depends(get_db)
):
    """
    Search locations by name, city, or state.

    Returns matching locations with mention counts and sentiment scores.
    """
    search_term = f"%{q}%"

    # Base query with aggregation
    query = db.query(
        Location,
        func.count(Mention.id).label("mention_count"),
        func.coalesce(func.avg(Mention.sentiment_score), 0.0).label("avg_sentiment")
    ).outerjoin(Mention)

    # Apply search filter
    query = query.filter(
        or_(
            Location.name.ilike(search_term),
            Location.city.ilike(search_term),
            Location.state.ilike(search_term),
            Location.place_type.ilike(search_term)
        )
    )

    # Apply time filter
    time_cutoff = get_time_filter(time_range)
    if time_cutoff:
        query = query.filter(
            (Mention.created_at >= time_cutoff) | (Mention.id.is_(None))
        )

    # Group and order by mention count
    results = query.group_by(Location.id).order_by(
        func.count(Mention.id).desc()
    ).limit(limit).all()

    return [
        LocationSearchResult(
            id=location.id,
            name=location.name,
            place_type=location.place_type,
            city=location.city,
            mention_count=mention_count,
            avg_sentiment=round(float(avg_sentiment), 2)
        )
        for location, mention_count, avg_sentiment in results
    ]


@router.get("/{location_id}", response_model=LocationDetail)
def get_location(
    location_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific location.

    Includes recent mentions with post context.
    """
    # Get location with aggregated stats
    result = db.query(
        Location,
        func.count(Mention.id).label("mention_count"),
        func.coalesce(func.avg(Mention.sentiment_score), 0.0).label("avg_sentiment")
    ).outerjoin(Mention).filter(
        Location.id == location_id
    ).group_by(Location.id).first()

    if not result:
        raise HTTPException(status_code=404, detail="Location not found")

    location, mention_count, avg_sentiment = result

    # Get recent mentions with post details
    recent_mentions = db.query(Mention).join(Post).filter(
        Mention.location_id == location_id
    ).order_by(Mention.created_at.desc()).limit(10).all()

    mentions_with_posts = []
    for mention in recent_mentions:
        post = db.query(Post).filter(Post.id == mention.post_id).first()
        mentions_with_posts.append(
            MentionWithPost(
                id=mention.id,
                location_id=mention.location_id,
                post_id=mention.post_id,
                sentiment_score=mention.sentiment_score,
                context=mention.context,
                created_at=mention.created_at,
                post=PostResponse(
                    id=post.id,
                    reddit_id=post.reddit_id,
                    title=post.title,
                    body=post.body,
                    subreddit=post.subreddit,
                    posted_at=post.posted_at,
                    scraped_at=post.scraped_at
                )
            )
        )

    return LocationDetail(
        id=location.id,
        name=location.name,
        lat=location.lat,
        lng=location.lng,
        place_type=location.place_type,
        city=location.city,
        state=location.state,
        created_at=location.created_at,
        mention_count=mention_count,
        avg_sentiment=round(float(avg_sentiment), 2),
        recent_mentions=mentions_with_posts
    )
