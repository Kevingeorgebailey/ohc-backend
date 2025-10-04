import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

load_dotenv()  # <-- reads backend/.env

config = context.config

db_url = os.getenv("DATABASE_URL")  # <-- THIS LINE (string key only)
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)
