# backend/create_tables.py
from app.db import Base, engine
from app import models  # ensure models are imported so tables are registered

if __name__ == "__main__":
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")
