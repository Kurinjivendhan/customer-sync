
# Customer Sync — Python API Integration Service

A Python integration service that retrieves customer data from an external REST API, validates the response, and synchronizes records into a MySQL database.

## Features

- External REST API integration
- Request timeouts and automatic retries
- Input validation and duplicate detection
- MySQL persistence with duplicate-safe updates
- Environment-based database configuration
- Logging and error handling
- Automated unit tests using pytest and mocks

## Tech Stack

- Python
- Requests
- MySQL
- mysql-connector-python
- python-dotenv
- pytest

## Architecture

External REST API
        ↓
HTTP request and retry handling
        ↓
JSON parsing and validation
        ↓
Duplicate detection
        ↓
MySQL database
        ↓
Logs and test verification

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Kurinjivendhan/customer-sync.git
cd customer-sync
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=customer_sync
DB_USER=your_database_user
DB_PASSWORD=your_database_password
```

Replace the example values with your local MySQL credentials. Never commit `.env` to GitHub.

### 5. Create the database

Use MySQL Workbench to create the database and table using `schema.sql`.

### 6. Run the synchronization

```bash
python customer_sync.py
```

### 7. Run automated tests

```bash
python -m pytest -v
```

## Design Decisions

- Uses a primary key to prevent duplicate customer records.
- Uses bounded retries for selected transient HTTP errors.
- Validates incoming records before database persistence.
- Uses environment variables for database credentials.
- Uses mocked responses to test failure scenarios without depending on a live API.

## Future Improvements

- Add continuous integration with GitHub Actions.
- Add metrics and structured logging.
- Add pagination support for APIs that require it.
- Add integration tests against a dedicated test database.
