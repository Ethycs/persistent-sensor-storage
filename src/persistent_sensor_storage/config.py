import os
from dotenv import load_dotenv
load_dotenv()
# Read database URL from environment or fallback to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
SENTRY_DSN = os.getenv("SENTRY_DSN")