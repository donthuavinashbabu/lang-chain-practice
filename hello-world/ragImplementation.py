import os
# from lib2to3.fixes.fix_input import context

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_ollama import OllamaEmbeddings

load_dotenv()

print("Initializing components")
# openai_embeddings = OpenAIEmbeddings()
# google_embeddings = GoogleGenerativeAIEmbeddings()
ollama_embeddings = OllamaEmbeddings(model="nomic-embed-text")

print("Initializing LLMs")
# openai_llm = ChatOpenAI()
google_llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        # value 0 to 0.3 make response deterministic, factual, probably repeatable
        # 0.8 to 1 - get creative results
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
ollama_llm = ChatOllama(
        # ollama with google gemma3:270m model
        model="gemma3:270m",
        # model="gpt-oss:latest",
        # value 0 to 0.3 make response deterministic, factual, probably repeatable
        # 0.8 to 1 - get creative results
        temperature=1,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

print("Initializing Vector Store")
vectorStore = PineconeVectorStore(index_name=os.environ["INDEX_NAME"], embedding=ollama_embeddings)
vectorStoreRetriever = vectorStore.as_retriever(search_kwargs={"k": 5}) # k=3 means while searching relevant document limit to 3 documents

promptTemplate = ChatPromptTemplate.from_template(
    """Answer the questions based only on the following content:
    
    {context}
    
    Question: {question}
    
    Provide details answer:"""
)

# form one string from multiple documents
def format_docs(docs):
    """Format retrieved documents from vector into one single string"""
    return "\n\n".join(doc.page_content for doc in docs)

def retrieval_chain_without_langchain_lcel(query: str):
    """
    Retrieval of chain without lcel (LangChain Expression Language)
    """
    # step 1 - retrieve relevant documents
    docs = vectorStoreRetriever.invoke(query)

    # Step 2 - Format documents to context string
    context = format_docs(docs)

    # Step 3 - format the prompt with context and question
    messages = promptTemplate.format_messages(context=context, question=query)

    response = google_llm.invoke(messages)
    return response.content

def create_retrieval_chain_with_lcel():
    """
    Create retrieval chain using LCEL
    """
    retrievalChain = (
        RunnablePassthrough.assign(
            context=itemgetter("question") | vectorStoreRetriever | format_docs
        )
        | promptTemplate | google_llm | StrOutputParser()
    )
    return retrievalChain

if __name__ == "__main__":
    print("Retrieving")

    # query
    query1 = "How to read all records from a table in SQL?"
    query2 = "What is the use of DISTINCT keyword in SQL?"
    query3 = "Give sample DISTINCT keyword query?"

    # Without RAG
    # print("Implementation - RAW LLM")
    # response1 = google_llm.invoke(HumanMessage(content=query))
    # print(response1.content)

    # RAG implementation without LCEL
    # response2 = retrieval_chain_without_langchain_lcel(query)
    # print(response2)

    # RAG implementation with LCEL
    chainWithLcel = create_retrieval_chain_with_lcel()
    response3 = chainWithLcel.invoke({"question": query3})
    print(response3)