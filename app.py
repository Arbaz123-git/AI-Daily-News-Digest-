import streamlit as st
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
import sys
import pathlib

from src.news_fetcher import NewsFetcher 
from src.text_extract_summarizer import ArticleSummarizer 
from src.analyze_sentiment import SentimentAnalyzer
from src.digest_generator import DailyDigestGenerator 

# Set page configuration
st.set_page_config(
    page_title="AI News Digest Generator",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

def main():
    # App title and description
    st.title("📰 AI-Powered News Digest Generator")
    st.markdown("""
    This application automatically fetches news articles on your chosen topic, 
    summarizes key insights, analyzes sentiment, and generates a concise daily digest.
    """)

    # Sidebar for user inputs
    with st.sidebar:
        st.header("Configuration")

        # User inputs
        topic = st.text_input("Topic/Query", "AI Startups", 
                             help="Enter the topic you want news about (e.g., 'AI startups', 'quantum computing')")
        
        num_articles = st.slider("Number of Articles", 1, 10, 5, 
                                help="How many articles would you like to include in your digest?")
        
        days_back = st.slider("Days Back", 1, 7, 1, 
                             help="How many days back should we search for news?")
        
        # Model selection
        model_name = st.selectbox(
            "LLM Model for Summarization",
            ["llama3-70b-8192", "mixtral-8x7b-32768", "llama3-8b-8192"],
            index=0,
            help="Select the language model for summarization (larger models are more accurate but slower)"
        )

        # Generate button
        generate_btn = st.button("Generate Digest", type="primary")

    # Main content area
    if generate_btn:
        if not os.getenv("NEWSAPI_KEY") or not os.getenv("GROQ_API_KEY"):
            st.error("Please ensure NEWSAPI_KEY and GROQ_API_KEY are set in your .env file")
            return
        
        # Initialize components with progress indicators
        with st.spinner("Initializing components..."):
            fetcher = NewsFetcher()
            summarizer = ArticleSummarizer(model_name=model_name)
            sentiment_analyzer = SentimentAnalyzer(model_name="llama3-8b-8192")
            digest_generator = DailyDigestGenerator(topic)

        # Fetch articles
        with st.spinner(f"Fetching {num_articles} articles about '{topic}'..."):
            raw_articles = fetcher.fetch_articles(
                query=topic, 
                num_articles=num_articles, 
                days_back=days_back
            )

            if not raw_articles:
                st.error("No articles found. Please try a different topic or check your API keys.")
                return
            
        # Process articles
        processed_articles = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, article in enumerate(raw_articles):
            status_text.text(f"Processing article {i+1}/{len(raw_articles)}: {article['title'][:50]}...")

            # Summarize
            summary = summarizer.summarize(article)
            
            # Analyze sentiment
            sentiment = sentiment_analyzer.analyze(summary)
            
            processed_articles.append({
                "title": article['title'],
                "source": article['source'],
                "url": article['url'],
                "summary": summary,
                "sentiment": sentiment
            })

            progress_bar.progress((i + 1) / len(raw_articles))
        
        status_text.text("Generating final digest...")
        
        # Generate digest
        digest = digest_generator.generate(processed_articles)
        
        # Display results
        st.success("Digest generated successfully!")

        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["Digest", "Individual Articles", "Sentiment Analysis"])
        
        with tab1:
            st.subheader(f"Daily Digest: {topic}")
            st.text(digest)
            
            # Download button
            st.download_button(
                label="Download Digest as TXT",
                data=digest,
                file_name=f"news_digest_{datetime.now(timezone.utc).strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )

        with tab2:
            for i, article in enumerate(processed_articles, 1):
                with st.expander(f"Article {i}: {article['title']}"):
                    st.markdown(f"**Source:** {article['source']}")
                    st.markdown(f"**Sentiment:** {article['sentiment']}")
                    st.markdown(f"**URL:** {article['url']}")
                    st.markdown("**Summary:**")
                    st.write(article['summary'])

        with tab3:
            # Sentiment analysis visualization
            sentiment_counts = {
                "POSITIVE": 0,
                "NEGATIVE": 0, 
                "NEUTRAL": 0
            }
            
            for article in processed_articles:
                sentiment_counts[article['sentiment']] += 1
            
            # Display sentiment distribution
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Positive", sentiment_counts["POSITIVE"], 
                         delta=None, delta_color="normal")
            with col2:
                st.metric("Neutral", sentiment_counts["NEUTRAL"], 
                         delta=None, delta_color="off")
            with col3:
                st.metric("Negative", sentiment_counts["NEGATIVE"], 
                         delta=None, delta_color="inverse")
            
            # Simple bar chart
            st.bar_chart(sentiment_counts)

        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()

if __name__ == "__main__":
    main()


        
            

        
