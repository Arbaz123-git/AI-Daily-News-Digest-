import requests 
import os 
from datetime import datetime, timedelta, timezone 
from dotenv import load_dotenv 

# load environment variables from .env file 
load_dotenv()

class NewsFetcher:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("NEWSAPI_KEY")
        if not self.api_key:
            raise ValueError("NEWSAPI_KEY not found in environment variables or .env file")
        self.base_url = "https://newsapi.org/v2/everything"

    def fetch_articles(self, query: str, num_articles: int = 5, days_back: int = 1, sources: str="", language: str = "en") -> list:
        """ 
        Fetch recent news articles based on user query 
        Returns list of artciles with: title, url, content, source, and publishedAt
        """
        # calculate date range 
        to_date = datetime.now(timezone.utc)
        from_date = to_date - timedelta(days=days_back)

        params = {
            "q": query, 
            "pageSize": num_articles, 
            "from": from_date.strftime("%Y-%m-%d"),
            "to": to_date.strftime("%Y-%m-%d"),
            "language": language,
            "sortBy": "relevancy",
            "apiKey": self.api_key # Make sure this is included 
        }

        if sources:
            params["sources"] = sources 

        try:
            response = requests.get(self.base_url, params=params)
            # Check for 401 specifically 
            if response.status_code == 401:
                print("401 Unauthorized: Check your API key")
                print(f"Key key: {self.api_key[:3]}...{self.api_key[-3:]}")
                print("Verify your key at https://newsapi_org/account")
                return []
            
            response.raise_for_status()
            data = response.json()

            if data['status'] == "ok":
                return [ 
                    {
                        "title": article['title'],
                        "url": article["url"],
                        "content": article["content"] or article["description"] or "",
                        "source": article["source"]["name"],
                        "published": article["publishedAt"]
                    }
                    for article in data["articles"]
                ]

            else:
                print(f"API Error: {data.get('message', 'Unknown error')}")
                return []


        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            return [] 
