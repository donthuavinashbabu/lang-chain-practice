import os
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader, DirectoryLoader

load_dotenv()

def main():
    print("Hello from langchain-chromadb!")


if __name__ == "__main__":
    main()
