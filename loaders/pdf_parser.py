import pymupdf
from loaders.models import PageContent
from loaders.normalization import normalize_text


def extract_page_text(page_data: dict) -> str:
    text = page_data["text"]

    return normalize_text(text)


def extract_pdf_pages(document: pymupdf.Document) -> list[PageContent]:
    extracted_pages = document.to_markdown(page_chunks=True)

    pages = []

    for page_data in extracted_pages:
        pages.append(
            PageContent(
                page_number=page_data["metadata"]["page_number"],
                text=extract_page_text(page_data),
            )
        )

    return pages
