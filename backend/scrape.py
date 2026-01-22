#!/usr/bin/env python3
"""
CLI script to run the Reddit scraper.

Usage:
    python scrape.py --subreddit hawaii --limit 100
    python scrape.py --subreddit maui --time-filter week --limit 50
"""

import argparse
import sys
from datetime import datetime

from app.database import SessionLocal, init_db
from app.models import Location, Post, Mention
from app.scraper.reddit import create_scraper
from app.scraper.extractor import get_extractor
from app.services.sentiment import get_sentiment_analyzer


def scrape_subreddit(subreddit: str, limit: int, time_filter: str):
    """Scrape a subreddit and extract location mentions."""

    # Initialize components
    scraper = create_scraper()
    if not scraper:
        print("Error: Reddit API credentials not configured.")
        print("Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET environment variables.")
        sys.exit(1)

    extractor = get_extractor()
    sentiment_analyzer = get_sentiment_analyzer()

    init_db()
    db = SessionLocal()

    try:
        print(f"Scraping r/{subreddit} (limit: {limit}, time_filter: {time_filter})...")

        posts_processed = 0
        mentions_created = 0

        for post_data in scraper.scrape_subreddit(subreddit, limit=limit, time_filter=time_filter):
            # Check if post already exists
            existing = db.query(Post).filter(Post.reddit_id == post_data["reddit_id"]).first()
            if existing:
                continue

            # Combine title and body for analysis
            text = f"{post_data['title'] or ''} {post_data['body'] or ''}".strip()
            if not text:
                continue

            # Extract locations
            locations = extractor.extract(text)
            if not locations:
                continue

            # Create post
            post = Post(
                reddit_id=post_data["reddit_id"],
                title=post_data["title"],
                body=post_data["body"],
                subreddit=post_data["subreddit"],
                posted_at=post_data["posted_at"],
                scraped_at=datetime.utcnow()
            )
            db.add(post)
            db.flush()
            posts_processed += 1

            # Process each found location
            for loc_name, place_type, city, lat, lng in locations:
                # Skip locations without coordinates (would need geocoding)
                if lat is None or lng is None:
                    continue

                # Find or create location
                location = db.query(Location).filter(
                    Location.name.ilike(loc_name)
                ).first()

                if not location:
                    location = Location(
                        name=loc_name,
                        lat=lat,
                        lng=lng,
                        place_type=place_type,
                        city=city,
                        state="HI"
                    )
                    db.add(location)
                    db.flush()

                # Get context and sentiment
                context = extractor.extract_context(text, loc_name)
                sentiment = sentiment_analyzer.analyze(context)

                # Create mention
                mention = Mention(
                    location_id=location.id,
                    post_id=post.id,
                    sentiment_score=sentiment,
                    context=context
                )
                db.add(mention)
                mentions_created += 1

            # Commit periodically
            if posts_processed % 10 == 0:
                db.commit()
                print(f"  Processed {posts_processed} posts, {mentions_created} mentions...")

        db.commit()
        print(f"\nDone! Processed {posts_processed} posts, created {mentions_created} mentions.")

    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="Scrape Reddit for location mentions")
    parser.add_argument(
        "--subreddit", "-s",
        required=True,
        help="Subreddit to scrape (without r/)"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=100,
        help="Maximum posts to fetch (default: 100)"
    )
    parser.add_argument(
        "--time-filter", "-t",
        choices=["hour", "day", "week", "month", "year", "all"],
        default="week",
        help="Time filter for top posts (default: week)"
    )

    args = parser.parse_args()
    scrape_subreddit(args.subreddit, args.limit, args.time_filter)


if __name__ == "__main__":
    main()
