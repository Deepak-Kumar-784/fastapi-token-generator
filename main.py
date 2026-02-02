"""
FastAPI Token Generation API
Author: Deepak
Date: February 2, 2026

This API provides endpoints for generating tokens and checksums from text.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import hashlib
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get configuration from environment variables
APP_NAME = os.getenv("APP_NAME", "Token Generation API")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_DESCRIPTION = os.getenv(
    "APP_DESCRIPTION", "API for generating tokens and checksums from text"
)
PARTICIPANT_NAME = os.getenv("PARTICIPANT_NAME", "Deepak")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Initialize FastAPI application
app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
)


# Pydantic model for accepting JSON input with text field
class TextInput(BaseModel):
    """
    Model for text input validation.

    Attributes:
        text (str): The input text to be processed
    """

    text: str = Field(..., description="The text to generate tokens from", min_length=1)


class TokenResponse(BaseModel):
    """
    Model for token response.

    Attributes:
        tokens (List[str]): List of generated tokens
        count (int): Number of tokens generated
    """

    tokens: List[str]
    count: int


class ChecksumResponse(BaseModel):
    """
    Model for checksum response.

    Attributes:
        checksum (str): MD5 checksum of the input text
        original_text (str): The original input text
    """

    checksum: str
    original_text: str


def generate(text: str) -> List[str]:
    """
    Generate tokens from the input text by splitting on whitespace.

    This function takes a string as input and splits it into individual tokens
    based on whitespace characters. Each token is stripped of leading/trailing
    whitespace.

    Args:
        text (str): The input text to tokenize

    Returns:
        List[str]: A list of tokens extracted from the text

    Example:
        >>> generate("Hello World")
        ['Hello', 'World']
    """
    # Split text by whitespace and filter out empty strings
    tokens = [token.strip() for token in text.split() if token.strip()]
    return tokens


@app.get("/")
async def welcome():
    """
    Welcome endpoint with customized message.

    Returns a personalized greeting message to the user.

    Returns:
        dict: Welcome message with participant name
    """
    return {
        "message": "Welcome to the Token Generation API!",
        "participant": PARTICIPANT_NAME,
        "environment": ENVIRONMENT,
        "description": "This API provides endpoints for text tokenization and checksum generation.",
        "endpoints": {
            "/": "Welcome message",
            "/generate": "GET - Generate tokens from query parameter",
            "/tokenize": "POST - Generate tokens from JSON body",
            "/checksum": "POST - Generate checksum from text",
        },
    }


@app.get("/generate")
async def generate_tokens_from_query(text: str):
    """
    Generate tokens from text provided as a query parameter.

    This endpoint accepts text as a query parameter and returns
    a list of tokens generated from that text.

    Args:
        text (str): The text to tokenize (query parameter)

    Returns:
        dict: Contains the list of tokens and their count

    Raises:
        HTTPException: If text parameter is empty or missing

    Example:
        GET /generate?text=Hello World
        Returns: {"tokens": ["Hello", "World"], "count": 2}
    """
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text parameter cannot be empty")

    tokens = generate(text)
    return {"tokens": tokens, "count": len(tokens)}


@app.post("/tokenize", response_model=TokenResponse)
async def tokenize_text(input_data: TextInput):
    """
    Generate tokens from text provided in JSON body.

    This endpoint accepts a POST request with a JSON body containing
    a 'text' field and returns a list of tokens generated from that text.

    Args:
        input_data (TextInput): Pydantic model containing the text field

    Returns:
        TokenResponse: Contains the list of tokens and their count

    Raises:
        HTTPException: If text is empty after stripping whitespace

    Example:
        POST /tokenize
        Body: {"text": "Hello World"}
        Returns: {"tokens": ["Hello", "World"], "count": 2}
    """
    if not input_data.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    # Use the generate() function to create tokens
    tokens = generate(input_data.text)

    return TokenResponse(tokens=tokens, count=len(tokens))


@app.post("/checksum", response_model=ChecksumResponse)
async def generate_checksum(input_data: TextInput):
    """
    Generate MD5 checksum from text provided in JSON body.

    This endpoint accepts a POST request with a JSON body containing
    a 'text' field and returns the MD5 checksum of that text.

    Args:
        input_data (TextInput): Pydantic model containing the text field

    Returns:
        ChecksumResponse: Contains the checksum and original text

    Example:
        POST /checksum
        Body: {"text": "Hello World"}
        Returns: {"checksum": "b10a8db164e0754105b7a99be72e3fe5", "original_text": "Hello World"}
    """
    # Generate MD5 checksum of the input text
    checksum = hashlib.md5(input_data.text.encode()).hexdigest()

    return ChecksumResponse(checksum=checksum, original_text=input_data.text)


# Entry point for running the application
if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application using environment variables
    uvicorn.run(app, host=HOST, port=PORT)
