from dataclasses import dataclass
from pathlib import Path


@dataclass
class PageContent:
    page_number: int
    text: str


@dataclass
class DocumentContent:
    source_path: Path
    page_count: str
    pages: list[PageContent]


@dataclass
class ChunkContent:
    text: str
    source_path: Path
    page_number: int
    chunk_index: int
