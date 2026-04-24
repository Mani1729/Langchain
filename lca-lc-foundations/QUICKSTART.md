# Quick Start Guide - Azure OpenAI

## ✅ Migration Complete!

Your workspace has been successfully configured to use Azure OpenAI. Here's how to get started:

## 🚀 Getting Started

### 1. Environment is Ready
The `.env` file has been created with your Azure OpenAI credentials:
```env
AZURE_OPENAI_API_KEY=YOUR_AZURE_OPENAI_API_KEY
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2025-01-01-preview
```

### 2. All Notebooks Updated
Every notebook now automatically configures Azure OpenAI in the first cell:
```python
from azure_openai_config import setup_azure_openai, get_azure_openai_model
setup_azure_openai()
```

### 3. Run Any Notebook
Simply open any notebook and run the cells as normal. Examples:
- [notebooks/module-1/1.1_prompting.ipynb](notebooks/module-1/1.1_prompting.ipynb) ← You're here!
- [notebooks/module-1/1.2_tools.ipynb](notebooks/module-1/1.2_tools.ipynb)
- [notebooks/module-2/2.1_travel_agent.ipynb](notebooks/module-2/2.1_travel_agent.ipynb)

## 📖 Documentation

- **[AZURE_OPENAI_SETUP.md](AZURE_OPENAI_SETUP.md)** - Complete configuration details
- **[MIGRATION_SUMMARY.md](MIGRATION_SUMMARY.md)** - Full list of changes

## 🔧 How It Works

### Before (Old Code)
```python
agent = create_agent(model="gpt-5-nano")
```

### After (New Code)
```python
model = get_azure_openai_model()
agent = create_agent(model=model)
```

Or simplified:
```python
agent = create_agent(model=get_azure_openai_model())
```

## 💡 Tips

### Custom Model Parameters
```python
# Adjust temperature
model = get_azure_openai_model(temperature=0.7)

# Set max tokens
model = get_azure_openai_model(max_tokens=500)

# Multiple parameters
model = get_azure_openai_model(
    temperature=0.8,
    max_tokens=1000,
    timeout=30
)
```

### Running Your First Cell

In the current notebook (1.1_prompting.ipynb):
1. ▶️ Run the first cell to initialize Azure OpenAI
2. ▶️ Run the second cell to create an agent
3. ✅ You're now using Azure OpenAI!

## 📊 What Was Changed

- ✅ 21 Jupyter notebooks updated
- ✅ 2 Python scripts updated
- ✅ All model references changed to Azure OpenAI
- ✅ Environment configured
- ✅ Helper module created (`azure_openai_config.py`)

## 🆘 Need Help?

If something doesn't work:
1. Check that `.env` file exists in the root directory
2. Verify `azure_openai_config.py` is in the root directory
3. Make sure all cells in order are executed
4. Review [AZURE_OPENAI_SETUP.md](AZURE_OPENAI_SETUP.md) for troubleshooting

## 🎉 You're All Set!

Everything is configured and ready to go. Just run your notebooks normally and they'll use Azure OpenAI automatically.

---
**Next**: Run the first cell in your current notebook to test the setup!
