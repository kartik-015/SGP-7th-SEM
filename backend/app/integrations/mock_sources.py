from __future__ import annotations


def build_mock_source_payload(source_name: str, ioc_value: str) -> dict:
    return {
        "source_name": source_name,
        "ioc_value": ioc_value,
        "confidence": 72.0,
        "description": f"Demo intelligence record sourced from {source_name}.",
        "sources": [source_name],
        "tags": ["demo", "sample"],
    }
