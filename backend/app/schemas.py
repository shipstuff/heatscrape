from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# Post schemas (defined first as they're referenced by others)
class PostBase(BaseModel):
    reddit_id: str
    title: Optional[str] = None
    body: Optional[str] = None
    subreddit: str
    posted_at: datetime


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    scraped_at: datetime

    class Config:
        from_attributes = True


# Mention schemas
class MentionBase(BaseModel):
    sentiment_score: float = Field(ge=-1.0, le=1.0, default=0.0)
    context: Optional[str] = None


class MentionCreate(MentionBase):
    location_id: int
    post_id: int


class MentionResponse(MentionBase):
    id: int
    location_id: int
    post_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MentionWithPost(MentionResponse):
    post: PostResponse


# Location schemas
class LocationBase(BaseModel):
    name: str
    lat: float
    lng: float
    place_type: str
    city: Optional[str] = None
    state: str = "HI"


class LocationCreate(LocationBase):
    pass


class LocationResponse(LocationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class LocationDetail(LocationResponse):
    mention_count: int = 0
    avg_sentiment: float = 0.0
    recent_mentions: list[MentionWithPost] = []


# GeoJSON schemas for heatmap
class GeoJSONPoint(BaseModel):
    type: str = "Point"
    coordinates: list[float]  # [lng, lat]


class HeatmapProperties(BaseModel):
    id: int
    name: str
    mention_count: int
    avg_sentiment: float
    place_type: str
    city: Optional[str] = None


class HeatmapFeature(BaseModel):
    type: str = "Feature"
    geometry: GeoJSONPoint
    properties: HeatmapProperties


class HeatmapResponse(BaseModel):
    type: str = "FeatureCollection"
    features: list[HeatmapFeature]


# Search response
class LocationSearchResult(BaseModel):
    id: int
    name: str
    place_type: str
    city: Optional[str] = None
    mention_count: int
    avg_sentiment: float
