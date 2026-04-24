from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
import os

load_dotenv()

client = AzureChatOpenAI(
    azure_deployment="gpt-4o",
    api_version="2025-01-01-preview",
    api_key= os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint= os.getenv("AZURE_OPENAI_ENDPOINT")
)

messages = [
            SystemMessage(content="You are a helpful assistant! Your name is Mani."),
            HumanMessage(content="What is your name?"),
        ]

response = client.invoke(messages)
# print(response.content)


tavily_search = TavilySearch(max_results=3, api_key=os.getenv("TAVILY_API_KEY"))

query = "What is LangChain?"
search_results = tavily_search.invoke(query)
search_docs = search_results.get("results", search_results)

for idx, result in enumerate(search_docs, start=1):
    print(f"Result {idx}:")
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Content: {result['content']}\n")





