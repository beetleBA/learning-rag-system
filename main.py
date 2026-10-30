
from embeddings.encoder import TextEmbedder
from storage.qdrant import QdrantStorage

from generation.gigachat_client import GigaChatGenerator
from generation.service import RAGService

import json


embedder = TextEmbedder()
storage = QdrantStorage()
generator = GigaChatGenerator()

try:
    rag = RAGService(
        embedder=embedder,
        storage=storage,
        generator=generator,
    )

    question = "С какого символа начинается переменная в PHP?"

    response = rag.answer(
        question=question,
        top_k=3,
    )

    print("\n=== RAG RESPONSE ===")

    print(
        json.dumps(
            response,
            ensure_ascii=False,
            indent=4,
        )
    )

finally:
    storage.close()
