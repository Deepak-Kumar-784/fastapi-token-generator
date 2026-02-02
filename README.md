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
- **Custom UI**: Beautiful HTML/CSS/JS interface for both FastAPI and static site
- **GitHub Pages Deployment**: Automated deployment of static site
- **CI/CD Pipeline**: Automated testing, linting, and deployment with GitHub Actions

## Project Structure

```
project-root/
├── .github/
│   └── workflows/
│       └── deploy.yaml         # CI/CD pipeline for GitHub Pages
├── docs/                       # Static site for GitHub Pages
│   ├── index.html             # Static homepage
│   ├── style.css              # Static CSS
│   ├── script.js              # Static JS
│   └── images/
│       └── rocket.png         # Images for static site
├── templates/                  # FastAPI templates
│   ├── index.html             # FastAPI homepage
│   ├── style.css              # FastAPI CSS
│   └── script.js              # FastAPI JS
├── static/                     # FastAPI static files
│   └── images/
│       └── rocket.png         # Images for FastAPI
├── main.py                     # Main FastAPI application
├── test_main.py                # Test cases for all endpoints
├── requirements.txt            # Python dependencies
├── requirements-dev.txt        # Development dependencies
├── .env.example                # Example environment file (do NOT commit .env)
├── .gitignore                  # Git ignore rules
├── .stylelintrc.json           # CSS linting configuration
├── LICENSE                     # MIT License
└── README.md                   # Project documentation
```

**Note:**

- `.env` and any files listed in `.gitignore` are NOT pushed to GitHub.
- Only `.env.example` is tracked for environment variable reference.
- The `docs/` folder contains the static site deployed to GitHub Pages.
- The `templates/` and `static/` folders are used by the FastAPI application.

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

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
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

**Important:** Never commit the `.env` file to version control! The `.env` file is excluded by `.gitignore`.

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

This will start the server on `http://0.0.0.0:8000` (or your configured host/port)

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

Returns a custom HTML UI, not a JSON welcome message. All API endpoints remain unchanged.

**Response:**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Welcome to the Token Generation API!</title>
  </head>
  <body>
    <h1>Welcome to the Token Generation API!</h1>
    <p>
      This API provides endpoints for text tokenization and checksum generation.
    </p>
    <p>Try out the API at <a href="/docs">/docs</a>.</p>
  </body>
</html>
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

This project uses a streamlined GitHub Actions workflow (`.github/workflows/deploy.yaml`) that runs on every push to the `main` branch:

### Workflow Stages:

1. **🚀 CI – Test, Lint, Validate, Build**
   - Runs all Python tests with pytest
   - Lints code with flake8 for critical errors
   - Validates HTML syntax with tidy
   - Creates a preview artifact (zip of the site)

2. **🌍 Deploy to GitHub Pages**
   - Automatically deploys the `docs/` folder to GitHub Pages
   - Only runs on main branch push (not pull requests)
   - Site accessible at: `https://your-username.github.io/your-repo-name/`

### Key Features:

- **Fast execution**: Optimized workflow with caching
- **Sequential stages**: Clear, step-by-step execution
- **Automated deployment**: No manual intervention needed
- **Preview artifacts**: Download site preview before deployment

View workflow status in the "Actions" tab on GitHub after pushing.

## Deployment

### GitHub Pages (Static Site) - Automated ✅

The static site in the `docs/` folder is automatically deployed to GitHub Pages via GitHub Actions:

1. **Enable GitHub Pages:**
   - Go to your repository → Settings → Pages
   - Source: "Deploy from a branch"
   - Branch: Select `gh-pages` and `/root` folder
   - Click "Save"

2. **Automatic Deployment:**
   - Every push to `main` branch triggers the CI/CD workflow
   - The workflow validates, tests, and deploys automatically
   - Your site will be live at: `https://your-username.github.io/your-repo-name/`

3. **View Deployment:**
   - Check the "Actions" tab to see deployment progress
   - Visit the "Environments" section to see the live URL

### FastAPI Backend Deployment

For deploying the FastAPI backend:

#### Deploy to Render (Free)

1. Push your code to GitHub
2. Go to [render.com](https://render.com) and sign up
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables from `.env.example`
7. Click "Create Web Service"

#### Deploy to Railway (Free)

1. Push your code to GitHub
2. Go to [railway.app](https://railway.app) and sign up
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables from `.env.example`
6. Railway auto-detects and deploys your FastAPI app

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

**Author:** Deepak
**Date:** February 2, 2026

---

## User Interface and Static Files

This project maintains **two separate UI implementations**:

### 1. FastAPI UI (Local Development)

- **Location**: `templates/` and `static/` folders
- **Access**: http://localhost:8000/ (when running FastAPI server)
- **Purpose**: Dynamic UI served by FastAPI with API integration
- **Features**:
  - Links to `/docs` for API documentation
  - Links to `/generate` endpoint for live testing
  - Served via Jinja2 templates

### 2. GitHub Pages Static Site (Production)

- **Location**: `docs/` folder
- **Access**: `https://your-username.github.io/your-repo-name/`
- **Purpose**: Static showcase site deployed automatically
- **Features**:
  - Same visual design as FastAPI UI
  - Standalone HTML/CSS/JS (no server required)
  - Automatically deployed via GitHub Actions

### Customization

- **Change images**: Replace `rocket.png` in both `static/images/` and `docs/images/`
- **Update styles**: Modify `style.css` in both `templates/` and `docs/`
- **Edit content**: Update `index.html` in both locations

**Note**: When updating UI, remember to sync changes between `templates/` and `docs/` folders.
