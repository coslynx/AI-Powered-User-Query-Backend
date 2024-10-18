from typing import Optional, List, Dict, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from config.settings import settings
from core.database import models

# Database Connection and Session:
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)  # Initialize database engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Define session maker

# Base Model for SQLAlchemy:
Base = declarative_base()

# Database Session Management:
def get_db():
    """Provides a database session for the application."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Main Database Operations:
def create_user(db: Session, username: str, password: str):
    """Creates a new user in the database."""
    new_user = models.User(username=username, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, username: str, password: str):
    """Authenticates a user against the database."""
    user = db.query(models.User).filter(models.User.username == username).first()
    if user and bcrypt.checkpw(password.encode(), user.password.encode()):
        return user
    return None

def store_query_and_response(db: Session, user_id: int, query_text: str, model: str, parameters: Dict, response: str):
    """Stores a new query and its response in the database."""
    new_query = models.Query(
        user_id=user_id,
        query_text=query_text,
        model=model,
        parameters=parameters,
        response=response,
        timestamp=datetime.utcnow()
    )
    db.add(new_query)
    db.commit()
    db.refresh(new_query)
    return new_query

def get_response_by_id(db: Session, query_id: int):
    """Retrieves the response for a given query ID from the database."""
    query = db.query(models.Query).filter(models.Query.id == query_id).first()
    if query:
        return query.response
    return None

def get_user_queries(db: Session, user_id: int):
    """Retrieves a list of queries for a specific user from the database."""
    queries = db.query(models.Query).filter(models.Query.user_id == user_id).all()
    return queries

# Optional: Caching Mechanism using Redis:
if settings.REDIS_HOST:
    redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    
    def cache_response(query_id: str, response: str):
        """Caches the response for a given query ID in Redis."""
        redis_client.set(query_id, response)

    def get_cached_response(query_id: str):
        """Retrieves the cached response for a given query ID from Redis."""
        return redis_client.get(query_id).decode("utf-8")