import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Second Brain API"}

# We will just do a basic test for root to ensure the app initializes correctly
# E2E tests for RAG and LLM require real or mocked API keys which is brittle,
# so we stick to structural validation.
