from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL
import os
import logging

# For SQLite, set connect_args accordingly
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith(
    "sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_database():
    """Initialize database tables. For development/testing only."""
    if DATABASE_URL.startswith("sqlite"):
        db_path = DATABASE_URL.replace("sqlite:///", "")
        if os.path.exists(db_path):
            os.remove(db_path)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    logging.info("Database initialized with clean slate")


def ensure_database():
    """Ensure database tables exist. Safe for production use."""
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    if not existing_tables:
        Base.metadata.create_all(bind=engine)
        logging.info("Database tables created")
    else:
        logging.info("Database tables already exist")


def reset_database():
    """Reset database to clean state. For testing only."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    logging.info("Database reset to clean state")


def cleanup_database():
    """Clean up database resources."""
    if DATABASE_URL.startswith("sqlite"):
        db_path = DATABASE_URL.replace("sqlite:///", "")
        if os.path.exists(db_path):
            os.remove(db_path)
            logging.info("SQLite database file removed")
