from __future__ import annotations

from collections import defaultdict
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.models import Alert, IOC


def get_dashboard_stats(db: Session) -> dict[str, int]:
    total_iocs = db.query(func.count(IOC.id)).scalar() or 0
    critical_threats = db.query(func.count(IOC.id)).filter(IOC.severity == "Critical").scalar() or 0
    high_risk_threats = db.query(func.count(IOC.id)).filter(IOC.severity == "High").scalar() or 0
    active_alerts = db.query(func.count(Alert.id)).filter(Alert.status != "Resolved").scalar() or 0
    return {
        "total_iocs": total_iocs,
        "critical_threats": critical_threats,
        "high_risk_threats": high_risk_threats,
        "active_alerts": active_alerts,
    }


def get_severity_distribution(db: Session) -> list[dict[str, int | str]]:
    severities = ["Low", "Medium", "High", "Critical"]
    counts = {severity: db.query(func.count(IOC.id)).filter(IOC.severity == severity).scalar() or 0 for severity in severities}
    return [{"name": name, "value": counts[name]} for name in severities]


def get_ioc_type_distribution(db: Session) -> list[dict[str, int | str]]:
    types = ["IP", "Domain", "URL", "Hash"]
    counts = {ioc_type: db.query(func.count(IOC.id)).filter(IOC.ioc_type == ioc_type).scalar() or 0 for ioc_type in types}
    return [{"name": name, "value": counts[name]} for name in types]


def get_activity_trend(db: Session) -> list[dict[str, int | str]]:
    rows = db.query(IOC.first_seen).all()
    bucket: dict[str, int] = defaultdict(int)
    for (timestamp,) in rows:
        if isinstance(timestamp, datetime):
            bucket[timestamp.date().isoformat()] += 1
    ordered_dates = sorted(bucket.keys())[-14:]
    return [{"date": item, "value": bucket[item]} for item in ordered_dates]


def get_source_distribution(db: Session) -> list[dict[str, int | str]]:
    counts = defaultdict(int)
    for ioc in db.query(IOC).all():
        metadata_sources = ioc.raw_metadata.get("sources") if isinstance(ioc.raw_metadata, dict) else None
        source_names = metadata_sources or [ioc.source]
        for source_name in source_names:
            counts[source_name] += 1
    preferred_order = ["VirusTotal", "AbuseIPDB", "AlienVault OTX", "InternetDB"]
    ordered = [{"name": name, "value": counts.get(name, 0)} for name in preferred_order]
    for name, value in counts.items():
        if name not in preferred_order:
            ordered.append({"name": name, "value": value})
    return ordered
