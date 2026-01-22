from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    """Wrapper for VADER sentiment analysis."""

    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze(self, text: str) -> float:
        """
        Analyze sentiment of text and return compound score.

        Args:
            text: The text to analyze

        Returns:
            Compound sentiment score from -1.0 (negative) to 1.0 (positive)
        """
        if not text:
            return 0.0

        scores = self.analyzer.polarity_scores(text)
        return scores["compound"]

    def analyze_with_details(self, text: str) -> dict:
        """
        Analyze sentiment and return detailed scores.

        Args:
            text: The text to analyze

        Returns:
            Dictionary with 'neg', 'neu', 'pos', and 'compound' scores
        """
        if not text:
            return {"neg": 0.0, "neu": 1.0, "pos": 0.0, "compound": 0.0}

        return self.analyzer.polarity_scores(text)


# Singleton instance
_analyzer = None


def get_sentiment_analyzer() -> SentimentAnalyzer:
    """Get or create sentiment analyzer instance."""
    global _analyzer
    if _analyzer is None:
        _analyzer = SentimentAnalyzer()
    return _analyzer
