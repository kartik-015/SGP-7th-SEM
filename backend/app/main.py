from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.alerts import router as alerts_router
from app.api.admin import router as admin_router
from app.api.auth import router as auth_router
from app.api.dashboard import router as dashboard_router
from app.api.search import router as search_router
from app.api.threats import router as threats_router
from app.api.exports import router as exports_router
from app.api.telemetry import router as telemetry_router
from app.core.config import settings
from app.database.database import SessionLocal, init_db
from app.utils.seed_data import seed_all


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    db = SessionLocal()
    try:
        seed_all(db)
    finally:
        db.close()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(threats_router)
app.include_router(search_router)
app.include_router(alerts_router)
app.include_router(admin_router)
app.include_router(exports_router)
app.include_router(telemetry_router)


@app.get("/")
def root():
    return {"message": "Cyber Threat Intelligence Dashboard API is running."}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
