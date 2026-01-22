# Scrapey - Reddit Heatmap for Places of Interest

A web application that displays mentions of places (restaurants, beaches, parks) from Reddit on an interactive heatmap, with sentiment analysis.

## Features

- Interactive heatmap using Mapbox GL JS
- Sentiment analysis visualization (positive/negative/neutral)
- Search for locations by name, city, or type
- Time-based filtering (all time, this week, today)
- Location details with recent Reddit mentions
- Reddit scraper with NLP location extraction (Phase 4)

## Tech Stack

- **Backend**: Python 3.11+ with FastAPI
- **Frontend**: React 18 with Vite
- **Map**: Mapbox GL JS
- **Database**: SQLite with SQLAlchemy ORM
- **NLP**: VADER for sentiment analysis

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Mapbox account (free tier: 50k loads/month)

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Seed database with mock Hawaii data
python seed_data.py

# Start the API server
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env
# Edit .env and add your Mapbox token

# Start development server
npm run dev
```

The app will be available at http://localhost:5173

## Environment Variables

### Frontend (.env)

```
VITE_MAPBOX_TOKEN=your_mapbox_token_here
```

Get a free Mapbox token at https://account.mapbox.com/access-tokens/

### Backend (.env) - For Reddit Scraping (Phase 4)

```
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=scrapey/1.0
```

## API Endpoints

### GET /api/heatmap
Returns GeoJSON data for the heatmap layer.

Query parameters:
- `time_range`: "all" | "week" | "day"
- `min_lat`, `max_lat`, `min_lng`, `max_lng`: Bounding box (optional)

### GET /api/locations/search
Search locations by name, city, or state.

Query parameters:
- `q`: Search query
- `time_range`: "all" | "week" | "day"
- `limit`: Max results (default: 20)

### GET /api/locations/{id}
Get detailed info about a location including recent mentions.

## Project Structure

```
scrapey/
├── backend/
│   ├── app/
│   │   ├── api/           # FastAPI endpoints
│   │   ├── scraper/       # Reddit scraper & NLP
│   │   └── services/      # Geocoding, sentiment
│   ├── seed_data.py       # Database seeder
│   └── scrape.py          # CLI scraper script
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── hooks/         # Custom hooks
│   │   └── api/           # API client
└── README.md
```

## Mock Data

The seeder creates ~55 realistic Hawaii locations including:
- Popular restaurants (Rainbow Drive-In, Mama's Fish House, etc.)
- Beaches (Waikiki, Lanikai, Hanauma Bay, etc.)
- Parks and hikes (Diamond Head, Manoa Falls, etc.)
- Attractions (Pearl Harbor, Polynesian Cultural Center, etc.)

Each location has:
- Realistic coordinates
- Simulated mention counts (5-100)
- Sentiment scores distributed across positive/neutral/negative
- Sample context snippets mimicking Reddit comments

## Reddit Scraper (Phase 4)

To use the Reddit scraper, configure API credentials and run:

```bash
cd backend
python scrape.py --subreddit hawaii --limit 100 --time-filter week
```

Target subreddits:
- r/Hawaii
- r/Honolulu
- r/Maui
- r/BigIsland
- r/Oahu
- r/Kauai
- r/HawaiiFoodPorn

## License

MIT
