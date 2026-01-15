from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, init_db, Vote
import time

# --- Database Initialization (Waiting for DB Service) ---
def wait_for_db():
    """Tries to initialize the DB, waiting a few seconds if connection fails."""
    retries = 5
    while retries > 0:
        try:
            init_db()
            print("Database initialized successfully!")
            return
        except Exception as e:
            print(f"Database connection failed, retrying in 5s... Error: {e}")
            time.sleep(5)
            retries -= 1
    raise ConnectionError("Could not connect to the database after multiple retries.")

# Initialize the database before the app starts
wait_for_db()

app = FastAPI()

# --- CORS Middleware ---
# Allows frontend (http://localhost:3000) to communicate with backend (http://localhost:8000)
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Dependency to get DB session ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API Endpoints ---

@app.get("/votes")
def get_votes(db: Session = Depends(get_db)):
    """Retrieve the current vote counts for all colors."""
    votes = db.query(Vote).all()
    # Return as a dictionary: {"Red": 0, "Green": 0, ...}
    return {vote.color: vote.count for vote in votes}

@app.post("/vote/{color}")
def cast_vote(color: str, db: Session = Depends(get_db)):
    """Cast a vote for a specific color."""
    vote_record = db.query(Vote).filter(Vote.color == color).first()

    if not vote_record:
        raise HTTPException(status_code=404, detail="Color not found")

    vote_record.count += 1
    db.commit()
    db.refresh(vote_record)

    return {"message": f"Voted for {color} successfully", "color": color, "new_count": vote_record.count}

@app.get("/")
def health_check():
    return {"msg": "Service is up"}