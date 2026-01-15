from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Database URL format: postgresql://USER:PASSWORD@HOST/DB_NAME
# The 'db' hostname is crucial and should match your PostgreSQL service name in docker-compose.yml
DATABASE_URL = os.environ.get(
    "DATABASE_URL", 
    "postgresql://user:password@db/voting_db" 
)

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models
Base = declarative_base()

# --- Database Model ---
class Vote(Base):
    __tablename__ = "votes"

    color = Column(String, primary_key=True, index=True)
    count = Column(Integer, default=0)

# Function to create tables and seed initial data
def init_db():
    Base.metadata.create_all(bind=engine)
    # Seed initial poll data
    try:
        db = SessionLocal()
        colors = ["Red", "Green", "Blue", "Yellow"]
        for color in colors:
            if db.query(Vote).filter(Vote.color == color).first() is None:
                vote = Vote(color=color, count=0)
                db.add(vote)
        db.commit()
    except Exception as e:
        print(f"Error initializing data: {e}")
    finally:
        db.close()