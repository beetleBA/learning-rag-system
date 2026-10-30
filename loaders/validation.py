from pathlib import Path
import pymupdf
from loaders.exceptions import PDFValidationError


def validate_pdf(file_path: Path | str) -> pymupdf.Document:
    path = Path(file_path)

    if not path.exists():
        raise PDFValidationError(f"Файл не найден: {path}")

    if not path.is_file():
        raise PDFValidationError(f"Указанный путь не является файлом: {path}")

    if path.suffix.lower() != ".pdf":
        raise PDFValidationError("Поддерживаются только PDF-файлы.")

    try:
        document = pymupdf.open(path)
    except Exception as error:
        raise PDFValidationError(
            f"Не удалось открыть PDF: {error}"
        ) from error

    if document.needs_pass:
        document.close()
        raise PDFValidationError("PDF защищён паролем.")

    if document.page_count == 0:
        document.close()
        raise PDFValidationError("PDF не содержит страниц.")

    return document