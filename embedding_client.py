import requests
import config


class EmbeddingClient:
    def __init__(self):
        self.api_url = config.EMBEDDING_API_URL
        self.model_name = config.EMBEDDING_MODEL_NAME
        self.timeout = 60

    def embed_text(self, text: str) -> list[float]:
        try:
            payload = {"model": self.model_name, "prompt": text}
            resp = requests.post(self.api_url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            if "embedding" in data:
                return data["embedding"]
            if "embeddings" in data:
                return data["embeddings"][0]
            raise ValueError(f"响应中未找到 embedding 字段: {data.keys()}")
        except requests.ConnectionError:
            raise ConnectionError(
                f"Embedding 服务不可用，请检查 EMBEDDING_API_URL ({self.api_url}) 是否可访问。"
            )
        except Exception as e:
            raise RuntimeError(f"Embedding 调用失败: {e}")

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        results = []
        for text in texts:
            results.append(self.embed_text(text))
        return results


embedding_client = EmbeddingClient()
