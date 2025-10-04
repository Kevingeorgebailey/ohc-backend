import os, psycopg
from dotenv import load_dotenv

load_dotenv()
u = os.getenv("DATABASE_URL")
print("URL present:", bool(u))
if not u:
    raise SystemExit("DATABASE_URL not found in .env")

with psycopg.connect(u) as conn, conn.cursor() as cur:
    cur.execute("select table_name from information_schema.tables where table_schema='public' order by 1")
    print("Tables:", [r[0] for r in cur.fetchall()])
