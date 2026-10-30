import pymupdf
import re
from loaders.models import PageContent


def _normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")
    text = text.replace("\x00", "")

    lines = [
        line.rstrip()
        for line in text.split("\n")
    ]

    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def _extract_page_text(page_data: dict) -> str:
    text = page_data["text"]
    return _normalize_text(text)


def extract_pdf_pages(document: pymupdf.Document) -> list[PageContent]:
    extracted_pages = document.to_markdown(page_chunks=True)

    pages = []

    for page_data in extracted_pages:
        pages.append(
            PageContent(
                page_number=page_data["metadata"]["page_number"],
                text=_extract_page_text(page_data),
            )
        )

    return pages
