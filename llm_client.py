import requests
import config


class LLMClient:
    def __init__(self):
        self.api_url = config.LLM_API_URL
        self.model_name = config.LLM_MODEL_NAME
        self.api_key = config.LLM_API_KEY
        self.timeout = 60

    def build_messages(self, system_prompt: str, user_prompt: str) -> list[dict]:
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    def chat(self, messages: list[dict], temperature: float = 0.3) -> str:
        if not self.api_key:
            return self.fallback_chat(messages[-1]["content"] if messages else "")

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": self.model_name,
                "messages": messages,
                "temperature": temperature,
            }
            resp = requests.post(
                self.api_url, json=payload, headers=headers, timeout=self.timeout
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[LLM 调用失败: {e}]"

    def fallback_chat(self, prompt: str) -> str:
        return (
            f"[Fallback 模式] 当前未配置 LLM_API_KEY，无法调用大模型。\n"
            f"您的问题是：{prompt}\n"
            f"请在 .env 文件中配置 LLM_API_KEY 后重试。"
        )


llm_client = LLMClient()
