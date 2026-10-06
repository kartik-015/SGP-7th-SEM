from __future__ import annotations

import csv
import io

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.database.database import get_db
from app.database.models import IOC, User


router = APIRouter(prefix="/api/exports", tags=["Exports"])


@router.get("/iocs.csv")
def export_iocs(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "ioc_type", "ioc_value", "source", "confidence", "risk_score", "severity", "first_seen", "last_seen", "description"])
    for ioc in db.query(IOC).order_by(IOC.risk_score.desc()).all():
        writer.writerow([ioc.id, ioc.ioc_type, ioc.ioc_value, ioc.source, ioc.confidence, ioc.risk_score, ioc.severity, ioc.first_seen.isoformat(), ioc.last_seen.isoformat(), ioc.description])
    output.seek(0)
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=ioc-export.csv"})