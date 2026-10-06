from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AlertRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ioc_id: int
    severity: str
    status: str
    triggered_at: datetime
    ioc_value: str | None = None
    ioc_type: str | None = None
    risk_score: float | None = None


class AlertReviewResponse(BaseModel):
    message: str


class AlertStatusUpdate(BaseModel):
    status: str = Field(pattern="^(New|In Progress|Reviewed|Resolved|False Positive)$")


class AuditLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    actor_id: int | None
    action: str
    entity_type: str
    entity_id: str | None
    details: dict
    created_at: datetime
