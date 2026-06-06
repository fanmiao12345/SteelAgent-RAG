from llm_client import llm_client
from prompts.system_prompt import SYSTEM_PROMPT
from prompts.rag_prompt import RAG_PROMPT


def generate_answer(
    query: str,
    context: str = "",
    tool_result: dict = None,
    history: list[dict] = None,
    citations: list[dict] = None,
    retrieval_errors: list[str] = None,
) -> str:
    parts = []

    if context:
        parts.append(f"参考资料：\n{context}")

    if tool_result:
        parts.append(f"工具计算结果：\n{str(tool_result)}")

    if history:
        history_text = "\n".join(
            [f"用户: {h['query']}\n助手: {h['answer']}" for h in history[-5:]]
        )
        parts.append(f"历史对话：\n{history_text}")

    parts.append(f"用户问题：{query}")
    parts.append("请使用中文回答；如果参考资料中有文档编号，请在答案中说明依据来源。")

    user_prompt = "\n\n".join(parts)

    messages = llm_client.build_messages(SYSTEM_PROMPT, user_prompt)
    answer = llm_client.chat(messages)

    notes = []
    if citations:
        source_text = "、".join(
            f"{c.get('title', '未知文档')}({c.get('doc_id', 'unknown')})" for c in citations
        )
        if "依据来源" not in answer and "参考来源" not in answer:
            notes.append(f"参考来源：{source_text}")
    if retrieval_errors:
        notes.append("检索提示：" + "；".join(retrieval_errors))
    if notes:
        answer = answer.rstrip() + "\n\n" + "\n".join(notes)
    return answer
