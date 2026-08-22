from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.database.database import get_db
from app.database.models import IOC, User
from app.schemas.threat import IOCRead


router = APIRouter(prefix="/api/threats", tags=["Threats"])


@router.get("", response_model=list[IOCRead])
def list_threats(
    severity: str | None = Query(default=None),
    ioc_type: str | None = Query(default=None),
    source: str | None = Query(default=None),
    search: str | None = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = db.query(IOC).order_by(IOC.last_seen.desc())
    if severity:
        query = query.filter(IOC.severity == severity)
    if ioc_type:
        query = query.filter(IOC.ioc_type == ioc_type)
    if source:
        query = query.filter(IOC.source.contains(source))
    if search:
        query = query.filter(IOC.ioc_value.contains(search))
    return query.all()


@router.get("/{ioc_id}", response_model=IOCRead)
def get_threat(ioc_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    ioc = db.query(IOC).filter(IOC.id == ioc_id).one_or_none()
    if not ioc:
        raise HTTPException(status_code=404, detail="IOC not found")
    return ioc
