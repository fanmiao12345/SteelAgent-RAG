from rag.vector_store import vector_store
from security.access_control import can_access_document


def retrieve(query: str, role: str = "visitor", top_k: int = 5) -> list[dict]:
    try:
        results = vector_store.search(query, top_k=top_k * 2)
    except Exception as exc:
        return [{"error": str(exc)}]
    if results and "error" in results[0]:
        return results
    filtered = []
    for r in results:
        if can_access_document(role, r.get("security_level", "public"), r.get("category", "")):
            filtered.append(r)
            if len(filtered) >= top_k:
                break
    return filtered
