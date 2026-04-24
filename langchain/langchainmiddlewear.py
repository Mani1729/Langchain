from dotenv import load_dotenv
from langchain.agents import create_agent
from dataclasses import dataclass
from langchain_openai import AzureChatOpenAI
from langchain.agents.middleware import ModelRequest, ModelResponse, dynamic_prompt

load_dotenv()


@dataclass
class Context:
    user_role: str

model = AzureChatOpenAI(
    azure_endpoint="https://your-resource-name.openai.azure.com",
    api_key="YOUR_AZURE_OPENAI_API_KEY",
    api_version="2025-01-01-preview",
    deployment_name="gpt-4o-mini",
    temperature=0
)

@dynamic_prompt
def user_role_request(request: ModelRequest) -> str:
    """Modify the prompt based on user role in context."""
    user_role = request.runtime.context.user_role
    base_prompt = "You are helpfull and very knowledgeable AI assistant."
    if user_role == "admin":
        return f"You are an admin user. {base_prompt} Provide detailed and technical explanations."
    elif user_role == "guest":
        return f"You are a guest user. {base_prompt} Provide simple and easy-to-understand explanations."
    else:
        return base_prompt
    
agent = create_agent(
        model=model,    
        middleware=[user_role_request],
        context_schema= Context,
    )

response = agent.invoke({'messages': [
    {"role": "user", "content": "Explain the concept of cloud computing."}]},
    context= Context(user_role="guest")
)

# print(response);
print(response['messages'][-1].content);
  