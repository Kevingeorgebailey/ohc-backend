# app/main.py
from __future__ import annotations

import os
from typing import Iterator

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import SessionLocal


def _allowed_origins() -> list[str]:
    raw = os.getenv("ALLOWED_ORIGINS")
    if not raw:
        return ["*"]
    parts = [p.strip() for p in raw.replace(" ", ",").split(",")]
    return [p for p in parts if p] or ["*"]


# ---------- FastAPI app ----------
app = FastAPI(
    title="OH Compare API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- DB dependency ----------
def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Routes ----------
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/providers", response_model=list[schemas.ProviderOut])
def list_providers(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
) -> list[schemas.ProviderOut]:
    q = db.query(models.Provider).offset(offset).limit(limit)
    return q.all()

@app.get("/")
def root() -> dict[str, str]:
    return {"docs": "/docs", "health": "/health"}
