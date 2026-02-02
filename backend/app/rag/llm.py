import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
google_api_key = os.environ['GOOGLE_API_KEY']
llm = ChatGoogleGenerativeAI(
    api_key = google_api_key,
    model = 'gemini-2.5-flash-preview-09-2025'
)
