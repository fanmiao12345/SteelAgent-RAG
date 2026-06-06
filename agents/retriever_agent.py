from rag.retriever import retrieve
from rag.citation import format_citations, build_context


def retrieve_knowledge(query: str, role: str = "visitor", top_k: int = 5) -> dict:
    results = retrieve(query, role=role, top_k=top_k)
    citations = format_citations(results)
    context = build_context(results)
    return {
        "results": results,
        "citations": citations,
        "context": context,
        "errors": [r["error"] for r in results if "error" in r],
    }
