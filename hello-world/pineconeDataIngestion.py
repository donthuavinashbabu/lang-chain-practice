import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

def hello(name: str):
    print(f'Hello {name}')

def printenvs() -> None:
    print(os.environ['PINECONE_API_KEY'])

if __name__ == '__main__':
    hello("World")
    printenvs()

    print("Loading file")
    # loader = PyPDFLoader(file_path="C:/MyPC/one-place/study/Top-10-java-performance-problems.pdf")
    loader = PyPDFLoader(file_path="C:/MyPC/one-place/books/SQLNotes.pdf")
    document = loader.load()  # load to langchain document

    print("Splitting")
    textSplitter =  CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = textSplitter.split_documents(document)
    print(f"created {len(texts)} chunks")

    # openai_embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))
    # models/embedding-001 or models/text-embedding-004
    google_genai_embeddings =GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.environ.get("GOOGLE_API_KEY"))
    ollama_embeddings = OllamaEmbeddings(model="nomic-embed-text")

    print("Ingestion")
    # PineconeVectorStore.from_documents(texts, openai_embeddings, index_name=os.environ.get("INDEX_NAME"))
    PineconeVectorStore.from_documents(texts, ollama_embeddings, index_name=os.environ.get("INDEX_NAME"))
    # PineconeVectorStore.from_documents(texts, google_genai_embeddings, index_name=os.environ.get("INDEX_NAME"))
    print("Finish")