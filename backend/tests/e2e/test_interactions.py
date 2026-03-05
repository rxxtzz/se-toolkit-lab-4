"""End-to-end tests for the GET /interactions endpoint."""

import os
import pytest
import httpx
from typing import Generator

API_BASE_URL = os.getenv("API_BASE_URL", "http://10.93.26.29:42000")
API_TOKEN = os.getenv("API_TOKEN", "my-secret-api-key")

@pytest.fixture
def client() -> Generator[httpx.Client, None, None]:
    """Create a test client with authentication."""
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    with httpx.Client(base_url=API_BASE_URL, headers=headers) as client:
        yield client

def test_get_interactions_returns_200(client: httpx.Client) -> None:
    """Test that GET /interactions/ returns 200 OK."""
    response = client.get("api/interactions/")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

def test_get_interactions_response_is_a_list(client: httpx.Client) -> None:
    """Test that GET /interactions/ returns a JSON array."""
    response = client.get("api/interactions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list), f"Expected list, got {type(data)}"
