from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to your domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from .db import get_db
from . import models, schemas
from .utils import haversine_km

app = FastAPI(title="OH Providers API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/providers", response_model=List[schemas.ProviderOut])
def list_providers(
    lat: Optional[float] = Query(None, description="Latitude for radius search"),
    lon: Optional[float] = Query(None, description="Longitude for radius search"),
    radius_km: float = Query(50.0, description="Radius in km"),
    db: Session = Depends(get_db),
):
    providers = db.query(models.Provider).join(models.Location).all()

    if lat is None or lon is None:
        return providers

    filtered = []
    for p in providers:
        for loc in p.locations:
            try:
                if loc.latitude and loc.longitude:
                    d = haversine_km(float(loc.latitude), float(loc.longitude), lat, lon)
                    if d <= radius_km:
                        filtered.append(p)
                        break
            except ValueError:
                continue
    return filtered

@app.get("/providers/{provider_id}", response_model=schemas.ProviderOut)
def get_provider(provider_id: int, db: Session = Depends(get_db)):
    p = db.query(models.Provider).filter(models.Provider.id == provider_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Provider not found")
    return p
