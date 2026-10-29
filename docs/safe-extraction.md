# Safe ZIP extraction

Archives from public catalogs are treated as untrusted input. The extractor rejects path traversal, absolute/drive-qualified paths, backslash paths, duplicate paths, symlinks and special files, encrypted entries, excessive entry/file/total sizes, and suspicious compression ratios. It validates the ZIP CRC before extraction and writes into a temporary staging directory; only a fully extracted archive is atomically renamed into the requested destination.

```python
from pathlib import Path
from brasil_eleitoral.ingestion.extractor import extract_zip

result = extract_zip(
    Path("data/landing/tse/results.zip"),
    Path("data/bronze/extracted/results"),
)
print(result)
```

The destination must not already exist. Configure limits explicitly for datasets whose documented size exceeds the conservative defaults. Extraction does not execute files or follow archive-created links.
