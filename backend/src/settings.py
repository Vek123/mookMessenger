import os
from pathlib import Path

from dotenv import load_dotenv


# KEEP IT SECRET
JWT_SECRET = os.environ.get("JWT_SECRET")
USER_MANAGER_SECRET = os.environ.get("USER_MANAGER_SECRET")

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

DATABASE_CONFIG = {
    "DB_HOST": os.environ.get("DB_HOST"),
    "DB_PORT": os.environ.get("DB_PORT"),
    "DB_NAME": os.environ.get("DB_NAME"),
    "DB_USER": os.environ.get("DB_USER"),
    "DB_PASS": os.environ.get("DB_PASS"),
}
