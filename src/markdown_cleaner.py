import re

from langchain_core.documents import Document


class MarkdownCleaner:
    """MarkdownCleaner class for cleaning markdown text."""

    @staticmethod
    def clean_document_content(content: str) -> str:
        """Clean markdown document content."""

        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r" +\n", "\n", content)
        content = re.sub(r"^\s*[\*\-\+]\s+", "- ", content, flags=re.MULTILINE)
        content = re.sub(r"!\[.*?\]\((?!http).*?\)", "[IMAGE]", content)
        content = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)
        content = re.sub(r"```\s*```", "", content)
        content = re.sub(r"^(#{1,6})\s+", r"\1 ", content, flags=re.MULTILINE)
        content = re.sub(r" {2,}", " ", content)
        content = content.replace("\\n", "\n").replace("\\t", " ")

        return content.strip()

    @staticmethod
    def remove_metadata_noise(content: str) -> str:
        """Remove metadata noise from markdown document content."""

        content = re.sub(
            r"^(Категория|Статус|Category|Status|Tags?|Дата|Date|Author|Created|Updated):.*$",
            "",
            content,
            flags=re.MULTILINE | re.IGNORECASE,
        )

        content = re.sub(
            r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
            "",
            content,
            flags=re.IGNORECASE,
        )

        content = re.sub(r"%20", " ", content)

        return content

    @classmethod
    def clean_documents(cls, documents: list[Document]) -> list[Document]:
        """Clean markdown documents."""

        cleaned_docs = []

        for doc in documents:
            content = doc.page_content

            content = cls.clean_document_content(content)
            content = cls.remove_metadata_noise(content)

            if len(content.strip()) > 50:
                cleaned_docs.append(doc)

        return cleaned_docs
