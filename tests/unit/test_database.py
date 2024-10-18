from typing import Dict

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# Third-party packages
from unittest.mock import Mock, patch
from core.database import database, models
from config.settings import settings
from core.utils.utils import hash_password

# Required versions
pytest.__version__ == "8.3.3"
sqlalchemy.__version__ == "2.0.36"
settings.__version__ == "1.0.1"

# Mocking database connection and session
@pytest.fixture(scope="function")
def db():
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test data
test_user_data = {
    "username": "testuser",
    "password": "testpassword",
}
test_query_data = {
    "user_id": 1,
    "query_text": "What is the meaning of life?",
    "model": "text-davinci-003",
    "parameters": {"temperature": 0.7, "max_tokens": 256},
    "response": "The meaning of life is a profound question...",
}

# Test functions
def test_create_user(db):
    """
    Test the creation of a new user in the database.
    """
    hashed_password = hash_password(test_user_data["password"])
    new_user = database.create_user(
        db, username=test_user_data["username"], password=hashed_password
    )
    assert new_user.username == test_user_data["username"]

def test_authenticate_user(db):
    """
    Test user authentication against the database.
    """
    hashed_password = hash_password(test_user_data["password"])
    new_user = database.create_user(
        db, username=test_user_data["username"], password=hashed_password
    )
    authenticated_user = database.authenticate_user(
        db, username=test_user_data["username"], password=test_user_data["password"]
    )
    assert authenticated_user.id == new_user.id

def test_authenticate_user_invalid_credentials(db):
    """
    Test authentication with incorrect credentials.
    """
    authenticated_user = database.authenticate_user(
        db, username="invaliduser", password="wrongpassword"
    )
    assert authenticated_user is None

def test_store_query_and_response(db):
    """
    Test storing a new query and its response in the database.
    """
    new_query = database.store_query_and_response(
        db,
        user_id=test_query_data["user_id"],
        query_text=test_query_data["query_text"],
        model=test_query_data["model"],
        parameters=test_query_data["parameters"],
        response=test_query_data["response"],
    )
    assert new_query.query_text == test_query_data["query_text"]
    assert new_query.response == test_query_data["response"]

def test_get_response_by_id(db):
    """
    Test retrieving the response for a given query ID.
    """
    new_query = database.store_query_and_response(
        db,
        user_id=test_query_data["user_id"],
        query_text=test_query_data["query_text"],
        model=test_query_data["model"],
        parameters=test_query_data["parameters"],
        response=test_query_data["response"],
    )
    retrieved_response = database.get_response_by_id(db, query_id=new_query.id)
    assert retrieved_response == test_query_data["response"]

def test_get_response_by_id_invalid_id(db):
    """
    Test retrieving a response with an invalid query ID.
    """
    retrieved_response = database.get_response_by_id(db, query_id=999)
    assert retrieved_response is None

def test_get_user_queries(db):
    """
    Test retrieving a list of queries for a specific user.
    """
    new_query = database.store_query_and_response(
        db,
        user_id=test_query_data["user_id"],
        query_text=test_query_data["query_text"],
        model=test_query_data["model"],
        parameters=test_query_data["parameters"],
        response=test_query_data["response"],
    )
    user_queries = database.get_user_queries(db, user_id=test_query_data["user_id"])
    assert len(user_queries) == 1
    assert user_queries[0].id == new_query.id
    assert user_queries[0].query_text == test_query_data["query_text"]

# Mocking OpenAI API calls (for testing)
@patch("core.services.openai_service.OpenAIService.process_query")
def test_store_query_and_response_with_openai_integration(mock_process_query, db):
    """
    Test storing a query and response, including mocked OpenAI API interaction.
    """
    mock_process_query.return_value = test_query_data["response"]
    new_query = database.store_query_and_response(
        db,
        user_id=test_query_data["user_id"],
        query_text=test_query_data["query_text"],
        model=test_query_data["model"],
        parameters=test_query_data["parameters"],
        response=test_query_data["response"],
    )
    assert new_query.query_text == test_query_data["query_text"]
    assert new_query.response == test_query_data["response"]
    mock_process_query.assert_called_once_with(
        test_query_data["query_text"],
        test_query_data["model"],
        test_query_data["parameters"],
    )