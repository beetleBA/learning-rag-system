class RAGLibraryError(Exception):
    """Базовая ошибка библиотеки."""


class PDFValidationError(RAGLibraryError):
    """Ошибка проверки PDF-файла."""
