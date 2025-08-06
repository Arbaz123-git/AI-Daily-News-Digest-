# AI-Powered News Digest Assistant

An intelligent news aggregation and summarization tool that fetches, analyzes, and generates concise news digests on specific topics using AI.

## Features

- **Topic-Based News Fetching**: Retrieve relevant news articles on any topic using NewsAPI
- **AI-Powered Summarization**: Generate concise, professional summaries of news articles using Groq's LLM API
- **Sentiment Analysis**: Automatically classify news sentiment as positive, negative, or neutral
- **Daily Digest Generation**: Compile processed articles into a well-formatted digest with sentiment distribution
- **Robust Text Extraction**: Extract full article content from web pages with fallback mechanisms

## Components

### News Fetcher
Fetches recent news articles based on user-defined topics, timeframes, and sources using the NewsAPI.

### Text Extractor & Summarizer
Extracts full article content from URLs and generates professional 2-paragraph summaries using Groq's LLM API. Includes robust error handling and fallback mechanisms.

### Sentiment Analyzer
Classifies news summaries as positive, negative, or neutral using Groq's LLM API with a specialized prompt.

### Digest Generator
Compiles processed articles into a well-formatted daily digest with sentiment distribution statistics and key takeaways.

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys:
   ```
   NEWSAPI_KEY=your_newsapi_key
   GROQ_API_KEY=your_groq_api_key
   ```

## Usage

```python
# Run the main script
python main.py
```

The script will:
1. Fetch recent news articles on the specified topic
2. Extract and summarize the content of each article
3. Analyze the sentiment of each summary
4. Generate a daily digest with all processed articles
5. Save the digest to a text file with the current date

## Customization

You can customize the following parameters in `main.py`:
- `topic`: The news topic to search for
- `num_articles`: Number of articles to fetch
- `days_back`: How many days back to search for news
- `model_name`: The Groq LLM model to use

## Requirements

- Python 3.8+
- NewsAPI key
- Groq API key
- Internet connection for fetching articles

## License

MIT