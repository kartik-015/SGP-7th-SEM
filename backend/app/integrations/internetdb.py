from __future__ import annotations

import ipaddress

import httpx

from app.schemas.threat import InternetDBResponse


class InternetDBError(RuntimeError):
    pass


async def lookup_ip(ip_address: str) -> InternetDBResponse:
    try:
        ipaddress.ip_address(ip_address)
    except ValueError as exc:
        raise ValueError("Please enter a valid IPv4 or IPv6 address.") from exc

    url = f"https://internetdb.shodan.io/{ip_address}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise InternetDBError("Threat intelligence service is currently unavailable. Please try again later.") from exc

    payload = response.json()
    return InternetDBResponse(
        ip=payload.get("ip", ip_address),
        hostnames=payload.get("hostnames", []) or [],
        ports=payload.get("ports", []) or [],
        cpes=payload.get("cpes", []) or [],
        vulnerabilities=payload.get("vulns", []) or payload.get("vulnerabilities", []) or [],
        tags=payload.get("tags", []) or [],
    )
