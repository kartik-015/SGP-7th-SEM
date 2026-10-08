from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.core.config import settings
from app.database.database import get_db
from app.database.models import TelemetryEvent, User
from app.schemas.telemetry import TelemetryEventCreate, TelemetryEventRead, TelemetryIngestResponse
from app.services.telemetry_service import ingest_event


router = APIRouter(prefix="/api/telemetry", tags=["Telemetry"])


def verify_agent_key(x_agent_key: str | None = Header(default=None)) -> None:
    if not x_agent_key or x_agent_key != settings.telemetry_agent_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid telemetry agent key")


@router.post("/events", response_model=TelemetryIngestResponse, status_code=status.HTTP_201_CREATED)
def ingest_telemetry(
    payload: TelemetryEventCreate,
    db: Session = Depends(get_db),
    _: None = Depends(verify_agent_key),
):
    event, threat_detected = ingest_event(db, payload)
    return TelemetryIngestResponse(
        event=event,
        threat_detected=threat_detected,
        message="Telemetry event recorded and analyzed.",
    )


@router.get("/events", response_model=list[TelemetryEventRead])
def list_telemetry(
    device_name: str | None = Query(default=None),
    severity: str | None = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = db.query(TelemetryEvent).order_by(TelemetryEvent.executed_at.desc())
    if device_name:
        query = query.filter(TelemetryEvent.device_name == device_name)
    if severity:
        query = query.filter(TelemetryEvent.severity == severity)
    return query.limit(200).all()