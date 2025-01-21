# Shared Ledger System

A scalable and reusable shared ledger system designed for tracking user credits across multiple applications in a monorepo.

## Table of Contents
- [Features](#features)
- [Technical Stack](#technical-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Database Setup](#database-setup)
  - [Configuration](#configuration)
- [Development](#development)
  - [Running the Application](#running-the-application)
  - [API Documentation](#api-documentation)
  - [Testing](#testing)
- [API Reference](#api-reference)
- [Database Management](#database-management)
  - [Development Database](#development-database)
  - [Test Database](#test-database)
  - [pgAdmin Access](#pgadmin-access)
- [Troubleshooting](#troubleshooting)
  - [Database Issues](#database-issues)
  - [Test Issues](#test-issues)


## Features

- Shared core ledger functionality for credit management
- Type-safe operation handling with Pydantic models
- Extensible architecture for application-specific operations
- Asynchronous database operations with SQLAlchemy
- Comprehensive API endpoints with FastAPI
- Database migration support using Alembic
- Docker for development environment
- Unit tests with pytest

## Technical Stack

- **Python**: ≥ 3.10 (Currently using 3.13)
- **Web Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0
- **Data Validation**: Pydantic v2
- **Database**: PostgreSQL 16
- **Migration Tool**: Alembic
- **Testing**: pytest, pytest-asyncio
- **Development Tools**:
  - Docker & Docker Compose (I highly suggest Orbstack)
  - pgAdmin 4
  - uvicorn (ASGI server)

## Project Structure

```
shared-ledger-system/
├── alembic/              # Database migrations
├── apps/                 # Application modules
│   └── example_app/     # Example application using the shared ledger
│       ├── api/         # FastAPI routes and dependencies
│       ├── models/      # App-specific database models
│       └── schemas/     # App-specific Pydantic models
├── core/                # Core shared ledger functionality
│   └── shared_ledger/   # Shared ledger implementation
│       ├── models/      # Core database models
│       ├── schemas/     # Core Pydantic models
│       ├── operations/  # Ledger operations
│       └── utils/       # Shared utilities
├── tests/               # Test suite
├── alembic.ini          # Alembic configuration
├── docker-compose.yml   # Docker services configuration
└── setup.py            # Package configuration
```

## Package Configuration

The project uses `setup.py` for package management and installation. This configuration is crucial for:
1. Installing the project as a package
2. Managing dependencies
3. Ensuring proper module imports

### [setup.py](setup.py) Configuration

```python
from setuptools import find_namespace_packages, setup

setup(
    name="shared-ledger-system",
    version="0.1.0",
    packages=find_namespace_packages(include=["core.*", "apps.*"]),
    install_requires=[
        "fastapi>=0.115.6",
        "uvicorn>=0.34.0",
        "sqlalchemy>=2.0.37",
        "pydantic>=2.10.5",
        "alembic>=1.14.1",
        "asyncpg>=0.30.0",
    ],
    extras_require={
        "test": [
            "pytest",
            "pytest-asyncio",
            "httpx",
        ],
    },
)
```

### Key Components

1. **Package Name and Version**:
   - Name: "shared-ledger-system"
   - Version: "0.1.0"

2. **Package Discovery**:
   - Uses `find_namespace_packages` to automatically find all packages
   - Includes both `core.*` and `apps.*` namespaces
   - This ensures proper module imports throughout the project

3. **Dependencies**:
   - Core dependencies in `install_requires`:
     - FastAPI for API framework
     - uvicorn for ASGI server
     - SQLAlchemy for ORM
     - Pydantic for data validation
     - Alembic for migrations
     - asyncpg for async PostgreSQL support
   - Test dependencies in `extras_require`:
     - pytest for testing framework
     - pytest-asyncio for async test support
     - httpx for async HTTP client

### Usage

1. **Development Installation**:
   ```bash
   pip install -e .
   ```
   This installs the package in editable mode, allowing you to modify the code without reinstalling.

2. **Installing with Test Dependencies**:
   ```bash
   pip install -e ".[test]"
   ```
   This installs both the package and test dependencies.

3. **Why We Need It**:
   - Enables Python to treat the project as a proper package
   - Ensures correct module imports (e.g., `from core.shared_ledger import ...`)
   - Manages project dependencies consistently
   - Supports namespace packages for modular architecture

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Docker and Docker Compose
- Git
- PostgreSQL client (optional, for direct database access)
- Make (optional, for using Makefile commands)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd shared-ledger-system
   ```

2. Start the database containers:
   ```bash
   docker-compose up -d
   ```
   This will automatically create and start:
   - Development database (ledger_db) on port 5432
   - Test database (test_ledger_db) on port 5433
   - pgAdmin on port 5050

   Wait for the databases to be ready. You can check their status with:
   ```bash
   docker-compose ps
   ```
   All containers should show as "running" and healthy before proceeding.

3. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

4. Install the package in development mode:
   ```bash
   pip install -e .
   ```

5. Apply migrations:
   ```bash
   alembic upgrade head
   ```

## Development

### Running the Application

1. Start the FastAPI server:
   ```bash
   uvicorn apps.example_app.main:app --reload
   ```

2. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Testing

Ensure all containers are running and healthy before running tests:
```bash
# Check container status
docker-compose ps

# Run all tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_api_endpoints.py -v

# Run tests with coverage report
pytest --cov=core --cov=apps
```

If you encounter database errors, wait a few seconds for the databases to be fully initialized and try again.

## API Reference

The example app provides the following endpoints:

### Health Check
- `GET /health`: Check API health status

### Balance Operations
- `GET /balance/{owner_id}`: Get balance for an owner
- `POST /ledger`: Create a new ledger entry

### Content Management
- `POST /content`: Create content (requires credits)
- `POST /content/{content_id}/access`: Access content (requires credits)

For detailed API documentation, including request/response schemas and examples, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc


## Database Management

### Development Database
- Host: ledger_db
- Port: 5432
- Database: ledger_db
- Username: postgres
- Password: postgres

### Test Database
- Host: ledger_test_db
- Port: 5433
- Database: test_ledger_db
- Username: postgres
- Password: postgres

### pgAdmin Access
- URL: http://localhost:5050
- Email: admin@admin.com
- Password: admin

#### Connecting to Databases in pgAdmin
1. Add New Server:
   - Name: Ledger DB (or any name you prefer)
   - Host: localhost
   - Port: 5432 (development) or 5433 (test)
   - Database: ledger_db or test_ledger_db
   - Username: postgres
   - Password: postgres

2. Important Notes:
   - Use 'localhost' when connecting from your local machine
   - Use 'postgres' when connecting from inside Docker containers

## Troubleshooting

### Database Issues

1. Common Connection Errors:
   - "connection refused": Ensure Docker containers are running (`docker-compose ps`)
   - "password authentication failed": Check the password (default is 'postgres')
   - If databases aren't ready, wait a few seconds and try again

2. Database Management Commands:
   ```bash
   # View container logs
   docker-compose logs postgres
   docker-compose logs postgres_test

   # Reset databases (removes all data)
   docker-compose down -v
   docker-compose up -d

   # Restart specific container
   docker-compose restart postgres_test
   ```

3. Migration Issues:
   ```bash
   # Reset migration state
   alembic stamp head

   # Create new migration
   alembic revision --autogenerate -m "description"

   # Apply migrations
   alembic upgrade head
   ```

### Test Issues

1. Database Connection:
   - Ensure test database container is running and healthy
   - Check if test database exists and is accessible
   - Verify database connection settings in test configuration

2. Transaction Errors:
   - Ensure no other tests are running
   - Try restarting the test database container
   - Check for proper cleanup in test fixtures

