from langchain_text_splitters import RecursiveCharacterTextSplitter
from loaders.models import DocumentContent, ChunkContent


def chunk_document(
        document: DocumentContent,
        chunk_size: int = 1500,
        chunk_overlap: int = 200,
) -> list[ChunkContent]:
    if chunk_size <= 0:
        raise ValueError("Размер чанка должен быть больше нуля.")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError(
            "Перекрытие должно быть неотрицательным "
            "и меньше размера чанка."
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )

    chunks = []

    for page in document.pages:
        if not page.text.strip():
            continue

        page_chunks = splitter.split_text(page.text)

        for chunk_text in page_chunks:
            chunks.append(
                ChunkContent(
                    text=chunk_text,
                    source_path=document.source_path,
                    page_number=page.page_number,
                    chunk_index=len(chunks),
                )
            )

    return chunks
