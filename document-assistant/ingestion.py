import os
import ssl
import certifi
import asyncio
from typing import List, Dict, Any
from dotenv import load_dotenv

# langchain imports 
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_tavily import TavilyCrawl, TavilyExtract, TavilyMap
from langchain_pinecone import PineconeVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

# read pdf file and return documents
def ingest_documents(file_path: str):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents

ssl_context = ssl.create_default_context(cafile=certifi.where())
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

ollama_embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
    )

chromaVectorStore = Chroma(persist_directory="chroma_db", embedding_function=ollama_embeddings)
pineconeVectorStore = PineconeVectorStore(index_name=os.environ["INDEX_NAME"], embedding=ollama_embeddings)
tavilyExtract = TavilyExtract(api_key=os.environ["TAVILY_API_KEY"])
tavilyMap = TavilyMap(api_key=os.environ["TAVILY_API_KEY"], max_depth=5, max_breadth=20, max_pages=1000)
tavilyCrawl = TavilyCrawl(api_key=os.environ["TAVILY_API_KEY"], max_depth=5, max_breadth=20, max_pages=1000)

async def main():
    print("Crawling python langchain documentation")
    crawlResult = tavilyCrawl.invoke({
        # "url": "https://python.langchain.com/docs/",
        # "url": "https://python.langchain.com/",
        "url": "https://github.com/donthuavinashbabu/book",
        "max_depth": 50,
        "extract_depth": "advanced"
        # "instructions": "content on ai agents" # used to filter the content while crawling
        })
    crawlDocs = crawlResult["results"]
    print(f"Crawled {len(crawlDocs)} documents")
    allDocs = [Document(page_content=doc["raw_content"], metadata={"source": doc["url"]}) for doc in crawlDocs]

    # split the documents into chunks
    textSplitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
    splittedDocs = textSplitter.split_documents(allDocs)
    print(f"Created {len(splittedDocs)} chunks")

    # embeddings
    # openai_embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))
    # google_genai_embeddings = GoogleGenerativeAIEmbeddings(google_gemini_api_key=os.environ.get("GOOGLE_GEMINI_API_KEY"))
    # ollama_embeddings = OllamaEmbeddings(model="nomic-embed-text")
    # models/embedding-001 or models/text-embedding-004
    google_genai_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.environ.get("GOOGLE_API_KEY"))
    ollama_embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # ingestion
    print("Ingestion")
    # PineconeVectorStore.from_documents(texts, openai_embeddings, index_name=os.environ.get("INDEX_NAME"))
    PineconeVectorStore.from_documents(splittedDocs, ollama_embeddings, index_name=os.environ.get("INDEX_NAME"))
    # PineconeVectorStore.from_documents(texts, google_genai_embeddings, index_name=os.environ.get("INDEX_NAME"))
    print("Finish")

if __name__ == "__main__":
    asyncio.run(main())