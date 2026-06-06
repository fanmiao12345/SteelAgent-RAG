def format_citations(results: list[dict]) -> list[dict]:
    seen = set()
    citations = []
    for r in results:
        if "error" in r:
            continue
        doc_id = r.get("doc_id", "")
        if doc_id and doc_id not in seen:
            seen.add(doc_id)
            citations.append({"doc_id": doc_id, "title": r.get("title", "")})
    return citations


def build_context(results: list[dict]) -> str:
    parts = []
    for i, r in enumerate(results, 1):
        if "error" in r:
            parts.append(f"[检索提示] {r['error']}")
            continue
        parts.append(f"[文档{i}] {r.get('title', '')}（{r.get('doc_id', '')}）\n{r.get('chunk_text', '')}")
    return "\n\n".join(parts)
