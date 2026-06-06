import os
import json
import numpy as np
import faiss
import config
from embedding_client import embedding_client


class VectorStore:
    def __init__(self, index_path: str = None):
        self.index_path = index_path or config.VECTOR_STORE_PATH
        self.index = None
        self.metadata = []
        self.dimension = None

    def build_index(self, chunks: list[dict]):
        texts = [c["chunk_text"] for c in chunks]
        embeddings = embedding_client.embed_documents(texts)
        self.dimension = len(embeddings[0])
        vectors = np.array(embeddings, dtype="float32")
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(vectors)
        self.metadata = chunks
        self.save()

    def save(self):
        os.makedirs(self.index_path, exist_ok=True)
        faiss.write_index(self.index, os.path.join(self.index_path, "index.faiss"))
        with open(os.path.join(self.index_path, "metadata.json"), "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)

    def load(self):
        index_file = os.path.join(self.index_path, "index.faiss")
        meta_file = os.path.join(self.index_path, "metadata.json")
        if not os.path.exists(index_file) or not os.path.exists(meta_file):
            return False
        self.index = faiss.read_index(index_file)
        with open(meta_file, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)
        return True

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        if self.index is None:
            if not self.load():
                return [{
                    "error": "向量索引不存在，请先运行 python scripts/ingest_docs.py 构建知识库索引。"
                }]
        query_vec = np.array([embedding_client.embed_text(query)], dtype="float32")
        distances, indices = self.index.search(query_vec, min(top_k, len(self.metadata)))
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.metadata):
                item = self.metadata[idx].copy()
                item["score"] = float(dist)
                results.append(item)
        return results


vector_store = VectorStore()
