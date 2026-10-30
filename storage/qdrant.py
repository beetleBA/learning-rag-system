from uuid import uuid5, NAMESPACE_URL

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)
from qdrant_client.models import SearchParams
from loaders.models import ChunkContent


class QdrantStorage:
    def __init__(
            self,
            url: str = "http://localhost:6333",
            collection_name: str = "rag_documents",
            vector_size: int = 384,
    ):
        self.client = QdrantClient(url=url)
        self.collection_name = collection_name
        self.vector_size = vector_size

    def create_collection(self) -> None:
        """Создаёт коллекцию, если она ещё не существует."""

        if self.client.collection_exists(self.collection_name):
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE,
            ),
        )

    def save_chunks(
            self,
            chunks: list[ChunkContent],
            vectors: list[list[float]],
    ) -> None:
        """Сохраняет чанки и их векторы в Qdrant."""

        if len(chunks) != len(vectors):
            raise ValueError(
                "Количество чанков и векторов должно совпадать."
            )

        if not chunks:
            return

        points = []

        for chunk, vector in zip(chunks, vectors):
            if len(vector) != self.vector_size:
                raise ValueError(
                    f"Ожидался вектор размерности {self.vector_size}, "
                    f"получен {len(vector)}."
                )

            # Стабильный ID: повторная загрузка того же чанка
            # по тому же пути обновит существующую точку.
            point_id = str(
                uuid5(
                    NAMESPACE_URL,
                    f"{chunk.source_path}:{chunk.page_number}:{chunk.chunk_index}",
                )
            )

            points.append(
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload={
                        "text": chunk.text,
                        "source_path": str(chunk.source_path),
                        "page_number": chunk.page_number,
                        "chunk_index": chunk.chunk_index,
                    },
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
            wait=True,
        )

    def count_points(self) -> int:
        """Возвращает количество точек в коллекции."""

        result = self.client.count(
            collection_name=self.collection_name,
            exact=True,
        )

        return result.count

    def close(self) -> None:
        self.client.close()


    def search(
        self,
        query_vector: list[float],
        limit: int = 5,
    ) -> list[dict]:

        if len(query_vector) != self.vector_size:
            raise ValueError(
                f"Ожидался вектор размерности {self.vector_size}."
            )

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            with_payload=True,
            search_params=SearchParams(
                exact=False,
            ),
        ).points

        return [
            {
                "text": point.payload["text"],
                "source_path": point.payload["source_path"],
                "page_number": point.payload["page_number"],
                "chunk_index": point.payload["chunk_index"],
                "score": point.score,
            }
            for point in results
        ]

