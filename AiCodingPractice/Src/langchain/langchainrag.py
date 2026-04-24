import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.tools import tool
from langchain.messages import HumanMessage
from pprint import pprint


load_dotenv()


model = AzureChatOpenAI(
    azure_deployment="gpt-4o",
    api_version="2025-01-01-preview",
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)


loader = PyPDFLoader("acmecorp-employee-handbook.pdf")

data = loader.load()


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,chunk_overlap=100, add_start_index=True)

all_splits = text_splitter.split_documents(data)

# print(len(all_splits))



embeddings = AzureOpenAIEmbeddings(
    azure_deployment="text-embedding-ada-002",
    api_version="2025-01-01-preview",
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

vector_store = InMemoryVectorStore(embeddings)

ids = vector_store.add_documents(documents=all_splits)

results = vector_store.similarity_search(
    "How many days of vacation does an employee get in their first year?"
)

# print(results[0])



@tool
def search_handbook(query: str) -> str:
    """Search the employee handbook for information"""
    results = vector_store.similarity_search(query)
    return results[0].page_content

from langchain.agents import create_agent

agent = create_agent(
    model=model,
    tools=[search_handbook],
    system_prompt="You are a helpful agent that can search the employee handbook for information."
    )

response = agent.invoke(
    {"messages": [HumanMessage(content="How many days of vacation does an employee get in their first year?")]}
)

pprint(response["messages"][-1].content)