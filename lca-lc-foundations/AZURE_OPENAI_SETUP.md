# Azure OpenAI Configuration

This workspace has been configured to use **Azure OpenAI** instead of standard OpenAI API.

## Configuration Details

### Azure OpenAI Endpoint
- **Base URL**: `https://your-resource-name.openai.azure.com`
- **Deployment Name**: `gpt-4o`
- **API Version**: `2025-01-01-preview`

### Environment Variables

The following environment variables have been added to `example.env` and `.env`:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY='YOUR_AZURE_OPENAI_API_KEY'
AZURE_OPENAI_ENDPOINT='https://your-resource-name.openai.azure.com'
AZURE_OPENAI_DEPLOYMENT_NAME='gpt-4o'
AZURE_OPENAI_API_VERSION='2025-01-01-preview'
OPENAI_API_TYPE='azure'
```

## Changes Made

### 1. New Helper Module: `azure_openai_config.py`

Created a utility module at the root of the project that provides:
- `setup_azure_openai()`: Configures environment variables for Azure OpenAI
- `get_azure_openai_model(**kwargs)`: Returns a configured `AzureChatOpenAI` instance

### 2. Updated Notebooks

All Jupyter notebooks in the following directories have been updated:
- `notebooks/module-1/` (7 notebooks)
- `notebooks/module-2/` (8 notebooks)
- `notebooks/module-3/` (6 notebooks)

#### Changes in each notebook:

**First cell (dotenv setup):**
```python
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to import azure_openai_config
sys.path.append(os.path.join(os.path.dirname(os.path.abspath('__file__')), '..', '..'))

load_dotenv()

from azure_openai_config import setup_azure_openai, get_azure_openai_model
setup_azure_openai()
```

**Model initialization:**
- Replaced `model="gpt-5-nano"` with `model=get_azure_openai_model()`
- Replaced `model="gpt-4o-mini"` with `model=get_azure_openai_model()`
- Replaced `model="claude-sonnet-4-5"` with `model=get_azure_openai_model()`
- Replaced `init_chat_model(...)` with `get_azure_openai_model()`

### 3. Updated Python Files

The following standalone Python files have been updated:
- `notebooks/module-1/1.5_personal_chef.py`
- `notebooks/module-3/3.5_email_agent.py`

### 4. Embeddings Configuration

In `notebooks/module-2/bonus_rag.ipynb`, the embeddings have been updated:
```python
from langchain_openai import AzureOpenAIEmbeddings

embeddings = AzureOpenAIEmbeddings(
    azure_deployment="text-embedding-3-large",
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview"),
)
```

## Usage

### Running Notebooks

Simply run the notebooks as before. The first cell will automatically configure Azure OpenAI:

```python
# This is done automatically in the first cell of each notebook
from azure_openai_config import setup_azure_openai, get_azure_openai_model
setup_azure_openai()

# Create agents with Azure OpenAI
agent = create_agent(model=get_azure_openai_model())
```

### Custom Model Parameters

You can pass additional parameters to customize the model:

```python
# Custom temperature
model = get_azure_openai_model(temperature=1.0)

# Custom max tokens
model = get_azure_openai_model(max_tokens=500)

# Multiple parameters
model = get_azure_openai_model(
    temperature=0.7,
    max_tokens=1000,
    timeout=30
)
```

## Files Modified

### Configuration Files
- ✅ `example.env` - Added Azure OpenAI configuration
- ✅ `.env` - Created from example.env with Azure credentials
- ✅ `azure_openai_config.py` - New helper module

### Jupyter Notebooks
- ✅ All notebooks in `notebooks/module-1/` (7 files)
- ✅ All notebooks in `notebooks/module-2/` (8 files)
- ✅ All notebooks in `notebooks/module-3/` (6 files)

### Python Scripts
- ✅ `notebooks/module-1/1.5_personal_chef.py`
- ✅ `notebooks/module-3/3.5_email_agent.py`

### Utility Scripts
- ✅ `update_notebooks.py` - Script used to batch update notebooks

## Notes

- All notebooks now use the **Azure OpenAI gpt-4o deployment**
- The configuration is centralized in `azure_openai_config.py` for easy maintenance
- Original model names (e.g., "gpt-5-nano", "claude-sonnet-4-5") have been replaced with Azure OpenAI
- The MCP server file (`2.1_mcp_server.py`) was not modified as it doesn't use LLM agents

## Verification

To verify the configuration is working:

1. Open any notebook
2. Run the first cell to setup Azure OpenAI
3. Run any cell that creates an agent - it should now use Azure OpenAI
4. Check the response to confirm it's working

## Troubleshooting

If you encounter issues:

1. Verify environment variables are set correctly in `.env`
2. Ensure `azure_openai_config.py` is in the root directory
3. Check that the API key and endpoint are valid
4. Verify the deployment name matches your Azure OpenAI deployment

---

**Last Updated**: December 26, 2025
