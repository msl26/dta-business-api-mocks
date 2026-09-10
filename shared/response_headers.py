"""Shared HTTP response header helpers for mock APIs."""

from datetime import datetime, timezone
import time
import uuid


def build_json_response_headers(include_security_headers=False):
    headers = {
        "Date": datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "Content-Type": "application/json",
        "Cache-Control": "no-store",
        "X-Request-Id": uuid.uuid4().hex,
        "X-Runtime": f"{time.time() % 10:.8f}",
    }
    if include_security_headers:
        headers.update({
            "Content-Security-Policy": "default-src 'self'",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        })
    return headers
