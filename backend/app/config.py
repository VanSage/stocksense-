import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Defaults to a local SQLite file so the project runs out of the box with
# zero external setup. For production, point DATABASE_URL at MySQL instead,
# e.g. mysql+pymysql://user:password@localhost:3306/stocksense
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/stocksense.db")

# Hosted providers (Neon, Render, Heroku...) hand out URLs that start with
# "postgres://" or "postgresql://". SQLAlchemy needs to be told which driver
# to use, so normalise them here once.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = "postgresql+psycopg2://" + DATABASE_URL[len("postgres://"):]
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = "postgresql+psycopg2://" + DATABASE_URL[len("postgresql://"):]

# Create the demo shop automatically on startup if it doesn't exist yet, so the
# demo login always works on a fresh deployment. Set AUTO_SEED=0 to disable.
AUTO_SEED = os.getenv("AUTO_SEED", "1") == "1"

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173,http://localhost:4173,http://127.0.0.1:4173"
).split(",")
