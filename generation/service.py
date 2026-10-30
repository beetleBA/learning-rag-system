from embeddings.encoder import TextEmbedder
import re
from storage.qdrant import QdrantStorage
from generation.gigachat_client import GigaChatGenerator


def normalize_source_id(value: str) -> str | None:
    if not isinstance(value, str):
        return None

    # Удаляем внешнее оформление
    value = value.strip().strip("`'\"[]$").strip()

    # Извлекаем номер источника
    match = re.fullmatch(
        r"CTX-?(\d+)",
        value,
        re.IGNORECASE,
    )

    if not match:
        return None

    return f"CTX-{match.group(1)}"


class RAGService:

    def __init__(
            self,
            embedder: TextEmbedder,
            storage: QdrantStorage,
            generator: GigaChatGenerator,
    ):
        self.embedder = embedder
        self.storage = storage
        self.generator = generator

    def answer(
            self,
            question: str,
            top_k: int = 3,
    ) -> dict:

        if not question.strip():
            raise ValueError("Вопрос не может быть пустым.")

        # Преобразуем вопрос в вектор
        query_vector = self.embedder.embed_query(question)

        # Ищем подходящие чанки в Qdrant
        results = self.storage.search(
            query_vector=query_vector,
            limit=top_k,
        )
        if not results:
            return {
                "answer_markdown": (
                    "В загруженных документах не найдена информация для ответа на вопрос."
                ),
                "sources": [],
                "insufficient_information": True,
            }

        # Назначаем временные ID найденным источникам
        contexts = []

        for index, result in enumerate(results, start=1):
            contexts.append({
                "source_id": f"CTX-{index}",
                "text": result["text"],
            })

        # Генерируем ответ
        draft = self.generator.generate(
            question=question,
            contexts=contexts,
        )

        # Формируем карту реальных источников
        source_map = {
            context["source_id"]: result
            for context, result in zip(contexts, results)
        }

        # Проверяем и нормализуем ID источников
        used_ids = list(dict.fromkeys(
            re.findall(
                r"\[(CTX-\d+)\]",
                draft.answer_markdown
            )
        ))

        for source_id in draft.used_source_ids:
            normalized_id = normalize_source_id(source_id)

            if (normalized_id in source_map and normalized_id not in used_ids):
                used_ids.append(normalized_id)

        sources = []

        for source_id in used_ids:
            result = source_map[source_id]

            sources.append({
                "source_id": source_id,
                "source_path": result["source_path"],
                "page_number": result["page_number"],
                "chunk_index": result["chunk_index"],
                "quote": result["text"],
                "score": result["score"],
            })

        return {
            "answer_markdown": draft.answer_markdown,
            "sources": sources,
            "insufficient_information": (
                draft.insufficient_information
            ),
        }
