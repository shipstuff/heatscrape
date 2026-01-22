from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Scrapey"
    database_url: str = "sqlite:///./scrapey.db"

    # Reddit API credentials (for Phase 4)
    reddit_client_id: str = ""
    reddit_client_secret: str = ""
    reddit_user_agent: str = "scrapey/1.0"

    # Default subreddits for Hawaii
    default_subreddits: list[str] = [
        "Hawaii",
        "Honolulu",
        "Maui",
        "BigIsland",
        "Oahu",
        "Kauai",
        "HawaiiFoodPorn"
    ]

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
