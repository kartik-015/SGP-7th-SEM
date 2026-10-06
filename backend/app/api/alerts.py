from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.database.database import get_db
from app.database.models import Alert, AuditLog, IOC, User
from app.schemas.alert import AlertRead, AlertReviewResponse, AlertStatusUpdate


router = APIRouter(prefix="/api/alerts", tags=["Alerts"])


@router.get("", response_model=list[AlertRead])
def list_alerts(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    alerts = db.query(Alert, IOC).join(IOC, Alert.ioc_id == IOC.id).order_by(Alert.triggered_at.desc()).all()
    return [
        AlertRead(
            id=alert.id,
            ioc_id=alert.ioc_id,
            severity=alert.severity,
            status=alert.status,
            triggered_at=alert.triggered_at,
            ioc_value=ioc.ioc_value,
            ioc_type=ioc.ioc_type,
            risk_score=ioc.risk_score,
        )
        for alert, ioc in alerts
    ]


@router.put("/{alert_id}/review", response_model=AlertReviewResponse)
def review_alert(alert_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    alert = db.query(Alert).filter(Alert.id == alert_id).one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.status = "Reviewed"
    db.add(alert)
    db.add(AuditLog(actor_id=current_user.id, action="alert.reviewed", entity_type="alert", entity_id=str(alert.id), details={"status": alert.status}))
    db.commit()
    return AlertReviewResponse(message="Alert marked as reviewed.")


@router.put("/{alert_id}/status", response_model=AlertReviewResponse)
def update_alert_status(alert_id: int, payload: AlertStatusUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    alert = db.query(Alert).filter(Alert.id == alert_id).one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.status = payload.status
    db.add(alert)
    db.add(AuditLog(actor_id=current_user.id, action="alert.status_changed", entity_type="alert", entity_id=str(alert.id), details={"status": alert.status}))
    db.commit()
    return AlertReviewResponse(message=f"Alert status updated to {payload.status}.")
