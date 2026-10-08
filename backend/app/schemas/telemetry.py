from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TelemetryEventCreate(BaseModel):
    command: str = Field(min_length=1, max_length=4000)
    device_name: str = Field(min_length=1, max_length=120)
    username: str = Field(min_length=1, max_length=120)
    shell: str = Field(default="unknown", max_length=80)
    platform: str = Field(default="unknown", max_length=80)
    source_address: str = Field(min_length=1, max_length=80)
    executed_at: datetime | None = None
    exit_code: int = Field(default=0, ge=-255, le=255)
    event_type: str = Field(default="command", min_length=1, max_length=40)


class TelemetryEventRead(TelemetryEventCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    executed_at: datetime
    success: bool
    detection_name: str | None = None
    detection_reason: str | None = None
    severity: str
    risk_score: float


class TelemetryIngestResponse(BaseModel):
    event: TelemetryEventRead
    threat_detected: bool
    message: str