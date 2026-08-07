"""Dispatch a source (path or URL) to the loader that handles it.

Auto-dispatch powers the generic ``DocumentSearchTool`` and the directory
loader: given a heterogeneous corpus, each source is routed by URL shape
(YouTube / GitHub / website) or file extension (.pdf, .docx, .csv, .json,
.md, .txt) to a default-constructed loader. Named search tools bypass this by
pinning an explicit, pre-configured loader instead.

Loaders are constructed fresh per call; the stdlib loaders are stateless and
cheap, and the optional-dependency loaders (PDF/DOCX) only check for their
package at construction (no import), so resolving a source is side-effect-free
beyond that check.
"""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

from philharmonica.adk.exceptions.exceptions import UnsupportedDocumentSourceError
from philharmonica.adk.rag.loaders.base import DocumentLoader
from philharmonica.adk.rag.loaders.directory import DirectoryLoader
from philharmonica.adk.rag.loaders.docx import DOCXLoader
from philharmonica.adk.rag.loaders.github import GithubLoader
from philharmonica.adk.rag.loaders.pdf import PDFLoader
from philharmonica.adk.rag.loaders.plaintext import MarkdownLoader, TextLoader
from philharmonica.adk.rag.loaders.structured import CSVLoader, JSONLoader
from philharmonica.adk.rag.loaders.website import WebsiteLoader
from philharmonica.adk.rag.loaders.youtube import YoutubeChannelLoader, YoutubeVideoLoader

FILE_EXTENSIONS: dict[str, str] = {
    ".txt": "text",
    ".text": "text",
    ".md": "markdown",
    ".markdown": "markdown",
    ".mdx": "markdown",
    ".csv": "csv",
    ".json": "json",
    ".pdf": "pdf",
    ".docx": "docx",
}
"""File extension → loader key. The key abstracts over the concrete class so
``resolve_loader`` stays a typed dispatch rather than dynamic lookup."""


def is_url(source: str) -> bool:
    """Return whether ``source`` is an ``http``/``https`` URL.

    Args:
        source: The source string to classify.

    Returns:
        ``True`` if ``source`` parses as an http(s) URL, else ``False``.
    """
    parsed = urlparse(source)
    return parsed.scheme in ("http", "https") and len(parsed.netloc) > 0


YOUTUBE_DOMAINS: frozenset[str] = frozenset({"youtube.com", "youtu.be"})
"""Domains whose URLs route to the YouTube loaders, with their subdomains."""

GITHUB_DOMAINS: frozenset[str] = frozenset({"github.com"})
"""Domains whose URLs route to the GitHub loader, with their subdomains."""

_CHANNEL_PATH_MARKERS = ("/channel/", "/@", "/c/", "/user/")


def _host_in(host: str, domains: frozenset[str]) -> bool:
    """Return whether ``host`` is one of ``domains`` or a subdomain of one.

    Substring containment would be wrong here in both directions:
    ``evil-youtube.com.attacker.net`` contains the marker without being
    served by it, and a bare ``netloc`` also carries userinfo, so
    ``youtube.com@evil.com`` would match while the origin is ``evil.com``.

    Args:
        host: A parsed hostname — no userinfo, no port, already lowercased.
        domains: Registrable domains to accept, along with their subdomains.

    Returns:
        ``True`` when ``host`` equals or sits under one of ``domains``.
    """
    return any(host == domain or host.endswith(f".{domain}") for domain in domains)


def _resolve_url_loader(source: str) -> DocumentLoader:
    """Route an http(s) URL to the YouTube, GitHub, or website loader."""
    parsed = urlparse(source)
    # `hostname` rather than `netloc`: it drops userinfo and port and
    # lowercases, so what is compared is the origin that will be fetched.
    host = parsed.hostname or ""
    if _host_in(host, YOUTUBE_DOMAINS):
        # Only the path distinguishes a channel from a video; a query string
        # can carry a `/@` that says nothing about what the URL addresses.
        path = parsed.path.lower()
        if any(marker in path for marker in _CHANNEL_PATH_MARKERS):
            return YoutubeChannelLoader()
        return YoutubeVideoLoader()
    if _host_in(host, GITHUB_DOMAINS):
        return GithubLoader()
    return WebsiteLoader()


def _resolve_file_loader(source: str, suffix: str) -> DocumentLoader:
    """Construct the loader for a recognised file ``suffix``."""
    key = FILE_EXTENSIONS.get(suffix)
    if key == "text":
        return TextLoader()
    if key == "markdown":
        return MarkdownLoader()
    if key == "csv":
        return CSVLoader()
    if key == "json":
        return JSONLoader()
    if key == "pdf":
        return PDFLoader()
    if key == "docx":
        return DOCXLoader()
    raise UnsupportedDocumentSourceError(
        source,
        f"No loader for '{suffix or source}'. Supported file types: "
        f"{', '.join(sorted(FILE_EXTENSIONS))}; or an http(s) URL.",
    )


def resolve_loader(source: str) -> DocumentLoader:
    """Return a default-constructed loader for ``source``.

    Args:
        source: A file path, directory path, or http(s) URL.

    Returns:
        The ``DocumentLoader`` that handles ``source``.

    Raises:
        UnsupportedDocumentSourceError: If no loader matches ``source``.
        ImportError: If the matched loader needs an optional package that
            is not installed.
    """
    if is_url(source):
        return _resolve_url_loader(source)
    path = Path(source)
    if path.is_dir():
        return DirectoryLoader()
    return _resolve_file_loader(source, path.suffix.lower())
