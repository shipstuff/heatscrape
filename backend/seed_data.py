#!/usr/bin/env python3
"""
Seed the database with realistic Hawaii mock data.
"""

import random
from datetime import datetime, timedelta

from app.database import SessionLocal, init_db
from app.models import Location, Post, Mention

# Realistic Hawaii locations
LOCATIONS = [
    # Restaurants - Oahu
    {"name": "Rainbow Drive-In", "lat": 21.2761, "lng": -157.8141, "place_type": "restaurant", "city": "Honolulu"},
    {"name": "Helena's Hawaiian Food", "lat": 21.3180, "lng": -157.8653, "place_type": "restaurant", "city": "Honolulu"},
    {"name": "Leonard's Bakery", "lat": 21.2853, "lng": -157.8185, "place_type": "restaurant", "city": "Honolulu"},
    {"name": "Marukame Udon", "lat": 21.2812, "lng": -157.8286, "place_type": "restaurant", "city": "Honolulu"},
    {"name": "Side Street Inn", "lat": 21.2970, "lng": -157.8432, "place_type": "restaurant", "city": "Honolulu"},
    {"name": "Ono Seafood", "lat": 21.2770, "lng": -157.8152, "place_type": "restaurant", "city": "Honolulu"},
    {"name": "Giovanni's Shrimp Truck", "lat": 21.6836, "lng": -157.9436, "place_type": "restaurant", "city": "Kahuku"},
    {"name": "Ted's Bakery", "lat": 21.6478, "lng": -158.0631, "place_type": "restaurant", "city": "Haleiwa"},
    {"name": "Matsumoto Shave Ice", "lat": 21.5922, "lng": -158.1032, "place_type": "restaurant", "city": "Haleiwa"},
    {"name": "Duke's Waikiki", "lat": 21.2766, "lng": -157.8263, "place_type": "restaurant", "city": "Honolulu"},
    {"name": "Zippy's", "lat": 21.2915, "lng": -157.8183, "place_type": "restaurant", "city": "Honolulu"},
    {"name": "Liliha Bakery", "lat": 21.3222, "lng": -157.8528, "place_type": "restaurant", "city": "Honolulu"},

    # Restaurants - Maui
    {"name": "Mama's Fish House", "lat": 20.9369, "lng": -156.3456, "place_type": "restaurant", "city": "Paia"},
    {"name": "Tin Roof Maui", "lat": 20.8893, "lng": -156.4729, "place_type": "restaurant", "city": "Kahului"},
    {"name": "Ululani's Shave Ice", "lat": 20.8783, "lng": -156.6825, "place_type": "restaurant", "city": "Lahaina"},
    {"name": "Leoda's Kitchen", "lat": 20.8550, "lng": -156.6100, "place_type": "restaurant", "city": "Lahaina"},

    # Restaurants - Big Island
    {"name": "Cafe 100", "lat": 19.7114, "lng": -155.0850, "place_type": "restaurant", "city": "Hilo"},
    {"name": "Ken's House of Pancakes", "lat": 19.7222, "lng": -155.0839, "place_type": "restaurant", "city": "Hilo"},
    {"name": "Merriman's", "lat": 20.0236, "lng": -155.6692, "place_type": "restaurant", "city": "Waimea"},

    # Beaches - Oahu
    {"name": "Waikiki Beach", "lat": 21.2766, "lng": -157.8278, "place_type": "beach", "city": "Honolulu"},
    {"name": "Lanikai Beach", "lat": 21.3920, "lng": -157.7150, "place_type": "beach", "city": "Kailua"},
    {"name": "Kailua Beach", "lat": 21.4022, "lng": -157.7267, "place_type": "beach", "city": "Kailua"},
    {"name": "Hanauma Bay", "lat": 21.2690, "lng": -157.6940, "place_type": "beach", "city": "Honolulu"},
    {"name": "Sunset Beach", "lat": 21.6761, "lng": -158.0431, "place_type": "beach", "city": "Haleiwa"},
    {"name": "Waimea Bay", "lat": 21.6422, "lng": -158.0656, "place_type": "beach", "city": "Haleiwa"},
    {"name": "Ala Moana Beach Park", "lat": 21.2890, "lng": -157.8500, "place_type": "beach", "city": "Honolulu"},
    {"name": "Sandy Beach", "lat": 21.2864, "lng": -157.6728, "place_type": "beach", "city": "Honolulu"},

    # Beaches - Maui
    {"name": "Ka'anapali Beach", "lat": 20.9261, "lng": -156.6944, "place_type": "beach", "city": "Lahaina"},
    {"name": "Wailea Beach", "lat": 20.6867, "lng": -156.4422, "place_type": "beach", "city": "Wailea"},
    {"name": "Big Beach (Makena)", "lat": 20.6306, "lng": -156.4461, "place_type": "beach", "city": "Makena"},
    {"name": "Ho'okipa Beach", "lat": 20.9350, "lng": -156.3569, "place_type": "beach", "city": "Paia"},

    # Beaches - Big Island
    {"name": "Hapuna Beach", "lat": 19.9889, "lng": -155.8261, "place_type": "beach", "city": "Waimea"},
    {"name": "Punalu'u Black Sand Beach", "lat": 19.1361, "lng": -155.5047, "place_type": "beach", "city": "Pahala"},
    {"name": "Kua Bay", "lat": 19.8789, "lng": -155.8942, "place_type": "beach", "city": "Kona"},

    # Beaches - Kauai
    {"name": "Poipu Beach", "lat": 21.8769, "lng": -159.4583, "place_type": "beach", "city": "Poipu"},
    {"name": "Hanalei Bay", "lat": 22.2067, "lng": -159.5008, "place_type": "beach", "city": "Hanalei"},
    {"name": "Tunnels Beach", "lat": 22.2233, "lng": -159.5589, "place_type": "beach", "city": "Haena"},

    # Parks/Hikes - Oahu
    {"name": "Diamond Head", "lat": 21.2614, "lng": -157.8056, "place_type": "park", "city": "Honolulu"},
    {"name": "Manoa Falls", "lat": 21.3331, "lng": -157.8025, "place_type": "park", "city": "Honolulu"},
    {"name": "Koko Head Trail", "lat": 21.2781, "lng": -157.6972, "place_type": "park", "city": "Honolulu"},
    {"name": "Lanikai Pillbox", "lat": 21.3867, "lng": -157.7419, "place_type": "park", "city": "Kailua"},
    {"name": "Makapuu Lighthouse Trail", "lat": 21.3108, "lng": -157.6500, "place_type": "park", "city": "Waimanalo"},
    {"name": "Stairway to Heaven (Haiku Stairs)", "lat": 21.4044, "lng": -157.8169, "place_type": "park", "city": "Kaneohe"},

    # Parks/Hikes - Maui
    {"name": "Haleakala National Park", "lat": 20.7097, "lng": -156.1731, "place_type": "park", "city": "Kula"},
    {"name": "Iao Valley", "lat": 20.8833, "lng": -156.5431, "place_type": "park", "city": "Wailuku"},
    {"name": "Road to Hana", "lat": 20.7575, "lng": -155.9903, "place_type": "attraction", "city": "Hana"},

    # Parks/Hikes - Big Island
    {"name": "Hawaii Volcanoes National Park", "lat": 19.4194, "lng": -155.2878, "place_type": "park", "city": "Volcano"},
    {"name": "Akaka Falls", "lat": 19.8536, "lng": -155.1522, "place_type": "park", "city": "Honomu"},
    {"name": "Waipio Valley", "lat": 20.1169, "lng": -155.5853, "place_type": "park", "city": "Honokaa"},

    # Parks/Hikes - Kauai
    {"name": "Na Pali Coast", "lat": 22.1833, "lng": -159.6500, "place_type": "park", "city": "Kauai"},
    {"name": "Waimea Canyon", "lat": 22.0728, "lng": -159.6603, "place_type": "park", "city": "Waimea"},
    {"name": "Kalalau Trail", "lat": 22.2153, "lng": -159.5839, "place_type": "park", "city": "Kauai"},

    # Attractions
    {"name": "Pearl Harbor", "lat": 21.3650, "lng": -157.9683, "place_type": "attraction", "city": "Honolulu"},
    {"name": "Polynesian Cultural Center", "lat": 21.6392, "lng": -157.9231, "place_type": "attraction", "city": "Laie"},
    {"name": "Dole Plantation", "lat": 21.5250, "lng": -158.0389, "place_type": "attraction", "city": "Wahiawa"},
    {"name": "Aulani Disney Resort", "lat": 21.3400, "lng": -158.1300, "place_type": "resort", "city": "Ko Olina"},
    {"name": "Ala Moana Center", "lat": 21.2911, "lng": -157.8444, "place_type": "shopping", "city": "Honolulu"},
]

# Sample Reddit-style comments for context
POSITIVE_CONTEXTS = [
    "Just had the best experience at {location}! Highly recommend it to anyone visiting.",
    "{location} is absolutely amazing. Can't believe we almost skipped it!",
    "If you're in {city}, you HAVE to visit {location}. Life-changing!",
    "Went to {location} yesterday and wow, it exceeded all expectations.",
    "{location} was the highlight of our entire trip. 10/10 would recommend.",
    "Pro tip: {location} is way less crowded in the morning. Go early!",
    "Finally tried {location} after all the hype. It lives up to it!",
    "We go to {location} every time we're on the island. Never disappoints.",
]

NEUTRAL_CONTEXTS = [
    "Visited {location} today. It was okay, pretty standard for the area.",
    "{location} was crowded when we went. The {city} spot everyone talks about.",
    "Stopped by {location}. Nothing special but worth checking off the list.",
    "Has anyone been to {location} recently? Wondering if it's worth the drive.",
    "{location} is decent. Expected more given all the reviews.",
    "We checked out {location}. Good for tourists I guess.",
]

NEGATIVE_CONTEXTS = [
    "Disappointed by {location}. Way too crowded and overpriced.",
    "Skip {location}, honestly. There are better spots in {city}.",
    "{location} used to be great but it's gone downhill lately.",
    "The line at {location} was insane. Not worth the 2 hour wait.",
    "{location} was underwhelming. Save your time and money.",
    "Unpopular opinion but {location} is overrated. Fight me.",
]

SUBREDDITS = ["Hawaii", "Honolulu", "Maui", "BigIsland", "Oahu", "Kauai", "HawaiiFoodPorn"]


def generate_reddit_id():
    """Generate a fake Reddit-style ID."""
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    return "".join(random.choices(chars, k=7))


def generate_sentiment_and_context(location_name: str, city: str) -> tuple[float, str]:
    """Generate a sentiment score and matching context."""
    # Weighted random: 60% positive, 25% neutral, 15% negative
    roll = random.random()
    if roll < 0.60:
        sentiment = random.uniform(0.4, 1.0)
        context = random.choice(POSITIVE_CONTEXTS)
    elif roll < 0.85:
        sentiment = random.uniform(-0.2, 0.3)
        context = random.choice(NEUTRAL_CONTEXTS)
    else:
        sentiment = random.uniform(-1.0, -0.3)
        context = random.choice(NEGATIVE_CONTEXTS)

    context = context.format(location=location_name, city=city or "Hawaii")
    return round(sentiment, 2), context


def seed_database():
    """Seed the database with mock data."""
    init_db()
    db = SessionLocal()

    try:
        # Check if already seeded
        existing = db.query(Location).count()
        if existing > 0:
            print(f"Database already has {existing} locations. Skipping seed.")
            return

        print("Seeding database with Hawaii locations...")

        # Create locations
        location_objects = []
        for loc_data in LOCATIONS:
            location = Location(
                name=loc_data["name"],
                lat=loc_data["lat"],
                lng=loc_data["lng"],
                place_type=loc_data["place_type"],
                city=loc_data["city"],
                state="HI",
                created_at=datetime.utcnow() - timedelta(days=random.randint(30, 90))
            )
            db.add(location)
            location_objects.append(location)

        db.commit()
        print(f"Created {len(location_objects)} locations.")

        # Create posts and mentions
        posts_created = 0
        mentions_created = 0

        for location in location_objects:
            # Each location gets 5-100 mentions
            num_mentions = random.randint(5, 100)

            for _ in range(num_mentions):
                # Create a fake post
                posted_at = datetime.utcnow() - timedelta(
                    days=random.randint(0, 30),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )

                sentiment, context = generate_sentiment_and_context(location.name, location.city)

                post = Post(
                    reddit_id=generate_reddit_id(),
                    title=f"Question about {location.city}" if random.random() > 0.5 else None,
                    body=context,
                    subreddit=random.choice(SUBREDDITS),
                    posted_at=posted_at,
                    scraped_at=datetime.utcnow()
                )
                db.add(post)
                db.flush()  # Get the post ID
                posts_created += 1

                # Create mention
                mention = Mention(
                    location_id=location.id,
                    post_id=post.id,
                    sentiment_score=sentiment,
                    context=context,
                    created_at=posted_at
                )
                db.add(mention)
                mentions_created += 1

        db.commit()
        print(f"Created {posts_created} posts and {mentions_created} mentions.")
        print("Database seeding complete!")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
