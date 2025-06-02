from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL from environment
#DATABASE_URL = os.getenv('DATABASE_URL', default='postgresql://postgres:password123@localhost:5432/fastapi_db')

# Database URL from environment - SQLite configuration
DATABASE_URL = os.getenv('DATABASE_URL', default='sqlite:///./fastapi_app.db')

# Create engine
engine = create_engine(DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()