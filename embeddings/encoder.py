from sentence_transformers import SentenceTransformer
from loaders.models import ChunkContent


class TextEmbedder:
    def __init__(
            self,
            model_name: str = "intfloat/multilingual-e5-small",
    ):
        self.model = SentenceTransformer(model_name)

    def embed_chunks(
            self,
            chunks: list[ChunkContent],
    ) -> list[list[float]]:
        if not chunks:
            return []

        texts = [
            f"passage: {chunk.text}"
            for chunk in chunks
        ]

        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True,
            convert_to_numpy=True,
        )

        return vectors.tolist()

    def embed_query(self, query: str) -> list[float]:
        vector = self.model.encode(
            f"query: {query}",
            normalize_embeddings=True,
            convert_to_numpy=True,
        )

        return vector.tolist()
