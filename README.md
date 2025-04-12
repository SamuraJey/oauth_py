# OAuth-Py

## Overview

OAuth-Py is a Flask-based web application that implements VK OAuth authentication. The application provides a personalized experience, allowing users to authenticate through VK, access a notes feature, and play Conway's Game of Life.

## Features

- **OAuth Authentication**: Secure login via VK OAuth 2.0
- **Note Taking**: Users can create and view notes stored in CouchDB
- **Game of Life**: Interactive implementation of Conway's Game of Life
- **Containerized**: Docker and Docker Compose for easy deployment
- **CI/CD Pipeline**: GitHub Actions workflow for testing, building, and deploying

## Technology Stack

- **Backend**: Python 3.13 with Flask
- **Database**: CouchDB
- **Authentication**: Authlib for OAuth integration
- **Testing**: Pytest with requests-mock
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Docker, Docker Compose
- **CI/CD**: GitHub Actions

## Project Structure

```
oauth_py/
├── .github/workflows/        # GitHub Actions workflows
├── src/                      # Source code
│   ├── app/                  # Application configuration
│   ├── db/                   # Database utilities
│   ├── oauth/                # OAuth implementation
│   ├── routes/               # Flask route blueprints
│   ├── static/               # Static files (CSS, JavaScript)
│   ├── templates/            # HTML templates
│   ├── tests/                # Test cases
│   │   └── unit/             # Unit tests
│   ├── utils/                # Utility functions
│   └── run.py                # Application entry point
├── .dockerignore             # Files to exclude from Docker builds
├── .env_example              # Example environment variables
├── docker-compose.yml        # Docker Compose configuration
├── Dockerfile                # Docker image definition
├── Makefile                  # Development utility commands
├── poetry.lock               # Poetry dependencies lock file
└── pyproject.toml            # Project and dependencies configuration
```

## Getting Started

### Prerequisites

- Python 3.13
- Docker and Docker Compose
- Poetry (Python dependency manager)
- VK Developer account for OAuth credentials

### Environment Setup

1. Copy the example environment file:
   ```bash
   cp .env_example .env
   ```

2. Edit the .env file with your VK OAuth credentials and other settings:
   ```
   FLASK_SECRET_KEY=your_secret_key
   VK_CLIENT_ID=your_vk_client_id
   VK_CLIENT_SECRET=your_vk_client_secret
   PORT=8080
   DEBUG=False
   REDIRECT_URI=your_redirect_uri
   COUCHDB_USER=your_couchdb_username
   COUCHDB_PASSWORD=your_couchdb_password
   ```

### Local Development

1. Initialize the development environment:
   ```bash
   make init
   ```

2. Run the application:
   ```bash
   poetry run python src/run.py
   ```

### Docker Deployment

1. Build and run with Docker Compose:
   ```bash
   docker-compose up --build -d
   ```

2. Access the application at `http://localhost:8080`

## CI/CD Pipeline

The project includes a GitHub Actions workflow that:

1. Builds and tests the application
2. Pushes the Docker image to GitHub Container Registry
3. Deploys to the production server (when triggered manually)

## Testing

Run the tests using pytest:

```bash
poetry run pytest
```

## License

This project is licensed under the BSD 3-Clause License - see the LICENSE file for details.

## Author

Sergei Zaremba
