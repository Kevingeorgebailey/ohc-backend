from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, text, Index
from sqlalchemy.orm import relationship
from .db import Base

class Provider(Base):
    __tablename__ = "providers"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    website = Column(String)
    phone = Column(String)
    email = Column(String)
    summary = Column(String)
    created_at = Column(DateTime, server_default=text("NOW()"))  # ← removed extra ')'
    updated_at = Column(DateTime, server_default=text("NOW()"), onupdate=text("NOW()"))

    locations = relationship("Location", back_populates="provider", cascade="all, delete-orphan")

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    provider_id = Column(Integer, ForeignKey("providers.id", ondelete="CASCADE"), nullable=False)
    address = Column(String)
    postcode = Column(String)
    latitude = Column(String)
    longitude = Column(String)

    provider = relationship("Provider", back_populates="locations")

# Index("ix_providers_name", Provider.name)
