import os
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict, Any
from pydantic import BaseSettings, validator

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    ALLOWED_HOSTS: List[str] = os.getenv("ALLOWED_HOSTS", ["*"]).split(",")

    @validator("DATABASE_URL", pre=True)
    def validate_database_url(cls, v: str) -> str:
        if not v:
            raise ValueError("DATABASE_URL environment variable is required.")
        return v

    @validator("OPENAI_API_KEY", pre=True)
    def validate_openai_api_key(cls, v: str) -> str:
        if not v:
            raise ValueError("OPENAI_API_KEY environment variable is required.")
        return v

    @validator("JWT_SECRET", pre=True)
    def validate_jwt_secret(cls, v: str) -> str:
        if not v:
            raise ValueError("JWT_SECRET environment variable is required.")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True

    @property
    def db_url(self) -> str:
        return self.DATABASE_URL

    @property
    def redis_connection_params(self) -> Dict[str, Any]:
        return {"host": self.REDIS_HOST, "port": self.REDIS_PORT}

    @property
    def openai_config(self) -> Dict[str, str]:
        return {"api_key": self.OPENAI_API_KEY}

settings = Settings()