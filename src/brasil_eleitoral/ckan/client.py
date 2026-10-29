"""Small, resilient client for the CKAN Action API (stdlib only)."""
from __future__ import annotations
import json
import logging
import random
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

LOG = logging.getLogger(__name__)

class CKANError(RuntimeError):
    """Raised for transport errors or unsuccessful CKAN Action API responses."""

class CKANClient:
    def __init__(self, base_url: str, *, timeout: float = 30.0, retries: int = 4,
                 backoff: float = 0.8, user_agent: str = "BrasilEleitoralDataLab/0.1 (+https://github.com/nrdataanalysis-1908/brasil-eleitoral-datalab)") -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout, self.retries, self.backoff, self.user_agent = timeout, retries, backoff, user_agent

    def action(self, name: str, **params: Any) -> Any:
        url = f"{self.base_url}/api/3/action/{name}?{urlencode(params, doseq=True)}"
        request = Request(url, headers={"Accept": "application/json", "User-Agent": self.user_agent})
        last_error: Exception | None = None
        for attempt in range(self.retries + 1):
            try:
                with urlopen(request, timeout=self.timeout) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                if not isinstance(payload, dict) or payload.get("success") is not True:
                    detail = payload.get("error", payload) if isinstance(payload, dict) else payload
                    raise CKANError(f"CKAN action {name!r} returned success=false: {detail}")
                return payload.get("result")
            except HTTPError as exc:
                last_error = exc
                if exc.code not in {408, 425, 429, 500, 502, 503, 504} or attempt >= self.retries:
                    break
            except (URLError, TimeoutError, json.JSONDecodeError, UnicodeDecodeError) as exc:
                last_error = exc
                if attempt >= self.retries:
                    break
            delay = self.backoff * (2 ** attempt) + random.uniform(0, self.backoff / 4)
            LOG.warning("CKAN request failed (%s); retry %d/%d in %.2fs", last_error, attempt + 1, self.retries, delay)
            time.sleep(delay)
        raise CKANError(f"CKAN action {name!r} failed after {self.retries + 1} attempts: {last_error}") from last_error

    def search_page(self, *, start: int, rows: int) -> dict[str, Any]:
        result = self.action("package_search", q="*:*", start=start, rows=rows, include_private=False)
        if not isinstance(result, dict) or not isinstance(result.get("results"), list):
            raise CKANError("Unexpected package_search response shape")
        return result
