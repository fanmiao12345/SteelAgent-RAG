def split_document(doc: dict, chunk_size: int = 500, overlap: int = 50) -> list[dict]:
    content = doc.get("content", "")
    if not content:
        return []

    chunks = []
    start = 0
    while start < len(content):
        end = start + chunk_size
        chunk_text = content[start:end]
        chunks.append({
            "doc_id": doc.get("doc_id", ""),
            "title": doc.get("title", ""),
            "category": doc.get("category", ""),
            "security_level": doc.get("security_level", "public"),
            "allowed_roles": doc.get("allowed_roles", []),
            "chunk_text": chunk_text,
        })
        start = end - overlap
    return chunks
