from __future__ import annotations

from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_iocs: int
    critical_threats: int
    high_risk_threats: int
    active_alerts: int


class SeverityItem(BaseModel):
    name: str
    value: int


class IOCTypeItem(BaseModel):
    name: str
    value: int


class SourceItem(BaseModel):
    name: str
    value: int


class ActivityItem(BaseModel):
    date: str
    value: int
