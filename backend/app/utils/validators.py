from __future__ import annotations

import ipaddress
import re
from urllib.parse import urlparse


HASH_PATTERN = re.compile(r"^[A-Fa-f0-9]{32}$|^[A-Fa-f0-9]{40}$|^[A-Fa-f0-9]{64}$")


def is_valid_ip(value: str) -> bool:
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False


def identify_ioc_type(value: str) -> str:
    candidate = value.strip()
    if is_valid_ip(candidate):
        return "IP"
    if candidate.startswith(("http://", "https://")):
        return "URL"
    if HASH_PATTERN.match(candidate):
        return "Hash"
    return "Domain"


def is_valid_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
