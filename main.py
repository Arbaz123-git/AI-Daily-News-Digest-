# 5

from datetime import datetime, timezone
from src.news_fetcher import NewsFetcher 
from src.text_extract_summarizer import ArticleSummarizer 
from src.analyze_sentiment import SentimentAnalyzer
from src.digest_generator import DailyDigestGenerator 
from dotenv import load_dotenv 

load_dotenv()
def main():
    load_dotenv()
    topic = "AI Startups"

    fetcher = NewsFetcher()
    summarizer = ArticleSummarizer()
    sentiment_analyzer = SentimentAnalyzer(model_name="llama3-8b-8192")
    digest_generator = DailyDigestGenerator(topic)

    # Get and process articles
    raw_articles = fetcher.fetch_articles(query=topic, num_articles=5, days_back=1)
    processed_articles = []

    for article in raw_articles:
        summary = summarizer.summarize(article)
        sentiment = sentiment_analyzer.analyze(summary)
        processed_articles.append({
            "title": article['title'],
            "source": article['source'],
            "url": article['url'],
            "summary": summary,
            "sentiment": sentiment
        })

    # Generate and save digest
    digest = digest_generator.generate(processed_articles)
    print(digest)
    filename = f"news_digest_{datetime.now(timezone.utc).strftime('%Y%m%d')}.txt"
    # Open file with utf-8 encoding to support emojis
    with open(filename, "w", encoding="utf-8") as f:
        f.write(digest)
    print(f"\nDigest saved to {filename}")

if __name__ == "__main__":
    main()
