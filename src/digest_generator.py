# 4 

from datetime import datetime, timezone

class DailyDigestGenerator:
    def __init__(self, topic: str):
        self.topic = topic

    def generate(self, articles: list[dict]) -> str:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        # Count sentiment distribution
        sentiment_counts = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}
        for article in articles:
            sentiment = article.get('sentiment', 'NEUTRAL')
            sentiment_counts.setdefault(sentiment, 0)
            sentiment_counts[sentiment] += 1

        # Create sentiment summary
        sentiment_summary = (
            f"🔥 {sentiment_counts['POSITIVE']} Positive | "
            f"⚠️ {sentiment_counts['NEUTRAL']} Neutral | "
            f"⚡ {sentiment_counts['NEGATIVE']} Negative"
        )

        # Create key takeaways
        takeaways = []
        for article in articles:
            emoji = (
                "🔥" if article['sentiment'] == "POSITIVE" else
                "⚡" if article['sentiment'] == "NEGATIVE" else
                "⚠️"
            )
            takeaways.append(
                f"{emoji} {article['title']} ({article['sentiment']})\n"
                f"   - {article['summary']}\n"
                f"   - Source: {article['source']}"
            )
        # Generate digest
        lines = [
            f"DAILY NEWS DIGEST: {self.topic.upper()}",
            f"Date: {date_str}",
            f"Articles: {len(articles)}", 
            sentiment_summary,
            "",
            "KEY TAKEAWAYS:"
        ]
        for tk in takeaways:
            lines.append(f"• {tk}")
        lines.append("")
        lines.append("SOURCES:")
        for i, article in enumerate(articles, 1):
            lines.append(f"[{i}] {article['url']}")

        return "\n".join(lines)


        