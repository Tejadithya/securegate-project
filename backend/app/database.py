from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Use environment variable or default (@ symbol encoded as %40)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:teja%402004@localhost:5432/progres")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
