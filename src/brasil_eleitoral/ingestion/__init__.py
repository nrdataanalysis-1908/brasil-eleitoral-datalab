"""Ingestion primitives for public electoral datasets."""
from .downloader import DownloadError, download_resource, download_resources
from .extractor import ExtractionError, extract_zip

__all__ = [
    "DownloadError", "download_resource", "download_resources",
    "ExtractionError", "extract_zip",
]
