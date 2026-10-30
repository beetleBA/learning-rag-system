import re


def normalize_text(text: str) -> str:
    # - Унифицирует переносы строк
    # - Удаляет нулевые символы
    # - Объединяет пустые строки в одно разделение между блоками
    # - Убирает лишние пробелы в начале и конце текста

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
