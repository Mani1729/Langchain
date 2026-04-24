# Chat Model Documents: https://python.langchain.com/v0.2/docs/integrations/chat/
# OpenAI Chat Model Documents: https://python.langchain.com/v0.2/docs/integrations/chat/openai/

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

# Load environment variables from .env
load_dotenv()

# Create a ChatOpenAI model
model = AzureChatOpenAI(
    azure_deployment="gpt-4o",
    api_version="2025-01-01-preview"
)

# Invoke the model with a message
result = model.invoke("What is 81 divided by 9?")
print("Full result:")
print(result)
print("Content only:")
print(result.content)
