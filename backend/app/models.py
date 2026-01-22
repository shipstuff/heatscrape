from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    place_type = Column(String(50), nullable=False, index=True)  # restaurant, park, beach, etc.
    city = Column(String(100), index=True)
    state = Column(String(50), default="HI", index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    mentions = relationship("Mention", back_populates="location", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Location(name='{self.name}', city='{self.city}')>"


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    reddit_id = Column(String(20), unique=True, nullable=False, index=True)
    title = Column(Text, nullable=True)  # Null for comments
    body = Column(Text, nullable=True)
    subreddit = Column(String(100), nullable=False, index=True)
    posted_at = Column(DateTime, nullable=False)
    scraped_at = Column(DateTime, default=datetime.utcnow)

    mentions = relationship("Mention", back_populates="post", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Post(reddit_id='{self.reddit_id}', subreddit='{self.subreddit}')>"


class Mention(Base):
    __tablename__ = "mentions"

    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False, index=True)
    sentiment_score = Column(Float, default=0.0)  # -1.0 to 1.0
    context = Column(Text)  # Snippet of text mentioning the location
    created_at = Column(DateTime, default=datetime.utcnow)

    location = relationship("Location", back_populates="mentions")
    post = relationship("Post", back_populates="mentions")

    def __repr__(self):
        return f"<Mention(location_id={self.location_id}, sentiment={self.sentiment_score})>"
