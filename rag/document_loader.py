import json
import os


def load_documents(docs_dir: str = "data/docs") -> list[dict]:
    documents = []
    if not os.path.exists(docs_dir):
        return documents
    for filename in os.listdir(docs_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(docs_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    documents.extend(data)
                else:
                    documents.append(data)
    return documents
