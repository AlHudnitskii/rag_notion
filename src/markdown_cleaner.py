import re
from typing import List
from langchain_core.documents import Document


class MarkdownCleaner:
    """Utility for cleaning markdown documents before indexing."""

    @staticmethod
    def clean_text(text: str) -> str:
        text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
        text = re.sub(r"\*{1,2}(.+?)\*{1,2}", r"\1", text)
        text = re.sub(r"_{1,2}(.+?)_{1,2}", r"\1", text)
        text = re.sub(r"`(.+?)`", r"\1", text)
        text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
        text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
        text = re.sub(r"^[-*_]{3,}\s*$", "", text, flags=re.MULTILINE)
        text = re.sub(r"^>\s+", "", text, flags=re.MULTILINE)
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    @classmethod
    def clean_documents(cls, documents: List[Document]) -> List[Document]:
        cleaned = []
        for doc in documents:
            cleaned_text = cls.clean_text(doc.page_content)
            if not cleaned_text:
                continue
            cleaned.append(
                Document(
                    page_content=cleaned_text,
                    metadata=doc.metadata,
                )
            )
        return cleaned
