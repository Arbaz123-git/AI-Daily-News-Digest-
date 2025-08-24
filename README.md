AI-Powered News Digest Assistant
An intelligent news aggregation and summarization tool that fetches, analyzes, and generates concise news digests on specific topics using AI. Now available with both CLI and interactive web interfaces!

✨ Features
Topic-Based News Fetching: Retrieve relevant news articles on any topic using NewsAPI
AI-Powered Summarization: Generate concise, professional summaries using Groq's LLM API
Sentiment Analysis: Automatically classify news sentiment as positive, negative, or neutral
Daily Digest Generation: Compile processed articles into well-formatted digests with sentiment distribution
Robust Text Extraction: Extract full article content with fallback mechanisms
Interactive Web Interface: User-friendly Streamlit web application for easy interaction
Real-time Processing: Watch articles being processed live
Downloadable Reports: Save generated digests as text files
🏗️ Components
News Fetcher
Fetches recent news articles based on user-defined topics, timeframes, and sources using the NewsAPI.

Text Extractor & Summarizer
Extracts full article content from URLs and generates professional 2-paragraph summaries using Groq's LLM API with robust error handling.

Sentiment Analyzer
Classifies news summaries as positive, negative, or neutral using Groq's LLM API with specialized prompts.

Digest Generator
Compiles processed articles into well-formatted daily digests with sentiment distribution statistics and key takeaways.

Streamlit Web Interface
Interactive web application providing:

Clean, intuitive user interface
Real-time news digest generation
Topic selection with custom input
Adjustable article count and timeframe
Visual sentiment analysis display
Download functionality
🚀 Setup
Prerequisites
Python 3.8+
NewsAPI key (get from newsapi.org)
Groq API key (get from console.groq.com)
Internet connection for fetching articles
Installation
1.
Clone the repository
2.
Install dependencies:
Bash



Run
pip install -r requirements.txt
3.
Create a .env file with your API keys:
PlainText



NEWSAPI_KEY=your_newsapi_keyGROQ_API_KEY=your_groq_api_key
📱 Usage Options
Option 1: Web Interface (Recommended)
Bash



Run
# Run the Streamlit web applicationstreamlit run app.py
Web Interface Features:

Topic Selection: Enter any news topic in the input field
Article Count: Choose 1-10 articles with a slider
Timeframe: Select 1-7 days back with dropdown
Real-time Processing: Watch live progress as articles are fetched, summarized, and analyzed
Visual Results: Clean display with sentiment indicators (🟢 Positive, 🔴 Negative, 🟡 Neutral)
Download: Save your digest as a text file with one click
Responsive Design: Works on desktop and mobile browsers
Option 2: Command Line Interface
Bash



Run
# Run the CLI versionpython main.py
CLI Customization Parameters:

topic: News topic to search for (default: "AI Startups")
num_articles: Number of articles to fetch (1-10)
days_back: Days back to search (1-7)
model_name: Groq LLM model (default: "llama3-8b-8192")
🎨 Web Interface Walkthrough
1.
Launch: Run streamlit run app.py and open http://localhost:8501
2.
Configure: Enter your topic, select article count and timeframe
3.
Generate: Click "Generate News Digest" to start processing
4.
Monitor: Watch real-time progress with status updates
5.
Review: View summaries with sentiment analysis
6.
Download: Save your digest as news_digest_YYYYMMDD.txt
🔧 Customization
Web Interface
All parameters can be configured through the Streamlit interface:

Custom topic input
Adjustable article count (1-10)
Flexible timeframe selection (1-7 days)
Model selection dropdown
Command Line
Modify parameters directly in main.py:

Python



topic = "Your Topic Here"num_articles = 5days_back = 1model_name = "llama3-8b-8192"
📋 Dependencies
Key packages include:

streamlit: Web interface framework
langchain-groq: LLM integration
beautifulsoup4: Web scraping
requests: HTTP client
python-dotenv: Environment management
nltk: Text processing
🐛 Troubleshooting
Common Issues
ModuleNotFoundError: Run pip install -r requirements.txt
API Key Error: Ensure .env file exists with valid keys
Streamlit Not Found: Install with pip install streamlit
Port Already in Use: Streamlit will automatically use next available port
Getting Help
Check the .env.example file for API key format
Ensure stable internet connection for API calls
Verify NewsAPI and Groq API key validity
📝 License
MIT License - See LICENSE file for details.

🤝 Contributing
Contributions are welcome! Feel free to submit issues and pull requests to improve the web interface or add new features.

⭐ Star this repository if you find it useful!