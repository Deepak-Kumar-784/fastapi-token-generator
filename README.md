# Token Generation API

**Author:** Deepak  
**Date:** February 2, 2026  
**Version:** 1.0.0

## Overview

This is a FastAPI-based REST API that provides endpoints for text tokenization and checksum generation. The API accepts text input and returns either a list of tokens or an MD5 checksum of the provided text.

## Features

- **Text Tokenization**: Split text into individual tokens
- **Checksum Generation**: Generate MD5 checksums for text
- **Input Validation**: Pydantic models for robust data validation
- **Interactive Documentation**: Automatic Swagger UI and ReDoc documentation
- **Comprehensive Testing**: Full test suite using FastAPI TestClient
- **Environment Variables**: Secure configuration using .env files
- **Security Best Practices**: Sensitive data stored in environment variables

## Project Structure

```
Python_Task_Accenture/
├── main.py              # Main FastAPI application
├── test_main.py         # Test cases for all endpoints
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not in git)
├── .env.example         # Example environment file
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Security Features

### Environment Variables

This project uses `.env` file to store sensitive configuration data:

- API keys
- Secret keys
- Database credentials (if needed)
- Application settings

**Important:** The `.env` file is excluded from version control via `.gitignore` to prevent exposing sensitive data.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

### 1. Clone or navigate to the project directory

```bash
cd c:\Users\Deepak\Desktop\Python_Task_Accenture
```

### 2. Create a virtual environment (recommended)

**Windows:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and configure your settings:

**Windows:**

```powershell
copy .env.example .env
```

**Linux/Mac:**

```bash
cp .env.example .env
```

Then edit `.env` file and update the values as needed:

- `PARTICIPANT_NAME`: Your name
- `APP_NAME`: Application name
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `ENVIRONMENT`: Set to `production` for production deployment

**Important:** Never commit the `.env` file to version control!

## Running the Application

### Method 1: Using Uvicorn from Command Line

```bash
uvicorn main:app --reload
```

**Options:**

- `--reload`: Enable auto-reload on code changes (useful for development)
- `--host 0.0.0.0`: Make the server accessible from other machines
- `--port 8000`: Specify the port (default is 8000)

**Example with custom host and port:**

```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### Method 2: Running the Python Script Directly

```bash
python main.py
```

This will start the server on `http://0.0.0.0:8000`

### Method 3: Using Uvicorn with Workers (Production)

For production deployment with multiple worker processes:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Accessing the API

Once the server is running, you can access:

- **API Base URL**: http://localhost:8000
- **Interactive API Documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative Documentation (ReDoc)**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## API Endpoints

### 1. Welcome Endpoint

**GET** `/`

Returns a welcome message with participant information and available endpoints.

**Response:**

```json
{
  "message": "Welcome to the Token Generation API!",
  "participant": "Deepak",
  "description": "This API provides endpoints for text tokenization and checksum generation.",
  "endpoints": {
    "/": "Welcome message",
    "/generate": "GET - Generate tokens from query parameter",
    "/tokenize": "POST - Generate tokens from JSON body",
    "/checksum": "POST - Generate checksum from text"
  }
}
```

### 2. Generate Tokens (Query Parameter)

**GET** `/generate?text={your_text}`

Generate tokens from text provided as a query parameter.

**Parameters:**

- `text` (string, required): The text to tokenize

**Example Request:**

```bash
curl "http://localhost:8000/generate?text=Hello%20World"
```

**Response:**

```json
{
  "tokens": ["Hello", "World"],
  "count": 2
}
```

### 3. Tokenize Text (POST)

**POST** `/tokenize`

Generate tokens from text provided in JSON body.

**Request Body:**

```json
{
  "text": "Hello World"
}
```

**Example Request:**

```bash
curl -X POST "http://localhost:8000/tokenize" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Hello World\"}"
```

**Response:**

```json
{
  "tokens": ["Hello", "World"],
  "count": 2
}
```

### 4. Generate Checksum

**POST** `/checksum`

Generate MD5 checksum from text provided in JSON body.

**Request Body:**

```json
{
  "text": "Hello World"
}
```

**Example Request:**

```bash
curl -X POST "http://localhost:8000/checksum" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Hello World\"}"
```

**Response:**

```json
{
  "checksum": "b10a8db164e0754105b7a99be72e3fe5",
  "original_text": "Hello World"
}
```

## Running Tests

The project includes comprehensive test cases covering all endpoints and functions.

### Run all tests:

```bash
pytest test_main.py -v
```

### Run tests with coverage:

```bash
pip install pytest-cov
pytest test_main.py --cov=main --cov-report=html
```

### Run specific test class:

```bash
pytest test_main.py::TestGenerateFunction -v
```

## Code Documentation

### Pydantic Models

1. **TextInput**: Validates incoming JSON with text field
   - `text` (str): Required field with minimum length of 1

2. **TokenResponse**: Response model for tokenization
   - `tokens` (List[str]): List of generated tokens
   - `count` (int): Number of tokens

3. **ChecksumResponse**: Response model for checksum generation
   - `checksum` (str): MD5 hash of the text
   - `original_text` (str): The input text

### Core Function

**`generate(text: str) -> List[str]`**

The core tokenization function that splits text into tokens based on whitespace. This function is used by both the `/generate` and `/tokenize` endpoints.

## Error Handling

The API provides appropriate HTTP status codes and error messages:

- **400 Bad Request**: Empty or whitespace-only text
- **422 Unprocessable Entity**: Invalid JSON structure or missing required fields
- **500 Internal Server Error**: Server-side errors

## Development Tips

1. **Enable auto-reload during development:**

   ```bash
   uvicorn main:app --reload
   ```

2. **Check API documentation at** http://localhost:8000/docs for interactive testing

3. **View logs in the terminal** where uvicorn is running

4. **Test endpoints using the Swagger UI** before writing integration code

## Production Deployment

For production deployment, consider:

1. **Disable auto-reload:**

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. **Use multiple workers:**

   ```bash
   uvicorn main:app --workers 4
   ```

3. **Use a process manager** like systemd, supervisor, or PM2

4. **Set up a reverse proxy** (nginx or Apache)

5. **Enable HTTPS** for secure communication

## Troubleshooting

### Port Already in Use

If port 8000 is already in use, specify a different port:

```bash
uvicorn main:app --port 8080
```

### Module Not Found Error

Ensure all dependencies are installed:

```bash
pip install -r requirements.txt
```

### Virtual Environment Issues

Make sure your virtual environment is activated before running the application.

## CI/CD with GitHub Actions

This project includes automated testing with GitHub Actions. On every push to `master` or `main` branch:

1. **Automated Tests**: Runs all test cases with pytest
2. **Code Coverage**: Generates coverage report
3. **Code Quality**: Lints code with flake8

View workflow status in the "Actions" tab on GitHub after pushing.

## Deployment

### Deploy to Render (Free)

1. Push your code to GitHub
2. Go to [render.com](https://render.com) and sign up
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables from `.env.example`
7. Click "Create Web Service"

### Deploy to Railway (Free)

1. Push your code to GitHub
2. Go to [railway.app](https://railway.app) and sign up
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables from `.env.example`
6. Railway auto-detects and deploys your FastAPI app

### Deploy to Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Set environment variables: `heroku config:set PARTICIPANT_NAME=Deepak`
5. Deploy: `git push heroku master`

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is created as part of an Accenture Python task assignment.

## Contact

**Author:** Deepak  
**Date:** February 2, 2026

---

**Note:** This API is designed for educational and demonstration purposes as part of the Accenture Python task assignment.
