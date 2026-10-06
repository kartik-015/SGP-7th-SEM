from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.auth import require_admin
from app.core.security import get_password_hash
from app.database.database import get_db
from app.database.models import AuditLog, User
from app.schemas.alert import AuditLogRead
from app.schemas.user import UserAdminUpdate, UserCreate, UserRead


router = APIRouter(prefix="/api/admin", tags=["Administration"])


@router.get("/users", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return db.query(User).order_by(User.created_at.desc()).all()


@router.post("/users", response_model=UserRead, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    if payload.role not in {"Analyst", "Administrator"}:
        raise HTTPException(status_code=400, detail="Invalid role")
    if db.query(User).filter(User.email == payload.email).one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(full_name=payload.full_name, email=payload.email, hashed_password=get_password_hash(payload.password), role=payload.role)
    db.add(user)
    db.flush()
    db.add(AuditLog(actor_id=current_user.id, action="user.created", entity_type="user", entity_id=str(user.id), details={"email": user.email, "role": user.role}))
    db.commit()
    db.refresh(user)
    return user


@router.patch("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, payload: UserAdminUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_user.id and payload.is_active is False:
        raise HTTPException(status_code=400, detail="You cannot deactivate your own account")
    if payload.role is not None and payload.role not in {"Analyst", "Administrator"}:
        raise HTTPException(status_code=400, detail="Invalid role")
    if payload.role is not None:
        user.role = payload.role
    if payload.is_active is not None:
        user.is_active = payload.is_active
    db.add(user)
    db.add(AuditLog(actor_id=current_user.id, action="user.updated", entity_type="user", entity_id=str(user.id), details={"role": user.role, "is_active": user.is_active}))
    db.commit()
    db.refresh(user)
    return user


@router.get("/audit", response_model=list[AuditLogRead])
def list_audit_logs(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(200).all()