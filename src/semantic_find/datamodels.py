from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Paragraph:
    paragraph_number: int
    content: str


@dataclass
class Document:
    file_name: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    byte_count: Optional[int] = None
    page_count: Optional[int] = None
    type: Optional[str] = None
    paragraphs: Optional[list[Paragraph]] = None

    def get_paragraphs(self):
        return [p.content for p in self.paragraphs]

    def __dict__(self):
        return asdict(
            self, dict_factory=lambda x: {k: v for (k, v) in x if k != "paragraphs"}
        )
