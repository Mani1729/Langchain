import json
import sys

notebook_path = sys.argv[1]
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    source = ''.join(cell.get('source', []))
    if 'langchain_openai import ChatOpenAI' in source:
        print(f"Cell {i}: ID={cell.get('id', 'no-id')}")
        print(f"  Lines: {source[:200]}")
        print()
