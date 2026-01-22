"""
Reddit scraper using PRAW.

Note: This module requires Reddit API credentials to function.
Set REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and REDDIT_USER_AGENT
in environment variables or .env file.
"""

from datetime import datetime
from typing import Generator, Optional
import praw
from praw.models import Submission, Comment

from ..config import get_settings


class RedditScraper:
    """Scraper for Reddit posts and comments using PRAW."""

    def __init__(self):
        settings = get_settings()

        if not settings.reddit_client_id or not settings.reddit_client_secret:
            raise ValueError(
                "Reddit API credentials not configured. "
                "Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET environment variables."
            )

        self.reddit = praw.Reddit(
            client_id=settings.reddit_client_id,
            client_secret=settings.reddit_client_secret,
            user_agent=settings.reddit_user_agent,
        )

    def scrape_subreddit(
        self,
        subreddit_name: str,
        limit: int = 100,
        time_filter: str = "week"
    ) -> Generator[dict, None, None]:
        """
        Scrape posts from a subreddit.

        Args:
            subreddit_name: Name of the subreddit (without r/)
            limit: Maximum number of posts to fetch
            time_filter: Time filter for top posts (hour, day, week, month, year, all)

        Yields:
            Dictionary with post data
        """
        subreddit = self.reddit.subreddit(subreddit_name)

        for submission in subreddit.top(time_filter=time_filter, limit=limit):
            yield self._submission_to_dict(submission)

    def scrape_comments(
        self,
        submission: Submission,
        limit: Optional[int] = None
    ) -> Generator[dict, None, None]:
        """
        Scrape comments from a submission.

        Args:
            submission: PRAW Submission object
            limit: Maximum number of comments (None for all)

        Yields:
            Dictionary with comment data
        """
        submission.comments.replace_more(limit=limit)
        for comment in submission.comments.list():
            yield self._comment_to_dict(comment, submission.subreddit.display_name)

    def _submission_to_dict(self, submission: Submission) -> dict:
        """Convert PRAW Submission to dictionary."""
        return {
            "reddit_id": submission.id,
            "title": submission.title,
            "body": submission.selftext,
            "subreddit": submission.subreddit.display_name,
            "posted_at": datetime.utcfromtimestamp(submission.created_utc),
            "score": submission.score,
            "num_comments": submission.num_comments,
            "url": submission.url,
            "is_comment": False,
        }

    def _comment_to_dict(self, comment: Comment, subreddit: str) -> dict:
        """Convert PRAW Comment to dictionary."""
        return {
            "reddit_id": comment.id,
            "title": None,
            "body": comment.body,
            "subreddit": subreddit,
            "posted_at": datetime.utcfromtimestamp(comment.created_utc),
            "score": comment.score,
            "is_comment": True,
        }


def create_scraper() -> Optional[RedditScraper]:
    """
    Create a Reddit scraper instance.

    Returns None if credentials are not configured.
    """
    try:
        return RedditScraper()
    except ValueError:
        return None
