from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .database import Base
from .config import DATABASE_URL
import os

# Remove existing database file if it exists
if DATABASE_URL.startswith("sqlite"):
    db_path = DATABASE_URL.replace("sqlite:///", "")
    if os.path.exists(db_path):
        os.remove(db_path)

# Create new database with updated schema
engine = create_engine(DATABASE_URL)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
