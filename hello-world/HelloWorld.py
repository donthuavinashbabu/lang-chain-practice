from itertools import chain

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

load_dotenv()

def getGoogleGeminiLLM():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        # value 0 to 0.3 make response deterministic, factual, probably repeatable
        # 0.8 to 1 - get creative results
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

def getOllamaLLM():
    return ChatOllama(
        # ollama with google gemma3:270m model
        model="gemma3:270m",
        # value 0 to 0.3 make response deterministic, factual, probably repeatable
        # 0.8 to 1 - get creative results
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

def generateFunnyFact(llm, information_key: str) -> str:
    summaryTemplate = """
            Give me 1 funny fact about {informationKey}
        """
    summaryPromptTemplate = PromptTemplate(
        input_variables=["informationKey"],
        template=summaryTemplate
    )
    # LangChain Expression Language (LCEL)
    chain = summaryPromptTemplate | llm
    response = chain.invoke(input={"informationKey": information_key})
    return response.content

def main():
    # use Google Gemini 2.5 Flash model
    # llm = getGoogleGeminiLLM()

    # use Ollama with Google Gemma 3:270m model
    llm = getOllamaLLM()

    informationValue = "Google"
    fact = generateFunnyFact(llm, informationValue)
    print(fact)

if __name__ == "__main__":
    main()