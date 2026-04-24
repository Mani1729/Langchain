# Azure OpenAI Setup Guide for LangChain Essentials Course

## ✅ Configuration Complete

Your environment has been configured to use Azure OpenAI instead of standard OpenAI.

## 📋 What Was Set Up

### 1. Environment Variables (.env file)
The `.env` file has been created with your Azure OpenAI credentials:
- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint
- `AZURE_OPENAI_DEPLOYMENT_NAME`: gpt-4o
- `AZURE_OPENAI_API_VERSION`: 2025-01-01-preview

### 2. Helper Module (azure_openai_setup.py)
A helper module has been created to simplify Azure OpenAI usage in the notebooks.

## 🔧 How to Use Azure OpenAI in the Notebooks

### Method 1: Using the Helper Module (Recommended)

Instead of:
```python
from langchain.agents import create_agent

agent = create_agent(
    model="openai:gpt-5-mini",
    tools=[execute_sql],
    system_prompt=SYSTEM_PROMPT,
    context_schema=RuntimeContext,
)
```

Use:
```python
from langchain.agents import create_agent
from azure_openai_setup import get_model_string

agent = create_agent(
    model=get_model_string(),
    tools=[execute_sql],
    system_prompt=SYSTEM_PROMPT,
    context_schema=RuntimeContext,
)
```

### Method 2: Direct Configuration

You can also directly use AzureChatOpenAI:
```python
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_agent
import os

model = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    temperature=0,
)

agent = create_agent(
    model=model,
    tools=[execute_sql],
    system_prompt=SYSTEM_PROMPT,
    context_schema=RuntimeContext,
)
```

## 📝 Modifying Each Notebook

For each notebook (L1-L9), you'll need to update the model initialization. Here's what to change:

### Original Code Pattern:
```python
model = "openai:gpt-5-mini"  # or similar
```

### Updated Code Pattern:
```python
from azure_openai_setup import get_azure_chat_model

model = get_azure_chat_model()
```

## 🚀 Next Steps

1. **Install Dependencies** (if not already done):
   ```powershell
   cd c:\Users\manikanta.reddy\source\repos\lca-langchainV1-essentials\python
   pip install -r requirements.txt
   ```

2. **Ensure langchain-openai is installed** (required for Azure OpenAI):
   ```powershell
   pip install langchain-openai
   ```

3. **Start Jupyter Lab**:
   ```powershell
   jupyter lab
   ```

4. **Open L1_fast_agent.ipynb** and modify the cell where the agent is created:
   
   **Find this cell (around line 80):**
   ```python
   from langchain.agents import create_agent

   agent = create_agent(
       model="openai:gpt-5-mini",
       tools=[execute_sql],
       system_prompt=SYSTEM_PROMPT,
       context_schema=RuntimeContext,
   )
   ```
   
   **Change it to:**
   ```python
   from langchain.agents import create_agent
   from azure_openai_setup import get_model_string

   agent = create_agent(
       model=get_model_string(),
       tools=[execute_sql],
       system_prompt=SYSTEM_PROMPT,
       context_schema=RuntimeContext,
   )
   ```

5. **Test the setup** by running the first notebook cells

## 🔍 Troubleshooting

### If you get authentication errors:
- Verify your Azure OpenAI API key is correct in the `.env` file
- Ensure your endpoint URL is correct
- Check that your deployment name matches what's in Azure Portal

### If you get module import errors:
```powershell
pip install --upgrade langchain-openai langchain-core
```

### If you need to change the deployment:
Edit the `.env` file and update `AZURE_OPENAI_DEPLOYMENT_NAME` to match your Azure deployment name.

## 📚 Additional Notes

- **LangSmith**: If you want to use LangSmith tracing, add your LangSmith API key to the `.env` file
- **Studio Setup**: If using LangGraph Studio, copy the `.env` file to the studio directory:
  ```powershell
  Copy-Item .env .\studio\.env
  ```

## 🔐 Security Reminder

⚠️ **Never commit the `.env` file to version control!** It contains your API keys.

The `.env` file should already be in `.gitignore`, but double-check to ensure your credentials stay private.
