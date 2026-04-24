"""
Batch update all notebooks to use Azure OpenAI
"""
import json
import os
import re
from pathlib import Path

# Setup code to add to the first cell
SETUP_CODE = """import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to import azure_openai_config
sys.path.append(os.path.join(os.path.dirname(os.path.abspath('__file__')), '..', '..'))

load_dotenv()

from azure_openai_config import setup_azure_openai, get_azure_openai_model
setup_azure_openai()"""

def update_notebook(notebook_path):
    """Update a single notebook to use Azure OpenAI"""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    changes = 0
    
    for i, cell in enumerate(notebook['cells']):
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source'])
            
            # Update first cell with load_dotenv()
            if i == 0 or 'load_dotenv()' in source:
                if 'azure_openai_config' not in source:
                    cell['source'] = [line + '\n' for line in SETUP_CODE.split('\n')]
                    changes += 1
                    continue
            
            # Replace model initializations
            original_source = source
            
            # Replace init_chat_model calls
            source = re.sub(
                r'init_chat_model\(\s*model\s*=\s*["\']gpt-5-nano["\']\s*,',
                'get_azure_openai_model(',
                source
            )
            source = re.sub(
                r'init_chat_model\(\s*model\s*=\s*["\']gpt-5-nano["\']\s*\)',
                'get_azure_openai_model()',
                source
            )
            source = re.sub(
                r'init_chat_model\(["\']gpt-5-nano["\']\)',
                'get_azure_openai_model()',
                source
            )
            source = re.sub(
                r'init_chat_model\(["\']claude-sonnet-4-5["\']\)',
                'get_azure_openai_model()',
                source
            )
            
            # Replace model= parameters in create_agent and other functions
            source = re.sub(
                r'model\s*=\s*["\']gpt-5-nano["\']',
                'model=get_azure_openai_model()',
                source
            )
            source = re.sub(
                r'model\s*=\s*["\']gpt-4o-mini["\']',
                'model=get_azure_openai_model()',
                source
            )
            source = re.sub(
                r'model\s*=\s*["\']gpt-4o-audio-preview["\']',
                'model=get_azure_openai_model()',
                source
            )
            source = re.sub(
                r'model\s*=\s*["\']claude-sonnet-4-5["\']',
                'model=get_azure_openai_model()',
                source
            )
            
            # Update OpenAIEmbeddings
            if 'OpenAIEmbeddings' in source and 'AzureOpenAIEmbeddings' not in source:
                source = source.replace(
                    'from langchain_openai import OpenAIEmbeddings',
                    'from langchain_openai import AzureOpenAIEmbeddings'
                )
                source = re.sub(
                    r'OpenAIEmbeddings\(model=["\']text-embedding-3-large["\']\)',
                    '''AzureOpenAIEmbeddings(
    azure_deployment="text-embedding-3-large",
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview"),
)''',
                    source
                )
            
            if source != original_source:
                cell['source'] = [line + '\n' if not line.endswith('\n') else line 
                                 for line in source.split('\n')]
                # Remove the extra newline at the end
                if cell['source'] and cell['source'][-1] == '\n':
                    cell['source'][-1] = ''
                changes += 1
    
    if changes > 0:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1, ensure_ascii=False)
        print(f"✓ Updated {notebook_path.name}: {changes} changes")
        return True
    return False

def main():
    """Update all notebooks in the workspace"""
    base_path = Path(__file__).parent
    notebooks_path = base_path / 'notebooks'
    
    # Skip these notebooks (already manually updated)
    skip = ['1.1_prompting.ipynb', '1.1_foundational_models.ipynb']
    
    updated = 0
    for notebook_path in notebooks_path.rglob('*.ipynb'):
        if notebook_path.name in skip:
            print(f"⊘ Skipping {notebook_path.name} (already updated)")
            continue
        
        if '.ipynb_checkpoints' in str(notebook_path):
            continue
            
        if update_notebook(notebook_path):
            updated += 1
    
    print(f"\n✓ Updated {updated} notebooks")

if __name__ == '__main__':
    main()
