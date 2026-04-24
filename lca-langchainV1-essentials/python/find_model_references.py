"""
Script to help identify where to make Azure OpenAI changes in the notebooks.
This script searches for model initialization patterns in all notebooks.
"""

import json
from pathlib import Path
import re

def find_model_references_in_notebook(notebook_path):
    """Find cells in a notebook that reference model initialization."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    results = []
    for i, cell in enumerate(nb.get('cells', [])):
        if cell.get('cell_type') != 'code':
            continue
        
        source = ''.join(cell.get('source', []))
        
        # Look for common model initialization patterns
        patterns = [
            r'model\s*=\s*["\']openai:',
            r'model\s*=\s*["\']anthropic:',
            r'ChatOpenAI\(',
            r'from langchain_openai import',
            r'create_agent\(',
        ]
        
        matches = []
        for pattern in patterns:
            if re.search(pattern, source, re.IGNORECASE):
                matches.append(pattern)
        
        if matches:
            results.append({
                'cell_number': i + 1,
                'patterns': matches,
                'preview': source[:200] + ('...' if len(source) > 200 else '')
            })
    
    return results

def main():
    """Find all notebooks and report model initialization locations."""
    python_dir = Path(__file__).parent
    notebooks = list(python_dir.glob('L*.ipynb'))
    
    print("=" * 80)
    print("Azure OpenAI Migration Helper")
    print("=" * 80)
    print("\nSearching for model initialization patterns in notebooks...\n")
    
    for nb_path in sorted(notebooks):
        results = find_model_references_in_notebook(nb_path)
        if results:
            print(f"\n📓 {nb_path.name}")
            print("-" * 80)
            for result in results:
                print(f"\n  Cell #{result['cell_number']}:")
                print(f"  Found patterns: {', '.join(result['patterns'])}")
                print(f"  Preview:\n    {result['preview'][:150]}")
    
    print("\n" + "=" * 80)
    print("\n💡 To update these notebooks:")
    print("   1. Add import: from azure_openai_setup import get_model_string")
    print("   2. Replace model=\"openai:...\" with model=get_model_string()")
    print("   3. Or replace ChatOpenAI(...) with get_azure_chat_model(...)")
    print("\n📖 See AZURE_SETUP.md for detailed instructions")
    print("=" * 80)

if __name__ == "__main__":
    main()
