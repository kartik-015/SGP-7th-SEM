from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class IOCBase(BaseModel):
    ioc_type: str
    ioc_value: str
    source: str
    first_seen: datetime | None = None
    last_seen: datetime | None = None
    confidence: float = Field(ge=0, le=100)
    risk_score: float = Field(ge=0, le=100)
    severity: str
    description: str = ""
    raw_metadata: dict[str, Any] = Field(default_factory=dict)


class IOCRead(IOCBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ThreatSourceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_name: str
    reliability_weight: float
    api_endpoint: str


class IOCSearchRequest(BaseModel):
    ioc: str


class InternetDBResponse(BaseModel):
    ip: str
    hostnames: list[str] = []
    ports: list[int] = []
    cpes: list[str] = []
    vulnerabilities: list[str] = []
    tags: list[str] = []
