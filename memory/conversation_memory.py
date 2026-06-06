import json
import os
from datetime import datetime
import config


class ConversationMemory:
    def __init__(self, max_turns: int = 10):
        self.max_turns = max_turns
        self.memory_path = config.MEMORY_PATH
        os.makedirs(self.memory_path, exist_ok=True)

    def _get_session_file(self, session_id: str) -> str:
        return os.path.join(self.memory_path, f"{session_id}.json")

    def load_session(self, session_id: str) -> list[dict]:
        filepath = self._get_session_file(session_id)
        if not os.path.exists(filepath):
            return []
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_turn(self, session_id: str, user_id: str, role: str, query: str, answer: str):
        history = self.load_session(session_id)
        history.append({
            "user_id": user_id,
            "role": role,
            "query": query,
            "answer": answer,
            "timestamp": datetime.now().isoformat(),
        })
        if len(history) > self.max_turns:
            history = history[-self.max_turns:]
        filepath = self._get_session_file(session_id)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    def get_history(self, session_id: str) -> list[dict]:
        return self.load_session(session_id)


conversation_memory = ConversationMemory()
