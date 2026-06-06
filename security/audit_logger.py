import json
import os
from datetime import datetime
import config


def log_request(
    session_id: str,
    user_id: str,
    role: str,
    query: str,
    decision: str,
    used_tools: list[str] = None,
    used_docs: list[str] = None,
):
    log_dir = os.path.dirname(config.AUDIT_LOG_PATH)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "session_id": session_id,
        "user_id": user_id,
        "role": role,
        "query": query,
        "decision": decision,
        "used_tools": used_tools or [],
        "used_docs": used_docs or [],
    }

    with open(config.AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
