from __future__ import annotations

import re
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.database.models import Alert, IOC, TelemetryEvent
from app.schemas.telemetry import TelemetryEventCreate
from app.services.risk_service import calculate_risk_score, determine_severity


DETECTION_RULES = (
    ("network.scan", re.compile(r"\b(nmap|masscan|zmap|netcat|nc)\b", re.IGNORECASE), "Network scanning or probing command"),
    ("credential.attack", re.compile(r"\b(hydra|john|hashcat|medusa)\b", re.IGNORECASE), "Credential attack tool detected"),
    ("privilege.escalation", re.compile(r"\b(sudo\s+su|sudo\s+-i|chmod\s+[0-7]*7|setuid)\b", re.IGNORECASE), "Privilege escalation pattern detected"),
    ("dangerous.file.operation", re.compile(r"\b(rm\s+-rf|mkfs|dd\s+if=|shred)\b", re.IGNORECASE), "Destructive file or disk operation detected"),
    ("account.change", re.compile(r"\b(useradd|usermod|passwd|chage)\b", re.IGNORECASE), "Account administration command detected"),
)


def detect_command(command: str, exit_code: int) -> tuple[str | None, str | None, float, str]:
    for name, pattern, reason in DETECTION_RULES:
        if pattern.search(command):
            score = calculate_risk_score(90.0, 75.0, 2 if exit_code == 0 else 1)
            return name, reason, score, determine_severity(score)
    if exit_code != 0:
        return "command.failure", "Command returned a non-zero exit status", 35.0, "Medium"
    return None, None, 5.0, "Low"


def ingest_event(db: Session, payload: TelemetryEventCreate) -> tuple[TelemetryEvent, bool]:
    detection_name, reason, risk_score, severity = detect_command(payload.command, payload.exit_code)
    executed_at = payload.executed_at or datetime.now(timezone.utc)
    event = TelemetryEvent(
        **payload.model_dump(exclude={"executed_at"}),
        executed_at=executed_at,
        success=payload.exit_code == 0,
        detection_name=detection_name,
        detection_reason=reason,
        severity=severity,
        risk_score=risk_score,
    )
    db.add(event)
    db.flush()

    if detection_name:
        ioc = IOC(
            ioc_type="Command",
            ioc_value=payload.command,
            source=f"Telemetry:{payload.device_name}",
            first_seen=executed_at,
            last_seen=executed_at,
            confidence=90.0,
            risk_score=risk_score,
            severity=severity,
            description=reason or "Telemetry command matched a detection rule.",
            raw_metadata={"device_name": payload.device_name, "source_address": payload.source_address, "event_id": event.id},
        )
        db.add(ioc)
        db.flush()
        db.add(Alert(ioc_id=ioc.id, status="New", triggered_at=executed_at, severity=severity))

    db.commit()
    db.refresh(event)
    return event, bool(detection_name)