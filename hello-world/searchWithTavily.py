import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    print("Searching with Tavily")
    client = TavilyClient(os.environ["TAVILY_API_KEY"])
    response = client.search(
        query="What is the best LLM in the market?",
        search_depth="advanced"
    )
    print(response)
    print("Search completed")