from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.database.database import get_db
from app.database.models import IOC, User
from app.integrations.internetdb import InternetDBError, lookup_ip
from app.schemas.threat import IOCSearchRequest
from app.utils.validators import identify_ioc_type, is_valid_ip


router = APIRouter(prefix="/api/search", tags=["Search"])


@router.post("/ioc")
async def search_ioc(payload: IOCSearchRequest, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    indicator = payload.ioc.strip()
    if not indicator:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No threat intelligence data was found for this indicator.")

    local_matches = db.query(IOC).filter(IOC.ioc_value == indicator).all()
    local_payload = [
        {
            "id": item.id,
            "ioc_type": item.ioc_type,
            "ioc_value": item.ioc_value,
            "source": item.source,
            "confidence": item.confidence,
            "risk_score": item.risk_score,
            "severity": item.severity,
            "first_seen": item.first_seen,
            "last_seen": item.last_seen,
            "description": item.description,
            "raw_metadata": item.raw_metadata,
        }
        for item in local_matches
    ]

    internetdb_payload = None
    if is_valid_ip(indicator):
        try:
            internetdb_payload = await lookup_ip(indicator)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
        except InternetDBError as exc:
            return {"query": indicator, "ioc_type": "IP", "local_matches": local_payload, "internetdb": None, "message": str(exc)}

    if not local_payload and internetdb_payload is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No threat intelligence data was found for this indicator.")

    return {"query": indicator, "ioc_type": identify_ioc_type(indicator), "local_matches": local_payload, "internetdb": internetdb_payload.model_dump() if internetdb_payload else None, "message": None}
