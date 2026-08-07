"""Document loaders — turn a source (path or URL) into loaded text spans.

Loaders are the only format-specific surface in the RAG layer. Stdlib loaders
(text, Markdown, CSV, JSON, directory) are always available; the remaining
loaders need an optional packaging extra (``rag-pdf``, ``rag-docx``,
``rag-web``, ``rag-github``, ``rag-youtube``) and verify it at construction.

:func:`resolve_loader` routes a source to a default-constructed loader by URL
shape or file extension; the ``*SearchTool`` family pins explicit, configured
loaders instead.
"""

from philharmonica.adk.rag.loaders.base import DocumentLoader
from philharmonica.adk.rag.loaders.directory import DirectoryLoader
from philharmonica.adk.rag.loaders.docx import DOCXLoader
from philharmonica.adk.rag.loaders.github import GithubLoader
from philharmonica.adk.rag.loaders.pdf import PDFLoader
from philharmonica.adk.rag.loaders.plaintext import MarkdownLoader, TextLoader
from philharmonica.adk.rag.loaders.registry import FILE_EXTENSIONS, is_url, resolve_loader
from philharmonica.adk.rag.loaders.structured import CSVLoader, JSONLoader
from philharmonica.adk.rag.loaders.website import WebsiteLoader
from philharmonica.adk.rag.loaders.youtube import YoutubeChannelLoader, YoutubeVideoLoader

__all__ = [
    "FILE_EXTENSIONS",
    "CSVLoader",
    "DOCXLoader",
    "DirectoryLoader",
    "DocumentLoader",
    "GithubLoader",
    "JSONLoader",
    "MarkdownLoader",
    "PDFLoader",
    "TextLoader",
    "WebsiteLoader",
    "YoutubeChannelLoader",
    "YoutubeVideoLoader",
    "is_url",
    "resolve_loader",
]
