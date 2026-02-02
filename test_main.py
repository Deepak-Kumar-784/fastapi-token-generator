"""
Test cases for the Token Generation API
Author: Deepak
Date: February 2, 2026

This module contains comprehensive test cases for all API endpoints
using the FastAPI TestClient.
"""

from fastapi.testclient import TestClient
from main import app, generate
import pytest

# Create a test client for the FastAPI application
client = TestClient(app)


class TestWelcomeEndpoint:
    """Test cases for the welcome endpoint"""

    def test_welcome_message(self):
        """Test that the welcome endpoint returns HTML homepage"""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "Deepak" in response.text
        assert "Welcome" in response.text


class TestGenerateFunction:
    """Test cases for the generate() function"""

    def test_generate_simple_text(self):
        """Test tokenization of simple text"""
        result = generate("Hello World")
        assert result == ["Hello", "World"]
        assert len(result) == 2

    def test_generate_multiple_words(self):
        """Test tokenization with multiple words"""
        result = generate("This is a test sentence")
        assert result == ["This", "is", "a", "test", "sentence"]
        assert len(result) == 5

    def test_generate_with_extra_spaces(self):
        """Test tokenization with extra whitespace"""
        result = generate("Hello    World   Test")
        assert result == ["Hello", "World", "Test"]
        assert len(result) == 3

    def test_generate_empty_string(self):
        """Test tokenization of empty string"""
        result = generate("")
        assert result == []
        assert len(result) == 0

    def test_generate_single_word(self):
        """Test tokenization of single word"""
        result = generate("Hello")
        assert result == ["Hello"]
        assert len(result) == 1


class TestGenerateEndpoint:
    """Test cases for the /generate GET endpoint"""

    def test_generate_endpoint_success(self):
        """Test successful token generation via query parameter"""
        response = client.get("/generate?text=Hello World")
        assert response.status_code == 200
        data = response.json()
        assert "tokens" in data
        assert "count" in data
        assert data["tokens"] == ["Hello", "World"]
        assert data["count"] == 2

    def test_generate_endpoint_with_multiple_words(self):
        """Test endpoint with multiple words"""
        response = client.get("/generate?text=FastAPI is awesome")
        assert response.status_code == 200
        data = response.json()
        assert data["tokens"] == ["FastAPI", "is", "awesome"]
        assert data["count"] == 3

    def test_generate_endpoint_empty_text(self):
        """Test endpoint with empty text parameter"""
        response = client.get("/generate?text=")
        assert response.status_code == 400
        assert "detail" in response.json()

    def test_generate_endpoint_whitespace_only(self):
        """Test endpoint with whitespace-only text"""
        response = client.get("/generate?text=   ")
        assert response.status_code == 400


class TestTokenizeEndpoint:
    """Test cases for the /tokenize POST endpoint"""

    def test_tokenize_success(self):
        """Test successful tokenization via POST request"""
        response = client.post("/tokenize", json={"text": "Hello World"})
        assert response.status_code == 200
        data = response.json()
        assert data["tokens"] == ["Hello", "World"]
        assert data["count"] == 2

    def test_tokenize_complex_sentence(self):
        """Test tokenization of complex sentence"""
        response = client.post("/tokenize", json={"text": "This is a FastAPI test"})
        assert response.status_code == 200
        data = response.json()
        assert data["tokens"] == ["This", "is", "a", "FastAPI", "test"]
        assert data["count"] == 5

    def test_tokenize_empty_text(self):
        """Test tokenization with empty text"""
        response = client.post("/tokenize", json={"text": ""})
        assert response.status_code == 422  # Validation error due to min_length=1

    def test_tokenize_whitespace_only(self):
        """Test tokenization with whitespace-only text"""
        response = client.post("/tokenize", json={"text": "   "})
        assert response.status_code == 400

    def test_tokenize_missing_text_field(self):
        """Test request with missing text field"""
        response = client.post("/tokenize", json={})
        assert response.status_code == 422  # Validation error

    def test_tokenize_invalid_json(self):
        """Test request with invalid field name"""
        response = client.post("/tokenize", json={"invalid_field": "test"})
        assert response.status_code == 422


class TestChecksumEndpoint:
    """Test cases for the /checksum POST endpoint"""

    def test_checksum_success(self):
        """Test successful checksum generation"""
        response = client.post("/checksum", json={"text": "Hello World"})
        assert response.status_code == 200
        data = response.json()
        assert "checksum" in data
        assert "original_text" in data
        assert data["original_text"] == "Hello World"
        # MD5 checksum of "Hello World"
        assert data["checksum"] == "b10a8db164e0754105b7a99be72e3fe5"

    def test_checksum_consistency(self):
        """Test that same text produces same checksum"""
        text = "FastAPI is great"
        response1 = client.post("/checksum", json={"text": text})
        response2 = client.post("/checksum", json={"text": text})

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response1.json()["checksum"] == response2.json()["checksum"]

    def test_checksum_different_texts(self):
        """Test that different texts produce different checksums"""
        response1 = client.post("/checksum", json={"text": "Hello"})
        response2 = client.post("/checksum", json={"text": "World"})

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response1.json()["checksum"] != response2.json()["checksum"]

    def test_checksum_empty_text(self):
        """Test checksum with empty text"""
        response = client.post("/checksum", json={"text": ""})
        assert response.status_code == 422  # Validation error


class TestAPIDocumentation:
    """Test cases for API documentation and metadata"""

    def test_openapi_schema_available(self):
        """Test that OpenAPI schema is accessible"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "info" in schema
        assert schema["info"]["title"] == "Token Generation API"

    def test_docs_endpoint_available(self):
        """Test that Swagger UI documentation is accessible"""
        response = client.get("/docs")
        assert response.status_code == 200


# Additional integration tests
class TestIntegrationScenarios:
    """Integration test scenarios"""

    def test_tokenize_and_checksum_same_text(self):
        """Test that tokenize and checksum work correctly with same text"""
        test_text = "Integration test scenario"

        # Test tokenize endpoint
        tokenize_response = client.post("/tokenize", json={"text": test_text})
        assert tokenize_response.status_code == 200

        # Test checksum endpoint
        checksum_response = client.post("/checksum", json={"text": test_text})
        assert checksum_response.status_code == 200

        # Verify both return correct data
        assert tokenize_response.json()["count"] == 3
        assert checksum_response.json()["original_text"] == test_text


if __name__ == "__main__":
    # Run tests using pytest
    pytest.main([__file__, "-v"])
