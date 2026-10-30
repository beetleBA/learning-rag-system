from pathlib import Path

from loaders.models import DocumentContent
from loaders.pdf_parser import extract_pdf_pages
from loaders.validation import validate_pdf


def process_pdf(file_path: Path | str) -> DocumentContent:
    document = validate_pdf(file_path)

    try:
        pages = extract_pdf_pages(document)

        return DocumentContent(
            source_path=Path(file_path),
            page_count=document.page_count,
            pages=pages,
        )

    finally:
        document.close()