# 2
import os 
import requests 
from langchain_groq import ChatGroq 
from langchain.prompts import PromptTemplate 
from langchain.schema import StrOutputParser 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
from bs4 import BeautifulSoup
#from newspaper import Article, ArticleException
import re 
import nltk 
import logging 
#from nltk.corpus import stopwords 
#from nltk.tokenize import sent_tokenize 

# Configure logging 
logging.basicConfig(level=logging.INFO, format='%(asctime)s -%(levelname)s - %(message)s')

# download required NLTK data 
#nltk.download('punkt')
#nltk.download('stopwords')

# load environment variables 
load_dotenv()

class FullTextExtractor:
    """Robust text extraction without newspaper library"""
    @staticmethod
    def extract_text(url: str) -> str:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'Referer': 'https://www.google.com/'
            }

            # Try to bypass paywalls for specific sites
            if "businessinsider.com" in url:
                headers['Referer'] = 'https://www.facebook.com/'
                headers['Cookie'] = 'bounceClientVisit=1; bounceClientFirstVisit=1'
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'lxml')

            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'aside', 'form', 'header', 
                                 'iframe', 'button', 'svg', 'figure', 'noscript', 'img', 'link']):
                element.decompose()

            # Find main content using common selectors
            selectors = [
                'article', 
                'div.article-body',
                'div.post-content',
                'div.story-content',
                'div.entry-content',
                'div.content-wrapper',
                'div.main-content',
                'section.main',
                'div.article-content',
                'div#article-body',
                'div.article-text',
                'div.post-body'
            ]
            
            article_body = None
            for selector in selectors:
                article_body = soup.select_one(selector)
                if article_body:
                    break

            # Fallback to body if no specific content found
            if not article_body:
                article_body = soup.body

            # Extract text with paragraph structure
            text = ""
            for element in article_body.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'blockquote']):
                if element.name == 'p':
                    text += element.get_text().strip() + "\n\n"
                elif element.name == 'blockquote':
                    text += f"> {element.get_text().strip()}\n\n"
                else:  # Headings
                    text += f"\n\n{element.get_text().strip().upper()}\n\n"

            # Clean and compress text
            text = re.sub(r'\n{3,}', '\n\n', text)  # Remove excessive newlines
            text = re.sub(r'\[\+[0-9,]+\s*chars?\]', '', text)  # Remove truncation markers
            return text.strip()
                
        except Exception as e:
            logging.error(f"Extraction failed for {url}: {str(e)}")
            return ""

class ArticleSummarizer:
    def __init__(self, model_name="llama3-70b-8192"):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")
        
        self.model = ChatGroq(
            temperature=0.3,
            model_name=model_name,
            api_key=self.groq_api_key
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=8000,
            chunk_overlap=300,
            length_function=len 
        )

        self.summary_prompt = PromptTemplate.from_template(
            """
            Create a professional 2-paragraph news summary from the following article content.
            Follow these guidelines:
            1. Omit any introductory phrases like "Here is a summary"
            2. First paragraph: Core innovation/event and key facts 
            3. Second paragraph: Key entities and business implications 
            4. Include specific numbers and metrics when available 
            5. Maintain jouranlistic tone

            Example structure:
            [Company] has [achievement] using [technology]. The development [specific impact]... 
            Key players include [names] from [organizations]. This could [business implication]...

            Article Content:
            {content}

            Professional Summary: 

            """ 
        )

        self.summary_chain = (
            {"content": RunnablePassthrough()}
            | self.summary_prompt
            | self.model
            |StrOutputParser()
        )

    def summarize(self, article: dict) -> str:
        """Robust summarization with multiple fallbacks"""
        # Get full article content 
        full_text = FullTextExtractor.extract_text(article['url'])

        # Use snippet if full text extraction failed 
        if not full_text.strip() or len(full_text) < 300:
            logging.warning(f"Using snippet for {article['url']}")
            full_text = self.clean_snippet(article['content'])
            if len(full_text) < 100:
                return "Summary unavailable: Could not retrieve content"
            
        # Clean and prepare text 
        clean_text = self.preprocess_text(full_text)
        logging.info(f"Processing text: {len(clean_text)} characters")
        
        # Handle long articles with chunking 
        if len(clean_text) > 8000:
            chunks = self.text_splitter.split_text(clean_text)
            chunk_summaries = []

            for i, chunk in enumerate(chunks, 1):
                logging.info(f"Summarizing chunk {i}/{len(chunks)}")
                chunk_summaries.append(self.summarize_chunk(chunk))
                
            combined_content = "\n\n".join(chunk_summaries)
            return self.summarize_chunk(combined_content)
        
        return self.summarize_chunk(clean_text)
     
    def summarize_chunk(self, text: str) -> str:
        """Handle single chunk summarization with error recovery"""
        try:
            return self.summary_chain.invoke(text)
        except Exception as e:
            logging.error(f"Summarization error: {str(e)}")
            return "Summary generation failed" 
        
    def preprocess_text(self, text: str) -> str:
        """Clean text before processing"""
        # Remove common boilerplate
        patterns = [
            r"Sign up for.*newsletters",
            r"Subscribe to.*channel",
            r"Follow us on.*",
            r"Download our.*app",
            r"Read more:.*",
            r"Continue reading.*",
            r"Advertisement",
            r"Recommended for you",
            r"Related:.*",
            r"Please enter your email",
            r"Already have an account\? Log in",
            r"Create a free account",
            r"© Copyright.*"
        ]
        
        
        for pattern in patterns:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)
        
        return text.strip()
        
    def clean_snippet(self, snippet: str) -> str:
        """Clean NewsAPI snippets"""
        # Remove truncation markers
        snippet = re.sub(r'\[\+[0-9,]+\s*chars?\]', '', snippet)
        # Remove HTML tags
        snippet = re.sub(r'<[^>]+>', '', snippet)
        return snippet
