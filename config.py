import os
from dotenv import load_dotenv

load_dotenv()

LLM_API_URL = os.getenv("LLM_API_URL", "https://token-plan-cn.xiaomimimo.com/v1/chat/completions")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "mimo-v2.5-pro")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")

EMBEDDING_API_URL = os.getenv("EMBEDDING_API_URL", "http://10.199.194.246:11434/api/embeddings")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "bge-m3")

VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "storage/vector_index")
MEMORY_PATH = os.getenv("MEMORY_PATH", "storage/memory")
AUDIT_LOG_PATH = os.getenv("AUDIT_LOG_PATH", "logs/audit.log")
