from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy.orm import Session

from app.database.models import IOC, ThreatSource
from app.services.risk_service import calculate_risk_score, determine_severity
from app.utils.validators import identify_ioc_type


def normalize_ioc(raw_item: dict[str, Any], source_name: str, source_reliability: float) -> dict[str, Any]:
    ioc_value = raw_item["ioc_value"].strip()
    ioc_type = raw_item.get("ioc_type") or identify_ioc_type(ioc_value)
    confidence = float(raw_item.get("confidence", 50.0))
    corroborating_sources = len(raw_item.get("sources", [source_name]))
    vulnerability_count = len(raw_item.get("vulnerabilities", []))
    risk_score = calculate_risk_score(confidence, source_reliability, corroborating_sources, vulnerability_count)

    return {
        "ioc_type": ioc_type,
        "ioc_value": ioc_value,
        "source": source_name,
        "first_seen": raw_item.get("first_seen") or datetime.now(timezone.utc),
        "last_seen": raw_item.get("last_seen") or datetime.now(timezone.utc),
        "confidence": confidence,
        "risk_score": risk_score,
        "severity": determine_severity(risk_score),
        "description": raw_item.get("description", ""),
        "raw_metadata": raw_item,
    }


def find_duplicate_ioc(db: Session, ioc_type: str, ioc_value: str) -> IOC | None:
    return db.query(IOC).filter(IOC.ioc_type == ioc_type, IOC.ioc_value == ioc_value).one_or_none()


def merge_duplicate_iocs(existing: IOC, new_payload: dict[str, Any]) -> IOC:
    existing.last_seen = max(existing.last_seen, new_payload["last_seen"])
    existing.first_seen = min(existing.first_seen, new_payload["first_seen"])
    existing.confidence = round((existing.confidence + new_payload["confidence"]) / 2, 2)
    existing.risk_score = max(existing.risk_score, new_payload["risk_score"])
    existing.severity = determine_severity(existing.risk_score)

    existing_sources = set(existing.raw_metadata.get("sources", [existing.source]))
    incoming_sources = set(new_payload.get("raw_metadata", {}).get("sources", [new_payload["source"]]))
    merged_sources = sorted(existing_sources.union(incoming_sources))

    merged_metadata = dict(existing.raw_metadata)
    merged_metadata.update(new_payload["raw_metadata"])
    merged_metadata["sources"] = merged_sources
    existing.raw_metadata = merged_metadata
    existing.source = merged_sources[0]
    existing.description = new_payload.get("description") or existing.description
    return existing


def save_ioc(db: Session, payload: dict[str, Any]) -> IOC:
    existing = find_duplicate_ioc(db, payload["ioc_type"], payload["ioc_value"])
    if existing:
        merged = merge_duplicate_iocs(existing, payload)
        db.add(merged)
        db.commit()
        db.refresh(merged)
        return merged

    ioc = IOC(**payload)
    db.add(ioc)
    db.commit()
    db.refresh(ioc)
    return ioc


def get_source_reliability(db: Session, source_name: str) -> float:
    source = db.query(ThreatSource).filter(ThreatSource.source_name == source_name).one_or_none()
    return source.reliability_weight if source else 50.0
