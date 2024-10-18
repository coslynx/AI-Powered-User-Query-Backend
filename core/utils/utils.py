import logging
from typing import Dict, Optional
import bcrypt
import redis
import jwt
from datetime import datetime, timedelta

from config.settings import settings

logger = logging.getLogger(__name__)

def generate_token(user_id: int) -> str:
    """Generates a JSON Web Token (JWT) for a given user ID."""
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES),
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
    return token.decode("utf-8")

def verify_token(token: str) -> Optional[Dict]:
    """Verifies a JWT token and returns its payload."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("JWT token has expired.")
        return None
    except jwt.InvalidTokenError:
        logger.warning("Invalid JWT token.")
        return None

def hash_password(password: str) -> str:
    """Hashes a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt).decode()
    return hashed_password

def check_password(password: str, hashed_password: str) -> bool:
    """Checks if a given password matches a hashed password."""
    try:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
    except bcrypt.exceptions.InvalidHashError:
        logger.error("Invalid hashed password.")
        return False

def cache_response(query_id: str, response: str) -> None:
    """Caches the response for a given query ID in Redis."""
    if settings.REDIS_HOST:
        redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        redis_client.set(query_id, response)
        logger.info(f"Cached response for query ID: {query_id}")

def get_cached_response(query_id: str) -> Optional[str]:
    """Retrieves the cached response for a given query ID from Redis."""
    if settings.REDIS_HOST:
        redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        cached_response = redis_client.get(query_id)
        if cached_response:
            return cached_response.decode("utf-8")
    return None