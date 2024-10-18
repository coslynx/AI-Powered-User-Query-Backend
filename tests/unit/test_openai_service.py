import pytest
from unittest.mock import patch
from core.services.openai_service import OpenAIService  # Version 1.52.0

# Test data
test_query = "What is the meaning of life?"
test_model = "text-davinci-003"
test_parameters = {"temperature": 0.7, "max_tokens": 256}
test_response = "The meaning of life is a question that has been pondered..."

# Mock OpenAI API responses
@patch("openai.Completion.create")
def test_process_query_success(mock_create, openai_service: OpenAIService):
    """
    Test successful query processing using OpenAI's API.

    This test verifies that the `process_query` function correctly sends a request
    to OpenAI's API, retrieves the response, and returns it to the caller.
    """
    mock_create.return_value = {"choices": [{"text": test_response}]}
    response = openai_service.process_query(
        query=test_query, model=test_model, parameters=test_parameters
    )
    assert response == test_response
    mock_create.assert_called_once_with(
        engine=test_model,
        prompt=test_query,
        temperature=test_parameters.get("temperature", 0.7),
        max_tokens=test_parameters.get("max_tokens", 256),
        top_p=test_parameters.get("top_p"),
        frequency_penalty=test_parameters.get("frequency_penalty"),
        presence_penalty=test_parameters.get("presence_penalty"),
    )

@patch("openai.Completion.create")
def test_process_query_api_error(mock_create, openai_service: OpenAIService):
    """
    Test handling of OpenAI API errors during query processing.

    This test ensures that the `process_query` function correctly handles
    OpenAI API errors and raises the appropriate exception.
    """
    mock_create.side_effect = openai.error.APIError("Test API error")
    with pytest.raises(openai.error.APIError):
        openai_service.process_query(
            query=test_query, model=test_model, parameters=test_parameters
        )

@patch("openai.Completion.create")
def test_process_query_network_error(mock_create, openai_service: OpenAIService):
    """
    Test handling of network errors during query processing.

    This test verifies that the `process_query` function correctly handles
    network errors and raises the appropriate exception.
    """
    mock_create.side_effect = requests.exceptions.RequestException("Test network error")
    with pytest.raises(requests.exceptions.RequestException):
        openai_service.process_query(
            query=test_query, model=test_model, parameters=test_parameters
        )

# Test fixture to create an instance of the OpenAIService
@pytest.fixture
def openai_service():
    """
    Fixture to create an instance of the OpenAIService.
    """
    return OpenAIService()

# Test setup and teardown
def test_openai_service_init(openai_service: OpenAIService):
    """
    Test the initialization of the OpenAIService.

    This test verifies that the OpenAIService is initialized with the correct
    API key from settings.
    """
    assert openai_service.api_key == "sk-your-openai-api-key" # Replace with your API key