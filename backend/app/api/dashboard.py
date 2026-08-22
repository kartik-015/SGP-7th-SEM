from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.database.database import get_db
from app.database.models import User
from app.schemas.dashboard import ActivityItem, DashboardStats, IOCTypeItem, SeverityItem, SourceItem
from app.services.dashboard_service import get_activity_trend, get_dashboard_stats, get_ioc_type_distribution, get_severity_distribution, get_source_distribution


router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStats)
def stats(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return DashboardStats(**get_dashboard_stats(db))


@router.get("/severity-distribution", response_model=list[SeverityItem])
def severity_distribution(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return [SeverityItem(**item) for item in get_severity_distribution(db)]


@router.get("/ioc-types", response_model=list[IOCTypeItem])
def ioc_types(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return [IOCTypeItem(**item) for item in get_ioc_type_distribution(db)]


@router.get("/activity", response_model=list[ActivityItem])
def activity(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return [ActivityItem(**item) for item in get_activity_trend(db)]


@router.get("/sources", response_model=list[SourceItem])
def sources(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return [SourceItem(**item) for item in get_source_distribution(db)]
