import json
import os

def load_servers():
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    json_path = os.path.join(parent_dir, 'servers.json')

    if not os.path.exists(json_path):
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)

    with open(json_path, 'r', encoding='utf-8') as fp:
        return json.load(fp)