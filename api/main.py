from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Dict, Optional

from . import routes
from .database import database, models
from .services import openai_service
from .utils import logger
from .utils.utils import generate_token

# Import Statements:
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import os, json 

# Third-Party Packages:
from fastapi.responses import JSONResponse  # 0.115.2: Modern API framework for building APIs with type safety, automatic documentation, and ASGI support
import uvicorn  # 0.32.0: ASGI server for running FastAPI applications
from pydantic import BaseModel  # 2.9.2:  Data validation and type checking for API models
from sqlalchemy import create_engine  # 2.0.36: Object-relational mapper for database interactions
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker  # Manage database sessions efficiently
import openai  # 1.52.0: Interact with OpenAI's API for query processing
import requests  # 2.32.3: Make HTTP requests to external APIs, including OpenAI
import json  # Built-in library for working with JSON data
from python_dotenv import load_dotenv  # 1.0.1: Load environment variables from a `.env` file
import pyjwt  # 2.9.0: Generate and verify JSON Web Tokens (JWT) for authentication
from bcrypt import hashpw, gensalt  # 4.2.0: Securely hash passwords using bcrypt
import psycopg2_binary  # 2.9.10: PostgreSQL database connector for Python
import redis  # 5.1.1: Redis library for caching frequently accessed data

# Internal Modules:
from .services.openai_service import OpenAIService  # Import OpenAI service for handling API interactions
from .database.database import engine, SessionLocal, Base  # Import database configurations and session management
from .database.models import User, Query  # Import data models for database interaction
from .utils.logger import logger # Import logging module
from .utils.utils import generate_token # Import utility functions

# Environment Variable Loading:
load_dotenv()

# Configuration:
DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
JWT_SECRET = os.getenv("JWT_SECRET")

# Package Initialization:
openai.api_key = OPENAI_API_KEY

# Database Connection:
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base Model:
Base = declarative_base()

# Redis Connection:
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

# Main Components:
app = FastAPI()

# CORS Configuration:
origins = ["*"]  # Adjust origins as needed for security
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication Setup:
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency Injection:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes:
app.include_router(routes.router)

# Start Server:
if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,  # Or the port specified in the .env file
        reload=True,
    )