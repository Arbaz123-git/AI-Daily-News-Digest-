# 3 
import os 
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.schema import StrOutputParser


class SentimentAnalyzer:
    def __init__(self, model_name="llama3-70b-8192"):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")
        
        self.model = ChatGroq(
            temperature=0.1,  # Lower temperature for classification
            model_name=model_name,
            api_key=self.groq_api_key
        )
        self.sentiment_prompt = PromptTemplate.from_template(
            """Classify the sentiment of the following news summary as POSITIVE, NEGATIVE, or NEUTRAL.
            Consider these guidelines:
            1. POSITIVE: Describes growth, success, breakthroughs, or favorable outcomes
            2. NEGATIVE: Describes failures, controversies, losses, or unfavorable outcomes
            3. NEUTRAL: Balanced reporting, announcements without clear positive/negative slant
            
            Respond ONLY with one word: POSITIVE, NEGATIVE, or NEUTRAL
            
            News Summary:
            {summary}
            Sentiment:"""
        )
        self.sentiment_chain = (
            {"summary": RunnablePassthrough()} 
            | self.sentiment_prompt
            | self.model
            | StrOutputParser()
        )

    def analyze(self, summary: str) -> str:
        """Analyze sentiment of a news summary"""
        if "unavailable" in summary.lower() or len(summary) < 20:
            return "NEUTRAL"
        
        try:
            sentiment = self.sentiment_chain.invoke(summary)
            # Clean and standardize the output
            sentiment = sentiment.strip().upper()
            if "POSITIVE" in sentiment:
                return "POSITIVE"
            elif "NEGATIVE" in sentiment:
                return "NEGATIVE"
            return "NEUTRAL"
        except Exception as e:
            print(f"Sentiment analysis failed: {str(e)}")
            return "NEUTRAL"

