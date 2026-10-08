from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(30), nullable=False, default="Analyst")
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action = Column(String(80), nullable=False, index=True)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(String(80), nullable=True)
    details = Column(JSON, default=dict, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    actor = relationship("User")


class TelemetryEvent(Base):
    __tablename__ = "telemetry_events"

    id = Column(Integer, primary_key=True, index=True)
    command = Column(Text, nullable=False)
    device_name = Column(String(120), nullable=False, index=True)
    username = Column(String(120), nullable=False)
    shell = Column(String(80), nullable=False, default="unknown")
    platform = Column(String(80), nullable=False, default="unknown")
    source_address = Column(String(80), nullable=False, index=True)
    executed_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    exit_code = Column(Integer, nullable=False, default=0)
    success = Column(Boolean, nullable=False, default=True)
    event_type = Column(String(40), nullable=False, default="command")
    detection_name = Column(String(120), nullable=True)
    detection_reason = Column(Text, nullable=True)
    severity = Column(String(20), nullable=False, default="Low", index=True)
    risk_score = Column(Float, nullable=False, default=0.0)


class ThreatSource(Base):
    __tablename__ = "threat_sources"

    id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String(100), unique=True, nullable=False)
    reliability_weight = Column(Float, default=50.0, nullable=False)
    api_endpoint = Column(String(255), default="", nullable=False)


class IOC(Base):
    __tablename__ = "iocs"
    __table_args__ = (UniqueConstraint("ioc_type", "ioc_value", name="uq_ioc_type_value"),)

    id = Column(Integer, primary_key=True, index=True)
    ioc_type = Column(String(20), nullable=False, index=True)
    ioc_value = Column(String(512), nullable=False, index=True)
    source = Column(String(255), nullable=False, index=True)
    first_seen = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_seen = Column(DateTime, default=datetime.utcnow, nullable=False)
    confidence = Column(Float, default=50.0, nullable=False)
    risk_score = Column(Float, default=0.0, nullable=False)
    severity = Column(String(20), default="Medium", nullable=False, index=True)
    description = Column(Text, default="", nullable=False)
    raw_metadata = Column(JSON, default=dict, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    ioc_id = Column(Integer, ForeignKey("iocs.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(20), default="New", nullable=False, index=True)
    triggered_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    severity = Column(String(20), nullable=False, index=True)

    ioc = relationship("IOC")
