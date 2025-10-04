from .db import SessionLocal
from .models import Provider, Location

seed = [
    {
        "name": "Acme Occupational Health",
        "website": "https://acme-oh.example",
        "phone": "+44 20 7123 4567",
        "email": "info@acme-oh.example",
        "summary": "Full-service OH provider with UK-wide remote coverage",
        "locations": [
            {"address": "10 King St, Manchester", "postcode": "M2 6AQ", "latitude": "53.4808", "longitude": "-2.2426"},
        ],
    },
    {
        "name": "Fleet Street Clinic OH",
        "website": "https://fleetstreet.example",
        "phone": "+44 20 7353 5678",
        "email": "contact@fleetstreet.example",
        "summary": "City-based clinic with rapid turnaround",
        "locations": [
            {"address": "29 Fleet St, London", "postcode": "EC4Y 1AA", "latitude": "51.5136", "longitude": "-0.1058"},
        ],
    },
]

def run():
    db = SessionLocal()
    try:
        for p in seed:
            provider = Provider(
                name=p["name"],
                website=p.get("website"),
                phone=p.get("phone"),
                email=p.get("email"),
                summary=p.get("summary"),
            )
            db.add(provider)
            db.flush()
            for loc in p["locations"]:
                db.add(Location(provider_id=provider.id, **loc))
        db.commit()
        print("Seeded providers.")
    finally:
        db.close()

if __name__ == "__main__":
    run()
