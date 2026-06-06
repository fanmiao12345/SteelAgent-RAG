import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.document_loader import load_documents
from rag.splitter import split_document
from rag.vector_store import vector_store


def main():
    print("正在加载文档...")
    docs = load_documents("data/docs")
    print(f"加载了 {len(docs)} 个文档")

    print("正在切分文档...")
    all_chunks = []
    for doc in docs:
        chunks = split_document(doc)
        all_chunks.extend(chunks)
    print(f"生成了 {len(all_chunks)} 个文本块")

    print("正在构建向量索引...")
    try:
        vector_store.build_index(all_chunks)
        print("向量索引构建完成！")
    except Exception as e:
        print(f"构建向量索引失败: {e}")
        print("请检查 EMBEDDING_API_URL 是否可访问。")


if __name__ == "__main__":
    main()
